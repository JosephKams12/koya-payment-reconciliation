
#!/usr/bin/env python3

"""Payment reconciliation."""

import json

latest_payments = {}

with open("payments.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        try:
            event = json.loads(line)

            if not isinstance(event, dict):
                continue

            txn_id = event.get("txn_id")
            timestamp = event.get("ts")

            if not txn_id or not timestamp:
                continue

            if (
                txn_id not in latest_payments
                or timestamp > latest_payments[txn_id]["ts"]
            ):
                latest_payments[txn_id] = event

        except (json.JSONDecodeError, TypeError):
            continue

total = 0.0
count = 0

for event in latest_payments.values():
    if event.get("status") == "success":
        total += float(str(event["amount"]).replace(",", ""))
        count += 1

with open("expected.txt", "r", encoding="utf-8") as file:
    expected = int(file.read().strip())

if count != expected:
    print(
        f"Check failed: counted {count} successful payments, "
        f"expected {expected}."
    )
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
