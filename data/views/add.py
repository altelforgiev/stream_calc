import streamlit as st
import pandas as pd

# Initialize a placeholder for storing enterprises in session state
if 'enterprises' not in st.session_state:
    st.session_state.enterprises = pd.DataFrame(columns=["Транспортное предприятие", "Описание"])


def add_enterprise(name, description):
    new_data = {"Транспортное предприятие": name, "Описание": description}
    st.session_state.enterprises = st.session_state.enterprises.append(new_data, ignore_index=True)


def edit_enterprise(index, name, description):
    if 0 <= index < len(st.session_state.enterprises):
        st.session_state.enterprises.at[index, "Транспортное предприятие"] = name
        st.session_state.enterprises.at[index, "Описание"] = description


def delete_enterprise(index):
    if 0 <= index < len(st.session_state.enterprises):
        st.session_state.enterprises = st.session_state.enterprises.drop(index).reset_index(drop=True)


st.title("Управление Транспортными Предприятиями")

# Input fields for the form
with st.form("enterprise_form"):
    enterprise_name = st.text_input("Транспортное предприятие")
    description = st.text_input("Описание")
    action = st.selectbox("Действие", ["Добавить", "Редактировать", "Удалить"])
    index = st.number_input("Индекс (только для редактирования/удаления)", min_value=0, step=1, format="%d")
    submitted = st.form_submit_button("Применить")

    if submitted:
        if action == "Добавить":
            add_enterprise(enterprise_name, description)
            st.success("Предприятие добавлено!")
        elif action == "Редактировать":
            edit_enterprise(index, enterprise_name, description)
            st.success("Предприятие обновлено!")
        elif action == "Удалить":
            delete_enterprise(index)
            st.success("Предприятие удалено!")

# Display the enterprise table
st.subheader("Список Транспортных Предприятий")
st.dataframe(st.session_state.enterprises)
