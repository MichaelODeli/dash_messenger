import datetime

def get_current_date_str(plus5days=False):
    "Получить текущую дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now_plus5days = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    return now_plus5days if plus5days else now