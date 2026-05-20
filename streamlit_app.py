import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Compliance request templates",
    page_icon="📄",
    layout="centered"
)

st.title("AML request templates")


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


def build_cards_text(tpd_entries: list[dict]) -> str:
    cards = [entry["card"] for entry in tpd_entries if entry.get("card")]
    return ", ".join(cards) if cards else "(card_number)"


def build_owners_text(tpd_entries: list[dict]) -> str:
    owners = sorted(set(entry["owner"] for entry in tpd_entries if entry.get("owner")))
    return ", ".join(owners) if owners else "(third_party_name)"


def build_tpd_accounts_phrase(tpd_entries: list[dict]) -> str:
    if not tpd_entries:
        return "the payment account (card_number) of (third_party_name)"

    grouped = {}

    for entry in tpd_entries:
        card = entry.get("card") or "(card_number)"
        owner = entry.get("owner") or "(third_party_name)"

        if owner not in grouped:
            grouped[owner] = []

        grouped[owner].append(card)

    parts = []

    for owner, cards in grouped.items():
        if len(cards) == 1:
            parts.append(f"the payment account {cards[0]} of {owner}")
        else:
            cards_text = ", ".join(cards)
            parts.append(f"the payment accounts {cards_text} of {owner}")

    if len(parts) == 1:
        return parts[0]

    return "; ".join(parts)


def build_tpd_accounts_phrase_without_article(tpd_entries: list[dict]) -> str:
    phrase = build_tpd_accounts_phrase(tpd_entries)

    if phrase.startswith("the "):
        phrase = phrase[4:]

    return phrase


def apply_tpd_placeholders(text: str, client_name: str, tpd_entries: list[dict]) -> str:
    accounts_phrase = build_tpd_accounts_phrase(tpd_entries)
    accounts_phrase_without_article = build_tpd_accounts_phrase_without_article(tpd_entries)
    cards_text = build_cards_text(tpd_entries)
    owners_text = build_owners_text(tpd_entries)

    return (
        text.replace("(client_name)", client_name if client_name else "(client_name)")
            .replace("[tpd_accounts_phrase]", accounts_phrase)
            .replace("[tpd_accounts_phrase_without_article]", accounts_phrase_without_article)
            .replace("(card_number)", cards_text)
            .replace("(third_party_name)", owners_text)
    )


# =========================
# Tabs
# =========================

tab_sof_kyc, tab_tpd, tab_light = st.tabs(["SOF/KYC", "TPD", "Light check"])

# =========================
# TAB 1: SOF/KYC
# Existing template logic
# =========================

with tab_sof_kyc:
    st.subheader("SOF/KYC request template")

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

    selected_parts = st.multiselect(
        "Choose your request:",
        options=["SOF", "ID", "UB"],
        default=["SOF"]
    )

    language = st.radio("Select request language:", list(intro_texts.keys()))

    PRIORITY = ["SOF", "ID", "UB"]

    def sort_by_priority(keys):
        return [k for k in PRIORITY if k in keys]

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

We have noted that you used [tpd_accounts_phrase_without_article].
Please be aware that using a third party's account for deposits is prohibited under clause 13.3 of the Client Agreement. You can review the full agreement here: https://my.roboforex.com/files/document/client_agreement_bz_en.pdf

What you need to do for future withdrawals:
1. Initiate your withdrawal using the same payment account(s) (card_number) you used to make your deposit through refund: https://my.roboforex.com/en/operations/withdraw-funds/form/cc-refund-bz/
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

Furthermore, upon review, we have noted that you used [tpd_accounts_phrase_without_article] to deposit funds into your trading account.
Please be aware that using a third party's account for deposits is prohibited under clause 13.3 of the Client Agreement. You can review the full agreement here: https://my.roboforex.com/files/document/client_agreement_bz_en.pdf

What you need to do for future withdrawals:
1. Initiate your withdrawal using the same payment account(s) (card_number) you used to make your deposit through refund: https://my.roboforex.com/en/operations/withdraw-funds/form/cc-refund-bz/
2. For any remaining balance, you can withdraw it later on your personal payment account details after the refund is performed in full, and you will be able to use your account in a normal manner.

