                + ", ".join(missing_fields)
                + "."
            )

        raw_text = get_template_text(
            "Antifraud",
            selected_antifraud_template,
            antifraud_templates[selected_antifraud_template]
        )
        text = apply_antifraud_placeholders(
            raw_text,
            verification_link,
            antifraud_client_name
        )

        st.text_area("Result:", text, height=480, key="antifraud_result")
        render_copy_button(text, "copyButtonAntifraud")

# =========================
# TAB 5: ADMIN
# =========================

with tab_admin:
    st.subheader("Template editor")

    admin_password = get_secret("ADMIN_PASSWORD")

    if not admin_password:
        st.info(
            "Admin mode is disabled. Add ADMIN_PASSWORD to Streamlit Secrets to enable it."
        )
    else:
        entered_password = st.text_input(
            "Admin password",
            type="password",
            key="admin_password_input",
        )

        if entered_password == admin_password:
            if not supabase_configured():
                st.warning(
                    "Supabase is not configured. Add SUPABASE_URL and "
                    "SUPABASE_SERVICE_ROLE_KEY to Streamlit Secrets."
                )
            else:
                sections = {
                    "TPD": tpd_templates,
                    "Light check": light_templates,
                    "Antifraud": antifraud_templates,
                }

                selected_admin_section = st.selectbox(
                    "Section",
                    options=list(sections.keys()),
                    key="admin_section",
                )

                selected_admin_template = st.selectbox(
                    "Template",
                    options=list(sections[selected_admin_section].keys()),
                    key="admin_template",
                )

                default_admin_text = sections[selected_admin_section][selected_admin_template]

                try:
                    current_admin_text = get_template_text(
                        selected_admin_section,
                        selected_admin_template,
                        default_admin_text,
                    )
                    has_override = (
                        selected_admin_section,
                        selected_admin_template,
                    ) in load_template_overrides()
                except RuntimeError as exc:
                    st.error(str(exc))
                    current_admin_text = default_admin_text
                    has_override = False

                if has_override:
                    st.caption("This template currently uses a saved custom version.")
                else:
                    st.caption("This template currently uses the default version from app.py.")

                editor_key = (
                    f"admin_editor_{selected_admin_section}_{selected_admin_template}"
                )

                edited_admin_text = st.text_area(
                    "Template text",
                    value=current_admin_text,
                    height=430,
                    key=editor_key,
                )

                missing_placeholders = validate_template_placeholders(
                    selected_admin_section,
                    selected_admin_template,
                    edited_admin_text,
                )

                if missing_placeholders:
                    st.warning(
                        "The edited text is missing the following placeholder(s): "
                        + ", ".join(missing_placeholders)
                        + ". The template can still be saved, but automatic field replacement may no longer work as expected."
                    )

                col_save, col_restore = st.columns(2)

                with col_save:
                    if st.button("Save template", type="primary", key="admin_save_template"):
                        try:
                            save_template_override(
                                selected_admin_section,
                                selected_admin_template,
                                edited_admin_text,
                            )
                            st.success("Template saved successfully.")
                        except RuntimeError as exc:
                            st.error(str(exc))

                with col_restore:
                    if st.button("Restore default", key="admin_restore_template"):
                        try:
                            delete_template_override(
                                selected_admin_section,
                                selected_admin_template,
                            )
                            st.success("Default template restored.")
                            st.rerun()
                        except RuntimeError as exc:
                            st.error(str(exc))

        elif entered_password:
            st.error("Incorrect password.")
            
