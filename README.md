# 💻 Custom Laptop E-Commerce Platform

A production-quality custom laptop e-commerce platform blending a familiar, high-conversion marketplace storefront (similar to Jumia / Jiji) with an interactive 3D laptop configurator.

---

## 🎨 Visual Identity & Design System
- **Theme**: Blue + White + Modern Technology + Trustworthy + Accessible
- **Primary Color**: `#1769FF` (Tech Blue)
- **Deep Navy**: `#0B1F3A` (Contrast / Text / Badges)
- **Background**: `#F6F9FF` (Clean Soft Slate Blue)
- **Soft Accent**: `#EAF2FF` (Card highlights & active states)
- **Sky Blue**: `#4DA3FF` (Interactive accents & gradients)

---

## 🏗 Monorepo Architecture

```text
custom-laptop-store/
├── apps/
│   ├── web/                     # Next.js 14+ (App Router), Tailwind CSS, Framer Motion, Zustand, Three.js
│   └── api/                     # Python 3.11+ FastAPI, SQLAlchemy, Pydantic v2, Alembic
├── infrastructure/
│   ├── docker/                  # Dockerfiles for Web and API
│   └── keycloak/                # Keycloak realm & client configuration
└── docs/                        # Architecture, API & Configurator documentation
```

---

## 🚀 Getting Started

### 1. Backend (FastAPI)
```bash
cd apps/api
# Recommended: Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# Install requirements
pip install -r requirements.txt
# Run FastAPI server
uvicorn app.main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/v1/health`

### 2. Frontend (Next.js)
```bash
cd apps/web
npm install
npm run dev
```
- Storefront: `http://localhost:3000`

### 3. Docker Compose (Full Stack)
```bash
docker compose up -d
```
