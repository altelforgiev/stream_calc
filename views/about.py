import streamlit as st

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/profile_image.png", width=640)
with col2:
    st.title("", anchor=False)
    st.write(
    "ПРОГРАММА ДЛЯ ЭВМ «Расчет тарифов за проезд по действующим социально значимым межрайонным (междугородным внутри-областным) маршрутам Карагандинской агломерации»"
    )

st.write("")
st.subheader("Описание", anchor=False)
st.write(
    """
    ГУ «Управление пассажирского транспорта и автомобильных дорог Карагандинской области»
    """
)

