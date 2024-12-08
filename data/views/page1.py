import locale
locale.setlocale(locale.LC_ALL)
import calendar
import datetime
import streamlit as st
import pandas as pd


#months = list(calendar.month_name[1:])

#with st.form("entry_form", clear_on_submit=True):
#    col1, col2 = st.columns(2)
#    col1.selectbox("Выберите месяц:", months, key="month")    

d = st.date_input("Выберите дату", datetime.date.today())

df = pd.DataFrame(columns=['name','age','color'])
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
config = {
    'name' : st.column_config.TextColumn('Наименование', width='large', required=True),
    'age' : st.column_config.NumberColumn('Срок службы', min_value=0, max_value=122),
    'color' : st.column_config.SelectboxColumn('Цвет', options=colors)
}

result = st.data_editor(df, column_config = config, num_rows='dynamic')

if st.button('Get results'):
    st.write(result)
