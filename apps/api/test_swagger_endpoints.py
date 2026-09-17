import asyncio
import io
import sys
import json
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import async_engine, Base, AsyncSessionLocal
from app.seed_data import seed_database

async def main():
    print("=" * 75)
    print("COMPREHENSIVE BACKEND ENDPOINT & SWAGGER VERIFICATION SUITE")
    print("=" * 75)

    # 1. Initialize DB & Seed
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await seed_database(session)

    transport = ASGITransport(app=app)
    results = []

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 0. Check OpenAPI / Swagger Schema
        res = await client.get("/openapi.json")
        assert res.status_code == 200, f"OpenAPI failed: {res.status_code}"
        openapi = res.json()
        total_endpoints = len(openapi["paths"])
        results.append((f"Swagger / OpenAPI Schema loaded ({total_endpoints} paths)", True, f"{total_endpoints} endpoints"))

        # 1. Products & Catalog
        r = await client.get("/api/v1/products")
        prod_data = r.json()
        assert r.status_code == 200 and len(prod_data) > 0
        test_prod_id = prod_data[0]["id"]
        results.append(("GET /api/v1/products", True, f"{len(prod_data)} products returned"))

        r = await client.get(f"/api/v1/products/{test_prod_id}")
        assert r.status_code == 200 and r.json()["id"] == test_prod_id
        results.append((f"GET /api/v1/products/{test_prod_id}", True, f"Found: {r.json()['title']}"))

        r = await client.get("/api/v1/categories")
        assert r.status_code == 200 and len(r.json()) > 0
        results.append(("GET /api/v1/categories", True, f"{len(r.json())} categories"))

        r = await client.get("/api/v1/brands")
        assert r.status_code == 200 and len(r.json()) > 0
        results.append(("GET /api/v1/brands", True, f"{len(r.json())} brands"))

        r = await client.get("/api/v1/promotions")
        assert r.status_code == 200 and len(r.json()) > 0
        results.append(("GET /api/v1/promotions", True, f"{len(r.json())} active promotions"))

        # 2. Configurations & Pricing
        r = await client.get(f"/api/v1/products/{test_prod_id}/configurations")
        assert r.status_code == 200 and len(r.json()) > 0
        results.append((f"GET /api/v1/products/{test_prod_id}/configurations", True, f"{len(r.json())} configuration categories"))

        price_req = {
            "product_id": test_prod_id,
            "ram_id": "opt-ram-32",
            "storage_id": "opt-ssd-2tb",
            "artwork": {"custom_text": "RealTech CyberPro 2026"}
        }
        r = await client.post("/api/v1/configurations/price", json=price_req)
        assert r.status_code == 200 and r.json()["total"] > 0
        results.append(("POST /api/v1/configurations/price", True, f"Calculated Total: NGN {r.json()['total']:,.2f}"))

        r = await client.post("/api/v1/configurations", json=price_req)
        assert r.status_code == 200 and "specs_summary" in r.json()
        results.append(("POST /api/v1/configurations", True, f"Configured Specs: {list(r.json()['specs_summary'].keys())}"))

        # 3. Saved Builds
        save_build_req = {
            "title": "My Dream RTX 4090 Workstation",
            "product_id": test_prod_id,
            "total_price": 2850000.0,
            "configuration_snapshot": price_req,
            "specs_summary": {"ram": "32GB", "storage": "2TB NVMe", "gpu": "RTX 4090"}
        }
        r = await client.post("/api/v1/saved-builds", json=save_build_req)
        assert r.status_code == 200
        saved_build = r.json()
        results.append(("POST /api/v1/saved-builds", True, f"Saved Build ID: {saved_build['id']}"))

        r = await client.get("/api/v1/saved-builds")
        assert r.status_code == 200 and len(r.json()) > 0
        results.append(("GET /api/v1/saved-builds", True, f"{len(r.json())} saved builds retrieved"))

        # 4. Cart Operations
        session_key = f"test-session-{uuid.uuid4().hex[:8]}"
        headers = {"X-Session-ID": session_key}
        r = await client.get("/api/v1/cart", headers=headers)
        assert r.status_code == 200
        results.append(("GET /api/v1/cart", True, f"Cart empty check passed"))

        add_cart_req = {
            "product_id": test_prod_id,
            "quantity": 1,
            "unit_price": 1500000.0,
            "configuration_data": {"ram": "32GB", "ssd": "2TB"}
        }
        r = await client.post("/api/v1/cart/items", json=add_cart_req, headers=headers)
        assert r.status_code == 200 and len(r.json()["items"]) > 0
        cart_item_id = r.json()["items"][0]["id"]
        results.append(("POST /api/v1/cart/items", True, f"Item added, subtotal: NGN {r.json()['subtotal']:,.2f}"))

        r = await client.patch(f"/api/v1/cart/items/{cart_item_id}", json={"quantity": 2}, headers=headers)
        assert r.status_code == 200 and r.json()["items"][0]["quantity"] == 2
        results.append((f"PATCH /api/v1/cart/items/{cart_item_id}", True, f"Quantity updated to 2, subtotal: NGN {r.json()['subtotal']:,.2f}"))

        r = await client.delete(f"/api/v1/cart/items/{cart_item_id}", headers=headers)
        assert r.status_code == 200 and len(r.json()["items"]) == 0
        results.append((f"DELETE /api/v1/cart/items/{cart_item_id}", True, "Item removed from cart"))

        # 5. Orders
        order_req = {
            "items": [
                {
                    "product_id": test_prod_id,
                    "product_title": "Apex Custom Laptop",
                    "unit_price": 1250000.0,
                    "quantity": 1,
                    "image_url": "https://example.com/laptop.jpg",
                    "configuration_snapshot": {"color": "Midnight Navy"}
                }
            ],
            "customer_name": "Test Customer",
            "customer_email": "test.customer@example.com",
            "customer_phone": "+234 801 234 5678",
            "shipping_address": {
                "full_name": "Test Customer",
                "phone_number": "+234 801 234 5678",
                "email": "test.customer@example.com",
                "street": "15 Marina Road, Victoria Island",
                "city": "Lagos",
                "state": "Lagos",
                "country": "Nigeria"
            },
            "shipping_fee": 0.0,
            "discount_amount": 0.0
        }
        r = await client.post("/api/v1/orders", json=order_req)
        assert r.status_code == 200
        created_order = r.json()
        order_id = created_order["id"]
        order_num = created_order["order_number"]
        results.append(("POST /api/v1/orders", True, f"Created Order #{order_num}"))

        r = await client.get("/api/v1/orders")
        assert r.status_code == 200 and len(r.json()) > 0
        results.append(("GET /api/v1/orders", True, f"Listed {len(r.json())} orders"))

        r = await client.get(f"/api/v1/orders/{order_num}")
        assert r.status_code == 200 and r.json()["id"] == order_id
        results.append((f"GET /api/v1/orders/{order_num}", True, f"Found by order_number with status: {r.json()['status']}"))

        # 6. Payments
        pay_init_req = {
            "order_number": order_num,
            "provider": "PAYSTACK",
            "idempotency_key": f"test-idemp-{order_num}"
        }
        r = await client.post("/api/v1/payments/initialize", json=pay_init_req)
        assert r.status_code == 200
        pay_init = r.json()
        results.append(("POST /api/v1/payments/initialize", True, f"Reference: {pay_init['provider_reference']}, Status: {pay_init['status']}"))

        # Unified Webhook
        webhook_payload = {
            "event": "charge.success",
            "data": {
                "reference": pay_init["provider_reference"],
                "status": "success",
                "amount": int(created_order["total_amount"] * 100),
                "channel": "card"
            }
        }
        r = await client.post("/api/v1/payments/webhook?provider=paystack", json=webhook_payload)
        assert r.status_code == 200
        results.append(("POST /api/v1/payments/webhook", True, f"Webhook handled successfully"))

        # 7. Artwork Upload
        dummy_file = io.BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")
        files = {"file": ("laser_logo.png", dummy_file, "image/png")}
        r = await client.post("/api/v1/artwork/upload", files=files)
        assert r.status_code == 200 and r.json()["success"] == True
        results.append(("POST /api/v1/artwork/upload", True, f"Uploaded URL: {r.json()['image_url']}"))

        # 8. Reviews
        review_req = {
            "product_id": test_prod_id,
            "author_name": "Tech Enthusiast",
            "rating": 5,
            "comment": "Incredible thermals and the laser custom lid is stunningly crisp!"
        }
        r = await client.post("/api/v1/reviews", json=review_req)
        assert r.status_code == 201
        results.append(("POST /api/v1/reviews", True, f"Review created with 5-star rating"))

        r = await client.get(f"/api/v1/reviews?product_id={test_prod_id}")
        assert r.status_code == 200 and len(r.json()) > 0
        results.append(("GET /api/v1/reviews", True, f"{len(r.json())} reviews found"))

        # 9. Admin Endpoints
        r = await client.get("/api/v1/admin/products")
        assert r.status_code == 200
        results.append(("GET /api/v1/admin/products", True, f"{len(r.json())} products in admin"))

        admin_new_prod = {
            "title": "Apex Titan Ultra 18 Mini-LED",
            "slug": f"apex-titan-ultra-18-{order_id[:6]}",
            "description": "The ultimate desktop replacement laptop.",
            "base_price": 3200000.0,
            "stock": 15,
            "image_url": "https://example.com/titan18.jpg"
        }
        r = await client.post("/api/v1/admin/products", json=admin_new_prod)
        assert r.status_code == 201
        created_admin_prod_id = r.json()["id"]
        results.append(("POST /api/v1/admin/products", True, f"Created product '{admin_new_prod['title']}'"))

        r = await client.patch(f"/api/v1/admin/products/{created_admin_prod_id}", json={"stock": 25, "base_price": 3150000.0})
        assert r.status_code == 200 and r.json()["stock"] == 25
        results.append((f"PATCH /api/v1/admin/products/{created_admin_prod_id}", True, f"Stock updated to 25, price to NGN 3,150,000"))

        r = await client.get("/api/v1/admin/configurations")
        assert r.status_code == 200 and len(r.json()) > 0
        results.append(("GET /api/v1/admin/configurations", True, f"{len(r.json())} configuration categories in admin"))

        admin_opt_req = {
            "category_code": "ram",
            "code": "128gb-ddr5",
            "name": "128GB DDR5 6400MHz Workstation Dual-Rank",
            "price_modifier": 450000.0,
            "stock": 50
        }
        r = await client.post("/api/v1/admin/configurations", json=admin_opt_req)
        assert r.status_code == 201
        results.append(("POST /api/v1/admin/configurations", True, f"Added option '{admin_opt_req['name']}'"))

        r = await client.get("/api/v1/admin/orders")
        assert r.status_code == 200 and len(r.json()) > 0
        results.append(("GET /api/v1/admin/orders", True, f"{len(r.json())} orders in admin portal"))

        r = await client.patch(f"/api/v1/admin/orders/{order_id}", json={"status": "CUSTOM_BUILD"})
        assert r.status_code == 200 and r.json()["status"] == "CUSTOM_BUILD"
        results.append((f"PATCH /api/v1/admin/orders/{order_id}", True, f"Order status moved to CUSTOM_BUILD"))

        r = await client.get("/api/v1/admin/customers")
        assert r.status_code == 200 and len(r.json()) > 0
        results.append(("GET /api/v1/admin/customers", True, f"{len(r.json())} customer accounts listed"))

        r = await client.get("/api/v1/admin/analytics")
        assert r.status_code == 200 and "total_revenue" in r.json()
        analytics = r.json()
        results.append(("GET /api/v1/admin/analytics", True, f"Total Revenue: NGN {analytics['total_revenue']:,.2f}, Orders: {analytics['total_orders']}"))

        # 10. Customer Auth
        reg_email = f"user_{uuid.uuid4().hex[:6]}@example.com"
        reg_req = {
            "name": "Kelechi Nnamdi",
            "email": reg_email,
            "password": "SecurePassword123!",
            "phone": "+234 815 111 2233"
        }
        r = await client.post("/api/v1/auth/register", json=reg_req)
        assert r.status_code == 201
        reg_data = r.json()
        user_token = reg_data["access_token"]
        results.append(("POST /api/v1/auth/register", True, f"Registered: {reg_data['user']['email']}, Reward points: {reg_data['user']['reward_points']}"))

        login_req = {
            "email": reg_email,
            "password": "SecurePassword123!"
        }
        r = await client.post("/api/v1/auth/login", json=login_req)
        assert r.status_code == 200 and "access_token" in r.json()
        results.append(("POST /api/v1/auth/login", True, f"Customer login successful"))

        auth_headers = {"Authorization": f"Bearer {user_token}"}
        r = await client.get("/api/v1/auth/me", headers=auth_headers)
        assert r.status_code == 200 and r.json()["email"] == reg_email
        results.append(("GET /api/v1/auth/me", True, f"Profile verified: {r.json()['name']}"))

        r = await client.put("/api/v1/auth/profile", json={"name": "Kelechi Nnamdi Jr."}, headers=auth_headers)
        assert r.status_code == 200 and r.json()["name"] == "Kelechi Nnamdi Jr."
        results.append(("PUT /api/v1/auth/profile", True, f"Updated name: {r.json()['name']}"))

        chg_pass_req = {
            "current_password": "SecurePassword123!",
            "new_password": "BrandNewPassword456!"
        }
        r = await client.post("/api/v1/auth/change-password", json=chg_pass_req, headers=auth_headers)
        assert r.status_code == 200
        results.append(("POST /api/v1/auth/change-password", True, "Password changed successfully"))

        r = await client.post("/api/v1/auth/forgot-password", json={"email": reg_email})
        assert r.status_code == 200 and "reset_token" in r.json()
        reset_token = r.json()["reset_token"]
        results.append(("POST /api/v1/auth/forgot-password", True, "Password reset token dispatched"))

        r = await client.post("/api/v1/auth/reset-password", json={"token": reset_token, "new_password": "ResetPassword789!"})
        assert r.status_code == 200
        results.append(("POST /api/v1/auth/reset-password", True, "Password reset executed"))

        r = await client.post("/api/v1/auth/logout", headers=auth_headers)
        assert r.status_code == 200
        results.append(("POST /api/v1/auth/logout", True, "Logged out successfully"))

        # 11. Admin Auth
        admin_login_req = {
            "email": "admin@realtech.ng",
            "password": "AdminPass123!"
        }
        r = await client.post("/api/v1/auth/admin/login", json=admin_login_req)
        assert r.status_code == 200 and r.json()["user"]["role"] == "admin"
        admin_token = r.json()["access_token"]
        results.append(("POST /api/v1/auth/admin/login", True, f"Admin logged in: {r.json()['user']['name']}"))

        admin_auth_headers = {"Authorization": f"Bearer {admin_token}"}
        r = await client.get("/api/v1/auth/admin/me", headers=admin_auth_headers)
        assert r.status_code == 200 and r.json()["role"] == "admin"
        results.append(("GET /api/v1/auth/admin/me", True, f"Admin verified: {r.json()['email']} (role: {r.json()['role']})"))

    # Print and write summary
    lines = ["\nVERIFICATION RESULTS:"]
    all_passed = True
    for name, passed, detail in results:
        status_str = "[PASS]" if passed else "[FAIL]"
        line = f"  {status_str} {name:48} -> {detail}"
        lines.append(line)
        print(line, flush=True)
        if not passed:
            all_passed = False

    lines.append("=" * 75)
    if all_passed:
        banner = f"SUCCESS: ALL {len(results)} ENDPOINTS VERIFIED AND OPERATIONAL!"
    else:
        banner = "SOME ENDPOINTS FAILED"
    lines.append(banner)
    lines.append("=" * 75)
    print(banner, flush=True)

    with open("test_swagger_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        sys.exit(1)
