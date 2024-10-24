import sqlite3
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
import webbrowser

# تعيين حجم الشاشة إلى 400x600
Window.size = (400, 600)

# إنشاء أو فتح قاعدة البيانات
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT UNIQUE, 
                phone TEXT, 
                password TEXT)''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, 
                    phone TEXT, 
                    email TEXT, 
                    address TEXT, 
                    rating TEXT)''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, 
                phone TEXT, 
                email TEXT, 
                job_role TEXT, 
                work_type TEXT)''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, 
                phone TEXT, 
                email TEXT, 
                employe_admin TEXT, 
                work_time TEXT)''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS service (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_name TEXT, 
                service_price TEXT, 
                service_type TEXT, 
                admin TEXT, 
                clint_name TEXT)''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS train (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                t_clint_name TEXT, 
                email_train TEXT, 
                date_train TEXT, 
                payment_made TEXT,
                amount TEXT, 
                residual_amount TEXT)''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                freelane_name TEXT, 
                amount TEXT, 
                admin_name TEXT, 
                total_income TEXT,
                total_out TEXT, 
                residual TEXT)''')
conn.commit()

# شاشة إنشاء حساب
class SignUpScreen(Screen):
    dialog = None

    def create_account(self):
        username = self.ids.username.text
        phone = self.ids.phone.text
        password = self.ids.password.text

        if username == '' or phone == '' or password == '':
            self.show_dialog("All fields are required!")
        else:
            try:
                c.execute("INSERT INTO users (username, phone, password) VALUES (?, ?, ?)",
                          (username, phone, password))
                conn.commit()
                self.show_dialog("Account created successfully!")
                self.manager.current = 'main'  # الانتقال إلى الشاشة الرئيسية بعد إنشاء الحساب
            except sqlite3.IntegrityError:
                self.show_dialog("Username already exists!")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()

# شاشة تسجيل الدخول
class LoginScreen(Screen):
    dialog = None

    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text

        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()

        if result:
            self.show_dialog("Login successful!")
            self.manager.current = 'main'  # الانتقال إلى الشاشة الرئيسية بعد تسجيل الدخول
        else:
            self.show_dialog("Invalid username or password!")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()

# شاشة رئيسية
class MainScreen(Screen):
    dialog = None

    def show_about(self, *args):
    
        self.show_dialog("This is the About section.")

    def show_help(self, *args):
        self.show_dialog("This is the Help section.")

    def show_social_media(self, *args):
        self.show_dialog("This is the Social Media section.")

    def show_clients(self, *args):
        self.manager.current = 'clients'
    

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()
# شاشة العملاء
class ClientsScreen(Screen):
    def view_clintes(self, *args):
        self.manager.current ='v_clint'
    def edit_clintes(self, *args):
        self.manager.current ='edit_clint'
    def delete_clintes(self, *args):
        self.manager.current ='delete_clint'
    dialog = None

    def add_client(self):
        name = self.ids.name.text
        phone = self.ids.phone.text
        email = self.ids.email.text
        address = self.ids.address.text
        rating = self.ids.rating.text

        if name == '' or phone == '' or email == '' or address == '' or rating == '':
            self.show_dialog("All fields are required!")
        else:
            try:
                c.execute("INSERT INTO clients (name, phone, email, address, rating) VALUES (?, ?, ?, ?, ?)",
                          (name, phone, email, address, rating))
                conn.commit()
                self.show_dialog("Client added successfully!")
                self.ids.name.text = ''
                self.ids.phone.text = ''
                self.ids.email.text = ''
                self.ids.address.text = ''
                self.ids.rating.text = ''
            except sqlite3.Error as e:
                self.show_dialog(f"Error: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()
class View_clint_Screen(Screen):

    def on_enter(self):
        # عند فتح الشاشة، استرجع كل العملاء من قاعدة البيانات
        self.display_clients()

    def display_clients(self):
        # مسح أي بيانات سابقة في الواجهة
        self.ids.client_info.clear_widgets()

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()

        if clients:
            for client in clients:
                # عرض بيانات كل عميل في سطور منفصلة
                client_label = MDLabel(
                    text=f"Name: {client[0]}\nPhone: {client[1]}\nEmail: {client[2]}\nAddress: {client[4]}\nRating: {client[5]}",
                    theme_text_color="Custom",
                    text_color=(0.6, 0, 1, 1),
                    halign="left",
                    size_hint_y=None,
                    height=120  # تعديل الارتفاع ليتناسب مع عدد السطور
                )
                self.ids.client_info.add_widget(client_label)
        else:
            # إذا لم يكن هناك بيانات
            no_data_label = MDLabel(
                text="No clients found.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            self.ids.client_info.add_widget(no_data_label)

    def search_client(self):
        # البحث عن العميل باستخدام الاسم
        client_name = self.ids.search_input.text
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE name = ?", (client_name,))
        client_data = cursor.fetchone()

        self.ids.client_info.clear_widgets()

        if client_data:
            # عرض بيانات العميل المطلوب في سطور منفصلة
            client_label = MDLabel(
                text=f"Name: {client_data[0]}\nPhone: {client_data[1]}\nEmail: {client_data[2]}\nAddress: {client_data[4]}\nRating: {client_data[5]}",
                theme_text_color="Custom",
                text_color=(0.6, 0, 1, 1),
                halign="left",
                size_hint_y=None,
                height=120  # تعديل الارتفاع ليتناسب مع عدد السطور
            )
            self.ids.client_info.add_widget(client_label)
        else:
            no_data_label = MDLabel(
                text="Client not found.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            self.ids.client_info.add_widget(no_data_label)

class Edit_clint_Screen(Screen):
    dialog = None

    def search_client(self):
        client_name = self.ids.search_input.text.strip()
        if not client_name:
            self.show_dialog("Please enter a client name to search.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE name = ?", (client_name,))
        client_data = cursor.fetchone()

        if client_data:
            # الوصول إلى عناصر الإدخال من الشاشة الحالية
            self.ids.name.text = client_data[0] if client_data[0] is not None else ""
            self.ids.phone.text = client_data[1] if client_data[1] is not None else ""
            self.ids.email.text = client_data[2] if client_data[2] is not None else ""
            self.ids.address.text = client_data[4] if client_data[4] is not None else ""
            self.ids.rating.text = str(client_data[5]) if client_data[5] is not None else ""

            # جعل حقل الاسم قابل للتعديل
            self.ids.name.disabled = False

        else:
            self.show_dialog("Client not found.")

    def update_client(self):
        client_name = self.ids.search_input.text.strip()
        if not client_name:
            self.show_dialog("Please search for a client first.")
            return

        # Get updated data from TextFields
        name = self.ids.name.text.strip()
        phone = self.ids.phone.text.strip()
        email = self.ids.email.text.strip()
        address = self.ids.address.text.strip()
        rating = self.ids.rating.text.strip()

        if not all([name, phone, email, address, rating]):
            self.show_dialog("All fields are required.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE clients
                SET name = ?, phone = ?, email = ?, address = ?, rating = ?
                WHERE name = ?
            """, (name, phone, email, address, rating, client_name))
            conn.commit()
            self.show_dialog("Client updated successfully!")
        except sqlite3.Error as e:
            self.show_dialog(f"Error updating client: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()




class Delete_clint_Screen(Screen):
    dialog = None

    def search_client(self):
        client_name = self.ids.search_input.text.strip()
        if not client_name:
            self.show_dialog("Please enter a client name to search.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE name = ?", (client_name,))
        client_data = cursor.fetchone()

        if client_data:
            # عرض بيانات العميل (اختياري)
            self.ids.name.text = client_data[0] if client_data[0] is not None else ""
            self.ids.phone.text = client_data[1] if client_data[1] is not None else ""
            self.ids.email.text = client_data[2] if client_data[2] is not None else ""
            self.ids.address.text = client_data[4] if client_data[4] is not None else ""
            self.ids.rating.text = str(client_data[5]) if client_data[5] is not None else ""

            # تمكين زر الحذف
            self.ids.delete_button.disabled = False

        else:
            self.show_dialog("Client not found.")

    def delete_client(self):
        client_name = self.ids.search_input.text.strip()
        if not client_name:
            self.show_dialog("Please search for a client first.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE name = ?", (client_name,))
            if cursor.rowcount == 0:
                self.show_dialog("Client not found or already deleted.")
            else:
                conn.commit()
                self.show_dialog("Client deleted successfully!")
                # يمكنك مسح الحقول بعد الحذف
                self.ids.search_input.text = ""
                self.ids.name.text = ""
                self.ids.phone.text = ""
                self.ids.email.text = ""
                self.ids.address.text = ""
                self.ids.rating.text = ""
                self.ids.delete_button.disabled = True

        except sqlite3.Error as e:
            self.show_dialog(f"Error deleting client: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()
class Employee_Screen(Screen):
    dialog = None

    def add_employee(self):
        # الحصول على القيم من الحقول
        name = self.ids.name.text
        phone = self.ids.phone.text
        email = self.ids.email.text
        job_role = self.ids.job_role.text
        work_type = self.ids.work_type.text
        

        # التحقق من تعبئة كافة الحقول
        if not all([name, phone, email, job_role, work_type]):
            self.show_dialog("All fields are required!")
        else:
            try:
                # إدخال البيانات في قاعدة البيانات
                c.execute("INSERT INTO employee (name, phone, email, job_role, work_type) VALUES (?, ?, ?, ?, ?)",
                          (name, phone, email, job_role, work_type))
                conn.commit()
                self.show_dialog("Employee added successfully!")
                
                # مسح الحقول بعد إضافة الموظف
                self.ids.name.text = ''
                self.ids.phone.text = ''
                self.ids.email.text = ''
                self.ids.job_role.text = ''
                self.ids.work_type.text = ''
                
            except sqlite3.Error as e:
                self.show_dialog(f"Error: {e}")

    # عرض الرسائل في مربع حوار
    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()
class View_Employee_Screen(Screen):
    def on_enter(self):
        # عند فتح الشاشة، استرجع كل العملاء من قاعدة البيانات
        self.display_employee()

    def display_employee(self):
        # مسح أي بيانات سابقة في الواجهة
        self.ids.employee_info.clear_widgets()

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee")
        employee = cursor.fetchall()

        if employee:
            for employe in employee:
                # عرض بيانات كل عميل في سطور منفصلة
                employee_label = MDLabel(
                    text=f"Name: {employe[1]}\nPhone: {employe[2]}\nEmail: {employe[3]}\njob_role: {employe[4]}\nwork_type: {employe[5]}",
                    theme_text_color="Custom",
                    text_color=(0.6, 0, 1, 1),
                    halign="left",
                    size_hint_y=None,
                    height=120  # تعديل الارتفاع ليتناسب مع عدد السطور
                )
                self.ids.employee_info.add_widget(employee_label)
        else:
            # إذا لم يكن هناك بيانات
            no_data_label1 = MDLabel(
                text="No employee found.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            self.ids.employee_info.add_widget(no_data_label1)

    def search_employee(self):
        # البحث عن العميل باستخدام الاسم
        employee_name = self.ids.search_input.text
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE name = ?", (employee_name,))
        employee_data = cursor.fetchone()

        self.ids.employee_info.clear_widgets()

        if employee_data:
            # عرض بيانات العميل المطلوب في سطور منفصلة
            employee_label = MDLabel(
                text=f"Name: {employee_data[1]}\nPhone: {employee_data[2]}\nEmail: {employee_data[3]}\njob_role: {employee_data[4]}\nwork_type: {employee_data[5]}",
                theme_text_color="Custom",
                text_color=(0.6, 0, 1, 1),
                halign="left",
                size_hint_y=None,
                height=120  # تعديل الارتفاع ليتناسب مع عدد السطور
            )
            self.ids.employee_info.add_widget(employee_label)
        else:
            no_data_label = MDLabel(
                text="employee not found.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            self.ids.employee_info.add_widget(no_data_label)

class Edit_Employee_Screen(Screen):
    dialog = None

    def search_employee(self):
        employee_name = self.ids.search_input.text.strip()
        if not employee_name:
            self.show_dialog("Please enter a employee name to search.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE name = ?", (employee_name,))
        employee_data = cursor.fetchone()

        if employee_data:
            # الوصول إلى عناصر الإدخال من الشاشة الحالية
            self.ids.name.text = employee_data[1] if employee_data[1] is not None else ""
            self.ids.phone.text = employee_data[2] if employee_data[2] is not None else ""
            self.ids.email.text = employee_data[3] if employee_data[3] is not None else ""
            self.ids.job_role.text = employee_data[4] if employee_data[4] is not None else ""
            self.ids.work_type.text = str(employee_data[5]) if employee_data[5] is not None else ""

            # جعل حقل الاسم قابل للتعديل
            self.ids.name.disabled = False

        else:
            self.show_dialog("employee not found.")

    def update_employee(self):
        employee_name = self.ids.search_input.text.strip()
        if not employee_name:
            self.show_dialog("Please search for a employee first.")
            return

        # Get updated data from TextFields
        name = self.ids.name.text.strip()
        phone = self.ids.phone.text.strip()
        email = self.ids.email.text.strip()
        job_role = self.ids.job_role.text.strip()
        work_type = self.ids.work_type.text.strip()

        if not all([name, phone, email, job_role, work_type]):
            self.show_dialog("All fields are required.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE employee
                SET name = ?, phone = ?, email = ?, job_role = ?, work_type = ?
                WHERE name = ?
            """, (name, phone, email, job_role, work_type, employee_name))
            conn.commit()
            self.show_dialog("employee updated successfully!")
        except sqlite3.Error as e:
            self.show_dialog(f"Error updating emplyee: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()

class Delete_Employee_Screen(Screen):
    dialog = None

    def search_employee(self):
        employee_name = self.ids.search_input.text.strip()
        if not employee_name:
            self.show_dialog("Please enter a employee name to search.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE name = ?", (employee_name,))
        employee_data = cursor.fetchone()

        if employee_data:
            # عرض بيانات العميل (اختياري)
            self.ids.name.text = employee_data[1] if employee_data[1] is not None else ""
            self.ids.phone.text = employee_data[2] if employee_data[2] is not None else ""
            self.ids.email.text = employee_data[3] if employee_data[3] is not None else ""
            self.ids.job_role.text = employee_data[4] if employee_data[4] is not None else ""
            self.ids.work_type.text = str(employee_data[5]) if employee_data[5] is not None else ""

            # تمكين زر الحذف
            self.ids.delete_button.disabled = False

        else:
            self.show_dialog("employee not found.")

    def delete_employee(self):
        employee_name = self.ids.search_input.text.strip()
        if not employee_name:
            self.show_dialog("Please search for a employee first.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employee WHERE name = ?", (employee_name,))
            if cursor.rowcount == 0:
                self.show_dialog("employee not found or already deleted.")
            else:
                conn.commit()
                self.show_dialog("employee deleted successfully!")
                # يمكنك مسح الحقول بعد الحذف
                self.ids.search_input.text = ""
                self.ids.name.text = ""
                self.ids.phone.text = ""
                self.ids.email.text = ""
                self.ids.job_role.text = ""
                self.ids.work_type.text = ""
                self.ids.delete_button.disabled = True

        except sqlite3.Error as e:
            self.show_dialog(f"Error deleting employee: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()
class Admins_Screen(Screen):
    dialog = None

    def add_admins(self):
        # الحصول على القيم من الحقول
        name = self.ids.name.text
        phone = self.ids.phone.text
        email = self.ids.email.text
        employe_admin = self.ids.employe_admin.text
        work_time = self.ids.work_time.text
        

        # التحقق من تعبئة كافة الحقول
        if not all([name, phone, email, employe_admin, work_time]):
            self.show_dialog("All fields are required!")
        else:
            try:
                # إدخال البيانات في قاعدة البيانات
                c.execute("INSERT INTO admins (name, phone, email, employe_admin, work_time) VALUES (?, ?, ?, ?, ?)",
                          (name, phone, email, employe_admin, work_time))
                conn.commit()
                self.show_dialog("Employee added successfully!")
                
                # مسح الحقول بعد إضافة الموظف
                self.ids.name.text = ''
                self.ids.phone.text = ''
                self.ids.email.text = ''
                self.ids.employe_admin.text = ''
                self.ids.work_time.text = ''
                
            except sqlite3.Error as e:
                self.show_dialog(f"Error: {e}")

    # عرض الرسائل في مربع حوار
    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()
class Service_Screen(Screen):
    dialog = None

    def add_service(self):
        # الحصول على القيم من الحقول
        
        service_name = self.ids.service_name.text
        service_price=self.ids.service_price.text
        service_type = self.ids.service_type.text
        admin = self.ids.admin.text
        clint_name = self.ids.clint_name.text
        

        # التحقق من تعبئة كافة الحقول
        if not all([service_name, service_price,service_type, admin, clint_name]):
            self.show_dialog("All fields are required!")
        else:
            try:
                # إدخال البيانات في قاعدة البيانات
                c.execute("INSERT INTO service (service_name, service_price,service_type, admin, clint_name) VALUES (?, ?, ?, ?, ?)",
                          ( service_name, service_price , service_type, admin, clint_name))
                conn.commit()
                self.show_dialog("Employee added successfully!")
                
                self.ids.service_name.text = ''
                self.ids.service_price.text= ''
                self.ids.service_type.text = ''
                self.ids.admin.text = ''
                self.ids.clint_name.text = ''
                
            except sqlite3.Error as e:
                self.show_dialog(f"Error: {e}")

    # عرض الرسائل في مربع حوار
    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()
class View_Service_Screen(Screen):
    def on_enter(self):
        # عند فتح الشاشة، استرجع كل العملاء من قاعدة البيانات
        self.display_service()

    def display_service(self):
        # مسح أي بيانات سابقة في الواجهة
        self.ids.service_info.clear_widgets()

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service")
        service = cursor.fetchall()

        if service:
            for service in service:
                # عرض بيانات كل عميل في سطور منفصلة
                service_label = MDLabel(
                    text=f"service_name: {service[1]}\nservice_price: {service[2]}\nservice_type: {service[3]}\nadmin: {service[4]}\nclint_name: {service[5]}",
                    theme_text_color="Custom",
                    text_color=(0.6, 0, 1, 1),
                    halign="left",
                    size_hint_y=None,
                    height=120  # تعديل الارتفاع ليتناسب مع عدد السطور
                )
                self.ids.service_info.add_widget(service_label)
        else:
            # إذا لم يكن هناك بيانات
            no_data_label1 = MDLabel(
                text="No service found.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            self.ids.service_info.add_widget(no_data_label1)

    def search_service(self):
        # البحث عن العميل باستخدام الاسم
        service_name = self.ids.search_input.text
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service WHERE name = ?", (service_name,))
        service_data = cursor.fetchone()

        self.ids.service_info.clear_widgets()

        if service_data:
            # عرض بيانات العميل المطلوب في سطور منفصلة
            service_label = MDLabel(
                text=f"service_name: {service_data[1]}\nservice_price: {service_data[2]}\nservice_type: {service_data[3]}\nadmin: {service_data[4]}\nclint_name: {service_data[5]}",
                theme_text_color="Custom",
                text_color=(0.6, 0, 1, 1),
                halign="left",
                size_hint_y=None,
                height=120  # تعديل الارتفاع ليتناسب مع عدد السطور
            )
            self.ids.service_info.add_widget(service_label)
        else:
            no_data_label = MDLabel(
                text="service not found.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            self.ids.service_info.add_widget(no_data_label)


class Edit_Service_Screen(Screen):
    dialog = None

    def search_service(self):
        service_name = self.ids.search_input.text.strip()
        if not service_name:
            self.show_dialog("Please enter a employee name to search.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service WHERE clint_name = ?", (service_name,))
        service_data = cursor.fetchone()

        if service_data:
            # الوصول إلى عناصر الإدخال من الشاشة الحالية
            self.ids.service_name.text = service_data[1] if service_data[1] is not None else ""
            self.ids.service_price.text = service_data[2] if service_data[2] is not None else ""
            self.ids.service_type.text = service_data[3] if service_data[3] is not None else ""
            self.ids.admin.text = service_data[4] if service_data[4] is not None else ""
            self.ids.clint_name.text = str(service_data[5]) if service_data[5] is not None else ""

            # جعل حقل الاسم قابل للتعديل
            self.ids.clint_name.disabled = False

        else:
            self.show_dialog("service not found.")

    def update_service(self):
        original_clint_name = self.ids.search_input.text.strip()
        if not original_clint_name:
            self.show_dialog("Please search for a service first.")
            return

        # Get updated data from TextFields
        service_name = self.ids.service_name.text.strip()
        service_price = self.ids.service_price.text.strip()
        service_type = self.ids.service_type.text.strip()
        admin = self.ids.admin.text.strip()
        clint_name = self.ids.clint_name.text.strip()

        if not all([service_name, service_price, service_type, admin, clint_name]):
            self.show_dialog("All fields are required.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE service
                SET service_name = ?, service_price = ?, service_type = ?, admin = ?, clint_name = ?
                WHERE clint_name = ?
            """, (service_name, service_price, service_type, admin, clint_name,original_clint_name ))
            conn.commit()
            self.show_dialog("service updated successfully!")
        except sqlite3.Error as e:
            self.show_dialog(f"Error updating service: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()


class Delete_Service_Screen(Screen):
    dialog = None

    def search_service(self):
        service_name = self.ids.search_input.text.strip()
        if not service_name:
            self.show_dialog("Please enter a service name to search.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service WHERE clint_name = ?", (service_name,))
        service_data = cursor.fetchone()

        if service_data:
            # عرض بيانات العميل (اختياري)
            self.ids.service_name.text = service_data[1] if service_data[1] is not None else ""
            self.ids.service_price.text = service_data[2] if service_data[2] is not None else ""
            self.ids.service_type.text = service_data[3] if service_data[3] is not None else ""
            self.ids.admin.text = service_data[4] if service_data[4] is not None else ""
            self.ids.clint_name.text = str(service_data[5]) if service_data[5] is not None else ""

            # تمكين زر الحذف
            self.ids.delete_button.disabled = False

        else:
            self.show_dialog("service not found.")

    def delete_service(self):
        service_name = self.ids.search_input.text.strip()
        if not service_name:
            self.show_dialog("Please search for a service first.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM service WHERE clint_name = ?", (service_name,))
            if cursor.rowcount == 0:
                self.show_dialog("service not found or already deleted.")
            else:
                conn.commit()
                self.show_dialog("service deleted successfully!")
                # يمكنك مسح الحقول بعد الحذف
                self.ids.search_input.text = ""
                self.ids.service_name.text = ""
                self.ids.service_price.text = ""
                self.ids.service_type.text = ""
                self.ids.admin.text = ""
                self.ids.clint_name.text = ""
                self.ids.delete_button.disabled = True

        except sqlite3.Error as e:
            self.show_dialog(f"Error deleting service: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()

class Train_Screen(Screen):
    dialog = None

    def add_train(self):
        # الحصول على القيم من الحقول
        
        t_clint_name = self.ids.t_clint_name.text
        email_train=self.ids.email_train.text
        date_train = self.ids.date_train.text
        payment_made = self.ids.payment_made.text
        amount = self.ids.amount.text
        residual_amount=self.ids.residual_amount.text
        

        # التحقق من تعبئة كافة الحقول
        if not all([t_clint_name, email_train,date_train, payment_made, amount,residual_amount]):
            self.show_dialog("All fields are required!")
        else:
            try:
                # إدخال البيانات في قاعدة البيانات
                c.execute("INSERT INTO train (t_clint_name, email_train,date_train, payment_made, amount , residual_amount) VALUES (?, ?, ?, ?, ? ,?)",
                          ( t_clint_name, email_train , date_train, payment_made, amount , residual_amount))
                conn.commit()
                self.show_dialog("tran added successfully!")
                
                self.ids.t_clint_name.text = ''
                self.ids.email_train.text= ''
                self.ids.date_train.text = ''
                self.ids.payment_made.text = ''
                self.ids.amount.text = ''
                self.ids.residual_amount.text = ''
                
            except sqlite3.Error as e:
                self.show_dialog(f"Error: {e}")

    # عرض الرسائل في مربع حوار
    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()

class View_Train_Screen(Screen):
    def on_enter(self):
        # عند فتح الشاشة، استرجع كل العملاء من قاعدة البيانات
        self.display_train()

    def display_train(self):
        # مسح أي بيانات سابقة في الواجهة
        self.ids.train_info.clear_widgets()

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM train")
        train = cursor.fetchall()

        if train:
            for train in train:
                # عرض بيانات كل عميل في سطور منفصلة
                train_label = MDLabel(
                    text=f"t_clint_name: {train[1]}\n email_train: {train[2]}\n date_train: {train[3]}\n payment_made: {train[4]}\n amount: {train[5]}\n residual_amount: {train[6]}",
                    theme_text_color="Custom",
                    text_color=(0.6, 0, 1, 1),
                    halign="left",
                    size_hint_y=None,
                    height=120  # تعديل الارتفاع ليتناسب مع عدد السطور
                )
                self.ids.train_info.add_widget(train_label)
        else:
            # إذا لم يكن هناك بيانات
            no_data_label1 = MDLabel(
                text="No train found.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            self.ids.train_info.add_widget(no_data_label1)

    def search_train(self):
        # البحث عن العميل باستخدام الاسم
        t_clint_name= self.ids.search_input.text
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM train WHERE name = ?", (t_clint_name,))
        train_data = cursor.fetchone()

        self.ids.train_info.clear_widgets()

        if train_data:
            # عرض بيانات العميل المطلوب في سطور منفصلة
            train_label = MDLabel(
                text=f"t_clint_name: {train_data[1]}\n email_train: {train_data[2]}\n date_train: {train_data[3]}\n payment_made: {train_data[4]}\n amount: {train_data[5]}\n residual_amount{train_data[6]}",
                theme_text_color="Custom",
                text_color=(0.6, 0, 1, 1),
                halign="left",
                size_hint_y=None,
                height=120  # تعديل الارتفاع ليتناسب مع عدد السطور
            )
            self.ids.train_info.add_widget(train_label)
        else:
            no_data_label = MDLabel(
                text="train not found.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            self.ids.train_info.add_widget(no_data_label)

class Edit_Train_Screen(Screen):
    dialog = None

    def search_train(self):
        t_clint_name = self.ids.search_input.text.strip()
        if not t_clint_name:
            self.show_dialog("Please enter a train name to search.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM train WHERE t_clint_name = ?", (t_clint_name,))
        train_data = cursor.fetchone()

        if train_data:
            # الوصول إلى عناصر الإدخال من الشاشة الحالية
            self.ids.t_clint_name.text = train_data[1] if train_data[1] is not None else ""
            self.ids.email_train.text = train_data[2] if train_data[2] is not None else ""
            self.ids.date_train.text = train_data[3] if train_data[3] is not None else ""
            self.ids.payment_made.text = train_data[4] if train_data[4] is not None else ""
            self.ids.amount.text = str(train_data[5]) if train_data[5] is not None else ""
            self.ids.residual_amount.text = str(train_data[5]) if train_data[5] is not None else ""

            # جعل حقل الاسم قابل للتعديل
            self.ids.t_clint_name.disabled = False

        else:
            self.show_dialog("train not found.")

    def update_train(self):
        original_t_clint_name = self.ids.search_input.text.strip()
        if not original_t_clint_name:
            self.show_dialog("Please search for a train first.")
            return

        # Get updated data from TextFields
        t_clint_name = self.ids.t_clint_name.text.strip()
        email_train = self.ids.email_train.text.strip()
        date_train = self.ids.date_train.text.strip()
        payment_made = self.ids.payment_made.text.strip()
        amount = self.ids.amount.text.strip()
        residual_amount = self.ids.residual_amount.text.strip()

        if not all([t_clint_name, email_train, date_train, payment_made, amount,residual_amount]):
            self.show_dialog("All fields are required.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE train
                SET t_clint_name = ?, email_train = ?, date_train = ?, payment_made = ?, amount = ? , residual_amount = ?
                WHERE t_clint_name = ?
            """, (t_clint_name, email_train, date_train, payment_made, amount,residual_amount,original_t_clint_name ))
            conn.commit()
            self.show_dialog("train updated successfully!")
        except sqlite3.Error as e:
            self.show_dialog(f"Error updating train: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()

class Delete_Train_Screen(Screen):
    dialog = None

    def search_train(self):
        t_clint_name = self.ids.search_input.text.strip()
        if not t_clint_name:
            self.show_dialog("Please enter a transction name to search.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM train WHERE t_clint_name = ?", (t_clint_name,))
        train_data = cursor.fetchone()

        if train_data:
            # عرض بيانات العميل (اختياري)
            self.ids.t_clint_name.text = train_data[1] if train_data[1] is not None else ""
            self.ids.email_train.text = train_data[2] if train_data[2] is not None else ""
            self.ids.date_train.text = train_data[3] if train_data[3] is not None else ""
            self.ids.payment_made.text = train_data[4] if train_data[4] is not None else ""
            self.ids.amount.text = str(train_data[5]) if train_data[5] is not None else ""
            self.ids.residual_amount.text = str(train_data[6]) if train_data[6] is not None else ""

            # تمكين زر الحذف
            self.ids.delete_button.disabled = False

        else:
            self.show_dialog("transction not found.")

    def delete_train(self):
        t_clint_name = self.ids.search_input.text.strip()
        if not t_clint_name:
            self.show_dialog("Please search for a transction first.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM train WHERE t_clint_name = ?", (t_clint_name,))
            if cursor.rowcount == 0:
                self.show_dialog("transction not found or already deleted.")
            else:
                conn.commit()
                self.show_dialog("transction deleted successfully!")
                # يمكنك مسح الحقول بعد الحذف
                self.ids.t_clint_name.text = ""
                self.ids.email_train.text = ""
                self.ids.date_train.text = ""
                self.ids.payment_made.text = ""
                self.ids.amount.text = ""
                self.ids.residual_amount.text = ""
                self.ids.delete_button.disabled = True

        except sqlite3.Error as e:
            self.show_dialog(f"Error deleting transction: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()



class Accounts_Screen(Screen):
    dialog = None
    def add_accounts(self):
        # الحصول على القيم من الحقول
        
        freelane_name = self.ids.freelane_name.text
        amount=self.ids.amount.text
        admin_name = self.ids.admin_name.text

        

        # التحقق من تعبئة كافة الحقول
        if not all([freelane_name, amount,admin_name]):
            self.show_dialog("All fields are required!")
        else:
            try:
                # إدخال البيانات في قاعدة البيانات
                c.execute("INSERT INTO accounts (freelane_name, amount,admin_name) VALUES (?, ?, ?)",
                          ( freelane_name, amount , admin_name))
                conn.commit()
                self.show_dialog("tran added successfully!")
                
                self.ids.freelane_name.text = ''
                self.ids.amount.text= ''
                self.ids.admin_name.text = ''

                
            except sqlite3.Error as e:
                self.show_dialog(f"Error: {e}")

    # عرض الرسائل في مربع حوار
    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()

    def accounts(self):
        try:
            # حساب إجمالي الدخل من جدول train
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(payment_made) FROM train")
            total_income = cursor.fetchone()[0] or 0

            # حساب إجمالي الخارج من جدول accounts
            cursor.execute("SELECT SUM(amount) FROM accounts")
            total_out = cursor.fetchone()[0] or 0

            # حساب المتبقي
            residual = total_income - total_out

            self.ids.total_income.text = f"Total Income: {total_income}"
            self.ids.total_out.text = f"Total Out: {total_out}"
            self.ids.residual.text = f"residual: {residual}"

            # عرض النتائج في مربع حوار
            

            # عرض البيانات من جدول accounts
            

        except sqlite3.Error as e:
            self.show_dialog(f"Error: {e}")

    
    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()

class View_Accounts_Screen(Screen):
    def on_enter(self):
        # عند فتح الشاشة، استرجع كل العملاء من قاعدة البيانات
        self.display_accounts()

    def display_accounts(self):
        # مسح أي بيانات سابقة في الواجهة
        self.ids.accounts_info.clear_widgets()

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()

        if accounts:
            for accounts in accounts:
                # عرض بيانات كل عميل في سطور منفصلة
                accounts_label = MDLabel(
                    text=f"freelane_name: {accounts[1]}\n amount: {accounts[2]}\n admin_name: {accounts[3]}",
                    theme_text_color="Custom",
                    text_color=(0.6, 0, 1, 1),
                    halign="left",
                    size_hint_y=None,
                    height=120  # تعديل الارتفاع ليتناسب مع عدد السطور
                )
                self.ids.accounts_info.add_widget(accounts_label)
        else:
            # إذا لم يكن هناك بيانات
            no_data_label1 = MDLabel(
                text="No accounts found.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            self.ids.accounts_info.add_widget(no_data_label1)

    def search_accounts(self):
        # البحث عن العميل باستخدام الاسم
        freelane_name= self.ids.search_input.text
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE freelane_name = ?", (freelane_name,))
        accounts_data = cursor.fetchone()

        self.ids.accounts_info.clear_widgets()

        if accounts_data:
            # عرض بيانات العميل المطلوب في سطور منفصلة
            accounts_label = MDLabel(
                text=f"freelane_name: {accounts_data[1]}\n amount: {accounts_data[2]}\n admin_name: {accounts_data[3]}",
                theme_text_color="Custom",
                text_color=(0.6, 0, 1, 1),
                halign="left",
                size_hint_y=None,
                height=120  # تعديل الارتفاع ليتناسب مع عدد السطور
            )
            self.ids.accounts_info.add_widget(accounts_label)
        else:
            no_data_label = MDLabel(
                text="accounts not found.",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            )
            self.ids.accounts_info.add_widget(no_data_label)

class Edit_Accounts_Screen(Screen):
    dialog = None

    def search_accounts(self):
        freelane_name = self.ids.search_input.text.strip()
        if not freelane_name:
            self.show_dialog("Please enter a accounts name to search.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE freelane_name = ?", (freelane_name,))
        accounts_data = cursor.fetchone()

        if accounts_data:
            # الوصول إلى عناصر الإدخال من الشاشة الحالية
            self.ids.freelane_name.text = accounts_data[1] if accounts_data[1] is not None else ""
            self.ids.amount.text = accounts_data[2] if accounts_data[2] is not None else ""
            self.ids.admin_name.text = accounts_data[3] if accounts_data[3] is not None else ""

            # جعل حقل الاسم قابل للتعديل
            self.ids.freelane_name.disabled = False

        else:
            self.show_dialog("accounts not found.")

    def update_accounts(self):
        original_freelane_name = self.ids.search_input.text.strip()
        if not original_freelane_name:
            self.show_dialog("Please search for a accounts first.")
            return

        # Get updated data from TextFields
        freelane_name = self.ids.freelane_name.text.strip()
        amount = self.ids.amount.text.strip()
        admin_name = self.ids.admin_name.text.strip()


        if not all([freelane_name, amount, admin_name]):
            self.show_dialog("All fields are required.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE accounts
                SET freelane_name = ?, amount = ?, admin_name = ?
                WHERE freelane_name = ?
            """, (freelane_name, amount, admin_name, original_freelane_name))
            conn.commit()
            self.show_dialog("accounts updated successfully!")
        except sqlite3.Error as e:
            self.show_dialog(f"Error updating accounts: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()

class Delete_Accounts_Screen(Screen):
    dialog = None

    def search_accounts(self):
        freelane_name  = self.ids.search_input.text.strip()
        if not freelane_name:
            self.show_dialog("Please enter a accounts name to search.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE freelane_name = ?", (freelane_name,))
        accounts_data = cursor.fetchone()

        if accounts_data:
            # عرض بيانات العميل (اختياري)
            self.ids.freelane_name.text = accounts_data[1] if accounts_data[1] is not None else ""
            self.ids.amount.text = accounts_data[2] if accounts_data[2] is not None else ""
            self.ids.admin_name.text = accounts_data[3] if accounts_data[3] is not None else ""

            # تمكين زر الحذف
            self.ids.delete_button.disabled = False

        else:
            self.show_dialog("accounts not found.")

    def delete_train(self):
        freelane_name = self.ids.search_input.text.strip()
        if not freelane_name:
            self.show_dialog("Please search for a accounts first.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM accounts WHERE freelane_name = ?", (freelane_name,))
            if cursor.rowcount == 0:
                self.show_dialog("accounts not found or already deleted.")
            else:
                conn.commit()
                self.show_dialog("accounts deleted successfully!")
                # يمكنك مسح الحقول بعد الحذف
                self.ids.freelane_name.text = ""
                self.ids.amount.text = ""
                self.ids.admin_name.text = ""
                self.ids.delete_button.disabled = True

        except sqlite3.Error as e:
            self.show_dialog(f"Error deleting accounts: {e}")

    def show_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = message
        self.dialog.open()




# إدارة الشاشات
class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"  # لون الأزرار البنفسجي
        return Builder.load_string(KV)

# واجهات المستخدم بلغة KV
KV = '''
ScreenManager:
    LoginScreen:
    SignUpScreen:
    MainScreen:
    ClientsScreen:
    View_clint_Screen:
    Edit_clint_Screen:
    Delete_clint_Screen:
    Employee_Screen:
    View_Employee_Screen:
    Edit_Employee_Screen:
    Delete_Employee_Screen:
    Admins_Screen:
    Service_Screen:
    View_Service_Screen:
    Edit_Service_Screen:
    Delete_Service_Screen:
    Train_Screen:
    View_Train_Screen:
    Edit_Train_Screen:
    Delete_Train_Screen:
    Accounts_Screen:
    View_Accounts_Screen:
    Edit_Accounts_Screen:
    Delete_Accounts_Screen:

    

