from django.utils import timezone
from datetime import timedelta
from .models import Invoice, Plan
from accounts.models import Account

def generate_invoice(account_id):
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        raise ValueError("Account not found.")

    lines = account.lines.filter(status='active')

    if not lines.exists():
        raise ValueError("Account has no active lines to bill.")

    total = sum(line.plan.monthly_fee for line in lines if line.plan)

    if total == 0:
        raise ValueError("No billable plans found on active lines.")

    due_date = timezone.now().date() + timedelta(days=30)

    invoice = Invoice.objects.create(
        account=account,
        amount=total,
        due_date=due_date,
        is_paid=False
    )
    return invoice

def generate_invoices_for_all_accounts():
    accounts = Account.objects.filter(status='active')
    results = []

    for account in accounts:
        try:
            invoice = generate_invoice(account.id)
            results.append({
                'account': account.name,
                'invoice_id': invoice.id,
                'amount': str(invoice.amount),
                'due_date': str(invoice.due_date),
                'status': 'generated'
            })
        except ValueError as e:
            results.append({
                'account': account.name,
                'status': 'skipped',
                'reason': str(e)
            })

    return results

def mark_invoice_paid(invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        raise ValueError("Invoice not found.")

    if invoice.is_paid:
        raise ValueError("Invoice is already paid.")

    invoice.is_paid = True
    invoice.save()

    unpaid = Invoice.objects.filter(account=invoice.account, is_paid=False)
    if not unpaid.exists():
        invoice.account.is_in_arrears = False
        invoice.account.save()

    return invoice


def check_arrears():
    today = timezone.now().date()

    overdue_invoices = Invoice.objects.filter(is_paid=False, due_date__lt=today)

    affected_accounts = set()

    for invoice in overdue_invoices:
        account = invoice.account
        if not account.is_in_arrears:
            account.is_in_arrears = True
            account.save()
            affected_accounts.add(account.id)

    return len(affected_accounts)