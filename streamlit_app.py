import streamlit as st
import html

# Фиксированные части текста
intro = """Добрый день,

в соответствии с требованиями регулятора FSC Белиза и законодательством по борьбе с отмыванием денежных средств RoboForex Ltd обязана на регулярной основе осуществлять постоянную проверку и мониторинг личной информации своих клиентов."""

closing = """Мы ценим ваше сотрудничество.

Если у вас есть какие-либо вопросы, пожалуйста, свяжитесь с нами.

С уважением,"""

# Словарь с вариантами для середины текста
queries = {
    "SOF (Источник средств)": """
В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.

Прилагаем список документов, которые можно использовать для проверки происхождения средств.

Вы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе.
    """,
    "ID (Идентификация)": """
В связи с этим мы просим вас предоставить актуальный паспорт или иной документ, удостоверяющий вашу личность.
    """,
    "UB (Подтверждение адреса)": """
В связи с этим мы просим вас предоставить счет за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.
    """
}

# Заголовок страницы
st.title("Генератор текста для запросов")

# Выбор запроса
query = st.selectbox("Выберите тип запроса:", list(queries.keys()))

# Кнопка для генерации текста
if st.button("Сгенерировать текст"):
    middle = queries[query]
    text = f"{intro}\n\n{middle}\n\n{closing}"
    
    # Отображение сгенерированного текста
    st.text_area("Сгенерированный текст:", text, height=300)

    # Экранирование текста для HTML и JavaScript
    escaped_text = html.escape(text).replace("\n", "<br>")

    # Добавляем кнопку "Copy to Clipboard" с использованием JavaScript
    copy_button_html = f"""
    <button onclick="navigator.clipboard.writeText('{escaped_text}')">Скопировать текст</button>
    """
    st.markdown(copy_button_html, unsafe_allow_html=True)