<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1
        MDLabel:
            text: "Login"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1
            
        Image:
            source: 'D:\\programming project\\python\\kivy\\kivyproject\\lo.png'
            size_hint: (0.5, 0.5)
            pos_hint: {"center_x": 0.5}
        MDTextField:
            id: username
            hint_text: "Username"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDTextField:
            id: password
            hint_text: "Password"
            password: True
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current_screen.login()
        MDTextButton:
            text: "Don't have an account? Sign Up"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "signup"


<SignUpScreen>:
    name: "signup"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1
        MDLabel:
            text: "Sign Up"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1
        Image:
            source: 'D:\\programming project\\python\\kivy\\kivyproject\\lo.png'
            size_hint: (0.5, 0.5)
            pos_hint: {"center_x": 0.5}
        MDTextField:
            id: username
            hint_text: "Username"
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
            id: password
            hint_text: "Password"
            password: True
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDRaisedButton:
            text: "Sign Up"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current_screen.create_account()
        MDTextButton:
            text: "Already have an account? Login"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "login"

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0, 0, 0, 1  # الخلفية سوداء

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.2  # يشغل الجزء العلوي من الشاشة
            padding: dp(10)
            spacing: dp(10)

            MDRaisedButton:
                text: "About"
                md_bg_color: 0.6, 0, 1, 1  # اللون البنفسجي
                text_color: 1, 1, 1, 1
                size_hint_x: 1  # الحجم متساوٍ بين الأزرار
                on_release: app.root.current_screen.show_about()

            MDRaisedButton:
                text: "Help"
                md_bg_color: 0.6, 0, 1, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 1  # الحجم متساوٍ بين الأزرار
                on_release: app.root.current_screen.show_help()

            MDRaisedButton:
                text: "Social Media"
                md_bg_color: 0.6, 0, 1, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 1  # الحجم متساوٍ بين الأزرار
                on_release: app.root.current_screen.show_social_media()


        Image:
            source: "D:\\programming project\\python\\kivy\\kivyproject\\lo.png"  # ضع هنا مسار صورتك
            size_hint: 0.9, 0.6
            pos_hint: {"center_x": 0.5}

        MDGridLayout:
            cols: 1
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height  # يضمن أن الشبكة تأخذ الحجم الصحيح

            MDRaisedButton:
                text: "Clients"
                md_bg_color: 0.6, 0, 1, 1  # اللون البنفسجي
                text_color: 1, 1, 1, 1
                size_hint_x: 0.5
                pos_hint: {"center_x": 0.5}
                on_release: app.root.current = "clients"

            MDRaisedButton:
                text: "Employees"
                md_bg_color: 0.6, 0, 1, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.5
                pos_hint: {"center_x": 0.5}
                on_release: app.root.current ="employee"

            MDRaisedButton:
                text: "Admins"
                md_bg_color: 0.6, 0, 1, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.5
                pos_hint: {"center_x": 0.5}
                on_release: app.root.current="admins"

            MDRaisedButton:
                text: "Services"
                md_bg_color: 0.6, 0, 1, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.5
                pos_hint: {"center_x": 0.5}
                on_release: app.root.current="service"

            MDRaisedButton:
                text: "Transactions"
                md_bg_color: 0.6, 0, 1, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.5
                pos_hint: {"center_x": 0.5}
                on_release: app.root.current="train"

            MDRaisedButton:
                text: "Accounts"
                md_bg_color: 0.6, 0, 1, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.5
                pos_hint: {"center_x": 0.5}
                on_release: app.root.current="accounts"
