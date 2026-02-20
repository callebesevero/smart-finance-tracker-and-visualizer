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


def bank_format(df, bank):
    if bank == 'Caixa':
        is_income = df['Valor'].str.contains('C', na=False)
        df['Income/Expense'] = is_income.map({True: 'I', False: 'E'})

        df = df.rename(columns={'Data': 'Date', 'Valor': 'Value', 'Favorecido': 'Category'})

        df['Value'] = df['Value'].str.replace('C', '', regex=False).str.replace('D', '', regex=False)
        df['Value'] = df['Value'].str.replace('.', '')
        df['Value'] = df['Value'].astype(float) / 100
    elif bank == 'Developer option':
        df['Income/Expense'] = df['Income/Expense'].replace('Income', 'I')
        df['Income/Expense'] = df['Income/Expense'].replace('Expense', 'E')

        df = df.rename(columns={'INR': 'Value'})
    return df