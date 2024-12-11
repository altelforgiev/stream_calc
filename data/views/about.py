import streamlit as st

#st.write("")
#st.subheader("О ПРОГРАММЕ", anchor=False)
#st.write()


program_description = """
<h2 style="color:blue;text-align:center;">Информация о программе</h2>
<p>Программное обеспечение <b>«Расчет тарифов за проезд по действующим социально значимым межрайонным (междугородным внутриобластным) маршрутам Карагандинской агломерации»</b> разработано Научно-техническим центром <a href="https://www.kstu.kz/nauchno-tehnicheskij-tsentr-promyshlennyj-transport/" target="_blank">«STU-ENGINEERING»</a> Карагандинского технического университета имени Абылкаса Сагинова для Государственного учреждения <a href="https://www.gov.kz/memleket/entities/karaganda-transport" target="_blank">
«Управление пассажирского транспорта и автомобильных дорог Карагандинской области»</a>
в рамках выполнения научно-исследовательской работы на тему «Проведение научно-исследовательской работы по изучению транспортной системы Карагандинской агломерации и разработка Концепции развития транспортной системы Карагандинской агломерации до 2030 года» (Договор №113 2024-11-21).</p>
"""
st.markdown(program_description, unsafe_allow_html=True)
# The detailed, consolidated HTML content above already replaces this html_content variable, making it redundant.