If third-party details are used again, you risk having access to your Member's Area suspended.

Thank you for your prompt attention to this matter.

If you have any questions, please don't hesitate to reply to this email or contact our support team.""",

        "TPD docs request": """Dear (client_name),

To comply with the Financial Services Commission of Belize and our anti-money laundering obligations, RoboForex Ltd must periodically verify and monitor our clients' personal information.

Upon review, we have noted that you used [tpd_accounts_phrase_without_article] to deposit funds into your trading account.
Please be aware that using a third party's account for deposits is prohibited under clause 13.3 of the Client Agreement. You can review the full agreement here: https://my.roboforex.com/files/document/client_agreement_bz_en.pdf

In this regard we ask you to provide the following documents:

- Explanation of why the third-party deposit was used;
- ID/Passport of the Third Party - (third_party_name);
- Utility Bill of the third party (third_party_name) or any other reliable document for address confirmation (not older than 6 months);
- Photo of a Power of attorney where it will be stated that the owner of the funds agreed with the transfer of funds to yours trading account, and he has nothing against it. The example can be found below;
- Photo next to the third party's face with his ID/passport and Power of Attorney in his hands. The photo must be clearly seen;
- Photos of the bank card(s) (card_number) with the first six and last four digits visible. The photos must also show the card owner's name. CVV code must be hidden.

I, the sender of the funds________________________ (Name, Surname), ID/Passport Number ____________________ agreed to transfer the amount of funds from my personal payment details with the number: __________________________________________ to my ______________________________(relation who is the owner of members area to third party), __________________________________(Name, Surname), the receiver, on his/her trading account(s): _______________________________________ on RoboForex Ltd. Company. I authorize the receiver to use the deposited funds, by his/her own will, on his/her trading account(s). The receiver can perform any trading, transfer, withdrawal of funds with the deposited amount without any restrictions from my side. I do not have any intent in using or returning the deposited funds. Also, I do understand that the company does not compensate for losses incurred due to the forced closing of positions on the client’s account. I agree with all internal policies of receiver RoboForex Ltd. company, and I do not have any claims concerning the rules of removal of funds. RoboForex Ltd cannot under any circumstances be held liable for any conditions coming from my consent to trust the funds to the receiver.

Sender (Name, Surname): _____________________________
Date: _____________________________________________
Signature: __________________________________________

Additional information and/or documents may be requested upon review of the submitted documents.

Thank you for your prompt attention to this matter.""",

        "TPD docs request + KYC": """Dear (client_name),

To comply with the Financial Services Commission of Belize and our anti-money laundering obligations, RoboForex Ltd must periodically verify and monitor our clients' personal information.

Upon review, we have noted that you used [tpd_accounts_phrase_without_article] to deposit funds into your trading account.
Please be aware that using a third party's account for deposits is prohibited under clause 13.3 of the Client Agreement. You can review the full agreement here: https://my.roboforex.com/files/document/client_agreement_bz_en.pdf

In this regard we ask you to provide the following documents:

- Your current ID or passport;
- Your latest Utility or bank statement (not older than 6 months) to identify your residence.
- Explanation of why the third-party deposit was used;
- ID/Passport of the Third Party - (third_party_name);
- Utility Bill of the third party (third_party_name) or any other reliable document for address confirmation (not older than 6 months);
- Photo of a Power of attorney where it will be stated that the owner of the funds agreed with the transfer of funds to yours trading account, and he has nothing against it. The example can be found below;
- Photo next to the third party's face with his ID/passport and Power of Attorney in his hands. The photo must be clearly seen;
- Photos of the bank card(s) (card_number) with the first six and last four digits visible. The photos must also show the card owner's name. CVV code must be hidden.

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

    client_name = st.text_input(
        "Client name",
        placeholder="Example: John Smith",
        key="tpd_client_name"
    )

    st.markdown("Third-party payment accounts")

    tpd_count = st.number_input(
        "How many third-party payment accounts?",
        min_value=1,
        max_value=10,
        value=1,
        step=1
    )

    tpd_entries = []

    for i in range(tpd_count):
        st.markdown(f"Account #{i + 1}")

        col1, col2 = st.columns(2)

        with col1:
            card = st.text_input(
                "Card / payment account",
                key=f"tpd_card_{i}",
                placeholder="Example: 444111******1111"
            )

        with col2:
            owner = st.text_input(
                "Third party name",
                key=f"tpd_owner_{i}",
                placeholder="Example: Vasya Pupkin"
            )

        if card or owner:
            tpd_entries.append({
                "card": card.strip() if card else "(card_number)",
                "owner": owner.strip() if owner else "(third_party_name)"
            })

    if st.button("Generate text", key="generate_tpd"):
        raw_text = tpd_templates[selected_tpd_template]

        final_text = apply_tpd_placeholders(
            raw_text,
            client_name,
            tpd_entries
        )

        st.text_area("Result:", final_text, height=560, key="tpd_result")
        render_copy_button(final_text, "copyButtonTpd")


# =========================
# TAB 3: LIGHT CHECK
# =========================

with tab_light:
    st.subheader("Light check templates")

    light_templates = {
        "Initial request": """Hello,

