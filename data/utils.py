import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def button_with_icon(icon_code: str, button_text: str, button_key: str = None, css_styles: str = None, tooltip: str = ""):
    """
    Создает кнопку с иконкой.

    :param icon_code: Код иконки для Font Awesome (например, '\\f0fe').
    :param button_text: Текст внутри кнопки.
    :param button_key: Уникальный ключ для кнопки (по умолчанию None).
    :param css_styles: Дополнительные CSS-стили для контейнера (по умолчанию None).
    """
    # Добавляем Font Awesome CSS
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>',
        unsafe_allow_html=True,
    )
    #st.markdown(
    #    f"""
    #    <style>
    #    [data-testid="stButton"][key="{button_key}"] {{
    #        background-image: url('path/to/icon');
    #        background-size: contain;
    #    }}
    #    </style>
    #    """,
    #    unsafe_allow_html=True
    #)

    css_styles = css_styles or f"""
        button p {{
            display: inline-block;  /* Показываем содержимое кнопки */
            font-size: 15px;       /* Размер иконки */
            color: inherit;        /* Наследуем цвет кнопки */
            margin: 0;
        }}
        button p:before {{
            font-family: 'Font Awesome 5 Free';
            content: '{icon_code}';
            display: inline-block;
            padding-right: 3px;
            vertical-align: middle;
            font-weight: 900;
        }}
        }}
    """

    # Обертка для стилей.
    #with stylable_container(key="styled_button_container", css_styles=css_styles):
    #    clicked = st.button(button_text, key=button_key)
    #    return clicked
    with stylable_container(key="styled_button_container", css_styles=css_styles):
        if icon_code:
            # Пустая строка или пробел нужен для корректной работы Streamlit
            clicked = st.button(button_text, key=button_key, help=tooltip)  # Пробел для кнопки
        else:
            clicked = st.button(button_text, key=button_key)
        return clicked