# REALTECH Custom Laptop Store - Backend API Service

High-performance, decoupled FastAPI backend for products, 3D laptop hardware configuration engine, multi-gateway payments (Paystack, Flutterwave, OPay), and live order tracking.

---

## 🚀 How to Run the Backend Standalone

### Option 1: Quick Run (Batch Script)
Double-click `start_backend.bat` or run:
```cmd
start_backend.bat
```

### Option 2: PowerShell Script
```powershell
.\start_backend.ps1
```

### Option 3: Direct Command
```bash
cd apps/api
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 📖 Interactive API Documentation (Swagger & ReDoc)

Once running, access the interactive API docs directly in your browser:

- **Swagger UI (Interactive Playground)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc (Specification Reader)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔌 Core API Endpoints

### 1. Health
- `GET /api/v1/health/` — Server status, database ping, and uptime check.

### 2. Products & Catalog
- `GET /api/v1/products/` — List laptops with category, brand, and search filters.
- `GET /api/v1/products/{id_or_slug}` — Get laptop detail and default specs.
- `GET /api/v1/products/categories` — List laptop categories (Gaming, Pro Creator, Ultrabook, Business).
- `GET /api/v1/products/brands` — List certified brands (TitanForge, Apex, Razer, ROG).

### 3. Hardware Configuration Engine
- `GET /api/v1/configurations/options` — List all customizable dimensions (Color, RAM, SSD, GPU, Display, Artwork).
- `POST /api/v1/configurations/calculate-price` — Authoritative server-side price calculation.

### 4. Orders
- `POST /api/v1/orders/` — Place order with snapshot of configured hardware.
- `GET /api/v1/orders/{order_number}` — Fetch order invoice and status.

### 5. Multi-Gateway Payments
- `POST /api/v1/payments/initialize` — Initiate payment via Paystack, Flutterwave, or OPay.
- `POST /api/v1/payments/webhook/{gateway}` — Process idempotent payment webhook events.
- `GET /api/v1/payments/order/{order_number}/status` — Fetch real-time payment and build status.
