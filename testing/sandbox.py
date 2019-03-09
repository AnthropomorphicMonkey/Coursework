import datetime

date = datetime.date(7809, 3, 5)
print(date)
due_year_month_day: list = str(date).split('-')
string_due_date: str = ("{}-{}-{}").format(due_year_month_day[0], int(due_year_month_day[1]), due_year_month_day[2])
print(string_due_date)
