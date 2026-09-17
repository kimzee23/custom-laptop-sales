import asyncio
import sys
import traceback

# Import test cases from tests.test_payment_service
from tests.test_payment_service import (
    test_db,
    test_1_new_payment_creation,
    test_2_same_idempotency_key_returns_existing,
    test_3_gateway_timeout_and_verification_recovery,
    test_4_duplicate_webhook_safely_ignored,
    test_5_successful_payment_fulfills_order,
    test_6_duplicate_payment_completed_event_is_idempotent,
    test_7_concurrent_requests_handled_safely
)

async def run_all():
    lines = []
    lines.append("=" * 70)
    lines.append("RUNNING PAYMENT ARCHITECTURE TEST SUITE")
    lines.append("=" * 70)

    tests = [
        ("Test 1: New payment creation & gateway invocation", test_1_new_payment_creation),
        ("Test 2: Same idempotency key (gateway NOT re-invoked, existing returned)", test_2_same_idempotency_key_returns_existing),
        ("Test 3: Gateway timeout & verification recovery", test_3_gateway_timeout_and_verification_recovery),
        ("Test 4: Duplicate webhook safely ignored & deduplicated", test_4_duplicate_webhook_safely_ignored),
        ("Test 5: Successful payment triggers decoupled order fulfillment", test_5_successful_payment_fulfills_order),
        ("Test 6: Duplicate payment completed event is idempotent", test_6_duplicate_payment_completed_event_is_idempotent),
        ("Test 7: Concurrent requests with same idempotency key handled safely", test_7_concurrent_requests_handled_safely),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        # Create fresh DB session for each test
        async for session in test_db():
            try:
                await test_fn(session)
                lines.append(f"  [PASS] {name}")
                passed += 1
            except Exception as e:
                lines.append(f"  [FAIL] {name}: {e}")
                failed += 1
            break

    lines.append("=" * 70)
    lines.append(f"RESULTS: {passed} PASSED, {failed} FAILED")
    lines.append("=" * 70)

    output = "\n".join(lines)
    print(output)
    import os
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_log.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(output)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_all())
