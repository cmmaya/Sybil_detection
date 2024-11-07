def get_unique_accounts(transactions):
    unique_accounts = set()
    for frm, to in transactions:
        unique_accounts.add(frm)
        unique_accounts.add(to)
    return len(unique_accounts)