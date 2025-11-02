from collections import defaultdict
from typing import Dict, Iterable

# debts[u] positive -> u is owed; negative -> u owes
def compute_balances(expenses: Iterable[dict], payments: Iterable[dict]) -> Dict[int, float]:
    bal = defaultdict(float)
    for e in expenses:
        amount = float(e["amount"])  # payer pays total
        bal[e["payer_id"]] += amount
        for uid, share in e["shares"].items():
            bal[int(uid)] -= float(share)
    for p in payments:
        bal[p["payer_id"]] -= float(p["amount"])  # payer pays payee
        bal[p["payee_id"]] += float(p["amount"])  # payee receives
    return dict(bal)

