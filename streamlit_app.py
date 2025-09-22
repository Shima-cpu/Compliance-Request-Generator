import streamlit as st
import streamlit.components.v1 as components

st.title("Compliance request template")

# ----- фиксированные части -----
intro_texts = {
    "Русский": """Добрый день,

в соответствии с требованиями регулятора FSC Белиза и законодательством по борьбе с отмыванием денежных средств RoboForex Ltd обязана на регулярной основе осуществлять постоянную проверку и мониторинг личной информации своих клиентов.""",
    "English": """Hello,

in accordance with the requirements of the FSC Belize regulator and anti-money laundering legislation, RoboForex Ltd is obliged to regularly verify and monitor the personal information of its clients."""
}

closing_texts = {
    "Русский": """Мы ценим ваше сотрудничество.

Если у вас есть какие-либо вопросы, пожалуйста, свяжитесь с нами.

С уважением,""",
    "English": """We appreciate your cooperation.

If you have any questions, please contact us.

Best regards,"""
}

# ----- адаптивные блоки -----
# lead — первый, add — второй, final — третий и последующие
blocks = {
    "SOF": {
        "Русский": {
            "lead": "В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.",
            "add":  "Также, пожалуйста, предоставьте информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.",
            "final": "Помимо этого, пожалуйста, предоставьте информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.",
            "rest": "\n\nПрилагаем список документов, которые можно использовать для проверки происхождения средств.\n\nВы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе."
        },
        "English": {
            "lead": "In this regard, we ask you to provide information on the source of funds credited to your trading accounts with RoboForex Ltd.",
            "add":  "Additionally, please provide information on the source of funds credited to your trading accounts with RoboForex Ltd.",
            "final": "Moreover, please provide information on the source of funds credited to your trading accounts with RoboForex Ltd.",
            "rest": "\n\nAttached is a list of documents that can be used to verify the origin of funds.\n\nYou can provide us with any documents, such as salary certificates, tax returns, business income, property sales, etc., or any other document specified in the attached document."
        }
    },
    "ID": {
        "Русский": {
            "lead": "В связи с этим, мы просим вас предоставить скан или фото актуального паспорта, удостоверяющего вашу личность.",
            "add":  "Также, пожалуйста, предоставьте скан или фото актуального паспорта, удостоверяющего вашу личность.",
            "final": "Помимо этого, пожалуйста, предоставьте скан или фото актуального паспорта, удостоверяющего вашу личность.",
            "rest": ""
        },
        "English": {
            "lead": "In this regard, we ask you to provide a scan or photo of your valid passport or another identity document.",
            "add":  "Additionally, please provide a scan or photo of your valid passport or another identity document.",
            "final": "Moreover, please provide a scan or photo of your valid passport or another identity document.",
            "rest": ""
        }
    },
    "UB": {
        "Русский": {
            "lead": "В связи с этим, мы просим вас предоставить счёт за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.",
            "add":  "Также, пожалуйста, предоставьте счёт за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.",
            "final": "Помимо этого, пожалуйста, предоставьте счёт за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.",
            "rest": ""
        },
        "English": {
            "lead": "In this regard, we ask you to provide a utility bill or a bank statement to confirm your residential address.",
            "add":  "Additionally, please provide a utility bill or a bank statement to confirm your residential address.",
            "final": "Moreover, please provide a utility bill or a bank statement to confirm your residential address.",
            "rest": ""
        }
    }
}

# Мультивыбор
selected_parts = st.multiselect(
    "Choose your request:",
    options=["SOF", "ID", "UB"],
    default=["SOF"]
)

# Фиксированный приоритет
PRIORITY = ["SOF", "ID", "UB"]

def sort_by_priority(keys):
    return [k for k in PRIORITY if k in keys]

language = st.radio("Select request language:", list(intro_texts.keys()))

# ----- генерация середины с учётом lead / add / final -----
def render_middle_adaptive(lang: str, reqs: list) -> str:
    ordered = sort_by_priority(reqs)
    parts = []
    for i, r in enumerate(ordered):
        seg = blocks[r][lang]
        if i == 0:
            first_sentence = seg["lead"]
        elif i == 1:
            first_sentence = seg["add"]
        else:
            first_sentence = seg["final"]
        parts.append((first_sentence + seg.get("rest", "")).strip())
    return "\n\n".join(parts)

# экранирование для JS
def js_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
         .replace("`", "\\`")
         .replace("\r", "")
         .replace("\n", "\\n")
    )

# ----- генерация -----
if st.button("Generate text"):
    middle_text = render_middle_adaptive(language, selected_parts) if selected_parts else ""
    text = f"{intro_texts[language]}\n\n{middle_text}\n\n{closing_texts[language]}".strip()

    st.text_area("Result:", text, height=320)

    components.html(
        f"""
        <button id="copyButton">Copy text</button>
        <script>
            document.getElementById('copyButton').addEventListener('click', function() {{
                const text = `{js_escape(text)}`;
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
