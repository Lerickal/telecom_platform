from .models import Account


def create_account(name, email, phone_number):
    if Account.objects.filter(email=email).exists():
        raise ValueError("An account with this email already exists.")

    account = Account.objects.create(
        name=name,
        email=email,
        phone_number=phone_number,
        status='active',
        is_in_arrears=False
    )
    return account


def update_account(account_id, data):
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        raise ValueError("Account not found.")

    for field, value in data.items():
        setattr(account, field, value)

    account.save()
    return account