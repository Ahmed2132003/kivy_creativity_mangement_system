<ClientsScreen>:
    name: "clients"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        md_bg_color: 0, 0, 0, 1  # اللون الأسود للخلفية

        MDLabel:
            text: "Clients Section"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1  # اللون الأبيض للنص

        MDTextField:
            id: name
            hint_text: "Client Name"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDTextField:
            id: phone
            hint_text: "Phone Number"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDTextField:
            id: email
            hint_text: "Email"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDTextField:
            id: transactions
            hint_text: "Transactions"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDTextField:
            id: address
            hint_text: "Address"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDTextField:
            id: rating
            hint_text: "Rating"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDTextField:
            id: amount_spent
            hint_text: "Amount Spent"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDRaisedButton:
            text: "Add Client"
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: root.add_client()
        MDRaisedButton:
            text: "Delete Client"
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: root.delete_client()
        MDRaisedButton:
            text: "Edit Client"
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: root.edit_client()
        MDRaisedButton:
            text: "Clear Fields"
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: root.clear_fields()

        # عرض العملاء
        MDDataTable:
            id: clients_table
            column_data: [
                ("Name", dp(30)),
                ("Phone", dp(30)),
                ("Email", dp(30)),
                ("Transactions", dp(30)),
                ("Address", dp(30)),
                ("Rating", dp(30)),
                ("Amount Spent", dp(30))
            ]
            row_data: []