import datetime as dt
from typing import Optional


class Calculator:
    """Сохранение записей. Лимиты. Вычесления."""

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_week_stats(self) -> str:
        """Статистика за 7 дней"""
        it_now = dt.datetime.now().date()
        it_week_ago = it_now - dt.timedelta(days=7)
        amount = (record.amount for record in self.records
                  if it_week_ago < record.date <= it_now)
        return sum(amount)

    def add_record(self, record):
        """Сохранение записей"""
        self.records.append(record)

    def get_today_stats(self) -> str:
        """Статистика за день"""
        it_now = dt.datetime.now().date()
        amount = (record.amount for record
                  in self.records if it_now == record.date)
        return sum(amount)

    def get_today_remained(self) -> float:
        """Сколько осталось от лимита."""
        total_amount = self.get_today_stats()
        balance = self.limit - total_amount
        return balance


class Record:
    """Запись данных."""

    def __init__(
            self,
            amount: float,
            comment: str,
            date: Optional[str] = None
    ):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if isinstance(date, str):
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            date is None
            self.date = dt.datetime.now().date()


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""

    def get_calories_remained(self) -> str:
        """Сколько ещё калорий можно/
        нужно получить сегодня."""
        z = self.get_today_remained()
        if z > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    ' но с общей калорийностью не более '
                    f'{z:.0f} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор денег."""

    USD_RATE = 73.0
    EURO_RATE = 85.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        """сколько ещё денег можно потратить сегодня
        в рублях, долларах или евро."""
        if self.get_today_remained() == 0:
            return 'Денег нет, держись'
        currencies = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE),
        }
        currency_na, currency_rate = currencies[currency]
        today_cash_remained = round(self.get_today_remained()
                                    / currency_rate, 2)
        if today_cash_remained > 0:
            return f'На сегодня осталось {today_cash_remained} {currency_na}'
        mod = abs(today_cash_remained)
        return ('Денег нет, держись: твой долг '
                f'- {mod} {currency_na}')
