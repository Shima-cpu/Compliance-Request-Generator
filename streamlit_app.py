import streamlit as st
import streamlit.components.v1 as components

# Заголовок страницы
st.title("Compliance генератор запросов")

# Фиксированные части текста на русском и английском
intro_texts = {
    "Русский": """Добрый день,

в соответствии с требованиями регулятора FSC Белиза и законодательством по борьбе с отмыванием денежных средств RoboForex Ltd обязана на регулярной основе осуществлять постоянную проверку и мониторинг личной информации своих клиентов.""",
    "English": """Hello,

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

# Словарь с вариантами для середины текста
queries = {
    "SOF": {
        "Русский": """В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.

Прилагаем список документов, которые можно использовать для проверки происхождения средств.

Вы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе.""",
        "English": """In this regard, we ask you to provide information on the source of funds credited to your trading accounts with RoboForex Ltd.

Attached is a list of documents that can be used to verify the origin of funds.

You can provide us with any documents, such as salary certificates, tax returns, business income, property sales, etc., or any other document specified in the attached document."""
    },
    "ID": {
        "Русский": """В связи с этим, мы просим вас предоставить актуальный паспорт или иной документ, удостоверяющий вашу личность.""",
        "English": """In this regard, we ask you to provide a valid passport or another identity document."""
    },
    "UB": {
        "Русский": """В связи с этим, мы просим вас предоставить счет за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.""",
        "English": """In this regard, we ask you to provide a utility bill or a bank statement to confirm your residential address."""
    },
    "SOF + ID": {
        "Русский": """В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.

Прилагаем список документов, которые можно использовать для проверки происхождения средств.

Вы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе.

Также пожалуйста предоставьте актуальный паспорт или иной документ, удостоверяющий вашу личность.""",
        "English": """In this regard, we ask you to provide information on the source of funds credited to your trading accounts with RoboForex Ltd.

Attached is a list of documents that can be used to verify the origin of funds.

You can provide us with any documents, such as salary certificates, tax returns, business income, property sales, etc., or any other document specified in the attached document.

Additionally, please provide a valid passport or another identity document."""
    },
    "SOF + UB": {
        "Русский": """В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.

Прилагаем список документов, которые можно использовать для проверки происхождения средств.

Вы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе.

Также пожалуйста предоставьте счет за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.""",
        "English": """In this regard, we ask you to provide information on the source of funds credited to your trading accounts with RoboForex Ltd.

Attached is a list of documents that can be used to verify the origin of funds.

You can provide us with any documents, such as salary certificates, tax returns, business income, property sales, etc., or any other document specified in the attached document.

Additionally, please provide a utility bill or a bank statement to confirm your residential address."""
    },
    "SOF + ID + UB": {
        "Русский": """В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.

Прилагаем список документов, которые можно использовать для проверки происхождения средств.

Вы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе.

Также пожалуйста предоставьте актуальный паспорт или иной документ, удостоверяющий вашу личность.

Помимо этого пожалуйста предоставьте счет за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.""",
        "English": """In this regard, we ask you to provide information on the source of funds credited to your trading accounts with RoboForex Ltd.

Attached is a list of documents that can be used to verify the origin of funds.

You can provide us with any documents, such as salary certificates, tax returns, business income, property sales, etc., or any other document specified in the attached document.

Additionally, please provide a valid passport or another identity document.

Moreover, please provide a utility bill or a bank statement to confirm your residential address."""
    }
}

# Выбор запроса
query = st.selectbox("Выберите тип запроса:", list(queries.keys()))

# Выбор языка
language = st.radio("Выберите язык / Select language:", list(intro_texts.keys()))

# Кнопка для генерации текста
if st.button("Сгенерировать текст"):
    text = f"{intro_texts[language]}\n\n{queries[query][language]}\n\n{closing_texts[language]}"
    st.text_area("Сгенерированный текст:", text, height=300)
    components.html(
        f"""
        <button id="copyButton">Скопировать текст</button>
        <script>
            document.getElementById('copyButton').addEventListener('click', function() {{
                const text = `{text.replace("\n", "\\n").replace("'", "\\'")}`;
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
