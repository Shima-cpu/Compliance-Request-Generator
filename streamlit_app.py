import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Compliance request templates",
    page_icon="📄",
    layout="centered"
)

st.title("Compliance request templates")


# =========================
# Helpers
# =========================

def js_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
         .replace("`", "\\`")
         .replace("${", "\\${")
         .replace("\r", "")
         .replace("\n", "\\n")
    )


def render_copy_button(text: str, button_id: str):
    components.html(
        f"""
        <button id="{button_id}">Copy text</button>
        <script>
            document.getElementById('{button_id}').addEventListener('click', function() {{
                const text = `{js_escape(text)}`;
                navigator.clipboard.writeText(text).then(function() {{
                    alert('Text copied to clipboard!');
                }}).catch(function(err) {{
                    alert('Error copying text!');
                }});
            }});
        </script>
        """,
        height=100
    )


def apply_tpd_placeholders(text: str, client_name: str, card_number: str, third_party_name: str) -> str:
    return (
        text.replace("(client_name)", client_name if client_name else "(client_name)")
            .replace("(card_number)", card_number if card_number else "(card_number)")
            .replace("(third_party_name)", third_party_name if third_party_name else "(third_party_name)")
    )


# =========================
# Tabs
# =========================

tab_sof_kyc, tab_tpd = st.tabs(["SOF/KYC", "TPD"])


# =========================
# TAB 1: SOF/KYC
# Existing template logic
# =========================

with tab_sof_kyc:
    st.subheader("SOF/KYC request template")

    # ----- fixed intro and closing texts -----
    intro_texts = {
        "Russian": """Добрый день,

в соответствии с требованиями регулятора FSC Белиза и законодательством по борьбе с отмыванием денежных средств RoboForex Ltd обязана на регулярной основе осуществлять постоянную проверку и мониторинг личной информации своих клиентов.""",
        "English": """Hello,

in accordance with the requirements of the FSC Belize regulator and anti-money laundering legislation, RoboForex Ltd is obliged to regularly verify and monitor the personal information of its clients."""
    }

    closing_texts = {
        "Russian": """Мы ценим ваше сотрудничество.

Если у вас есть какие-либо вопросы, пожалуйста, свяжитесь с нами.

С уважением,""",
        "English": """We appreciate your cooperation.

If you have any questions, please contact us.

Best regards,"""
    }

    # ----- adaptive blocks -----
    blocks = {
        "SOF": {
            "Russian": {
                "lead": "В связи с этим, мы просим вас предоставить информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.",
                "add": "Также, пожалуйста, предоставьте информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.",
                "final": "Помимо этого, пожалуйста, предоставьте информацию об источнике средств, которые были зачислены на ваши торговые счета в RoboForex Ltd.",
                "rest": "\n\nПрилагаем список документов, которые можно использовать для проверки происхождения средств.\n\nВы можете предоставить нам любые документы, такие как: справки о зарплате, налоговые декларации, доходы от бизнеса, продажи имущества и т. д. или любой другой документ, указанный в прилагаемом документе."
            },
            "English": {
                "lead": "In this regard, we ask you to provide information on the source of funds credited to your trading accounts with RoboForex Ltd.",
                "add": "Additionally, please provide information on the source of funds credited to your trading accounts with RoboForex Ltd.",
                "final": "Moreover, please provide information on the source of funds credited to your trading accounts with RoboForex Ltd.",
                "rest": "\n\nAttached is a list of documents that can be used to verify the origin of funds.\n\nYou can provide us with any documents, such as salary certificates, tax returns, business income, property sales, etc., or any other document specified in the attached document."
            }
        },
        "ID": {
            "Russian": {
                "lead": "В связи с этим, мы просим вас предоставить скан или фото актуального паспорта, удостоверяющего вашу личность.",
                "add": "Также, пожалуйста, предоставьте скан или фото актуального паспорта, удостоверяющего вашу личность.",
                "final": "Помимо этого, пожалуйста, предоставьте скан или фото актуального паспорта, удостоверяющего вашу личность.",
                "rest": ""
            },
            "English": {
                "lead": "In this regard, we ask you to provide a scan or photo of your valid passport or another identity document.",
                "add": "Additionally, please provide a scan or photo of your valid passport or another identity document.",
                "final": "Moreover, please provide a scan or photo of your valid passport or another identity document.",
                "rest": ""
            }
        },
        "UB": {
            "Russian": {
                "lead": "В связи с этим, мы просим вас предоставить счёт за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.",
                "add": "Также, пожалуйста, предоставьте счёт за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.",
                "final": "Помимо этого, пожалуйста, предоставьте счёт за коммунальные услуги или банковскую выписку для подтверждения вашего адреса проживания.",
                "rest": ""
            },
            "English": {
                "lead": "In this regard, we ask you to provide a utility bill or a bank statement to confirm your residential address.",
                "add": "Additionally, please provide a utility bill or a bank statement to confirm your residential address.",
                "final": "Moreover, please provide a utility bill or a bank statement to confirm your residential address.",
                "rest": ""
            }
        }
    }

    # ----- UI -----
    selected_parts = st.multiselect(
        "Choose your request:",
        options=["SOF", "ID", "UB"],
        default=["SOF"]
    )

    language = st.radio("Select request language:", list(intro_texts.keys()))

    # Fixed order: SOF → ID → UB
    PRIORITY = ["SOF", "ID", "UB"]

    def sort_by_priority(keys):
        return [k for k in PRIORITY if k in keys]

    # ----- build middle part -----
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

    # ----- generate -----
    if st.button("Generate text", key="generate_sof_kyc"):
        if not selected_parts:
            placeholder_text = "Please choose request options"
            st.text_area("Result:", placeholder_text, height=320, key="sof_kyc_empty_result")
        else:
            middle_text = render_middle_adaptive(language, selected_parts)
            text = f"{intro_texts[language]}\n\n{middle_text}\n\n{closing_texts[language]}".strip()

            st.text_area("Result:", text, height=320, key="sof_kyc_result")
            render_copy_button(text, "copyButtonSofKyc")


