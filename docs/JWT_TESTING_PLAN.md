# JWT Authentication Fix - Testing Plan

## Current Status
✅ Auth service rebuilt with JWT_ACCESS_EXPIRES_IN=1h
✅ Bridge UI rebuilt with updated token handling
✅ All services running and healthy

## Quick Test Steps

### 1. Basic Login & Session Persistence Test (5 minutes)
```
1. Open browser: http://localhost:3082
2. Login as: admin / admin
3. Open browser console (F12)
4. Look for this log message after login:
   "🔑 Login response tokens: { hasAccessToken: true, hasRefreshToken: true }"
5. Use the application normally (browse chatflows, etc.)
6. Wait 15 minutes (old expiration time)
7. Try to perform an action (e.g., open a chatflow)
8. EXPECTED: You should remain logged in (NOT logged out)
```

**What Changed**: 
- Before: Access token expired at 15 minutes → User logged out
- After: Access token expires at 60 minutes → User stays logged in

---

### 2. Background Token Refresh Test (55 minutes)
```
1. Login at: http://localhost:3082 (admin/admin)
2. Keep browser console open (F12)
3. Wait 50 minutes
4. Look for this console message:
   "🕐 Running background token check..."
5. Then look for:
   "🔄 Attempting to refresh token..."
   "✅ Token refreshed successfully"
6. Verify you're still logged in
7. Try an action (e.g., open a chatflow)
```

**What Changed**:
- Before: Background check at 14 min, but skipped if tab hidden
- After: Background check at 50 min, runs regardless of tab visibility

---

### 3. Tab Switching Test (20 minutes)
```
1. Login at: http://localhost:3082 (admin/admin)
2. Note the current time
3. Switch to a different browser tab (e.g., YouTube)
4. Leave that tab active for 20 minutes
5. Return to the application tab
6. Look for console message:
   "👁️ Page became visible - checking token status"
7. Try an action (should work)
```

**What Changed**:
- Before: Token checks skipped when tab hidden → Token expired → Logout
- After: Token still valid (1 hour expiry), check runs on tab focus

---

### 4. Server-Side Logout Test (2 minutes)
```
1. Login at: http://localhost:3082 (admin/admin)
2. Open browser DevTools → Network tab
3. Click "Logout" button
4. In Network tab, look for request to:
   POST /api/v1/chat/revoke
5. Verify request includes:
   - Authorization: Bearer <token>
   - Body: { "refresh_token": "..." }
6. Verify you're redirected to login page
7. Check localStorage is empty (Application tab → Local Storage)
```

**What Changed**:
- Before: Only cleared localStorage → Refresh tokens remained valid in DB
- After: Calls server to invalidate refresh token → More secure logout

---

### 5. Token Expiration Edge Case (65 minutes)
```
1. Login at: http://localhost:3082 (admin/admin)
2. Wait exactly 61 minutes (1 hour + 1 minute)
3. Try to perform an action (e.g., open a chatflow)
4. Watch console for:
   "🔄 Attempting to refresh token..."
5. EXPECTED: Token auto-refreshes via axios interceptor
6. Action completes successfully
7. You remain logged in
```

**What Changed**:
- Before: 15-minute expiration → Frequent interruptions
- After: 1-hour expiration with 50-min proactive refresh → Smooth UX

---

## Console Log Reference

### Successful Login
```javascript
🔑 Login response tokens: {
  hasAccessToken: true,
  hasRefreshToken: true,
  accessTokenLength: 200+,
  refreshTokenLength: 200+,
  expiresIn: 3600 // seconds (1 hour)
}
```

### Background Token Check (every 50 minutes)
```javascript
🕐 Running background token check...
🔍 Debug refresh token attempt: {
  hasTokens: true,
  hasAccessToken: true,
  hasRefreshToken: true,
  isBackground: true
}
🔄 Attempting to refresh token...
✅ Token refreshed successfully
```

### Tab Focus Check
```javascript
👁️ Page became visible - checking token status
```

### Failed Refresh (Only if refresh token expired)
```javascript
❌ Token refresh failed: {
  error: "Invalid or expired refresh token",
  status: 401,
  isBackground: false
}
```

---

## Automated Test Script (Optional)

You can use this PowerShell script to simulate a long session:

