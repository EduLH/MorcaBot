from django.core.management.base import BaseCommand
from django.db.models import Sum
from expenses.models import Expense
from django.utils import timezone
from utils.services.money import format_brl

class Command(BaseCommand):
    help = "Generates monthly expense report grouped by category"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        month = now.month
        year = now.year

        expenses = Expense.objects.filter(
            created_at__year=year,
            created_at__month=month
        )

        summary = (
            expenses
            .values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        if not summary:
            self.stdout.write("Nenhum gasto registrado neste mês.")
            return

        report = f"📊 Relatório Mensal ({month}/{year})\n\n"

        total_general = 0

        for item in summary:
            val = item["total"]
            report += f"• {item['category__name']}: {format_brl(val)}\n"
            total_general += val

        report += f"\n💰 Total: {format_brl(total_general)}"

        self.stdout.write(report)
