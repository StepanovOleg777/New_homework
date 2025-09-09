def format_price(price):
    """Форматирует цену для красивого вывода"""
    return f"{price:,.2f} руб.".replace(",", " ")
