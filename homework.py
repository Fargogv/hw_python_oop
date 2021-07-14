import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_week_stats(self):
        its_now = dt.datetime.now().date()
        its_week_ago = its_now - dt.timedelta(days=7)
        amount = ([record.amount for record in self.records
                   if its_week_ago <= record.date and record.date <= its_now ])
        return sum(amount)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        its_now = dt.datetime.now().date()
        amount = ([record.amount for record
                   in self.records if its_now == record.date])
        return sum(amount)


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if isinstance(date, str):
            date = dt.datetime.strptime(date, date_format).date()
        self.date = date
        if date is None:
            self.date = dt.datetime.now().date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        total_amount = self.get_today_stats()
        balance = self.limit - total_amount
        if total_amount < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё,' +
                    f' но с общей калорийностью не более {balance:.0f} кКал')
        elif total_amount >= self.limit:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 74.46
    EURO_RATE = 88.29

    def get_today_cash_remained(self, currency):
        currency_name = {"rub": ("руб", 1),
                         "usd": ("USD", self.USD_RATE),
                         "eur": ("Euro", self.EURO_RATE)}

        total_amount = self.get_today_stats()
        if currency in currency_name:
            currency_presentation, exchange_rate = currency_name[currency]
            balance = abs((self.limit - total_amount) / exchange_rate)
            if total_amount < self.limit:
                return ('На сегодня' +
                        f' осталось {balance:.2f} {currency_presentation}')
            elif total_amount == self.limit:
                return 'Денег нет, держись'
            else:
                return ('Денег нет, держись: твой' +
                        f' долг - {balance:.2f} {currency_presentation}')