<ClientsScreen>:
    name: "clients"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Clients"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1

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
            hint_text: "Client Phone"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: email
            hint_text: "Client Email"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: address
            hint_text: "Client Address"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: rating
            hint_text: "Client Rating"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDRaisedButton:
            text: "Add Client"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: root.add_client()
        MDRaisedButton:
            text: "VIEW CLINT"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "v_clint"
        MDRaisedButton:
            text: "EDIT CLINT"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "edit_clint"
        MDRaisedButton:
            text: "DELETE CLINT"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "delete_clint"

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "main"
<View_clint_Screen>:
    name: "v_clint"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "View Clients"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1

        ScrollView:
            size_hint: (1, 1)
            MDBoxLayout:
                id: client_info
                orientation: 'vertical'
                adaptive_height: True
                padding: 10
                spacing: 10

        MDTextField:
            id: search_input
            hint_text: "Enter client name"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1


        MDRaisedButton:
            text: "Search"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            on_press: root.search_client()
        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "clients"

<Edit_clint_Screen>:
    name: "edit_clint"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Edit Client"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1
        
        MDTextField:
            id: search_input
            hint_text: "Enter client name to search"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDRaisedButton:
            text: "Search"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.6, 0.9, 1
            text_color: 1, 1, 1, 1
            on_release: root.search_client()

        MDTextField:
            id: name
            hint_text: "Client Name"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: phone
            hint_text: "Client Phone"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: email
            hint_text: "Client Email"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: address
            hint_text: "Client Address"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: rating
            hint_text: "Client Rating"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDRaisedButton:
            text: "Update"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.4, 0.8, 0.4, 1
            text_color: 1, 1, 1, 1
            on_release: root.update_client()

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.8, 0.2, 0.2, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "clients"

