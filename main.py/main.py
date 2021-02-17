import time
import kivy
import threading
#Import library
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from database import DataBase 
from kivy.uix.image import Image, AsyncImage
from kivy.clock import Clock
from kivy.animation import Animation

#These are classes imported from different files. Kivy uses object oriented programming.
#Thus, we are able to import classes to make it easier for us to code.


class LogIn(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def LoginButton(self):
        if db.validate(self.email.text, self.password.text):
            WorkMode.current = self.email.text
            Shop.current = self.email.text
            Inventory.current = self.email.text
            Tasks.current = self.email.text
            Analysis.current = self.email.text
            Settings.current = self.email.text
            self.reset()
            sm.current = 'workmode'
        else:
            InvalidLogin()
    
    def CreateButton(self):
        self.reset()
        sm.current = 'createaccount'

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class CreateAccount(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def Submit(self):
        if self.namee.text != '' and self.email.text != '' and self.email.text.count("@") == 1 and self.email.text.count('.') > 0:
            if self.password.text != '':
                db.add_user(self.email.text, self.password.text, self.namee.text)
                self.reset()
                sm.current = "login"
            
            else:
                InvalidForm()
        else:
            InvalidForm()

    def login(self):
        self.reset()
        sm.current = 'login'

    def reset(self):
        self.namee.text = ""
        self.email.text = ''
        self.password.text = ''   

class WorkMode(Screen): 
    secs = ObjectProperty(None)
    secs_out = ObjectProperty(None)
    coins = ObjectProperty(None)
    xp = ObjectProperty(None)
    level = ObjectProperty(None)
    max_xp = ObjectProperty(None)
    current_character = ObjectProperty(None)
    current = ''

    def on_enter(self, *args):
        password, name, created, coinsdb, current_character, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level_num  = db.get_user(self.current)
        self.coins.text = coinsdb
        self.inventory_list = list(map(int, inventory[1:][:-1].split(',')))
        self.equiped_char = int(current_character)
        characters = {
        0: 'character1.1.png',
        1: 'character2.png',
        2: 'character3.png',
        3: 'character4.png',
        4: 'character5.png'
        }
        equipped = characters[self.equiped_char]
        self.ids.equipped_character.source = str(equipped)
        self.xp.text = exp_points
        self.max_xp.text = exp_max
        self.level.text = level_num

    def start_thread(self, sec_text, *args):
        threading.Thread(target=self.CountDown, args=(sec_text)).start()

    def CountDown(self, sec_text, *args):
        Finish = False
        coin = int(self.coins.text)
        level = int(self.level.text)
        xp = int(self.xp.text)
        max_xp = int(self.max_xp.text)

        try:
            seconds = int(self.secs.text)
        except ValueError:
            Invalid_time()
        if Finish == False:
            for i in range(seconds):
                self.secs_out.text = str(seconds)
                seconds = seconds - 1
                time.sleep(1)
                if seconds == 0:
                    Finish = True
                    coin += 10
                    xp += 10
                    if xp >= max_xp:
                        max_xp += 100
                        level += 1
                        db.add_level(1)
                        level_up()
                        xp = 0
                        db.reset_exp()
                        db.add_MaxExp(100)    
                        Finish_session()
                        db.add_time(int(self.secs.text))
                        self.secs.text = ''
                        self.secs_out.text = 'Timer'
                        self.coins.text = str(coin)
                        db.add_coins(10)
                        db.add_sessions(1)
                        self.xp.text = str(xp)
                        self.max_xp.text = str(max_xp)
                        self.level.text = str(level)
                    else:
                        Finish_session()
                        db.add_time(int(self.secs.text))
                        self.secs.text = ''
                        self.secs_out.text = 'Timer'
                        self.coins.text = str(coin)
                        db.add_coins(10)
                        db.add_exp(10)
                        db.add_sessions(1)
                        self.xp.text = str(xp)
                        self.max_xp.text = str(max_xp)
                        self.level.text = str(level)
                else:
                    Finish = False
 
    def logout(self):
        sm.current = 'login'

    def work(self):
        SamePage()

    def shop(self):
        sm.current = 'shop'

    def inventory(self):
        sm.current = 'inventory'

    def tasks(self):
        sm.current = 'tasks'

    def analysis(self):
        sm.current = 'analysis'

    def settings(self):
        sm.current = 'settings'


class Shop(Screen):
    coins = ObjectProperty(None)
    xp = ObjectProperty(None)
    level = ObjectProperty(None)
    max_xp = ObjectProperty(None)
    inventory_list = None
    buy_button1 = ObjectProperty(None)
    buy_button2 = ObjectProperty(None)
    buy_button3 = ObjectProperty(None)
    buy_button4 = ObjectProperty(None)
    equiped_char = None
    
    current = ''

    def on_enter(self, *args):
        password, name, created, coinsdb, current_character, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level_num  = db.get_user(self.current)
        self.coins.text = coinsdb
        self.inventory_list = list(map(int, inventory[1:][:-1].split(',')))
        self.equiped_char = int(current_character)
        self.xp.text = exp_points
        self.max_xp.text = exp_max
        self.level.text = level_num

    def buy1(self):
        if 1 in self.inventory_list:
            character_bought()
            self.buy_button1.text = 'Bought'
        else:
            if int(self.coins.text) >= 100:
                self.coins.text = str(int(self.coins.text) - 100)
                db.remove_coins(100)
                self.inventory_list.append(1)
                db.add_characters(str(self.inventory_list))
                self.buy_button1.text = 'Bought'
            else:
                low_coins()

    def equip1(self):
        if 1 in self.inventory_list:
            db.equip_character(1)
            char_equipped()
        else:
            char_invalid()

    def buy2(self):
        if 2 in self.inventory_list:
            character_bought()
            self.buy_button2.text = 'Bought'
        else:
            if int(self.coins.text) >= 100:
                self.coins.text = str(int(self.coins.text) - 100)
                db.remove_coins(100)
                self.inventory_list.append(2)
                db.add_characters(str(self.inventory_list))
                self.buy_button2.text = 'Bought'
            else:
                low_coins()

    def equip2(self):
        if 2 in self.inventory_list:
            db.equip_character(2)
            char_equipped()
        else:
            char_invalid()

    def buy3(self):
        if 3 in self.inventory_list:
            character_bought()
            self.buy_button3.text = 'Bought' 
        else:
            if int(self.coins.text) >= 100:
                self.coins.text = str(int(self.coins.text) - 100)
                db.remove_coins(100)
                self.inventory_list.append(3)
                db.add_characters(str(self.inventory_list))
                self.buy_button3.text = 'Bought'
            else:
                low_coins()

    def equip3(self):
        if 3 in self.inventory_list:
            db.equip_character(3)
            char_equipped()
        else:
            char_invalid()

    def buy4(self):
        if 4 in self.inventory_list:
            character_bought()
            self.buy_button4.text = 'Bought'
        else:
            if int(self.coins.text) >= 100:
                self.coins.text = str(int(self.coins.text) - 100)
                db.remove_coins(100)
                self.inventory_list.append(4)
                db.add_characters(str(self.inventory_list))
                self.buy_button4.text = 'Bought'
            else:
                low_coins()

    def equip4(self):
        if 4 in self.inventory_list:
            db.equip_character(4)
            char_equipped()
        else:
            char_invalid()

    def equip0(self):
        if 0 in self.inventory_list:
            db.equip_character(0)
            char_equipped()
        else:
            char_invalid()

    def logout(self):
        sm.current = 'login'

    def work(self):
        sm.current = 'workmode'

    def shop(self):
        SamePage()

    def inventory(self):
        sm.current = 'inventory'

    def tasks(self):
        sm.current = 'tasks'

    def analysis(self):
        sm.current = 'analysis'

    def settings(self):
        sm.current = 'settings'

class Inventory(Screen):
    coins = ObjectProperty(None)
    xp = ObjectProperty(None)
    level = ObjectProperty(None)
    max_xp = ObjectProperty(None)
    inventory_list = None

    current = ''

    def on_enter(self, *args):
        password, name, created, coinsdb, current_character, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level_num  = db.get_user(self.current)
        self.coins.text = coinsdb
        self.inventory_list = list(map(int, inventory[1:][:-1].split(',')))
        characters = {
        0: 'character1.1.png',
        '1': 'character2.png',
        '2': 'character3.png',
        '3': 'character4.png',
        '4': 'character5.png'
        }
        self.xp.text = exp_points
        self.max_xp.text = exp_max
        self.level.text = level_num
        #self.character = Image(source=characters[0])
        #self.character.pos_hint('x': 0.3, 'top': 0.5)
        #s = Widget()
        #s.add_widget(self.character)

        #remove the inventory window

    def logout(self):
        sm.current = 'login'

    def work(self):
        sm.current = 'workmode'

    def shop(self):
        sm.current = 'shop'

    def inventory(self):
        SamePage()

    def tasks(self):
        sm.current = 'tasks'

    def analysis(self):
        sm.current = 'analysis'

    def settings(self):
        sm.current = 'settings'

class Tasks(Screen):
    coins = ObjectProperty(None)
    xp = ObjectProperty(None)
    level = ObjectProperty(None)
    max_xp = ObjectProperty(None)
    inventory_list = None
    task_input = ObjectProperty(None)
    task1 = ObjectProperty(None)
    task2 = ObjectProperty(None)
    task3 = ObjectProperty(None)
    task4 = ObjectProperty(None)

    current = ''

    def on_enter(self, *args):
        password, name, created, coinsdb, current_character, inventory, session_num, task_num, time, task1name, task2name, task3name, task4name, exp_points, exp_max, level_num = db.get_user(self.current)
        self.coins.text = coinsdb
        self.inventory_list = list(map(int, inventory[1:][:-1].split(',')))
        self.equiped_char = int(current_character)
        self.task1.text = task1name
        self.task2.text = task2name
        self.task3.text = task3name
        self.task4.text = task4name
        self.xp.text = exp_points
        self.max_xp.text = exp_max
        self.level.text = level_num

    def add_task(self):
        if self.task1.text == '-':
            self.task1.text = self.task_input.text
            db.add_taskName1(self.task1.text)
            self.task_input.text = ''
        elif self.task2.text == '-':
            self.task2.text = self.task_input.text
            db.add_taskName2(self.task2.text)
            self.task_input.text = ''
        elif self.task3.text == '-':
            self.task3.text = self.task_input.text
            db.add_taskName3(self.task3.text)
            self.task_input.text = ''
        elif self.task4.text == '-':
            self.task4.text = self.task_input.text
            db.add_taskName4(self.task4.text)
            self.task_input.text = ''
        else:
            tasks_full()

    def task1_completed(self):
        coin = int(self.coins.text)
        xp = int(self.xp.text)
        max_xp = int(self.max_xp.text)
        level = int(self.level.text)
        task_complete()
        db.add_coins(10)
        coin += 10
        xp += 10
        self.coins.text = str(coin)
        self.task1.text = '-'
        db.add_taskName1(self.task1.text)
        db.add_tasks(1)
        if xp >= max_xp:
            level_up()
            db.reset_exp()
            db.add_MaxExp(100)
            db.add_level(1)
            xp = 0
            level += 1
            max_xp += 100
            self.level.text = str(level)
            self.xp.text = str(xp)
            self.max_xp.text = str(max_xp)
        else:
            db.add_exp(10)
            self.xp.text = str(xp)


    def task2_completed(self):
        coin = int(self.coins.text)
        xp = int(self.xp.text)
        max_xp = int(self.max_xp.text)
        level = int(self.level.text)
        task_complete()
        db.add_coins(10)
        coin += 10
        xp += 10
        self.coins.text = str(coin)
        self.task2.text = '-'
        db.add_taskName2(self.task2.text)
        db.add_tasks(1)
        if xp >= max_xp:
            level_up()
            db.reset_exp()
            db.add_MaxExp(100)
            db.add_level(1)
            xp = 0
            level += 1
            max_xp += 100
            self.level.text = str(level)
            self.xp.text = str(xp)
            self.max_xp.text = str(max_xp)
        else:
            db.add_exp(10)
            self.xp.text = str(xp)

    def task3_completed(self):
        coin = int(self.coins.text)
        xp = int(self.xp.text)
        max_xp = int(self.max_xp.text)
        level = int(self.level.text)
        task_complete()
        db.add_coins(10)
        coin += 10
        xp += 10
        self.coins.text = str(coin)
        self.task3.text = '-'
        db.add_taskName3(self.task3.text)
        db.add_tasks(1)
        if xp >= max_xp:
            level_up()
            db.reset_exp()
            db.add_MaxExp(100)
            db.add_level(1)
            xp = 0
            level += 1
            max_xp += 100
            self.level.text = str(level)
            self.xp.text = str(xp)
            self.max_xp.text = str(max_xp)
        else:
            db.add_exp(10)
            self.xp.text = str(xp)

    def task4_completed(self):
        coin = int(self.coins.text)
        xp = int(self.xp.text)
        max_xp = int(self.max_xp.text)
        level = int(self.level.text)
        task_complete()
        db.add_coins(10)
        coin += 10
        xp += 10
        self.coins.text = str(coin)
        self.task4.text = '-'
        db.add_taskName4(self.task4.text)
        db.add_tasks(1)
        if xp >= max_xp:
            level_up()
            db.reset_exp()
            db.add_MaxExp(100)
            db.add_level(1)
            xp = 0
            level += 1
            max_xp += 100
            self.level.text = str(level)
            self.xp.text = str(xp)
            self.max_xp.text = str(max_xp)
        else:
            db.add_exp(10)
            self.xp.text = str(xp)

    def logout(self):
        sm.current = 'login'

    def work(self):
        sm.current = 'workmode'

    def shop(self):
        sm.current = 'shop'

    def inventory(self):
        sm.current = 'inventory'

    def tasks(self):
        SamePage()

    def analysis(self):
        sm.current = 'analysis'

    def settings(self):
        sm.current = 'settings'

class Analysis(Screen):
    coins = ObjectProperty(None)
    xp = ObjectProperty(None)
    level = ObjectProperty(None)
    max_xp = ObjectProperty(None)
    session_number = ObjectProperty(None)
    time_number = ObjectProperty(None)
    task_number = ObjectProperty(None)

    current = ''

    def on_enter(self, *args):
        password, name, created, coinsdb, current_character, inventory, session_num, task_num, time, task1, task2, task3, task4, exp_points, exp_max, level_num  = db.get_user(self.current)
        self.coins.text = coinsdb
        self.inventory_list = list(map(int, inventory[1:][:-1].split(',')))
        self.equiped_char = int(current_character)
        self.time_number.text = time
        self.session_number.text = session_num
        self.task_number.text = task_num
        self.xp.text = exp_points
        self.max_xp.text = exp_max
        self.level.text = level_num

    def logout(self):
        sm.current = 'login'

    def work(self):
        sm.current = 'workmode'

    def shop(self):
        sm.current = 'shop'

    def inventory(self):
        sm.current = 'inventory'

    def tasks(self):
        sm.current = 'tasks'

    def analysis(self):
        SamePage()

    def settings(self):
        sm.current = 'settings'

class Settings(Screen):

    current = ''

    def logout(self):
        sm.current = 'login'

    def work(self):
        sm.current = 'workmode'

    def shop(self):
        sm.current = 'shop'

    def inventory(self):
        sm.current = 'inventory'

    def tasks(self):
        sm.current = 'tasks'

    def analysis(self):
        sm.current = 'analysis'

    def settings(self):
        SamePage()

class WindowManager(ScreenManager):
    pass



#popups for invalid login or invalid details.
def InvalidLogin():
    pop = Popup(title='Invalid Login',
    content=Label(text='Invalid Username or Password.'),
    size_hint=(None, None), size=(800, 800))

    pop.open()

def InvalidForm():
    pop = Popup(title='Invalid Form',
    content=Label(text='Please fill in the form with valid information'),
    size_hint=(None, None), size=(800, 800))

    pop.open()

def SamePage():
    pop = Popup(title='Already on requested page', 
    content=Label(text='The application is already on the requested page.'),
    size_hint=(None, None), size=(800,800))

    pop.open()

def Finish_session():
    pop = Popup(title='Successful session', 
    content=Label(text='You have completed a session, Well Done! \n You have earned 10 coins and 10 xp points'),
    size_hint=(None, None), size=(800,800))

    pop.open()

def Invalid_time():
    pop = Popup(title='Invalid input',
    content=Label(text='Please input an integer or a valid time.'),
    size_hint=(None,None), size=(800,800))

    pop.open()

def level_up():
    pop = Popup(title='Level Up',
    content=Label(text='Congratulations, you levelled up!'),
    size_hint=(None,None), size=(800,800))

    pop.open()

def character_bought():
    pop = Popup(title="Character already bought",
    content=Label(text="You already own this Character"),
    size_hint=(None,None), size=(800,800))

    pop.open()

def low_coins():
    pop = Popup(title="Insufficient number of coins",
    content=Label(text="You do not have enough coins to buy this \n Do more sessions in order to earn more coins!"),
    size_hint=(None,None), size=(800,800))

    pop.open()

def char_invalid():
    pop = Popup(title="Character not owned",
    content=Label(text="You do not own this character yet \n Please buy it first!"),
    size_hint=(None,None), size=(800,800))

    pop.open()

def char_equipped():
    pop = Popup(title="Character equipped",
    content=Label(text="This character is now equipped!"),
    size_hint=(None,None), size=(800,800))

    pop.open()

def tasks_full():
    pop = Popup(title="Tasks are full",
    content=Label(text="Tasks are full! \n Please complete some tasks to free up some space."),
    size_hint=(None,None), size=(800,800))

    pop.open()

def task_complete():
    pop = Popup(title="Task complete",
    content=Label(text="Well done! You have completed a task. \n You have earned 10 coins and 10 xp points"),
    size_hint=(None,None), size=(800,800))

    pop.open()

kv = Builder.load_file("my.kv") #assigning 'kv' to the kv file 'my.kv'

sm = WindowManager() 
db = DataBase("users.txt") 

screens = [LogIn(name='login'), CreateAccount(name='createaccount'), WorkMode(name='workmode'), Shop(name='shop'), 
Inventory(name='inventory'), Tasks(name='tasks'), Analysis(name='analysis'), Settings(name='settings')] 
#Shows all of the screens that will be managed

for screen in screens:
    sm.add_widget(screen)
sm.current = 'login'
#adds a screen widget and makes the default window the login screen when the app is loaded up.

class MyMainApp(App):
    def build(self):
        return sm
#builds the structure of the app

if __name__ == "__main__":
    MyMainApp().run()
#runs the app