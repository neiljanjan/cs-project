import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class DataBase():

    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.logged_user = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            email, password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = line.strip().split(";")
            self.users[email] = (password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level)

        self.file.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date(), '0', '0', '[0]', '0', '0', '0', '-', '-', '-', '-', '0', '100', '1')
            self.save()
            return 1
        else:
            InvalidEmail()
            return -1

    def add_coins(self, increment):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points,exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, (str(increment + int(coins))), current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level)
        self.save()

    def remove_coins(self, increment):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, (str(int(coins) - increment)), current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level)
        self.save()

    def add_characters(self, addCharacters):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, addCharacters, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level)
        self.save()

    def equip_character(self, character):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, str(character), inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level)
        self.save()

    def add_tasks(self, num):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, session_num, (str(int(task_num) + num)), time, task1, task2, task3, task4, exp_points, exp_max, level)
        self.save()

    def add_sessions(self, num):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, (str(int(session_num) + num)), task_num, time, task1, task2, task3, task4, exp_points, exp_max, level)
        self.save()

    def add_time(self, num):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, session_num, task_num, (str(int(time) + num)), task1, task2, task3, task4, exp_points, exp_max, level)
        self.save()

    def add_taskName1(self, taskname):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, session_num, task_num, time, taskname, task2, task3, task4, exp_points, exp_max, level)
        self.save()

    def add_taskName2(self, taskname):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, taskname, task3, task4, exp_points, exp_max, level)
        self.save()

    def add_taskName3(self, taskname):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, taskname, task4, exp_points, exp_max, level)
        self.save()

    def add_taskName4(self, taskname):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, taskname, exp_points, exp_max, level)
        self.save()

    def add_exp(self, increment):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, (str(int(exp_points) + increment)), exp_max, level)
        self.save()

    def reset_exp(self):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, str(0), exp_max, level)
        self.save()

    def add_MaxExp(self, increment):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, (str(int(exp_max) + increment)), level)
        self.save()

    def add_level(self, increment):
        password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level = self.users[self.logged_user]
        self.users[self.logged_user] = (password, name, created, coins, current_outfit, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, (str(int(level) + increment)))
        self.save()

    def validate(self, email, password):
        if self.get_user(email) != -1:
            self.logged_user = email
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ';' + self.users[user][0] + ';' + self.users[user][1] + ';' + self.users[user][2] + ';' + 
                self.users[user][3] + ';' + self.users[user][4] + ';' + self.users[user][5] + ';' + self.users[user][6] + ';' +
                self.users[user][7] + ';' + self.users[user][8] + ';' + self.users[user][9] + ';' + self.users[user][10] +
                ';' + self.users[user][11] + ';' + self.users[user][12] + ';' + self.users[user][13] + ';' + self.users[user][14] + 
                ';' + str(self.users[user][15]) + '\n')
            
    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(' ')[0]

def InvalidEmail():
    pop = Popup(title='Invalid Email',
    content=Label(text='This email already exists'),
    size_hint=(None, None), size=(800, 800))

    pop.open()

