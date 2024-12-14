import os
import sqlite3
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

DB_PATH = "data/transport_enterprises.db"


# Функции для работы с БД предприятий (остаются такими же, как в page1.py)
# --- Начало кода для page2.py ---

def load_data_from_db():
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT * FROM enterprises"
        df = pd.read_sql_query(query, conn)
    return df


def add_to_db(new_data):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO enterprises (name, address, phone_number, email)
            VALUES (?, ?, ?, ?)
        """, (new_data["name"], new_data["address"], new_data["phone"], new_data["email"]))



# Функция для создания таблицы маршрутов, если ее нет
def create_routes_table():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                service_days INTEGER,
                daily_trips INTEGER,
                trip_length REAL,
                fuel_type TEXT,
                enterprise_id INTEGER,
                FOREIGN KEY (enterprise_id) REFERENCES enterprises(id)
            )
        """)


# Функция для загрузки данных маршрутов из базы данных
def load_routes_data():
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT * FROM routes"
        df = pd.read_sql_query(query, conn)
    return df



def save_routes_data(df):
    with sqlite3.connect(DB_PATH) as conn:
        if not df.empty and "id" in df.columns:
            df["id"] = df["id"].astype(int)
        elif not df.empty:
            raise ValueError("Поле `id` отсутствует в DataFrame")

        if not df.empty:
            for _, row in df.iterrows():
                update_query = f"""
                    UPDATE routes 
                    SET name = ?, service_days = ?, daily_trips = ?, 
                        trip_length = ?, fuel_type = ?, enterprise_id = ?
                    WHERE id = ?
                """
                conn.execute(update_query, (
                    row['name'], row['service_days'], row['daily_trips'],
                    row['trip_length'], row['fuel_type'], row['enterprise_id'], row['id']
                ))
            conn.commit()  # Important to commit changes


def create_fuel_types_table():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fuel_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        # Insert initial values if the table is empty
        cursor = conn.execute("SELECT COUNT(*) FROM fuel_types")
        if cursor.fetchone()[0] == 0:
            default_fuel_types = ["Дизель", "Бензин", "Газ"]
            conn.executemany("INSERT INTO fuel_types (name) VALUES (?)", [(fuel,) for fuel in default_fuel_types])


def load_fuel_types():
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT name FROM fuel_types"
        fuel_types = pd.read_sql_query(query, conn)['name'].tolist()
        return fuel_types

create_fuel_types_table()

create_routes_table()  # Создаем таблицу маршрутов при запуске

if "routes" not in st.session_state:
    st.session_state.routes = load_routes_data()

st.title("Управление Маршрутами")

# Выбор предприятия
enterprises = load_data_from_db()
enterprise_names = enterprises['name'].tolist()
selected_enterprise = st.selectbox("Выберите предприятие:", enterprise_names)

# --- Форма для добавления маршрута ---
with st.form("add_route_form"):
    route_name = st.text_input("Наименование маршрута")
    service_days = st.number_input("Количество дней обслуживания", min_value=0, step=1)
    daily_trips = st.number_input("Ежедневное количество кругорейсов", min_value=0, step=1)
    trip_length = st.number_input("Протяженность кругорейса, км", min_value=0.0, step=0.1)
    fuel_types = load_fuel_types()
    fuel_type = st.selectbox("Вид топлива", fuel_types)

    if st.form_submit_button("Добавить маршрут"):
        if all([route_name, service_days, daily_trips, trip_length, fuel_type]):

            selected_enterprise_id = enterprises[enterprises['name'] == selected_enterprise]['id'].values[0]
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("""
                    INSERT INTO routes (name, service_days, daily_trips, trip_length, fuel_type, enterprise_id)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                             (route_name, service_days, daily_trips, trip_length, fuel_type, selected_enterprise_id)
                             )
            st.session_state.routes = load_routes_data()
            st.success("Маршрут успешно добавлен!")


        else:
            st.error("Заполните все поля!")

# --- Отображение таблицы маршрутов ---

st.subheader("Список Маршрутов")

if not st.session_state.routes.empty:
    gb_routes = GridOptionsBuilder.from_dataframe(st.session_state.routes)
    for col in st.session_state.routes.columns:
        gb_routes.configure_column(col, editable=True)

    gb_routes.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_options_routes = gb_routes.build()
    grid_response_routes = AgGrid(st.session_state.routes, gridOptions=grid_options_routes,
                                  update_mode=GridUpdateMode.MODEL_CHANGED,
                                  key=f"routes_table_{len(st.session_state.routes)}")

    updated_routes_data = grid_response_routes["data"]
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Сохранить изменения маршрутов", key="save_routes_button"):
            save_routes_data(pd.DataFrame(updated_routes_data))
            st.session_state.routes = load_routes_data()
            st.success("Изменения в маршрутах успешно сохранены!")

    with col2:
        selected_rows_routes = grid_response_routes.get("selected_rows")
        if st.button("Удалить выбранные маршруты", key="delete_routes_button"):
            if selected_rows_routes is not None:
                ids_to_delete = selected_rows_routes['id'].astype(float).tolist() #[row['id'] for row in selected_rows_routes]
                with sqlite3.connect(DB_PATH) as conn:
                    conn.executemany("DELETE FROM routes WHERE id = ?", [(row_id,) for row_id in ids_to_delete])
                st.session_state.routes = load_routes_data()
                st.success("Выбранные маршруты успешно удалены!")
                st.rerun()


else:
    st.warning("Список маршрутов пуст. Добавьте данные!")
