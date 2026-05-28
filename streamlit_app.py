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


def render_copy_button(text: str, button_id: str) -> None:
    components.html(
        f"""
        <button id="{button_id}" style="
            padding: 8px 14px;
            border-radius: 8px;
            border: 1px solid #cccccc;
            cursor: pointer;
            font-size: 14px;
        ">
            Copy text
        </button>

        <script>
            document.getElementById("{button_id}").addEventListener("click", function() {{
                const text = `{js_escape(text)}`;
                navigator.clipboard.writeText(text).then(function() {{
                    alert("Text copied to clipboard!");
                }}).catch(function(err) {{
                    alert("Error copying text!");
                }});
            }});
        </script>
        """,
        height=70
    )


def normalize(value: str) -> str:
    return value.strip() if value else ""


# =========================
# TPD helpers
# =========================

def build_cards_text(entries: list[dict]) -> str:
    cards = [entry["card"] for entry in entries if entry.get("card")]
    return ", ".join(cards) if cards else "(card_number)"


def build_owners_text(entries: list[dict]) -> str:
    owners = sorted(set(entry["owner"] for entry in entries if entry.get("owner")))
    return ", ".join(owners) if owners else "(third_party_name)"


def build_tpd_accounts_phrase(entries: list[dict]) -> str:
    if not entries:
        return "the payment account (card_number) of (third_party_name)"

    grouped = {}

    for entry in entries:
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
            parts.append(f"the payment accounts {', '.join(cards)} of {owner}")

    return "; ".join(parts)


def build_tpd_accounts_phrase_without_article(entries: list[dict]) -> str:
    phrase = build_tpd_accounts_phrase(entries)

    if phrase.startswith("the "):
        return phrase[4:]

    return phrase


def apply_tpd_placeholders(text: str, client_name: str, entries: list[dict]) -> str:
    cards_text = build_cards_text(entries)
    owners_text = build_owners_text(entries)
    accounts_phrase = build_tpd_accounts_phrase(entries)
    accounts_phrase_without_article = build_tpd_accounts_phrase_without_article(entries)

    return (
        text.replace("(client_name)", client_name if client_name else "(client_name)")
        .replace("[tpd_accounts_phrase]", accounts_phrase)
        .replace("[tpd_accounts_phrase_without_article]", accounts_phrase_without_article)
        .replace("(card_number)", cards_text)
        .replace("(third_party_name)", owners_text)
    )


def get_tpd_missing_fields(template_key: str, client_name: str, entries: list[dict]) -> list[str]:
    missing = []

    templates_without_required_fields = [
        "Docs NOT provided - closing ticket"
    ]

    templates_card_only = [
        "Docs provided - closing ticket"
    ]

    templates_client_only = [
        "TPD APS docs request"
    ]

    if template_key in templates_without_required_fields:
        return missing

    if template_key in templates_card_only:
        for i, entry in enumerate(entries):
            if not entry.get("card"):
                missing.append(f"card number in Account #{i + 1}")
        return missing

    if template_key in templates_client_only:
        if not client_name:
            missing.append("client name")
        return missing

    if not client_name:
        missing.append("client name")

    for i, entry in enumerate(entries):
        if not entry.get("card"):
            missing.append(f"card number in Account #{i + 1}")

        if not entry.get("owner"):
            missing.append(f"third party name in Account #{i + 1}")

    return missing


# =========================
# Antifraud helpers
# =========================

def apply_antifraud_placeholders(text: str, verification_link: str, client_name: str) -> str:
    return (
        text.replace("[Verification Link]", verification_link if verification_link else "[Verification Link]")
        .replace("[Client's Name]", client_name if client_name else "[Client's Name]")
    )


def get_antifraud_missing_fields(template_key: str, verification_link: str, client_name: str) -> list[str]:
    missing = []

    if template_key == "Liveness request" and not verification_link:
        missing.append("verification link")

    if template_key == "CR severe deposit/withdrawal" and not client_name:
        missing.append("client name")

    return missing


# =========================
# Tabs
# =========================

tab_sof_kyc, tab_tpd, tab_light, tab_antifraud = st.tabs(
    ["SOF/KYC", "TPD", "Light check", "Antifraud"]
)


# =========================
# TAB 1: SOF/KYC
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

    language = st.radio(
        "Select request language:",
        list(intro_texts.keys())
    )

    priority = ["SOF", "ID", "UB"]

    def sort_by_priority(keys: list[str]) -> list[str]:
        return [key for key in priority if key in keys]

    def render_middle_adaptive(lang: str, reqs: list[str]) -> str:
        ordered = sort_by_priority(reqs)
        parts = []

        for i, request_type in enumerate(ordered):
            segment = blocks[request_type][lang]

            if i == 0:
                first_sentence = segment["lead"]
            elif i == 1:
                first_sentence = segment["add"]
            else:
                first_sentence = segment["final"]

            parts.append((first_sentence + segment.get("rest", "")).strip())

        return "\n\n".join(parts)

    if st.button("Generate text", key="generate_sof_kyc"):
        if not selected_parts:
            st.warning("Please choose request options.")
            text = "Please choose request options"
        else:
            middle_text = render_middle_adaptive(language, selected_parts)
            text = f"{intro_texts[language]}\n\n{middle_text}\n\n{closing_texts[language]}".strip()

        st.text_area("Result:", text, height=330, key="sof_kyc_result")
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

