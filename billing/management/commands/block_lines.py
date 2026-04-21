from django.core.management.base import BaseCommand
from accounts.models import Account

class Command(BaseCommand):
    help = 'Suspend all active lines for accounts in arrears'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking for accounts in arrears...')

        accounts_in_arrears = Account.objects.filter(is_in_arrears=True)

        if not accounts_in_arrears.exists():
            self.stdout.write(self.style.SUCCESS('✔ No accounts in arrears.'))
            return

        total_lines_blocked = 0

        for account in accounts_in_arrears:
            lines = account.lines.filter(status='active')
            count = lines.count()
            lines.update(status='suspended')
            total_lines_blocked += count

            self.stdout.write(self.style.WARNING(
                f'⚠ {account.name} — {count} line(s) suspended.'
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {total_lines_blocked} line(s) blocked across {accounts_in_arrears.count()} account(s).'
        ))