from django.core.management.base import BaseCommand
from billing.services import check_arrears

class Command(BaseCommand):
    help = 'Check for overdue invoices and flag accounts in arrears'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking for overdue invoices...')
        count = check_arrears()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('✔ No accounts in arrears.'))
        else:
            self.stdout.write(self.style.WARNING(
                f'⚠ {count} account(s) flagged as in arrears and lines suspended.'
            ))

        self.stdout.write(self.style.SUCCESS('\nDone.'))