Thank you for your prompt attention to this matter.""",

        "TPD APS docs request": """Dear (client_name),

We hope this message finds you well.

We are contacting you regarding deposits made to your RoboForex trading account via Binance Pay. Our records indicate that the funds originated from a wallet not registered in your name.

In accordance with Clause 13.3 of the RoboForex Ltd Client Agreement and our internal Anti-Money Laundering (AML) policies, we are required to verify the source and legitimacy of all third-party transactions. To assess this transfer, we kindly ask that you explain the reason for the deposits and identify the individual who initiated them.

To proceed, please provide the following documents:

1) Proof of relationship with the third-party wallet owner (e.g., marriage certificate, birth certificate), if applicable.
2) A Power of Attorney from the wallet owner stating they authorized and initiated the transfer, and fully consent to your use of the funds. (See the Power of Attorney template below.)
3) A clear photo of a valid government-issued ID (passport, national ID, etc.) belonging to the wallet owner.
4) A recent utility bill or bank statement (dated within the last 6 months) showing the wallet owner's name and current residential address.
5) A selfie of the wallet owner holding the signed Power of Attorney next to their face (for identity verification).
6) A screenshot of the Binance Pay statement’s first page (from the account used for deposit), clearly showing the ownership (name, surname, Binance ID) of the account details, also a screenshot of at least 1 transaction, the date, amount deposited to the trading account (you can find the guide in the attachment).

Power of Attorney Template:

I, [Full Name of Wallet Owner], holder of [ID Type: Passport/National ID], ID number: [ID Number], residing at [Full Residential Address], hereby declare the following:
I am the lawful owner of the Binance Pay wallet from which funds were transferred to the RoboForex trading account registered under the name [Account Holder’s Full Name].
I confirm that I personally authorized and initiated the transfer of these funds and that I have no objection to their use by the account holder for trading or any other lawful activity within their RoboForex account.
Furthermore, I acknowledge that I have no claim, entitlement, or condition regarding the use, management, or withdrawal of these funds. I fully and irrevocably waive any right to contest or dispute the transaction.
This Power of Attorney is granted voluntarily, without coercion or undue influence. It is valid indefinitely unless revoked by me in writing.

Signed:

[Full Name of Wallet Owner]
Date: [DD/MM/YYYY]

Your cooperation is greatly appreciated.

Regards,
Your RoboForex""",

        "Docs NOT provided - closing ticket": """Dear Client,

We haven’t received a response from you, and we are proceeding with the closure of this ticket. Please note that the issue remains unresolved, and the requested documents and/or information are still outstanding.

Until this is completed, withdrawal limitations may apply. To avoid any delays in processing your withdrawals, we kindly recommend you to provide the required information as soon as possible.""",

        "Docs provided - closing ticket": """Hello,

Thank you very much for providing the requested documents.

We confirm that all documents have been successfully received and reviewed. Please initiate a refund to the card (card_number) via the following link: https://my.roboforex.com/en/operations/withdraw-funds/form/cc-refund-bz/

After the refund is completed in full you will be able to use your own cards without any resctrictions.

If you have any further questions or need assistance, please feel free to contact us."""
    }

    selected_tpd_template = st.selectbox(
        "Choose TPD request:",
        options=list(tpd_templates.keys())
    )

    requires_no_fields = selected_tpd_template in [
        "Docs NOT provided - closing ticket"
    ]

    requires_card_only = selected_tpd_template in [
        "Docs provided - closing ticket"
    ]

    requires_client_only = selected_tpd_template in [
        "TPD APS docs request"
    ]

    client_name = ""

    if not requires_no_fields and not requires_card_only:
        client_name = normalize(
            st.text_input(
                "Client name",
                placeholder="Example: John Smith",
                key="tpd_client_name"
            )
        )

    tpd_entries = []

    if not requires_no_fields and not requires_client_only:
        st.markdown("Third-party payment accounts")

        tpd_count = st.number_input(
            "How many payment accounts?",
            min_value=1,
            max_value=10,
            value=1,
            step=1,
            key="tpd_accounts_count"
        )

        for i in range(tpd_count):
            st.markdown(f"Account #{i + 1}")

            if requires_card_only:
                card = normalize(
                    st.text_input(
                        "Card / payment account",
                        key=f"tpd_card_{i}",
                        placeholder="Example: 444111******1111"
                    )
                )

                tpd_entries.append(
                    {
                        "card": card,
                        "owner": ""
                    }
                )

            else:
                col1, col2 = st.columns(2)

                with col1:
                    card = normalize(
                        st.text_input(
                            "Card / payment account",
                            key=f"tpd_card_{i}",
                            placeholder="Example: 444111******1111"
                        )
                    )

                with col2:
                    owner = normalize(
                        st.text_input(
                            "Third party name",
                            key=f"tpd_owner_{i}",
                            placeholder="Example: Vasya Pupkin"
                        )
                    )

                tpd_entries.append(
                    {
                        "card": card,
                        "owner": owner
                    }
                )

    if st.button("Generate text", key="generate_tpd"):
        missing_fields = get_tpd_missing_fields(
            selected_tpd_template,
            client_name,
            tpd_entries
        )

        if missing_fields:
            st.warning(
                "Template is incomplete. Missing: "
                + ", ".join(missing_fields)
                + "."
            )

        raw_text = tpd_templates[selected_tpd_template]
        final_text = apply_tpd_placeholders(raw_text, client_name, tpd_entries)

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

        st.text_area("Result:", text, height=430, key="light_result")
        render_copy_button(text, "copyButtonLight")


# =========================
# TAB 4: ANTIFRAUD
# =========================

with tab_antifraud:
    st.subheader("Antifraud templates")

    antifraud_templates = {
        "Liveness request": """Dear Trader,

