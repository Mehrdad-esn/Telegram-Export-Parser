# Frontend (Next.js + TypeScript + TailwindCSS)

This directory contains the Next.js (TypeScript) frontend for the Telegram Export Parser project, designed with a premium dark-mode-first aesthetic, dynamic Framer Motion animations, and responsive layout.

## 🚀 Quick Start

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
   The application will run on `http://localhost:3000`.

## 🏗️ Production Build

1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Run the production server:
   ```bash
   npm start
   ```

## 🛠️ Code Structure

- `pages/index.tsx`: Premium landing page highlighting local data safety and visual showcases.
- `pages/auth/`: User registration and login forms with security feedback.
- `pages/pricing.tsx`: SaaS tier details integrated with Stripe billing details.
- `pages/dashboard/index.tsx`: Active processing panel featuring file drag-and-drop, real-time analytics graphs (using Recharts), top talkers distribution, and multi-format exporters.
- `styles/`: Core styling containing Tailwind configurations and custom glassmorphism panels.

## 🔗 Backend Integration

Next.js is configured with proxy rewrites (in `next.config.js`) to route `/api/:path*` and `/billing/:path*` requests directly to the FastAPI backend service at `http://localhost:8000`.

## 🧪 Linting & Testing

- Run linter: `npm run lint` (using ESLint)