```powershell
# Save as: test_jwt_session.ps1

Write-Host "🧪 JWT Session Test Starting..." -ForegroundColor Cyan
Write-Host "Prerequisites: Services running, logged out" -ForegroundColor Yellow
Write-Host ""

$baseUrl = "http://localhost:8000"

# Step 1: Login
Write-Host "1️⃣  Logging in..." -ForegroundColor Green
$loginBody = @{
    username = "admin"
    password = "admin"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "$baseUrl/api/v1/chat/authenticate" -Method Post -Body $loginBody -ContentType "application/json"
$accessToken = $response.access_token
$refreshToken = $response.refresh_token

Write-Host "✅ Login successful" -ForegroundColor Green
Write-Host "   Access Token: $($accessToken.Substring(0,20))..." -ForegroundColor Gray
Write-Host "   Refresh Token: $($refreshToken.Substring(0,20))..." -ForegroundColor Gray
Write-Host ""

# Step 2: Wait 55 minutes
Write-Host "2️⃣  Waiting 55 minutes (simulating background refresh timing)..." -ForegroundColor Green
Write-Host "   You can cancel this test with Ctrl+C" -ForegroundColor Yellow

$waitMinutes = 55
$waitSeconds = $waitMinutes * 60

for ($i = 1; $i -le $waitMinutes; $i++) {
    Start-Sleep -Seconds 60
    Write-Host "   ⏱️  $i/$waitMinutes minutes elapsed..." -ForegroundColor Gray
}

Write-Host ""

# Step 3: Try API call (should trigger refresh if needed)
Write-Host "3️⃣  Making API call with current token..." -ForegroundColor Green
try {
    $headers = @{
        Authorization = "Bearer $accessToken"
    }
    $chatflowsResponse = Invoke-RestMethod -Uri "$baseUrl/api/v1/chat/chatflows" -Method Get -Headers $headers
    Write-Host "✅ API call successful - token still valid!" -ForegroundColor Green
} catch {
    Write-Host "❌ API call failed: $($_.Exception.Message)" -ForegroundColor Red
    
    # Step 4: Try refresh
    Write-Host "4️⃣  Attempting token refresh..." -ForegroundColor Green
    $refreshBody = @{
        refresh_token = $refreshToken
    } | ConvertTo-Json
    
    try {
        $refreshResponse = Invoke-RestMethod -Uri "$baseUrl/api/v1/chat/refresh" -Method Post -Body $refreshBody -ContentType "application/json"
        $newAccessToken = $refreshResponse.access_token
        Write-Host "✅ Token refresh successful!" -ForegroundColor Green
        Write-Host "   New Access Token: $($newAccessToken.Substring(0,20))..." -ForegroundColor Gray
        
        # Step 5: Retry API call
        Write-Host "5️⃣  Retrying API call with new token..." -ForegroundColor Green
        $headers.Authorization = "Bearer $newAccessToken"
        $chatflowsResponse = Invoke-RestMethod -Uri "$baseUrl/api/v1/chat/chatflows" -Method Get -Headers $headers
        Write-Host "✅ API call successful with refreshed token!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Token refresh failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 JWT Session Test Complete!" -ForegroundColor Cyan
```

Run with:
```bash
powershell -ExecutionPolicy Bypass -File test_jwt_session.ps1
```

---

## Expected Results Summary

| Test | Before Fix | After Fix |
|------|-----------|-----------|
| **15-min idle** | ❌ Logged out | ✅ Stays logged in |
| **50-min active** | ⚠️ May logout if tab hidden | ✅ Auto-refresh, stays logged in |
| **Tab switch 20min** | ❌ Logged out | ✅ Stays logged in |
| **Manual logout** | ⚠️ Token remains in DB | ✅ Token invalidated on server |
| **61-min idle** | ❌ Logged out | ✅ Auto-refresh via interceptor |

---

## Troubleshooting

### If still experiencing logouts:

1. **Check JWT config loaded**:
   ```powershell
   docker exec auth-service env | Select-String "JWT"
   ```
   Should show: `JWT_ACCESS_EXPIRES_IN=1h`

2. **Check browser console** for error messages:
   - "❌ Token refresh failed" → Check auth service logs
   - "❌ No refresh token available" → Token not stored properly
   - Network errors → Check service connectivity

3. **Check auth service logs**:
   ```powershell
   docker logs auth-service -f --tail 100
   ```
   Look for: "Token refresh error" or "Invalid refresh token"

4. **Verify localStorage**:
   - F12 → Application → Local Storage → http://localhost:3082
   - Should see: `auth-storage` with tokens object

5. **Check refresh token in database**:
   ```powershell
   docker exec mongodb-auth mongosh auth --eval "db.refreshtokens.find().pretty()"
   ```

---

## Success Criteria

✅ Users stay logged in for hours without interruption
✅ Token refresh happens automatically before expiration
✅ Logout properly invalidates tokens on server
✅ Tab switching doesn't cause session loss
✅ Console shows appropriate debug messages
✅ No unnecessary API calls or refresh attempts

---

## Rollback Instructions

If critical issues found, rollback immediately:

```powershell
# 1. Revert auth service config
cd c:\Users\user\Documents\ThankGodForJesusChrist\ThankGodForChatProxyPlatform\auth-service

# Edit .env: Change JWT_ACCESS_EXPIRES_IN back to 15m

# 2. Rebuild auth service
.\rebuild.bat

# 3. Revert frontend changes
cd ..\bridge
git checkout HEAD -- src/App.tsx src/api/auth.ts src/store/authStore.ts

# 4. Rebuild bridge
npm run build
docker-compose up -d --build

# 5. Verify rollback
docker exec auth-service env | Select-String "JWT_ACCESS_EXPIRES_IN"
# Should show: JWT_ACCESS_EXPIRES_IN=15m
```

---

## Next Steps After Testing

1. **If tests pass**: Document success, monitor production
2. **If tests fail**: 
   - Review console logs
   - Check auth service logs
   - Verify token timing logic
   - Consider adjusting timing parameters
3. **Future improvements**:
   - Add token refresh retry logic
   - Implement token preemptive refresh (at 45 min)
   - Add user notification before forced logout
   - Monitor token refresh success rate

---

## Monitoring Recommendations

Track these metrics after deployment:

1. **Token Refresh Success Rate**: Should be >99%
2. **Average Session Duration**: Should increase 4x (from ~15 min to ~1 hour+)
3. **Logout Error Rate**: Should be 0%
4. **Background Refresh Frequency**: Every 50 minutes per active user
5. **Failed Login Attempts**: Should remain constant (unchanged)

---

**Test Document Version**: 1.0
**Date**: 2026-02-11
**Tested By**: [Your Name]
**Test Results**: [To be filled after testing]