We hope you’re doing well.

As part of our ongoing commitment to maintaining a secure and seamless trading environment, we occasionally ask clients to complete a brief account update. This helps us ensure that your account information remains accurate and that you continue to enjoy uninterrupted access to all services.

Please follow the link below to complete a short verification at your convenience:

[Verification Link]

The process should only take a few minutes. If you have any questions or need assistance, our team will be happy to help.

Thank you for your cooperation and for trading with us.""",

        "WB fraud (deposit withdrawn)": """Dear Client,

Following a review of your account activity, the Company has identified violations of the Client Agreement, including misuse of the bonus program and issues related to the verification process.

In accordance with Clauses 4.8 and 4.15 of the Client Agreement, the Company has decided to terminate the Agreement with immediate effect and permanently close your account.

Please note that your deposited funds were previously withdrawn in full. The remaining balance has been cancelled and is not eligible for withdrawal.

This decision is final.""",

        "WB fraud (plain termination, no deposit)": """Dear Client,

Following a review of your account activity, the Company has identified violations of the Client Agreement.

In accordance with Clauses 4.8 and 4.15 of the Client Agreement, the Company has decided to terminate the Agreement with immediate effect and permanently close your account.

This decision is final.""",

        "Card/bank verification": """Dear Trader,

We kindly ask you to provide a bank statement related to the card you used to make deposits to your trading account.

Please ensure that the document meets the following requirements:

- Issued by your bank (PDF or printed copy);
- Clearly shows your full name;
- Displays the bank’s name and address;
- Contains details of the card used for the deposit (e.g. last 4 digits or transaction reference);
- Shows the relevant transaction(s) to our company, if possible;
- Is recent (typically within the last 3 months);

Please note that the statement must correspond specifically to the card used for funding your account, as this is required for verification and compliance purposes.

You may upload the document via your client portal or reply to this email with the attachment.

If you have any questions or need assistance, please feel free to contact us.

Kind regards,""",

        "CR severe deposit/withdrawal": """Dear [Client's Name],

As part of our ongoing compliance procedures in accordance with international Anti-Money Laundering (AML) standards and our internal policies, we conduct regular reviews of incoming transactions.

We have identified that recent transactions at your account were processed through third-party exchange services categorized as high-risk by industry-standard risk databases and monitoring tools.

In light of this, we kindly request that you provide:

- A brief explanation of the purpose and necessity of using these particular exchange platforms, specifically of wallet;
- Any supporting documents, such as transaction confirmations, screenshots, sender details, or payment receipts;

Please note that if a transaction is identified as high-risk, we may temporarily suspend processing until the origin and purpose of the funds are verified. Repeated use of high-risk third-party services or failure to provide adequate clarification may result in the termination of your account, in accordance with our AML obligations and the Client Agreement.

Please confirm this wallet or exchange will not be used for your further deposits or withdrawals.

We strongly recommend using regulated exchanges only.

We appreciate your prompt attention to this matter and your continued cooperation."""
    }

    selected_antifraud_template = st.selectbox(
        "Choose Antifraud template:",
        options=list(antifraud_templates.keys())
    )

    verification_link = ""
    antifraud_client_name = ""

    if selected_antifraud_template == "Liveness request":
        verification_link = normalize(
            st.text_input(
                "Verification link",
                placeholder="Paste verification link here",
                key="antifraud_verification_link"
            )
        )

    if selected_antifraud_template == "CR severe deposit/withdrawal":
        antifraud_client_name = normalize(
            st.text_input(
                "Client name",
                placeholder="Example: John Smith",
                key="antifraud_client_name"
            )
        )

    if st.button("Generate text", key="generate_antifraud"):
        missing_fields = get_antifraud_missing_fields(
            selected_antifraud_template,
            verification_link,
            antifraud_client_name
        )

        if missing_fields:
            st.warning(
                "Template is incomplete. Missing: "
                + ", ".join(missing_fields)
                + "."
            )

        raw_text = antifraud_templates[selected_antifraud_template]
        text = apply_antifraud_placeholders(
            raw_text,
            verification_link,
            antifraud_client_name
        )

        st.text_area("Result:", text, height=480, key="antifraud_result")
        render_copy_button(text, "copyButtonAntifraud")
        
