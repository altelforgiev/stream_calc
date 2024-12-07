
import streamlit as st
#import streamlit_authenticator as stauth
import hmac


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
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
    page="views/about.py",
    title="О программе",
    icon=":material/info:",
    default=True,
)

project_1_page = st.Page(
    page="views/page1.py",
    title="ТРАНСПОРТНЫЕ ПРЕДПРИЯТИЯ",
    icon=":material/room_preferences:"
)

project_2_page = st.Page(
    page="views/page2.py",
    title="МАРШРУТЫ",
    icon=":material/directions_bus:"
)

# --- NAVIGATION SETUP ---
#pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS] ---
pg = st.navigation(
    {
        "─────────────────────────── ": [about_page],
        "───────────────────────────": [project_1_page, project_2_page]
    }
)
# --- RUN NAVIGATION ---
pg.run()

# --- SHARED ON ALL PAGES
st.logo("assets/logo.png")
st.sidebar.text("© ГУ «Управление пассажирского транспорта и автомобильных дорог Карагандинской области»")