# Frontend (Next.js + TypeScript + TailwindCSS)

This directory contains a Next.js (TypeScript) frontend scaffold for the Telegram Export Parser project.

Quick start:

1. cd frontend
2. npm install
3. npm run dev

Build and run production:

1. npm run build
2. npm start

Linting:

- A basic ESLint setup is recommended. The project includes a lint script (uses `next lint`).

Recommended devDependencies to install when you run `npm install`:

- next
- react
- react-dom
- typescript
- tailwindcss
- postcss
- autoprefixer
- eslint
- eslint-config-next

This scaffold provides sample login/signup pages and a dashboard with an upload form that POSTs to `/api/upload` (placeholder). Connect these endpoints to your Python backend when ready.