<Delete_clint_Screen>:
    name: "delete_clint"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Delete Client"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDTextField:
            id: search_input
            hint_text: "Enter client name to search"
            size_hint_y: None
            height: "30dp"
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        
        MDRaisedButton:
            text: "Search"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: root.search_client()

        MDTextField:
            id: name
            hint_text: "Name"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: phone
            hint_text: "Phone"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        MDTextField:
            id: email
            hint_text: "Email"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: address
            hint_text: "Address"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: rating
            hint_text: "Rating"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        MDRaisedButton:
            id: delete_button
            text: "Delete"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 1, 0, 0, 1
            text_color: 1, 1, 1, 1
            on_release: root.delete_client()
            disabled: True
            
        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "clients"

<Employee_Screen>:
    name: "employee"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1
    
        MDLabel:
            text: "employee"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
        

        MDTextField:
            id: name
            hint_text: "employe name"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDTextField:
            id: phone
            hint_text: "employe Phone"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: email
            hint_text: "employe Email"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: job_role
            hint_text: "job role"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: work_type
            hint_text: "work type"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDRaisedButton:
            text: "Add Employe"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: root.add_employee()
        MDRaisedButton:
            text: "VIEW Employe"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "v_employe"
        MDRaisedButton:
            text: "EDIT Employe"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "edit_employe"
        MDRaisedButton:
            text: "DELETE Employe"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "delete_employe"

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "main"
        
