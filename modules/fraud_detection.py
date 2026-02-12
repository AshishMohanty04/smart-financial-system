def detect_fraud(transactions):
    frauds = []

    for txn in transactions:
        if txn["debit"] > 50000:
            txn["fraud_reason"] = "High Debit Transaction"
            frauds.append(txn)

    return frauds