According to clauses 4.4, 4.6, 4.9 and 13.18 of the Client Agreement, please provide a selfie with the ID you used for verification in your hands next to a computer/laptop with your RoboForex Member's area opened on it.""",

        "WD OK": """Hello,

Thank you for providing the requested documents.

Please withdraw all of your funds by performing a withdrawal request.

We kindly appreciate your cooperation.""",

        "LOW quality statements": """Hello,

Please note that the quality of your bank statements is poor. Please provide statements of better quality and highlight the salary transactions.

We kindly appreciate your cooperation.""",

        "UB": """Hello,

Please provide a recent utility bill confirming your residential address.""",

        "Under review": """Hello,

Please note that your documents are under review. Kindly wait for updates.

We kindly appreciate your cooperation.""",

        "LOW quality ID": """Hello,

Please note that all data of your ID and Member area should be clearly visible. Kindly provide a photo of a better quality.""",

        "Selfie with PoA with current date": """Hello,

Please take a selfie with a bank statement in one hand and a piece of paper with the current date in the other hand.

We kindly appreciate your cooperation.""",

        "Bank card verif.": """Please pass bank card verification used for deposit ******. Please provide photos of both sides of bank card.

Please sign the Card, Hide the CVC/CVV code. You need to hide all card numbers except the expiry date, the first 6 and last 4 numbers of the card.

If the bank cards are unnamed, please provide us with a screenshot from your internet banking from where we will be able to see your name, surname, bank card number""",

        "Still under review": """Dear ****,

We sincerely thank you for your patience.

Kindly be informed that your case is still under review.

We do our best to speed up the process and provide the best service to each client.

Please also note that we will try to resolve your issue as a higher priority as soon as possible.

We kindly appreciate your cooperation.""",

        "Ignoring. Ticket closure": """Dear Client

We hope you’re well.

As we have not received a response to our recent request for documentation, we will proceed to close this ticket for now.
Please note that we still require the requested documents to continue with your case. You may reply to this email at any time with the documents, and we will reopen the ticket immediately.

Thank you for your cooperation and understanding.

Should you have any questions, feel free to reply to this email or contact our support team—we’re here to help.

This ticket will now be closed.""",

        "Reply to toxic client": """Hello,

Please note that in accordance with the Client Agreement, clause 5.2 - The term for consideration of the Client's request is five working days. In some cases, the review period may be extended.

Kindly note that we have to follow our internal procedures to provide best service to our clients.

Please take note that your personal data are kept safe within the company in accordance with our privacy policy, GDPR, and AML Law requirements. Document(s) will be used in order to have your personal data updated in accordance to the AML Law requirements.

Please find more details by following links:

- https://roboforex.com/about/company/documents/
- https://roboforex.com/about/client/security-policy/

Would you please be so kind and provide us with the requested documents."""
    }

    selected_light_template = st.selectbox(
        "Choose template:",
        options=list(light_templates.keys())
    )

    if st.button("Generate text", key="generate_light"):
        text = light_templates[selected_light_template]

        st.text_area("Result:", text, height=400, key="light_result")
        render_copy_button(text, "copyButtonLight")