<View_Employee_Screen>:
    name: "v_employe"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "View employee"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1

        ScrollView:
            size_hint: (1, 1)
            MDBoxLayout:
                id: employee_info
                orientation: 'vertical'
                adaptive_height: True
                padding: 10
                spacing: 10

        MDTextField:
            id: search_input
            hint_text: "Enter employee name"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1


        MDRaisedButton:
            text: "Search"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            on_press: root.search_employee()
        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "employee"
<Edit_Employee_Screen>:
    name: "edit_employe"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Edit employe"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1
        
        MDTextField:
            id: search_input
            hint_text: "Enter employe name to search"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDRaisedButton:
            text: "Search"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.6, 0.9, 1
            text_color: 1, 1, 1, 1
            on_release: root.search_employee()

        MDTextField:
            id: name
            hint_text: "employe Name"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: phone
            hint_text: "employe Phone"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: email
            hint_text: "employe Email"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: job_role
            hint_text: "job role"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: work_type
            hint_text: "work type "
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDRaisedButton:
            text: "Update"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.4, 0.8, 0.4, 1
            text_color: 1, 1, 1, 1
            on_release: root.update_employee()

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.8, 0.2, 0.2, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "employee"

<Delete_Employee_Screen>:
    name: "delete_employe"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Delete employe"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDTextField:
            id: search_input
            hint_text: "Enter employe name to search"
            size_hint_y: None
            height: "30dp"
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        
        MDRaisedButton:
            text: "Search"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: root.search_employee()

        MDTextField:
            id: name
            hint_text: "Name"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: phone
            hint_text: "Phone"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        MDTextField:
            id: email
            hint_text: "Email"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: work_type
            hint_text: "work type"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: job_role
            hint_text: "job role"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        MDRaisedButton:
            id: delete_button
            text: "Delete"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 1, 0, 0, 1
            text_color: 1, 1, 1, 1
            on_release: root.delete_employee()
            disabled: True
            
        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "employee"

