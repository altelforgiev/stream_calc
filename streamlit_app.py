import os
import streamlit as st
# import streamlit_authenticator as stauth
import hmac

# --- LANGUAGE SETUP ---
translations = {
    "en": {
        "password": "Password",
        "password_incorrect": "Password incorrect",
        "about": "About",
        "project_1": "TRANSPORT ENTERPRISES",
        "project_2": "ROUTES",
        "project_3": "CALCULATING FARES",
        "footer": "2024 © Transport and Roads Department of Karagandy Region",
    },
    "ru": {
        "password": "Пароль",
        "password_incorrect": "Неверный пароль",
        "about": "О программе",
        "project_1": "ТРАНСПОРТНЫЕ ПРЕДПРИЯТИЯ",
        "project_2": "МАРШРУТЫ",
        "project_3": "РАСЧЕТ ТАРИФОВ",
        "footer": "2024 © ГУ «Управление пассажирского транспорта и автомобильных дорог Карагандинской области»",
    },
    "kk": {
        "password": "Құпия сөз",
        "password_incorrect": "Құпия сөз қате",
        "about": "Бағдарлама туралы",
        "project_1": "КӨЛІК КӘСІПОРЫНДАРЫ",
        "project_2": "МАРШРУТТАР",
        "project_3": "ТАРИФТЕРДІ ЕСЕПТЕУ",
        "footer": "2024 © Қарағанды облысының жолаушылар көлігі және автомобиль жолдары басқармасы",
    },
}

selected_language = st.sidebar.radio(
    ":material/language:", ["kk", "ru", "en"], index=1
)
lang = translations[selected_language]





# Add a check to use `os.environ["password"]` if `st.secrets["password"]` does not exist.
password_source = st.secrets["password"] if "password" in st.secrets else os.environ["password"]


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], password_source):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False
            st.error(lang["password_incorrect"])

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        lang["password"], type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


# --- PAGE SETUP ---

st.html("""
  <style>
    [alt=Logo] {
      height: 3.5rem;
    }
  </style>
        """)

about_page = st.Page(
    page='data/views/about.py',
    title=lang["about"],
    icon=":material/info:",
    default=True,
)

project_1_page = st.Page(
    page="data/views/page1.py",
    title=lang["project_1"],
    icon=":material/room_preferences:"
)

project_2_page = st.Page(
    page="data/views/page2.py",
    title=lang["project_2"],
    icon=":material/directions_bus:"
)

project_3_page = st.Page(
    page="data/views/page3.py",
    title=lang["project_3"],
    icon=":material/calculate:"
)

# --- NAVIGATION SETUP ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS] ---
pg = st.navigation(
    {
        "─────────────────────────── ": [about_page],
        "───────────────────────────": [project_1_page, project_2_page, project_3_page]
    }
)
# --- RUN NAVIGATION ---
pg.run()

# --- SHARED ON ALL PAGES
st.logo("data/assets/logo.png")
st.sidebar.text(lang["footer"])
