from django.core.management.base import BaseCommand
from billing.services import generate_invoices_for_all_accounts

class Command(BaseCommand):
    help = 'Generate monthly invoices for all active accounts'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating invoices...')
        results = generate_invoices_for_all_accounts()

        for result in results:
            if result['status'] == 'generated':
                self.stdout.write(self.style.SUCCESS(
                    f"✔ {result['account']} — Invoice #{result['invoice_id']} for R{result['amount']} due {result['due_date']}"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"⚠ {result['account']} — Skipped: {result['reason']}"
                ))

        self.stdout.write(self.style.SUCCESS('\nDone.'))