<Admins_Screen>:
    name: "admins"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1
    
        MDLabel:
            text: "Admins"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
        

        MDTextField:
            id: name
            hint_text: "admin name"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        MDTextField:
            id: phone
            hint_text: "admin Phone"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: email
            hint_text: "admin Email"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: employe_admin
            hint_text: "employe admin"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: work_time
            hint_text: "work time"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDRaisedButton:
            text: "Add Admin"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: root.add_admins()
        MDRaisedButton:
            text: "VIEW Admin"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "v_employe"
        MDRaisedButton:
            text: "EDIT Admin"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "edit_employe"
        MDRaisedButton:
            text: "DELETE Admin"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "delete_employe"

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "main"   
<Service_screen>:
    name: "service"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "service"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1


        MDTextField:
            id: service_name
            hint_text: "service name"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        
        MDTextField:
            id: service_price
            hint_text: "service price"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: service_type
            hint_text: "service type"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: admin
            hint_text: "admin"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: clint_name
            hint_text: "Client name"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        
        

        MDRaisedButton:
            text: "Add service"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: root.add_service()
        MDRaisedButton:
            text: "VIEW service"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "v_service"
        MDRaisedButton:
            text: "EDIT service"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "edit_service"
        MDRaisedButton:
            text: "DELETE service"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "delete_service"

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "main"
<View_Service_Screen>:
    name: "v_service"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "View service"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1

        ScrollView:
            size_hint: (1, 1)
            MDBoxLayout:
                id: service_info
                orientation: 'vertical'
                adaptive_height: True
                padding: 10
                spacing: 10

        MDTextField:
            id: search_input
            hint_text: "Enter service name"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1


        MDRaisedButton:
            text: "Search"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            on_press: root.search_service()
        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "service"
