import pandas as pd
import plotly.express as px
import functions

df = pd.read_csv('./database/expense_data_1.csv')
df = df[['Date', 'Category', 'INR', 'Income/Expense']]

df['Day'] = ''
df['Month'] = ''
df['Year'] = ''

datetype = 'mm/dd/yyyy'
for i, date in enumerate(df['Date']):
    date = str(date)
    
    dmy = functions.date_format(date, datetype)

    date = f'{dmy[0]}/{dmy[1]}/{dmy[2]}'

    df.at[i, 'Date'] = date
    
    df.at[i, 'Day'] = dmy[0]
    df.at[i, 'Month'] = dmy[1]
    df.at[i, 'Year'] = dmy[2]

# Calculating total expenses
total_expenses = df.loc[df['Income/Expense'] == 'Expense']['INR'].sum()

# Calculate daily expenses average
expenses_count = df.value_counts(df['Income/Expense'])['Expense']

expenses_daily_average = total_expenses / expenses_count

# Daily expenses chart
dfdate = df[['Date', 'Day', 'Month', 'Year', 'INR']].groupby(['Day', 'Month', 'Year', 'Date'])['INR'].sum().reset_index()

dfdate = dfdate.sort_values(['Year', 'Month', 'Day']).reset_index(drop='index')

chart = px.histogram(dfdate, x='Date', y='INR', text_auto=True)
chart.show()

# Expenses x Incomes
chart = px.pie(df, names='Income/Expense', title='Expenses x Incomes', values='INR')
chart.show()

# Category that people much expense
dfcategory_expense = df.drop(df[df['Income/Expense'] == 'Income'].index).reset_index(drop='index')
dfcategory_expense = dfcategory_expense[['Category', 'INR']]
dfcategory_expense = dfcategory_expense.groupby('Category').sum()
dfcategory_expense = dfcategory_expense.sort_values('INR', ascending=False)

category_expense = f'The most invested category is {dfcategory_expense.iloc[0].name} and the expense is {dfcategory_expense.iat[0, 0]}'

# Invested categories
print(dfcategory_expense)