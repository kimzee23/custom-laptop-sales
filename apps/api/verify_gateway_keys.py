import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "")
PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY", "")

FLUTTERWAVE_SECRET_KEY = os.getenv("FLUTTERWAVE_SECRET_KEY", "")
FLUTTERWAVE_PUBLIC_KEY = os.getenv("FLUTTERWAVE_PUBLIC_KEY", "")
FLUTTERWAVE_SECRET_HASH = os.getenv("FLUTTERWAVE_SECRET_HASH", "")

OPAY_MERCHANT_ID = os.getenv("OPAY_MERCHANT_ID", "")
OPAY_SECRET_KEY = os.getenv("OPAY_SECRET_KEY", "")
OPAY_PUBLIC_KEY = os.getenv("OPAY_PUBLIC_KEY", "")
OPAY_ENV = os.getenv("OPAY_ENV", "test")

def mask_key(k: str) -> str:
    if not k:
        return "[NOT SET]"
    if len(k) <= 8:
        return "***"
    return f"{k[:6]}...{k[-4:]}"

def verify_all_gateways():
    print("=" * 75)
    print("PAYMENT GATEWAY PRODUCTION READINESS & CREDENTIALS AUDIT")
    print("=" * 75)

    results = []

    # -----------------------
    # 1. PAYSTACK VERIFICATION
    # -----------------------
    print("\n[1] PAYSTACK CHECKOUT:")
    print(f"  Public Key:  {mask_key(PAYSTACK_PUBLIC_KEY)}")
    print(f"  Secret Key:  {mask_key(PAYSTACK_SECRET_KEY)}")
    
    is_live_paystack = PAYSTACK_SECRET_KEY.startswith("sk_live_")
    is_test_paystack = PAYSTACK_SECRET_KEY.startswith("sk_test_")
    
    if not PAYSTACK_SECRET_KEY:
        results.append(("Paystack Secret Key", False, "Missing PAYSTACK_SECRET_KEY in environment"))
    elif "mock" in PAYSTACK_SECRET_KEY.lower():
        results.append(("Paystack Mode", False, "Currently using MOCK/Sandbox credentials (sk_test_mock...)"))
    else:
        # Live ping to Paystack
        try:
            r = httpx.get(
                "https://api.paystack.co/balance",
                headers={"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"},
                timeout=10.0
            )
            if r.status_code == 200:
                mode_str = "PRODUCTION LIVE" if is_live_paystack else "SANDBOX TEST"
                results.append(("Paystack Live API Ping", True, f"SUCCESS ({mode_str} verified)"))
            else:
                results.append(("Paystack Live API Ping", False, f"HTTP {r.status_code}: {r.text[:100]}"))
        except Exception as e:
            results.append(("Paystack Network Ping", False, str(e)))

    # -----------------------
    # 2. FLUTTERWAVE VERIFICATION
    # -----------------------
    print("\n[2] FLUTTERWAVE STANDARD:")
    print(f"  Public Key:   {mask_key(FLUTTERWAVE_PUBLIC_KEY)}")
    print(f"  Secret Key:   {mask_key(FLUTTERWAVE_SECRET_KEY)}")
    print(f"  Secret Hash:  {mask_key(FLUTTERWAVE_SECRET_HASH)}")

    is_live_flw = "FLWSECK-" in FLUTTERWAVE_SECRET_KEY and "TEST" not in FLUTTERWAVE_SECRET_KEY
    if not FLUTTERWAVE_SECRET_KEY:
        results.append(("Flutterwave Secret Key", False, "Missing FLUTTERWAVE_SECRET_KEY in environment"))
    elif "mock" in FLUTTERWAVE_SECRET_KEY.lower():
        results.append(("Flutterwave Mode", False, "Currently using MOCK/Sandbox credentials"))
    else:
        try:
            r = httpx.get(
                "https://api.flutterwave.com/v3/balances",
                headers={"Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}"},
                timeout=10.0
            )
            if r.status_code == 200:
                mode_str = "PRODUCTION LIVE" if is_live_flw else "SANDBOX TEST"
                results.append(("Flutterwave Live API Ping", True, f"SUCCESS ({mode_str} verified)"))
            else:
                results.append(("Flutterwave Live API Ping", False, f"HTTP {r.status_code}: {r.text[:100]}"))
        except Exception as e:
            results.append(("Flutterwave Network Ping", False, str(e)))

    # -----------------------
    # 3. OPAY DIGITAL SERVICES
    # -----------------------
    print("\n[3] OPAY DIGITAL SERVICES:")
    print(f"  Merchant ID:  {mask_key(OPAY_MERCHANT_ID)}")
    print(f"  Secret Key:   {mask_key(OPAY_SECRET_KEY)}")
    print(f"  Public Key:   {mask_key(OPAY_PUBLIC_KEY)}")
    print(f"  Environment:  {OPAY_ENV}")

    if not OPAY_MERCHANT_ID or not OPAY_SECRET_KEY:
        results.append(("OPay Credentials", False, "Missing OPAY_MERCHANT_ID or OPAY_SECRET_KEY"))
    elif "mock" in OPAY_SECRET_KEY.lower():
        results.append(("OPay Mode", False, "Currently using MOCK/Sandbox credentials"))
    else:
        results.append(("OPay Credentials", True, f"Credentials formatted for {OPAY_ENV}"))

    # -----------------------
    # SUMMARY
    # -----------------------
    print("\n" + "=" * 75)
    print("GATEWAY AUDIT REPORT:")
    print("=" * 75)
    for name, ok, msg in results:
        status_tag = "[PASS]" if ok else "[ACTION REQUIRED]"
        print(f"  {status_tag:18} {name:28} : {msg}")
    print("=" * 75)
    print("\nNEXT STEP TO GO LIVE IN PRODUCTION:")
    print("  1. In Paystack Dashboard -> Settings -> API Keys & Webhooks:")
    print("     - Copy 'Live Secret Key' and 'Live Public Key'")
    print("     - Set Webhook URL to: https://api.yourdomain.com/api/v1/payments/webhooks/paystack")
    print("  2. In Flutterwave Dashboard -> Settings -> API Keys & Webhooks:")
    print("     - Copy 'Live Secret Key' and 'Live Public Key'")
    print("     - Set Webhook secret hash & URL to: https://api.yourdomain.com/api/v1/payments/webhooks/flutterwave")
    print("  3. In OPay Merchant Dashboard -> Developer:")
    print("     - Copy Live Merchant ID & Secret Key, set OPAY_ENV=live")
    print("=" * 75)

if __name__ == "__main__":
    verify_all_gateways()