<Edit_Service_Screen>:
    name: "edit_service"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Edit service"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1
        
        MDTextField:
            id: search_input
            hint_text: "Enter service name to search"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDRaisedButton:
            text: "Search"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.6, 0.9, 1
            text_color: 1, 1, 1, 1
            on_release: root.search_service()

        MDTextField:
            id: service_name
            hint_text: "service Name"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: service_price
            hint_text: "service price"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: service_type
            hint_text: "service type"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: admin
            hint_text: "admin"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: clint_name
            hint_text: "clint_name"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDRaisedButton:
            text: "Update"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.4, 0.8, 0.4, 1
            text_color: 1, 1, 1, 1
            on_release: root.update_service()

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.8, 0.2, 0.2, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "service"

<Delete_Service_Screen>:
    name: "delete_service"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Delete service"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDTextField:
            id: search_input
            hint_text: "Enter service name to search"
            size_hint_y: None
            height: "30dp"
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        
        MDRaisedButton:
            text: "Search"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: root.search_service()

        MDTextField:
            id: service_name
            hint_text: "service Name"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: service_price
            hint_text: "service price"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        MDTextField:
            id: service_type
            hint_text: "service type"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: admin
            hint_text: "admin"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: clint_name
            hint_text: "clint_name"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        MDRaisedButton:
            id: delete_button
            text: "Delete"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 1, 0, 0, 1
            text_color: 1, 1, 1, 1
            on_release: root.delete_service()
            disabled: True
            
        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "service"

