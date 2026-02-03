def format_date(date, datetype):
    date = date.split()

    for part in date:
        if '/' in part:
            date = part
            break

    after_index = date.index('/')
    before_index = date.index('/', after_index+1)

    if not datetype == 'dd/mm/yyyy': # Is mm/dd/yyyy
        day = date[after_index+1:before_index]
        month = date[:after_index]
        year = date[before_index+1:]
    else:
        day = date[:after_index]
        month = date[after_index+1:before_index]
        year = date[before_index+1:]
    
    if len(day) == 1:
        day = '0' + day
    if len(month) == 1:
        month = '0' + month
    return [day, month, year]


def exhibition_format(
        text: float | int, 
        currency: str = 'R$'
):
    return f'{currency} {text:.2f}'