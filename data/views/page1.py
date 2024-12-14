import os
import sqlite3
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Путь к базе данных
DB_PATH = "data/transport_enterprises.db"


# Функция для создания базы данных и таблицы, если их еще нет
def create_database():
    os.makedirs("data", exist_ok=True)  # Убедимся, что папка data существует
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS enterprises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)


# Функция для загрузки данных из базы в Pandas DataFrame
def load_data_from_db():
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT * FROM enterprises"
        df = pd.read_sql_query(query, conn)
    return df


# Функция для сохранения DataFrame в базу данных (заменяет все данные)
def save_data_to_db(df):
    with sqlite3.connect(DB_PATH) as conn:
        # Проверяем, что DataFrame имеет столбец `id`
        if "id" in df.columns:
            df["id"] = df["id"].astype(int)  # Убедимся, что `id` целое число
        else:
            raise ValueError("Поле `id` отсутствует в DataFrame")

        # Удаляем старые данные, но сохраняем структуру таблицы
        conn.execute("DELETE FROM enterprises")
        # Добавляем новые данные
        df.to_sql("enterprises", conn, if_exists="append", index=False)


# Функция для добавления новой записи в базу данных
def add_to_db(name, description):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO enterprises (name, description) VALUES (?, ?)", (name, description))
        new_id = cur.lastrowid
    return new_id


# Создаем базу данных и таблицу, если их еще нет
create_database()

# Загружаем данные из базы данных при запуске приложения
if "enterprises" not in st.session_state:
    st.session_state.enterprises = load_data_from_db()

# Интерфейс приложения
# st.title("Управление Транспортными Предприятиями")

# Состояние для раскрытия формы
if "show_form" not in st.session_state:
    st.session_state.show_form = False

# Кнопка "+/-" для раскрытия/скрытия формы
if st.session_state.show_form:
    button_label = "Скрыть форму"  # Label when form is shown
else:
    button_label = "Добавить предприятие"  # Label when form is hidden

if st.button(button_label):
    st.session_state.show_form = not st.session_state.show_form

# Форма для добавления новой записи (отображается только если show_form == True)
if st.session_state.show_form:
    with st.form("add_enterprise_form"):
        enterprise_name = st.text_input("Транспортное предприятие")
        description = st.text_input("Описание предприятия")
        submitted = st.form_submit_button("Добавить")

        if submitted:
            if enterprise_name.strip() and description.strip():
                new_id = add_to_db(enterprise_name, description)
                st.session_state.enterprises = load_data_from_db()
                st.success(f"Предприятие успешно добавлено. ID: {new_id}.")
                st.session_state.show_form = False  # Скрываем форму после добавления
                st.rerun()  # Обновляем страницу, чтобы форма скрылась
            else:
                st.error("Оба поля должны быть заполнены!")

# Отображение таблицы
st.subheader("Список Транспортных Предприятий")
if not st.session_state.enterprises.empty:
    # Настраиваем таблицу
    gb = GridOptionsBuilder.from_dataframe(st.session_state.enterprises)
    gb.configure_column("id", suppressMovable=True, editable=False)  # `id` теперь НЕ редактируем
    gb.configure_column("name", editable=True)
    gb.configure_column("description", editable=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)  # Выбор строк через чекбокс
    grid_options = gb.build()

    # Отображение интерактивной таблицы
    grid_response = AgGrid(
        st.session_state.enterprises,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,  # Обновление изменений вручную
        key=f"transport_table_{len(st.session_state.enterprises)}"  # Динамический ключ
    )

    # Получаем данные из таблицы
    updated_data = grid_response["data"]

    # Кнопки управления
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Сохранить изменения", key="save_changes_button"):
        #    # Сохраняем изменения в базу данных
            save_data_to_db(pd.DataFrame(updated_data))
            st.session_state.enterprises = load_data_from_db()  # Синхронизируем с состоянием
            st.success("Изменения успешно сохранены в базе данных!")

    with col2:
        selected_rows = grid_response.get("selected_rows")
        if st.button("Удалить выбранные", key="delete_selected_button"):
            if selected_rows is not None:
                ids_to_delete = selected_rows['id'].astype(float).tolist()
                with sqlite3.connect(DB_PATH) as conn:
                    conn.executemany("DELETE FROM enterprises WHERE id = ?", [(row_id,) for row_id in ids_to_delete])

                # Обновляем состояние и данные в таблице
                st.session_state.enterprises = load_data_from_db()
                st.success("Выбранные строки успешно удалены!")
                st.rerun()
            else:
                st.warning("Нет выбранных строк для удаления.")
else:
    st.warning("Список предприятий пуст. Добавьте данные!")