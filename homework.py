import datetime as dt
from typing import Optional

it_now = dt.datetime.now().date()


class Calculator:
    """Статистика"""
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_week_stats(self) -> str:
        it_week_ago = it_now - dt.timedelta(days=7)
        amount = ([record.amount for record in self.records
                   if it_week_ago <= record.date and (record.date <= it_now)])
        return sum(amount)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self) -> str:
        amount = ([record.amount for record
                   in self.records if it_now == record.date])
        return sum(amount)

    def get_today_remained(self) -> float:
        total_amount = self.get_today_stats()
        balance = self.limit - total_amount
        return balance


class Record:
    """Запись данных"""
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
            date = dt.datetime.strptime(date, date_format).date()
        self.date = date
        if date is None:
            self.date = dt.datetime.now().date()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        total = self.limit - self.get_today_stats()

        if total > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {total:.0f} кКал')

        return 'Хватит есть!'


class CashCalculator (Calculator):
    USD_RATE = 73.0
    EURO_RATE = 85.0

    def get_today_cash_remained(self, currency):
        """Сколько ещё можно потратить сегодня"""
        currencies = {
            'usd': ('USD', CashCalculator.USD_RATE),
            'eur': ('Euro', CashCalculator.EURO_RATE),
            'rub': ('руб', 1.0),
        }
        currency_na, currency_rate = currencies[currency]
        today_cash_remained = round(self.get_today_remained()
                                    / currency_rate, 2)

        if today_cash_remained > 0:
            return f'На сегодня осталось {today_cash_remained} {currency_na}'
        elif today_cash_remained < 0:
            return f'Денег нет, держись: твой долг ' \
                   f'- {abs(today_cash_remained)} ' \
                   f'{currency_na}'
        else:
            return 'Денег нет, держись'
