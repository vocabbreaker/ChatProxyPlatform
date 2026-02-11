# Bridge UI - React Chat Interface

React + TypeScript + Vite frontend for ChatProxy Platform.

---

## Quick Start (Windows Docker)

### Start the UI

```batch
start.bat
```

Access at: **http://localhost:3082**

### Other Commands

```batch
stop.bat      # Stop container
rebuild.bat   # Rebuild after code changes
logs.bat      # View real-time logs
```

---

## What is Bridge UI?

Bridge UI is the React frontend that provides:
- 💬 Chat interface for AI conversations
- 🔐 User authentication
- 📁 File upload support
- 🧮 Math equation rendering (MathJax)
- 📝 Markdown support
- 🌍 Multi-language support (i18n)
- 📌 Message pinning
- 🎨 Dark/Light theme

---

## Tech Stack

- **React 18** + **TypeScript**
- **Vite** - Fast build tool
- **Zustand** - State management
- **TailwindCSS** - Styling
- **MathJax** - Math rendering
- **i18next** - Internationalization

---

## Configuration

Edit API URL in `docker-compose.yml`:

```yaml
environment:
  - VITE_FLOWISE_PROXY_API_URL=http://host.docker.internal:8000
```

Or set environment variable:

```batch
set FLOWISE_PROXY_URL=https://your-api.com
start.bat
```

---

## Full Documentation

See **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** for:
- Detailed setup instructions
- Troubleshooting guide
- Architecture overview
- Development guide

---

## Expanding the ESLint Configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      ...tseslint.configs.recommendedTypeChecked,
      ...tseslint.configs.strictTypeChecked,
      ...tseslint.configs.stylisticTypeChecked,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
])
```

---

## Service Architecture

| Service | Port | Purpose |
|---------|------|---------|
| Bridge UI | 3082 | React frontend |
| Flowise Proxy | 8000 | Python API |
| Auth Service | 3000 | Authentication |
| Flowise | 3002 | AI flows |

---

## Support

**Issues?**
1. Check logs: `logs.bat`
2. Try rebuild: `rebuild.bat`
3. See [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
