# API Reference

Base URL: `http://localhost:8000/api/v1`

## Health Check
- `GET /health` - Service health status
- `GET /health/db` - Database connectivity status

## Products & Catalog
- `GET /products` - List products with filtering by category, brand, price, RAM, Storage, CPU, GPU
- `GET /products/{id}` - Product details with available configuration options
- `GET /categories` - List product categories
- `GET /deals` - Flash deals and promotional campaigns

## Configuration & Pricing Engine
- `GET /products/{id}/configurations` - Available configuration categories & options for a model
- `POST /configurations/price` - Calculate dynamic price breakdown and validate compatibility

## Cart & Orders
- `GET /cart` - Retrieve user or session cart
- `POST /cart/items` - Add item / customized build to cart
- `POST /orders` - Create order with verified pricing
- `POST /payments/initialize` - Initialize Paystack / payment provider transaction
- `POST /payments/webhook` - Authoritative payment webhook verification