<Train_screen>:
    name: "train"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "transction"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1


        MDTextField:
            id: t_clint_name
            hint_text: "transction clint name"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        
        MDTextField:
            id: email_train
            hint_text: "transction email"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: date_train
            hint_text: "transction date"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: payment_made
            hint_text: "payment made"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: amount
            hint_text: "amount"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        
        MDTextField:
            id: residual_amount
            hint_text: "residual amount"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        
        

        MDRaisedButton:
            text: "Add transction"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: root.add_train()
        MDRaisedButton:
            text: "VIEW transction"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "v_train"
        MDRaisedButton:
            text: "EDIT transction"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "edit_train"
        MDRaisedButton:
            text: "DELETE transction"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "delete_train"

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "main"

<View_Train_Screen>:
    name: "v_train"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "View transction"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1

        ScrollView:
            size_hint: (1, 1)
            MDBoxLayout:
                id: train_info
                orientation: 'vertical'
                adaptive_height: True
                padding: 10
                spacing: 10

        MDTextField:
            id: search_input
            hint_text: "Enter transction name"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1


        MDRaisedButton:
            text: "Search"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            on_press: root.search_train()
        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "train"

<Edit_Train_Screen>:
    name: "edit_train"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Edit transction"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1
        
        MDTextField:
            id: search_input
            hint_text: "Enter transction name to search"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDRaisedButton:
            text: "Search"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.6, 0.9, 1
            text_color: 1, 1, 1, 1
            on_release: root.search_train()

        MDTextField:
            id: t_clint_name
            hint_text: "transction Name"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: email_train
            hint_text: "transction email"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: date_train
            hint_text: "transction date "
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: payment_made
            hint_text: "payment_made"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: amount
            hint_text: "amount"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        
        MDTextField:
            id: residual_amount
            hint_text: "residual_amount"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDRaisedButton:
            text: "Update"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.4, 0.8, 0.4, 1
            text_color: 1, 1, 1, 1
            on_release: root.update_train()

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.8, 0.2, 0.2, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "train"

<Delete_Train_Screen>:
    name: "delete_train"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Delete transction"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDTextField:
            id: search_input
            hint_text: "Enter transction name to search"
            size_hint_y: None
            height: "30dp"
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        
        MDRaisedButton:
            text: "Search"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: root.search_train()

        MDTextField:
            id: t_clint_name
            hint_text: "transction Name"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: email_train
            hint_text: "transction email"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        MDTextField:
            id: date_train
            hint_text: "date transction"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: payment_made
            hint_text: "payment_made"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: amount
            hint_text: "amount"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        
        MDTextField:
            id: residual_amount
            hint_text: "residual_amount"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDRaisedButton:
            id: delete_button
            text: "Delete"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 1, 0, 0, 1
            text_color: 1, 1, 1, 1
            on_release: root.delete_train()
            disabled: True
            
        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "train"

<Accounts_Screen>:
    name: "accounts"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "accounts"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1


        MDTextField:
            id: freelane_name
            hint_text: "accounts freelane_name "
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1
        

        
        MDTextField:
            id: amount
            hint_text: "amount"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDTextField:
            id: admin_name
            hint_text: "admin_name"
            mode: "rectangle"
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1

        MDRaisedButton:
            id: total_income
            text: "total income"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: root.accounts()   

        MDRaisedButton:
            id: total_out
            text: "total_out"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: root.accounts() 

        MDRaisedButton:
            id: residual
            text: "residual"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: root.accounts()          

        MDRaisedButton:
            text: "Add freelancer"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: root.add_accounts()
        MDRaisedButton:
            text: "VIEW freelancer"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "v_freelancer"
        MDRaisedButton:
            text: "EDIT freelancer"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "edit_freelancer"
        MDRaisedButton:
            text: "DELETE freelancer"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            size_hint_x: 0.5
            on_release: app.root.current = "delete_freelancer"

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "main"

<View_Accounts_Screen>:
    name: "v_freelancer"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "View freelancer"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1

        ScrollView:
            size_hint: (1, 1)
            MDBoxLayout:
                id: accounts_info
                orientation: 'vertical'
                adaptive_height: True
                padding: 10
                spacing: 10

        MDTextField:
            id: search_input
            hint_text: "Enter accounts name"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.6, 0, 1, 1
            text_color_normal: 0.6, 0, 1, 1
            text_color_focus: 0.6, 0, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            line_color_focus: 0.6, 0, 1, 1
            fill_color_normal: 1, 1, 1, 1


        MDRaisedButton:
            text: "Search"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            on_press: root.search_accounts()
        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "accounts"

<Edit_Accounts_Screen>:
    name: "edit_freelancer"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Edit freelancer"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 0.6, 0, 1, 1
        
        MDTextField:
            id: search_input
            hint_text: "Enter freelancer name to search"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDRaisedButton:
            text: "Search"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.6, 0.9, 1
            text_color: 1, 1, 1, 1
            on_release: root.search_accounts()

        MDTextField:
            id: freelane_name
            hint_text: "freelane_name"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: amount
            hint_text: "amount"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: admin_name
            hint_text: "admin_name "
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1


        MDRaisedButton:
            text: "Update"
            size_hint_x: 0.5
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.4, 0.8, 0.4, 1
            text_color: 1, 1, 1, 1
            on_release: root.update_accounts()

        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.8, 0.2, 0.2, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "accounts"

<Delete_Accounts_Screen>:
    name: "delete_freelancer"
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        size_hint: None, None
        size: 400, 600
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0, 0, 0, 1

        MDLabel:
            text: "Delete freelancer"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDTextField:
            id: search_input
            hint_text: "Enter freelancer name to search"
            size_hint_y: None
            height: "30dp"
            pos_hint: {"center_x": 0.5}
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        
        MDRaisedButton:
            text: "Search"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: root.search_accounts()

        MDTextField:
            id: freelane_name
            hint_text: "freelancer Name"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        MDTextField:
            id: amount
            hint_text: "amount"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1
        MDTextField:
            id: admin_name
            hint_text: "admin_name"
            size_hint_y: None
            height: "30dp"
            readonly: True
            hint_text_color_normal: 0.8, 0.8, 0.8, 1
            text_color_normal: 1, 1, 1, 1
            line_color_normal: 0.6, 0, 1, 1
            hint_text_color_focus: 1, 1, 1, 1
            text_color_focus: 1, 1, 1, 1
            line_color_focus: 1, 1, 1, 1

        

        MDRaisedButton:
            id: delete_button
            text: "Delete"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 1, 0, 0, 1
            text_color: 1, 1, 1, 1
            on_release: root.delete_train()
            disabled: True
            
        MDRaisedButton:
            text: "BACK"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.5
            md_bg_color: 0.6, 0, 1, 1
            text_color: 1, 1, 1, 1
            on_release: app.root.current = "accounts"
'''

if __name__ == '__main__':
    MyApp().run()
