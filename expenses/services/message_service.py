from django.contrib.auth import get_user_model
from utils.services.money import format_brl
from expenses.parser import parse_message
from expenses.models import Expense, Category
from accounts.services.user_service import create_user_with_optional_coupon


User = get_user_model()


def get_or_create_category(name: str):
    return Category.objects.get_or_create(
        name=name.lower().strip()
    )[0]


def process_incoming_message(phone: str, message: str) -> dict:
    # Usa service layer para garantir trial e criação correta
    user, _, _ = create_user_with_optional_coupon(phone=phone)

    if not user.has_active_plan():
        return {
            "status": "blocked",
            "message": "⚠️ Seu plano expirou.\nRenove para continuar usando o Morça.",
        }

    parsed = parse_message(message)

    if not parsed:
        return {
            "status": "error",
            "message": "❌ Não entendi.\nUse: Nome - Categoria - Valor",
        }

    category_obj = get_or_create_category(parsed["category"])

    expense = Expense.objects.create(
        user=user,
        name=parsed["name"],
        category=category_obj,  # Agora FK correta
        amount=parsed["amount"],
    )

    message = f"✅ Gasto registrado:\n{expense.name} - {expense.category.name} - {format_brl(expense.amount)}"

    return {
        "status": "success",
        "message": message,
    }
