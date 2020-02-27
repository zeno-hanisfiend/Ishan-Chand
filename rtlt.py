from tkinter import *
from tkinter import ttk
import pickle


class Help(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.old_frame = None
        self.configure(bg='black')
        self.switch_frame(LoginPage)

    def switch_frame(self, frame):
        new_frame = frame(self)
        if self.old_frame is not None:
            self.old_frame.destroy()
        self.old_frame = new_frame
        self.old_frame.grid()


class LoginPage(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)
        self.window = window
        self.window.geometry("505x250+350+80")
        self.window.configure(bg='white')
        self.configure(bg='white')
         # Creating labels for login page
        self.lb_login_page = Label(self, text='User Login ', font='arial', fg='purple', bg='white')
        self.lb_user = Label(self, text='Username', font='arial', bg='white')
        self.lb_pass = Label(self, text='Password', font='arial', bg='white')
        # Using grid geometry manager to insert label in the window.
        self.lb_login_page.grid(row=0, column=0)
        self.lb_user.grid(row=1, column=0)
        self.lb_pass.grid(row=2, column=0)
        # Creating Entry boxes
        self.ent_username = Entry(self)
        self.ent_password = Entry(self, show='*')
        # Using grid geometry manager to insert entry box in the window.
        self.ent_username.grid(row=1, column=1)
        self.ent_password.grid(row=2, column=1)
        # Creating Buttons
        self.btn_login = Button(self, text='Login', command=self.login)
        self.btn_register = Button(self, text='Register', command=lambda: window.switch_frame(RegisterPage))
        # Using grid geometry manager to insert button in the window.
        self.btn_login.grid(row=3, column=1)
        self.btn_register.grid(row=3, column=3)
        self.lb_status = Label(self, text='', bg='white', font='arial')
        self.lb_status.grid(row=4, column=0)

    def login(self):
        try:
            file = open('user.pkl', 'rb')
            user_file_data = pickle.load(file)
            file.close()

            username = self.ent_username.get()
            password = self.ent_password.get()

            if user_file_data.get(username, 0) == 0:
                self.lb_status.configure(text='Invalid username or password')
                return

            if user_file_data[username]['password'] != password:
                self.lb_status.configure(text='Invalid username or password')
                return
            self.reset()
            self.window.switch_frame(DashboardPage)

        except FileNotFoundError:
            file = open('user.pkl', 'wb')
            pickle.dump({}, file)
            file.close()

    def reset(self):
        self.ent_username.delete(0, 'end')
        self.ent_password.delete(0, 'end')


class RegisterPage(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)
        self.window = window
        self.window.geometry("600x300")
        self.window.configure(bg='white')
        self.configure(bg='white')
        # Creating Labels of Register page
        self.lb_fname = Label(self, text='First Name', bg='white', font='arial')
        self.lb_lname = Label(self, text='Last Name', bg='white', font='arial')
        self.lb_number = Label(self, text='Mobile number', bg='white', font='arial')
        self.lb_email = Label(self, text='Username', bg='white', font='arial')
        self.lb_new_password = Label(self, text='New Password', bg='white', font='arial')
        self.lb_confirm_new = Label(self, text='Confirm Password', bg='white', font='arial')
        self.lb_fname.grid(row=0, column=0)
        self.lb_lname.grid(row=1, column=0)
        self.lb_number.grid(row=2, column=0)
        self.lb_email.grid(row=3, column=0)
        self.lb_new_password.grid(row=4, column=0)
        self.lb_confirm_new.grid(row=5, column=0)
        # Entry of register
        self.ent_fname = Entry(self)
        self.ent_lname = Entry(self)
        self.ent_number = Entry(self)
        self.ent_email = Entry(self)
        self.ent_new_password = Entry(self, show='*')
        self.ent_confirm_new = Entry(self, show='*')
        self.ent_fname.grid(row=0, column=1)
        self.ent_lname.grid(row=1, column=1)
        self.ent_number.grid(row=2, column=1)
        self.ent_email.grid(row=3, column=1)
        self.ent_new_password.grid(row=4, column=1)
        self.ent_confirm_new.grid(row=5, column=1)
        # Creating Buttons
        self.btn_reset = Button(self, text='Reset', command=self.reset)
        self.btn_back_to_login = Button(self, text='Back', command=lambda: window.switch_frame(LoginPage))
        self.btn_summit = Button(self, text='Summit', command=self.summit)
        # Using grid geometry manager to insert button in the window.
        self.btn_reset.grid(row=6, column=0)
        self.btn_back_to_login.grid(row=6, column=1)
        self.btn_summit.grid(row=6, column=2)
        self.lb_status = Label(self, text='', bg='white', font='arial')
        self.lb_status.grid(row=7, column=0)

    def summit(self):
        try:
            file = open('user.pkl', 'rb')
            user_file_data = pickle.load(file)
            file.close()

            if self.ent_fname.get() == '' or self.ent_lname.get() == '' or self.ent_email.get() == '' \
                    or self.ent_number.get() == '' or self.ent_new_password.get() == '':
                self.lb_status.configure(text='Fill all boxes')
                return
            elif self.ent_new_password.get() != self.ent_confirm_new.get():
                self.lb_status.configure(text='Password match.')
                return

            elif not self.ent_number.get().isdigit() and 8 < len(self.ent_number.get()) < 14:
                self.lb_status.configure(text='Number must contain (8-13)digits.')
                return

            user_data = {'firstname': self.ent_fname.get(), 'lastname': self.ent_lname.get(),
                         'password': self.ent_new_password.get(), 'number': self.ent_number.get()}

            email = self.ent_email.get()
            if user_file_data.get(email, 0) != 0:
                self.lb_status.configure(text='User exists. Use another username.')
                return

            self.lb_status.configure(text='')
            user_file_data[email] = user_data

            file = open('user.pkl', 'wb')
            pickle.dump(user_file_data, file)
            file.close()

            self.reset()
            self.lb_status.configure(text='Account created successfully.')

        except FileNotFoundError:
            file = open('user.pkl', 'wb')
            pickle.dump({}, file)
            file.close()

    def reset(self):
        self.ent_fname.delete(0, 'end')
        self.ent_lname.delete(0, 'end')
        self.ent_number.delete(0, 'end')
        self.ent_email.delete(0, 'end')
        self.ent_new_password.delete(0, 'end')
        self.ent_confirm_new.delete(0, 'end')


class DashboardPage(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)
        self.window = window
        self.window.geometry("500x250")
        self.window.configure(bg='white')
        self.configure(bg='white')

        # label
        self.lb_dashboard = Label(self, text='Dash Board', bg='white', font='arial')
        self.lb_dashboard.grid(row=0, column=0)

        # Creating Buttons
        self.btn_employee_form = Button(self, text='Employee form', command=lambda: window.switch_frame(EmployeePage))
        self.btn_department_form = Button(self, text='Department form',
                                          command=lambda: window.switch_frame(DepartmentPage))
        self.btn_logout = Button(self, text='Log Out', command=lambda: window.switch_frame(LoginPage))

        # Using grid geometry manager to insert button in the window.
        self.btn_employee_form.grid(row=1, column=0, padx=10, pady=10)
        self.btn_department_form.grid(row=1, column=1, padx=10, pady=10)
        self.btn_logout.grid(row=1, column=2, padx=10, pady=10)


class DepartmentPage(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)
        self.window = window
        self.window.geometry("500x420")
        self.window.configure(bg='white')
        self.configure(bg='white')

        self.upper_frame = Frame(self, bg='white')
        self.upper_frame = Frame(self, bg='white')
        self.lower_frame = Frame(self, width=400, height=304, bg='white')
        self.lower_frame.pack_propagate(0)

        self.upper_frame.pack(side=TOP)
        self.lower_frame.pack(side=BOTTOM)

        # Labels
        self.lb_depart_id = Label(self.upper_frame, text='Department Id', bg='white', font='arial')
        self.lb_depart_name = Label(self.upper_frame, text='Department Name', bg='white', font='arial')

        self.lb_depart_id.grid(row=0, column=0)
        self.lb_depart_name.grid(row=1, column=0)

        # Entries
        self.ent_depart_id = Entry(self.upper_frame)
        self.ent_depart_name = Entry(self.upper_frame)

        self.ent_depart_id.grid(row=0, column=1)
        self.ent_depart_name.grid(row=1, column=1)

        # Creating Buttons
        self.btn_add_depart = Button(self.upper_frame, text='Add department', command=self.add_department)
        self.btn_reset = Button(self.upper_frame, text='Reset', command=self.reset)
        self.btn_go_to_dashboard = Button(self.upper_frame, text='Back',
                                          command=lambda: window.switch_frame(DashboardPage))

        # Using grid geometry manager to insert button in the window.
        self.btn_reset.grid(row=2, column=0, padx=10, pady=10)
        self.btn_add_depart.grid(row=2, column=1, padx=10, pady=10)
        self.btn_go_to_dashboard.grid(row=2, column=2, padx=10, pady=10)

        self.lb_status = Label(self.upper_frame, text='', bg='white', font='arial')
        self.lb_status.grid(row=4, column=0)

        self.scrollbar_x = Scrollbar(self.lower_frame, orient=HORIZONTAL)
        self.scrollbar_y = Scrollbar(self.lower_frame, orient=VERTICAL)

        self.depart_table = ttk.Treeview(self.lower_frame, columns=('depart_id', 'depart_name'), height=13,
                                         xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x.pack(side=BOTTOM, fill=X)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.depart_table.place(x=0, y=0)

        self.depart_table.column('depart_id', width=190)
        self.depart_table.column('depart_name', width=190)

        self.depart_table.heading('depart_id', text='Department ID')
        self.depart_table.heading('depart_name', text='Department Name')

        self.depart_table['show'] = 'headings'

        self.scrollbar_x.configure(command=self.depart_table.xview)
        self.scrollbar_y.configure(command=self.depart_table.yview)

        self.show_department()

    def show_department(self):
        self.depart_table.delete(*self.depart_table.get_children())

        try:
            file = open('department_data.pkl', 'rb')
            department_data = pickle.load(file)
            file.close()

            department = []
            for key in department_data:
                department.append((key, department_data[key]))

            for data in department:
                self.depart_table.insert('', 'end', values=data)

        except FileNotFoundError:
            file = open('department_data.pkl', 'wb')
            pickle.dump({}, file)
            file.close()

    def add_department(self):
        try:
            file = open('department_data.pkl', 'rb')
            department_data = pickle.load(file)
            file.close()

            department_id = self.ent_depart_id.get()
            department_name = self.ent_depart_name.get()

            if department_id == '' or department_name == '':
                self.lb_status.configure(text='Fill all the entries')
                return

            elif department_data.get(department_id, 0) != 0:
                self.lb_status.configure(text='The department id already exists')
                return
            elif department_name in department_data.values():
                self.lb_status.configure(text='The department name already exists')
                return

            department_data.setdefault(department_id, department_name)

            file = open('department_data.pkl', 'wb')
            pickle.dump(department_data, file)
            file.close()

            self.reset()
            self.lb_status.configure(text='The department is added successfully.')

            self.show_department()

        except FileNotFoundError:
            file = open('department_data.pkl', 'wb')
            pickle.dump({}, file)
            file.close()

    def reset(self):
        self.ent_depart_id.delete(0, 'end')
        self.ent_depart_name.delete(0, 'end')


class EmployeePage(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)
        self.window = window
        self.window.geometry("800x400")
        self.window.configure(bg='white')
        self.configure(bg='white')

        self.upper_frame = Frame(self, bg='white')
        self.lower_frame = Frame(self, width=670, height=245, bg='white')
        self.lower_frame.pack_propagate(0)

        self.upper_frame.pack(side=TOP)
        self.lower_frame.pack(side=BOTTOM)

        self.lb_id = Label(self.upper_frame, text='Id', bg='white', font='arial')
        self.lb_fname = Label(self.upper_frame, text='First Name', bg='white', font='arial')
        self.lb_lname = Label(self.upper_frame, text='Last Name', bg='white', font='arial')
        self.lb_age = Label(self.upper_frame, text='Age', bg='white', font='arial')
        self.lb_number = Label(self.upper_frame, text='Mobile number', bg='white', font='arial')
        self.lb_address = Label(self.upper_frame, text='Address', bg='white', font='arial')

        self.lb_id.grid(row=1, column=0)
        self.lb_fname.grid(row=2, column=0)
        self.lb_lname.grid(row=3, column=0)
        self.lb_age.grid(row=4, column=0)
        self.lb_number.grid(row=5, column=0)
        self.lb_address.grid(row=6, column=0)

        self.ent_id = Entry(self.upper_frame)
        self.ent_fname = Entry(self.upper_frame)
        self.ent_lname = Entry(self.upper_frame)
        self.ent_age = Entry(self.upper_frame)
        self.ent_number = Entry(self.upper_frame)
        self.ent_address = Entry(self.upper_frame)

        self.ent_id.grid(row=1, column=1)
        self.ent_fname.grid(row=2, column=1)
        self.ent_lname.grid(row=3, column=1)
        self.ent_age.grid(row=4, column=1)
        self.ent_number.grid(row=5, column=1)
        self.ent_address.grid(row=6, column=1)

        self.scrollbar_x = Scrollbar(self.lower_frame, orient=HORIZONTAL)
        self.scrollbar_y = Scrollbar(self.lower_frame, orient=VERTICAL)

        self.employee_table = ttk.Treeview(self.lower_frame, columns=('id', 'firstname', 'lastname', 'age', 'number',
                                                                      'address', 'department'),
                                           xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x.pack(side=BOTTOM, fill=X)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.employee_table.place(x=0, y=0)

        self.employee_table.column('id', width=50)
        self.employee_table.column('firstname', width=100)
        self.employee_table.column('lastname', width=100)
        self.employee_table.column('age', width=100)
        self.employee_table.column('number', width=100)
        self.employee_table.column('address', width=100)
        self.employee_table.column('department', width=100)

        self.employee_table.heading('id', text='ID')
        self.employee_table.heading('firstname', text='First Name')
        self.employee_table.heading('lastname', text='Last Name')
        self.employee_table.heading('age', text='Age')
        self.employee_table.heading('number', text='Number')
        self.employee_table.heading('address', text='Address')
        self.employee_table.heading('department', text='Department')

        self.employee_table['show'] = 'headings'

        self.scrollbar_x.configure(command=self.employee_table.xview)
        self.scrollbar_y.configure(command=self.employee_table.yview)

        try:
            file = open('department_data.pkl', 'rb')
            department_data = pickle.load(file)
            file.close()

        except FileNotFoundError:
            file = open('department_data.pkl', 'wb')
            pickle.dump({}, file)
            file.close()

            file = open('department_data.pkl', 'rb')
            department_data = pickle.load(file)
            file.close()

        self.options = ['']
        for value in department_data.values():
            self.options.append(value)

        self.lb_choose_depart = Label(self.upper_frame, text='Choose department', bg='white', font='arial')
        self.lb_choose_depart.grid(row=7, column=0)

        # Options menu
        self.department = StringVar()
        self.department.set('None')
        self.options_department = OptionMenu(self.upper_frame, self.department, *self.options)
        self.options_department.grid(row=7, column=1)

        # Creating Buttons
        self.btn_add = Button(self.upper_frame, text='Add employee', command=self.add_employee)
        self.btn_reset = Button(self.upper_frame, text='Reset', command=self.reset)
        self.btn_back_to_dashboard = Button(self.upper_frame, text='Back',
                                            command=lambda: window.switch_frame(DashboardPage))

        # Using grid geometry manager to insert button in the window.
        self.btn_reset.grid(row=8, column=0, padx=10, pady=10)
        self.btn_add.grid(row=8, column=1, padx=10, pady=10)
        self.btn_back_to_dashboard.grid(row=8, column=2, padx=10, pady=10)

        self.lb_status = Label(self.upper_frame, text='', bg='white', font='arial')
        self.lb_status.grid(row=9, column=0)
        self.show_employee()

    def show_employee(self):
        self.employee_table.delete(*self.employee_table.get_children())

        try:
            file = open('employee_info.pkl', 'rb')
            employee_info = pickle.load(file)
            file.close()

            employee_list = []
            for key in employee_info:
                employee_list.append((key, employee_info[key]['firstname'],
                                      employee_info[key]['lastname'],
                                      employee_info[key]['age'],
                                      employee_info[key]['number'],
                                      employee_info[key]['address'],
                                      employee_info[key]['department']))

            for data in employee_list:
                self.employee_table.insert('', 'end', values=data)

        except FileNotFoundError:
            file = open('employee_info.pkl', 'wb')
            pickle.dump({}, file)
            file.close()

    def add_employee(self):
        try:
            file = open('employee_info.pkl', 'rb')
            employee_info = pickle.load(file)
            file.close()

            if self.ent_fname.get() == '' or self.ent_lname.get() == '' or \
                    self.ent_age.get() == '' or self.ent_number.get() == '' or self.ent_address.get() == '':
                self.lb_status.configure(text='Fill all the entries')
                return

            elif self.department.get() == 'None' or self.department.get() == '':
                self.lb_status.configure(text='Select department')
                return

            elif not self.ent_age.get().isdigit():
                self.lb_status.configure(text='Age must be number')
                return

            elif int(self.ent_age.get()) > 110:
                self.lb_status.configure(text='Age should be < 110')
                return

            elif not self.ent_number.get().isdigit() and 8 < len(self.ent_number.get()) < 14:
                self.lb_status.configure(text='Contact should contain (8-13)digit.')
                return

            employee_id = self.ent_id.get()
            employee_dict = {'firstname': self.ent_fname.get(),
                             'lastname': self.ent_lname.get(),
                             'age': self.ent_age.get(),
                             'number': self.ent_number.get(),
                             'address': self.ent_address.get(),
                             'department': self.department.get()}

            if employee_info.get(employee_id, 0) != 0:
                self.lb_status.configure(text='The employee already exists.')
                return

            employee_info[employee_id] = employee_dict

            file = open('employee_info.pkl', 'wb')
            pickle.dump(employee_info, file)
            file.close()

            self.reset()
            self.lb_status.configure(text='The employee is added successfully.')
            self.show_employee()

        except FileNotFoundError:
            file = open('employee_info.pkl', 'wb')
            pickle.dump({}, file)
            file.close()

    def reset(self):
        self.ent_id.delete(0, 'end')
        self.ent_fname.delete(0, 'end')
        self.ent_lname.delete(0, 'end')
        self.ent_age.delete(0, 'end')
        self.ent_number.delete(0, 'end')
        self.ent_address.delete(0, 'end')


application = Help()
application.mainloop()