import streamlit as st
import streamlit.components.v1 as components

# Фиксированные части текста на русском и английском
intro_texts = {
    "Русский": """Добрый день,

в соответствии с требованиями регулятора FSC Белиза и законодательством по борьбе с отмыванием денежных средств RoboForex Ltd обязана на регулярной основе осуществлять постоянную проверку и мониторинг личной информации своих клиентов.""",
    "English": """Good day,

In accordance with the requirements of the FSC Belize regulator and anti-money laundering legislation, RoboForex Ltd is obliged to regularly verify and monitor the personal information of its clients."""
}

closing_texts = {
    "Русский": """Мы ценим ваше сотрудничество.

Если у вас есть какие-либо вопросы, пожалуйста, свяжитесь с нами.

С уважением,""",
    "English": """We appreciate your cooperation.

If you have any questions, please contact us.

Best regards,"""
}

# Варианты для середины текста на русском и английском
queries = {
    "SOF (Источник средств)": {
        "Русский": """
В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.

Прилагаем список документов, которые можно использовать для проверки происхождения средств.

Вы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе.
        """,
        "English": """
In this regard, we ask you to provide information about the source of funds credited to your trading accounts at RoboForex Ltd.

Attached is a list of documents that can be used to verify the origin of funds.

You can provide us with any documents such as salary certificates, tax returns, business income, property sales, etc., or any other document listed in the attached document.
        """
    },
    "ID (Идентификация)": {
        "Русский": """
В связи с этим мы просим вас предоставить актуальный паспорт или иной документ, удостоверяющий вашу личность.
        """,
        "English": """
In this regard, we ask you to provide a valid passport or other identity document.
        """
    },
    "UB (Подтверждение адреса)": {
        "Русский": """
В связи с этим мы просим вас предоставить счет за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.
        """,
        "English": """
In this regard, we ask you to provide a utility bill or bank statement to confirm your residential address.
        """
    },
    "SOF + ID + UB": {
        "Русский": """
В связи с этим, мы просим вас предоставить информацию об источнике средств, актуальный документ, удостоверяющий вашу личность, и счет за коммунальные услуги либо банковскую выписку для подтверждения вашего адреса проживания.
        """,
        "English": """
In this regard, we ask you to provide information about the source of funds, a valid identity document, and a utility bill or bank statement to confirm your residential address.
        """
    },
    "SOF + ID": {
        "Русский": """
В связи с этим, мы просим вас предоставить информацию об источнике средств и актуальный документ, удостоверяющий вашу личность.
        """,
        "English": """
In this regard, we ask you to provide information about the source of funds and a valid identity document.
        """
    },
    "SOF + UB": {
        "Русский": """
В связи с этим, мы просим вас предоставить информацию об источнике средств и счет за коммунальные услуги либо банковскую выписку для подтверждения вашего адреса проживания.
        """,
        "English": """
In this regard, we ask you to provide information about the source of funds and a utility bill or bank statement to confirm your residential address.
        """
    },
    "ID + UB": {
        "Русский": """
В связи с этим, мы просим вас предоставить актуальный документ, удостоверяющий вашу личность, и счет за коммунальные услуги либо банковскую выписку для подтверждения вашего адреса проживания.
        """,
        "English": """
In this regard, we ask you to provide a valid identity document and a utility bill or bank statement to confirm your residential address.
        """
    }
}

# Заголовок страницы
st.title("Генератор текста для запросов")

# Выбор запроса
query = st.selectbox("Выберите тип запроса:", list(queries.keys()))

# Выбор языка
language = st.radio("Выберите язык:", ["Русский", "English"])

# Кнопка для генерации текста
if st.button("Сгенерировать текст"):
    intro = intro_texts[language]
    middle = queries[query][language]
    closing = closing_texts[language]
    text = f"{intro}\n\n{middle}\n\n{closing}"
    
    # Отображение сгенерированного текста
    st.text_area("Сгенерированный текст:", text, height=300)

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
