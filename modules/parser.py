import re

def parse_transactions(text):
    pattern = r'(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(\d+\.\d{2})?\s*(\d+\.\d{2})?\s+(\d+\.\d{2})'
    matches = re.findall(pattern, text)

    transactions = []

    for match in matches:
        date, desc, debit, credit, balance = match

        transactions.append({
            "date": date,
            "description": desc,
            "debit": float(debit) if debit else 0,
            "credit": float(credit) if credit else 0,
            "balance": float(balance)
        })

    return transactions
