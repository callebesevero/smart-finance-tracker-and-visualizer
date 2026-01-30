import pandas as pd
import plotly.express as px
import functions as f
import streamlit as st

if 'button_validator' not in st.session_state:
    st.session_state.button_validator = False

st.title('Finance manager', text_alignment='center', anchor=False)

if not st.session_state.button_validator:
    finance_database = st.file_uploader(label='Upload your csv finance file', type='csv')
    date_format = st.selectbox(
        'Choose the file date format', 
        options=['dd/mm/yyyy', 'mm/dd/yyyy'],
        index=None,
        placeholder='Choose the file date format'
    )
    bank = st.selectbox(
        'Choose your bank',
        options=['Caixa', 'Developer option'],
        index=None,
        placeholder='Choose the file date format'
    )

    if st.button('Continue'):
        if finance_database is not None and date_format is not None and bank is not None:
            st.session_state.df = pd.read_csv(finance_database)
            st.session_state.date_format = date_format
            st.session_state.bank = bank
            st.session_state.button_validator = True
            st.rerun()
        else:
            st.error('Please upload a file and choose a date format')
else:
    df = st.session_state.df

    if st.session_state.bank == 'Caixa':
        df = df[['Data', 'Histórico/Complemento', 'Favorecido', 'Valor']]

        df['Category'] = df['Histórico/Complemento'].astype(str) + '-' + df['Favorecido'].astype(str)

        is_income = df['Valor'].str.contains('C', na=False)
        df['Income/Expense'] = is_income.map({True: 'I', False: 'E'})

        df['Valor'] = df['Valor'].str.replace('C', '', regex=False).str.replace('D', '', regex=False)

        df = df.drop(columns=['Histórico/Complemento', 'Favorecido'])

        df = df.rename(columns={'Data': 'Date', 'Valor': 'Value'})
    elif st.session_state.bank == 'Developer option':
        df = df[['Date', 'Category', 'INR', 'Income/Expense']]

        df['Income/Expense'] = df['Income/Expense'].replace('Income', 'I')
        df['Income/Expense'] = df['Income/Expense'].replace('Expense', 'E')

        df = df.rename(columns={'INR': 'Value'})

    df['Day'] = ''
    df['Month'] = ''
    df['Year'] = ''
    for i, date in enumerate(df['Date']):
        date = str(date)
        dmy = f.format_date(date, st.session_state.date_format)

        date = f'{dmy[0]}/{dmy[1]}/{dmy[2]}'
        df.at[i, 'Date'] = date
        
        df.at[i, 'Day'] = dmy[0]
        df.at[i, 'Month'] = dmy[1]
        df.at[i, 'Year'] = dmy[2]

    # Calculating total expenses
    total_expenses = df.loc[df['Income/Expense'] == 'E']['Value'].sum()

    # Calculate daily expenses average
    expenses_count = df.value_counts(df['Income/Expense'])['E']
    expenses_daily_average = total_expenses / expenses_count

    # Daily expenses chart
    dfdate = df[['Date', 'Day', 'Month', 'Year', 'Value']].groupby(['Day', 'Month', 'Year', 'Date'])['Value'].sum().reset_index()
    dfdate = dfdate.sort_values(['Year', 'Month', 'Day']).reset_index(drop='index')
    chart_daily_expenses = px.histogram(dfdate, title='Daily expenses', x='Date', y='Value', text_auto=True)

    # Incomes X Expenses
    chart_incomes_expenses = px.pie(df, names='Income/Expense', title='Expenses x Incomes', values='Value')

    # Invested categories
    dfcategory_expense = df.drop(df[df['Income/Expense'] == 'I'].index).reset_index(drop='index')
    dfcategory_expense = dfcategory_expense[['Category', 'Value']]
    dfcategory_expense = dfcategory_expense.groupby('Category').sum()
    dfcategory_expense = dfcategory_expense.sort_values('Value', ascending=False)

    container_total_money = st.container(border=True)
    container_total_money.caption('The total volume of transactions', text_alignment='center')
    container_total_money.header(f.exibition_format(total_expenses), anchor=False, text_alignment='center')
    container_total_money.divider()
    container_total_money.caption('Average of transaction volume/total days', text_alignment='center')
    container_total_money.subheader(f.exibition_format(expenses_daily_average), anchor=False, text_alignment='center')

    st.space('large')

    tab1, tab2 = st.tabs(tabs=['Daily expenses', 'Expenses X Incomes'])
    with tab1:
        st.plotly_chart(chart_daily_expenses)
    with tab2:
        st.plotly_chart(chart_incomes_expenses)

    st.space('large')

    st.dataframe(
        dfcategory_expense, 
        width='stretch'
    )

    st.space('large')

    if st.button('Analyze next'):
        st.session_state.button_validator = False

        if 'df' in st.session_state:
            del st.session_state.df

        st.rerun()