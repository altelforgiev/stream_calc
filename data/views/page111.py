import os
import sqlite3
import pandas as pd
import streamlit as st  # Ensure Streamlit is installed using `pip install streamlit`
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Путь к базе данных
DB_PATH = "data/transport_enterprises.db"


# Функция для создания базы данных и таблицы, если их еще нет
def create_database():
    os.makedirs("data", exist_ok=True)  # Убедимся, что папка data существует
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS enterprises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Функция для загрузки данных из базы в Pandas DataFrame
def load_data_from_db():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM enterprises"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Функция для сохранения DataFrame в базу данных (заменяет все данные)
def save_data_to_db(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("enterprises", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()


# Функция для добавления новой записи в базу данных
def add_to_db(name, description):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO enterprises (name, description) VALUES (?, ?)", (name, description))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id

# Создаем базу данных и таблицу, если их еще нет
create_database()

# Загружаем данные из базы данных при запуске приложения
if "enterprises" not in st.session_state:
    st.session_state.enterprises = load_data_from_db()

# Интерфейс приложения
#st.title("Управление Транспортными Предприятиями")

# Форма для добавления новой записи
with st.form("add_enterprise_form"):
    enterprise_name = st.text_input("Транспортное предприятие")
    description = st.text_input("Описание предприятия")
    submitted = st.form_submit_button("Добавить предприятие")

    if submitted:
        if enterprise_name.strip() and description.strip():
            new_id = add_to_db(enterprise_name, description)  # Добавляем в базу данных
            st.session_state.enterprises = load_data_from_db()  # Обновляем данные в сессии
            st.success(f"Предприятие успешно добавлено. ID новой записи: {new_id}.")
        else:
            st.error("Оба поля должны быть заполнены!")

# Отображение таблицы
st.subheader("Список Транспортных Предприятий")
if not st.session_state.enterprises.empty:
    # Настраиваем таблицу
    gb = GridOptionsBuilder.from_dataframe(st.session_state.enterprises)
    gb.configure_pagination(paginationAutoPageSize=True)  # Пагинация
    gb.configure_default_column(editable=True)  # Все колонки редактируемые
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)  # Выбор строк через чекбокс
    grid_options = gb.build()

    # Отображение интерактивной таблицы
    grid_response = AgGrid(
        st.session_state.enterprises,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,  # Обновление изменений вручную
        editable=True,
        enable_enterprise_modules=False,
        allow_unsafe_jscode=True,
        #key="transport_table"
        #key=st.session_state.table_key  # Динамический ключ
        key=f"transport_table_{len(st.session_state.enterprises)}"  # Динамический ключ
    )

    # Получаем данные из таблицы
    updated_data = grid_response["data"]

    # Кнопки управления
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Сохранить изменения"):
            # Сохраняем изменения в базу данных
            save_data_to_db(pd.DataFrame(updated_data))
            st.session_state.enterprises = load_data_from_db()  # Синхронизируем с состоянием
            st.success("Изменения успешно сохранены в базе данных!")

    with col2:
        selected_rows = grid_response["selected_rows"]
        if st.button("Удалить выбранные строки"):
            #if len(selected_rows) > 0:
            if selected_rows is not None:
                # Удаляем выбранные строки
                ids_to_delete = selected_rows['id'].astype(float).tolist()
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.executemany("DELETE FROM enterprises WHERE id = ?", [(row_id,) for row_id in ids_to_delete])
                conn.commit()
                conn.close()

                # Обновляем состояние и данные в таблице
                st.session_state.enterprises = load_data_from_db()

                st.success("Выбранные строки успешно удалены!")
            else:
                st.warning("Пожалуйста, выберите строки для удаления.")
else:
    st.warning("Список предприятий пуст. Добавьте данные!")