# =========================
# TAB 2: TPD
# =========================

with tab_tpd:
    st.subheader("TPD request template")

    tpd_templates = {
        "TPD informing": """Dear (client_name),

To comply with the Financial Services Commission of Belize and our anti-money laundering obligations, RoboForex Ltd must periodically verify and monitor our clients' personal information.

We have noted that you used the payment account (card_number) of (third_party_name).
Please be aware that using a third party's account for deposits is prohibited under clause 13.3 of the Client Agreement. You can review the full agreement here: https://my.roboforex.com/files/document/client_agreement_bz_en.pdf

What you need to do for future withdrawals:
1. Initiate your withdrawal using the same payment account (card_number) you used to make your deposit through refund: https://my.roboforex.com/en/operations/withdraw-funds/form/cc-refund-bz/
2. For any remaining balance, you can withdraw it later on your personal payment account details after the refund is performed in full, and you will be able to use your account in a normal manner.

If third-party details are used again, you risk having access to your Member's Area suspended.

Thank you for your prompt attention to this matter.

If you have any questions, please don't hesitate to reply to this email or contact our support team.""",

        "TPD informing + KYC": """Dear (client_name),

To comply with the Financial Services Commission of Belize and our anti-money laundering obligations, RoboForex Ltd must periodically verify and monitor our clients' personal information.

Upon review, we have noted that some of your KYC documents have expired.

In this regard, we would like to ask you to provide:
- Your current ID or passport;
- Your latest Utility or bank statement (not older than 6 months) to identify your residence.

Furthermore, upon review, we have noted that you used the payment accounts (card_number) of (third_party_name) to deposit fund into your trading account.
Please be aware that using a third party's account for deposits is prohibited under clause 13.3 of the Client Agreement. You can review the full agreement here: https://my.roboforex.com/files/document/client_agreement_bz_en.pdf

What you need to do for future withdrawals:
1. Initiate your withdrawal using the same payment account (card_number) you used to make your deposit through refund: https://my.roboforex.com/en/operations/withdraw-funds/form/cc-refund-bz/
2. For any remaining balance, you can withdraw it later on your personal payment account details after the refund is performed in full, and you will be able to use your account in a normal manner.

If third-party details are used again, you risk having access to your Member's Area suspended.

Thank you for your prompt attention to this matter.

If you have any questions, please don't hesitate to reply to this email or contact our support team.""",

        "TPD docs request": """Dear (client_name),

To comply with the Financial Services Commission of Belize and our anti-money laundering obligations, RoboForex Ltd must periodically verify and monitor our clients' personal information.

Upon review, we have noted that you used the payment account (card_number) of (third_party_name) to deposit funds into your trading account.
Please be aware that using a third party's account for deposits is prohibited under clause 13.3 of the Client Agreement. You can review the full agreement here: https://my.roboforex.com/files/document/client_agreement_bz_en.pdf

In this regard we ask you to provide the following documents:

- Explanation of why the third-party deposit was used;
- ID/Passport of the Third Party - (third_party_name);
- Utility Bill of the third party (third_party_name) or any other reliable document for address confirmation (not older than 6 months);
- Photo of a Power of attorney where it will be stated that the owner of the funds agreed with the transfer of funds to yours trading account, and he has nothing against it. The example can be found below;
- Photo next to the third party's face with his ID/passport and Power of Attorney in his hands. The photo must be clearly seen;
- Photos of the bank card (card_number) with the first six and last four digits visible. The photos must also show the card owner's name. CVV code must be hidden.

I, the sender of the funds________________________ (Name, Surname), ID/Passport Number ____________________ agreed to transfer the amount of funds from my personal payment details with the number: __________________________________________ to my ______________________________(relation who is the owner of members area to third party), __________________________________(Name, Surname), the receiver, on his/her trading account(s): _______________________________________ on RoboForex Ltd. Company. I authorize the receiver to use the deposited funds, by his/her own will, on his/her trading account(s). The receiver can perform any trading, transfer, withdrawal of funds with the deposited amount without any restrictions from my side. I do not have any intent in using or returning the deposited funds. Also, I do understand that the company does not compensate for losses incurred due to the forced closing of positions on the client’s account. I agree with all internal policies of receiver RoboForex Ltd. company, and I do not have any claims concerning the rules of removal of funds. RoboForex Ltd cannot under any circumstances be held liable for any conditions coming from my consent to trust the funds to the receiver.

Sender (Name, Surname): _____________________________
Date: _____________________________________________
Signature: __________________________________________

Additional information and/or documents may be requested upon review of the submitted documents.

Thank you for your prompt attention to this matter.""",

        "TPD docs request + KYC": """Dear (client_name),

To comply with the Financial Services Commission of Belize and our anti-money laundering obligations, RoboForex Ltd must periodically verify and monitor our clients' personal information.

Upon review, we have noted that you used the payment account (card_number) of (third_party_name) to deposit funds into your trading account.
Please be aware that using a third party's account for deposits is prohibited under clause 13.3 of the Client Agreement. You can review the full agreement here: https://my.roboforex.com/files/document/client_agreement_bz_en.pdf

In this regard we ask you to provide the following documents:

- Your current ID or passport;
- Your latest Utility or bank statement (not older than 6 months) to identify your residence.
- Explanation of why the third-party deposit was used;
- ID/Passport of the Third Party - (third_party_name);
- Utility Bill of the third party (third_party_name) or any other reliable document for address confirmation (not older than 6 months);
- Photo of a Power of attorney where it will be stated that the owner of the funds agreed with the transfer of funds to yours trading account, and he has nothing against it. The example can be found below;
- Photo next to the third party's face with his ID/passport and Power of Attorney in his hands. The photo must be clearly seen;
- Photos of the bank card (card_number) with the first six and last four digits visible. The photos must also show the card owner's name. CVV code must be hidden.

I, the sender of the funds________________________ (Name, Surname), ID/Passport Number ____________________ agreed to transfer the amount of funds from my personal payment details with the number: __________________________________________ to my ______________________________(relation who is the owner of members area to third party), __________________________________(Name, Surname), the receiver, on his/her trading account(s): _______________________________________ on RoboForex Ltd. Company. I authorize the receiver to use the deposited funds, by his/her own will, on his/her trading account(s). The receiver can perform any trading, transfer, withdrawal of funds with the deposited amount without any restrictions from my side. I do not have any intent in using or returning the deposited funds. Also, I do understand that the company does not compensate for losses incurred due to the forced closing of positions on the client’s account. I agree with all internal policies of receiver RoboForex Ltd. company, and I do not have any claims concerning the rules of removal of funds. RoboForex Ltd cannot under any circumstances be held liable for any conditions coming from my consent to trust the funds to the receiver.

Sender (Name, Surname): _____________________________
Date: _____________________________________________
Signature: __________________________________________

Additional information and/or documents may be requested upon review of the submitted documents.

Thank you for your prompt attention to this matter."""
    }

    selected_tpd_template = st.selectbox(
        "Choose TPD request:",
        options=list(tpd_templates.keys())
    )

    with st.expander("Optional placeholders"):
        client_name = st.text_input("Client name", placeholder="Example: John Smith")
        card_number = st.text_input("Card number / payment account", placeholder="Example: 411111******1111")
        third_party_name = st.text_input("Third party name", placeholder="Example: Jane Smith")

    if st.button("Generate text", key="generate_tpd"):
        raw_text = tpd_templates[selected_tpd_template]
        final_text = apply_tpd_placeholders(
            raw_text,
            client_name,
            card_number,
            third_party_name
        )

        st.text_area("Result:", final_text, height=520, key="tpd_result")
        render_copy_button(final_text, "copyButtonTpd")
