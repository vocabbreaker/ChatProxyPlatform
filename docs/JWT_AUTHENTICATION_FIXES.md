# JWT Authentication Issues - Investigation & Fixes

## Problem Description
Users experiencing intermittent logout issues after 5-15 minutes of activity. The authentication system was not maintaining sessions reliably.

## Root Causes Identified

### 1. **Aggressive Token Expiration**
- **Issue**: Access tokens expired after only 15 minutes
- **Impact**: Users reading content or temporarily inactive would be logged out frequently
- **Solution**: ✅ Increased JWT_ACCESS_EXPIRES_IN from `15m` to `1h`

### 2. **Background Token Refresh Race Condition**
- **Issue**: Background check ran every 14 minutes, but was skipped when browser tab was hidden
- **Impact**: If user switched tabs for >15 minutes, access token expired without being refreshed
- **Solution**: ✅ Changed interval to 50 minutes (10 min before 1h expiration) and removed visibility check

### 3. **Missing Server-Side Logout**
- **Issue**: Logout only cleared localStorage, didn't invalidate refresh tokens on server
- **Impact**: Old refresh tokens remained valid in database, potential security issue
- **Solution**: ✅ Added API call to `/api/v1/chat/revoke` endpoint to invalidate tokens server-side

### 4. **Token Timing Mismatch**
- **Issue**: Access token (15m) expiring before background check (14m) could sometimes fail
- **Impact**: Race condition where token expires just before refresh attempt
- **Solution**: ✅ With 1-hour tokens and 50-minute checks, there's now a 10-minute safety buffer

## Changes Made

### 1. Auth Service Configuration
**File**: `auth-service/.env`
```diff
- JWT_ACCESS_EXPIRES_IN=15m
+ JWT_ACCESS_EXPIRES_IN=1h
```

### 2. Frontend Background Check
**File**: `bridge/src/App.tsx`
```diff
- }, 14 * 60 * 1000); // 14 minutes
+ }, 50 * 60 * 1000); // 50 minutes (10 min before 1h expiration)

- // Only check tokens if the page is visible
- if (!document.hidden) {
-   console.log('🕐 Running background token check...');
-   checkAuthStatus(true);
- } else {
-   console.log('📵 Skipping background token check - page is hidden');
- }
+ // Check tokens regardless of page visibility
+ console.log('🕐 Running background token check...');
+ checkAuthStatus(true);
```

### 3. Logout API Function
**File**: `bridge/src/api/auth.ts`
```typescript
/**
 * Logs out a user and invalidates their refresh token on the server.
 */
export const logout = async (refreshToken: string, accessToken: string): Promise<void> => {
  try {
    const response = await fetch(`${FLOWISE_PROXY_URL}/api/v1/chat/revoke`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    // ... error handling
  } catch (error) {
    console.warn('Logout request error, but continuing with local cleanup:', error);
  }
};
```

### 4. Auth Store Logout Update
**File**: `bridge/src/store/authStore.ts`
```typescript
logout: async () => {
  const { tokens } = get();
  // Call server to invalidate refresh token
  if (tokens?.refreshToken && tokens?.accessToken) {
    try {
      await apiLogout(tokens.refreshToken, tokens.accessToken);
    } catch (error) {
      console.error('Logout API call failed:', error);
      // Continue with local cleanup even if server call fails
    }
  }
  set(initialState);
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
},
```

## JWT Flow Analysis

### Current Token Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Authentication Flow                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Login Request                                           │
│     └─> Bridge → Flowise-Proxy → Auth-Service              │
│                                                              │
│  2. Token Generation (Auth-Service)                         │
│     ├─> Access Token:  JWT, 1 hour expiry                  │
│     └─> Refresh Token: JWT, 7 days expiry, stored in DB    │
│                                                              │
│  3. Token Storage (Bridge)                                  │
│     └─> localStorage via Zustand persist                    │
│                                                              │
│  4. Token Refresh (Every 50 minutes)                        │
│     ├─> Check if access token expired                      │
│     ├─> If expired, call /refresh with refresh token       │
│     └─> Bridge → Flowise-Proxy → Auth-Service              │
│                                                              │
│  5. Token Rotation (Auth-Service)                           │
│     ├─> Verify old refresh token                           │
│     ├─> Generate new access token (1h)                     │
│     ├─> Generate new refresh token (7d)                    │
│     └─> Delete old refresh token from DB                   │
│                                                              │
│  6. Logout (Both Client & Server)                           │
│     ├─> Call /revoke to invalidate refresh token           │
│     └─> Clear localStorage                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Token Timing
```
Time:     0min        50min       60min       110min      120min
          │           │           │           │           │
Access:   [─────────────────────────] EXPIRED
          └─ Valid for 1 hour ─────┘
                      │
Refresh:  [─────────────────────────────────────────────] ...continues for 7 days
          │           │           │           │
Check:    ✓           ✓           ✓           ✓
          Start       Check       Check       Check
                      (50min)     (100min)    (150min)

Legend:
- ✓ = Background token check triggers
- Access token checked at 50min mark (10min before expiry)
- New access token generated before old one expires
```

## Testing Recommendations

