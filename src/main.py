import pandas as pd

df = pd.read_csv('./database/expense_data_1.csv')
df = df[['Date', 'Category', 'INR', 'Income/Expense']]

for i, d in enumerate(df['Date']):
    d = str(d)
    # Get the index after and before the date

    # 23/01/2026 - 00:00:00
    # 00:00:00 - 23/01/2026
    print(f'== {d} ==')

    after_index = d.index('/')
    before_index = d.index('/', after_index+1)

    print(after_index)
    print(before_index)

    df.at[i, 'Date'] = d[0:-5].strip()
    
    day = ''
    month = ''
    year = ''

    bar_count = 0
    for caractere in df['Date'][i]:
        if caractere != '/':
            if bar_count == 0:
                month += caractere
            elif bar_count == 1:
                day += caractere
            else:
                year += caractere
        else:
            bar_count += 1
    
    if len(day) == 1:
        day = f'0{day}'
    if len(month) == 1:
        month = f'0{month}'
    if len(year) != 4:
        print('YEAR_ERROR')
    
    df.at[i, 'Date'] = f'{day}/{month}/{year}'