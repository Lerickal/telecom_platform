from .models import Line
from accounts.models import Account


def provision_line(account_id, msisdn, plan):
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        raise ValueError("Account not found.")

    if Line.objects.filter(msisdn=msisdn).exists():
        raise ValueError("This MSISDN is already in use.")

    line = Line.objects.create(
        account=account,
        msisdn=msisdn,
        plan=plan,
        status='provisioned'
    )
    return line


def activate_line(line_id):
    try:
        line = Line.objects.get(id=line_id)
    except Line.DoesNotExist:
        raise ValueError("Line not found.")

    if line.status == 'active':
        raise ValueError("Line is already active.")

    if line.account.is_in_arrears:
        raise ValueError("Cannot activate line. Account is in arrears.")

    line.status = 'active'
    line.save()
    return line


def suspend_line(line_id):
    try:
        line = Line.objects.get(id=line_id)
    except Line.DoesNotExist:
        raise ValueError("Line not found.")

    if line.status == 'suspended':
        raise ValueError("Line is already suspended.")

    line.status = 'suspended'
    line.save()
    return line


def restore_line(line_id):
    try:
        line = Line.objects.get(id=line_id)
    except Line.DoesNotExist:
        raise ValueError("Line not found.")

    if line.status != 'suspended':
        raise ValueError("Line is not suspended.")

    if line.account.is_in_arrears:
        raise ValueError("Cannot restore line. Account is in arrears.")

    line.status = 'active'
    line.save()
    return line