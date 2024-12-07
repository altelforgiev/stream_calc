import streamlit as st
import pandas as pd

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Sepal Length", 
                                                "Sepal Width", 
                                                "Petal Length", 
                                                "Petal Width", 
                                                "Variety"])

st.subheader("Add Record")

num_new_rows = st.sidebar.number_input("Add Rows",1,50)
ncol = st.session_state.df.shape[1]  # col count
rw = -1

with st.form(key="add form", clear_on_submit= True):
    cols = st.columns(ncol)
    rwdta = []

    for i in range(ncol):
        rwdta.append(cols[i].text_input(st.session_state.df.columns[i]))

    # you can insert code for a list comprehension here to change the data (rwdta) 
    # values into integer / float, if required

    if st.form_submit_button("Add"):
        if st.session_state.df.shape[0] == num_new_rows:
            st.error("Add row limit reached. Cant add any more records..")
        else:
            rw = st.session_state.df.shape[0] + 1
            st.info(f"Row: {rw} / {num_new_rows} added")
            st.session_state.df.loc[rw] = rwdta

            if st.session_state.df.shape[0] == num_new_rows:
                st.error("Add row limit reached...")

st.dataframe(st.session_state.df)