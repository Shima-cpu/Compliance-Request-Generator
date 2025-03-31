import streamlit as st
import streamlit.components.v1 as components

# Фиксированные части текста
intro = """Добрый день,

в соответствии с требованиями регулятора FSC Белиза и законодательством по борьбе с отмыванием денежных средств RoboForex Ltd обязана на регулярной основе осуществлять постоянную проверку и мониторинг личной информации своих клиентов."""

closing = """Мы ценим ваше сотрудничество.

Если у вас есть какие-либо вопросы, пожалуйста, свяжитесь с нами.

С уважением,"""

# Словарь с вариантами для середины текста
queries = {
    "SOF": """
В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.

Прилагаем список документов, которые можно использовать для проверки происхождения средств.

Вы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе.
    """,
    "ID": """
В связи с этим мы просим вас предоставить актуальный паспорт или иной документ, удостоверяющий вашу личность.
    """,
    "UB": """
В связи с этим мы просим вас предоставить счет за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.
    """,
    "SOF + ID + UB": """
В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.

Прилагаем список документов, которые можно использовать для проверки происхождения средств.

Вы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе.

Также пожалуйста предоставьте актуальный документ, удостоверяющий вашу личность и счет за коммунальные услуги либо банковскую выписку, для подтверждения вашего адреса проживания.
    """,
    "SOF + ID": """
В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.

Прилагаем список документов, которые можно использовать для проверки происхождения средств.

Вы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе.

Также пожалуйста предоставьте актуальный документ, удостоверяющий вашу личность.
    """,
    "SOF + UB": """
В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.

Прилагаем список документов, которые можно использовать для проверки происхождения средств.

Вы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе.

Также, пожалуйста, предоставьте счет за коммунальные услуги либо банковскую выписку, для подтверждения вашего адреса проживания.
    """,
    "ID + UB": """
В связи с этим, мы просим вас предоставить актуальный документ, удостоверяющий вашу личность и счет за коммунальные услуги либо банковскую выписку, для подтверждения вашего адреса проживания.
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
    
    # Отображение сгенерированного текста с одинаковыми отступами
    st.markdown(f"<pre style='white-space: pre-line; margin-bottom: 10px;'>{text}</pre>", unsafe_allow_html=True)

    # Подготовка текста для использования в JavaScript
    text_for_js = text.replace("\n", "\\n").replace("'", "\\'")

    # Добавление кнопки для копирования текста через HTML и JavaScript
    components.html(
        f"""
        <button id="copyButton">Скопировать текст</button>
        <script>
            document.getElementById('copyButton').addEventListener('click', function() {{
                const text = `{text_for_js}`;
                navigator.clipboard.writeText(text).then(function() {{
                    alert('Текст скопирован в буфер обмена!');
                }}).catch(function(err) {{
                    alert('Ошибка копирования текста!');
                }});
            }});
        </script>
        """, 
        height=100
    )