### 1. Normal Usage Test
```bash
# Start all services
cd auth-service && start_docker.bat
cd flowise-proxy-service-py && docker-compose up -d
cd bridge && npm run dev

# Test:
1. Login as admin/admin
2. Use the app normally for 15 minutes
3. Verify you remain logged in (should NOT logout now)
4. Check browser console for "🕐 Running background token check..." at 50-minute mark
```

### 2. Tab Switching Test
```bash
# Test:
1. Login to the app
2. Switch to another browser tab for 30 minutes
3. Return to the app tab
4. Verify you're still logged in
5. Check console for "👁️ Page became visible - checking token status"
```

### 3. Token Expiration Test
```bash
# Test:
1. Login to the app
2. Wait exactly 60 minutes without any activity
3. Try to make an API call (e.g., open a chatflow)
4. Verify automatic token refresh happens
5. Check console for "🔄 Attempting to refresh token..." and "✅ Token refreshed successfully"
```

### 4. Logout Test
```bash
# Test:
1. Login to the app
2. Open browser DevTools → Network tab
3. Click Logout
4. Verify request to /api/v1/chat/revoke with access token
5. Verify localStorage is cleared
6. Try to use old refresh token - should fail with 401
```

## Deployment Steps

### 1. Rebuild Auth Service
```bash
cd auth-service
rebuild_docker.bat
```

### 2. Rebuild Bridge Frontend
```bash
cd bridge
npm run build
docker-compose up -d --build
```

### 3. Verify Changes
```bash
# Check auth service logs
docker logs auth-service -f

# Check that JWT_ACCESS_EXPIRES_IN=1h is loaded
docker exec auth-service env | grep JWT

# Check bridge is running
curl http://localhost:3082
```

## Security Considerations

### Improved Security
- ✅ Refresh tokens now properly invalidated on logout
- ✅ Token rotation implemented (old refresh tokens deleted after use)
- ✅ Access tokens short-lived (1 hour vs 7 days)

### Additional Recommendations
1. **Enable HTTPS in production**: Protect tokens in transit
2. **Add rate limiting**: Prevent brute force attacks on /refresh endpoint
3. **Monitor refresh patterns**: Detect suspicious token refresh patterns
4. **Add IP validation**: Optional - bind tokens to IP addresses
5. **Implement token blacklist**: For compromised tokens before expiration

## Configuration Reference

### Auth Service Environment Variables
```env
JWT_ACCESS_SECRET=<secure-random-string>
JWT_REFRESH_SECRET=<secure-random-string>
JWT_ACCESS_EXPIRES_IN=1h          # Access token lifetime
JWT_REFRESH_EXPIRES_IN=7d         # Refresh token lifetime
```

### Frontend Environment Variables
```env
VITE_FLOWISE_PROXY_API_URL=http://localhost:8000
```

### Timing Configuration
- Access Token: 1 hour (3600 seconds)
- Refresh Token: 7 days (604800 seconds)
- Background Check: 50 minutes (3000 seconds)
- Safety Buffer: 10 minutes

## Troubleshooting

### User Still Getting Logged Out
1. Check browser console for error messages
2. Verify JWT_ACCESS_EXPIRES_IN=1h in auth-service
3. Check background refresh logs: `console.log('🕐 Running background token check...')`
4. Verify refresh token is being saved to localStorage

### Logout Not Working
1. Check network tab for /revoke request
2. Verify access token is valid when logout is called
3. Check flowise-proxy logs for authentication errors
4. Verify refresh_token field is being sent in request body

### Token Refresh Failing
1. Check if refresh token is expired (>7 days old)
2. Verify JWT secrets match between auth-service and flowise-proxy
3. Check auth-service logs for "Token refresh error"
4. Verify refresh token exists in MongoDB (auth database)

## Monitoring

### Key Metrics to Track
1. **Token Refresh Success Rate**: Should be >99%
2. **Average Session Duration**: Should increase significantly
3. **Logout Success Rate**: Should be 100%
4. **Background Check Frequency**: Every 50 minutes per active user

### Log Messages to Monitor
```
✅ Success:
- "✅ Token refreshed successfully"
- "🕐 Running background token check..."
- "👁️ Page became visible - checking token status"

❌ Errors:
- "❌ Token refresh failed"
- "❌ No refresh token available"
- "Logout API call failed"
```

## Rollback Plan

If issues occur after deployment:

1. **Revert Auth Service Token Expiration**:
   ```bash
   # In auth-service/.env
   JWT_ACCESS_EXPIRES_IN=15m  # Revert to original
   cd auth-service && rebuild_docker.bat
   ```

2. **Revert Frontend Changes**:
   ```bash
   git checkout HEAD -- bridge/src/App.tsx
   git checkout HEAD -- bridge/src/api/auth.ts
   git checkout HEAD -- bridge/src/store/authStore.ts
   cd bridge && npm run build && docker-compose up -d --build
   ```

## Success Criteria

✅ Users can stay logged in for hours without interruption
✅ Token refresh happens automatically in background
✅ Logout invalidates tokens on server
✅ No race conditions between token expiry and refresh
✅ Session persists across browser tab switches
✅ No security vulnerabilities with token handling

## Implementation Date
- **Analysis**: [Current Date]
- **Changes Applied**: [Current Date]
- **Testing Required**: Before production deployment
- **Deployment**: Pending testing confirmation
