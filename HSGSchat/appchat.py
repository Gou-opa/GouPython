# -*- coding: utf-8 -*-
import datetime, json, random, os, threading, time

EXIT = "exit"
#có thể nhìn qua cấu trúc biến config ở dòng 5, đây là kiểu dữ liệu dạng dictionary khá hay, cho phép lưu nhiều thứ trong 1 biến dưới dạng cấu trúc cây dễ dàng truy cập qua tên các node hoặc duyệt các mảng bên trong
config = {
    "s_prompt_word": "> ",
    "program": {
        "user": {
            "database": {
                "path": "./user.json"
            }
        },
        "chat": {
            "banner": {
                "format": {
                    "username": [
                        "Welcome {} ^-^",
                        "Glad you back, {} !!"
                    ]
                }
            }
        }
    },
    "history": {
        "path": "./history.json"
    },
    "mailboxs": {
        'path': 'mailboxs'
    }
}
MAIN_PROGRAM_PATH = os.path.dirname(os.path.abspath(__file__))
MAILBOXS_PATH = os.path.join(MAIN_PROGRAM_PATH, config['mailboxs']['path'])
if not os.path.exists(MAILBOXS_PATH):
    os.makedirs(MAILBOXS_PATH)

# utilities
def identify(var, tag=None):
    tag_presentation = ""
    if tag:
        tag_presentation = "At {} identify that".format(tag)
    if type(var) is list:
        print(tag_presentation, "Array len", len(var), "is", var)
    else:
        print(tag_presentation, type(var), var)

def get_json_element(dic, *element_maps):
    result = []
    for maps in element_maps:
        if type(maps) is list:
            pointer = dic
            for property in maps:
                pointer = pointer[property]
            element = pointer
        else:
            property = maps
            element = dic[property]
        result.append(element)
    return tuple(result)

# file operators
def tail(file_reader, n, k=0): # open file, seek to last n line, then read k line from that line
    assert n >= 0, "Number of tail lines must be positive integer"
    assert k <= n, "Can't read {} lines form last {} lines".format(k,n)
    k = n if not k else k
    pos, lines = n+1, []
    while len(lines) <= n:
        try:
            file_reader.seek(-pos, 2)
        except IOError:
            file_reader.seek(0)
            break
        finally:
            lines = list(file_reader)
        pos *= 2
    return lines[-n:-(n-k)] if k < n else lines[-n:]


class Message():
    def __init__(self, in_program, from_user, to_user, message):
        # create temp attributes
        self.current_program = in_program
        self.user = from_user
        self.to_user = to_user
        self.content = None
        self.time = datetime.datetime.fromtimestamp(0)
        # assign attreibutes
        if message:
            self.content = message
            self.time = datetime.datetime.utcnow().timestamp()
            self.buildup()
            self.store()
    def __str__(self):
        return self.content
    def buildup(self):
        self.summary = json.dumps({
            "from": self.user.username,
            "from_name" : self.user.name,
            "to": self.to_user.username,
            "to_name" : self.to_user.name,
            "message": self.content,
            "time": self.time
        })
    def store(self):
        self.user.deliver_message(self.summary)
        self.to_user.deliver_message(self.summary)
        
class User():
    def __init__(self, d_user_data):
        self.name = d_user_data['name']
        self.username = d_user_data['username']
        self.role = d_user_data['role']
        self.mailbox = os.path.join(MAILBOXS_PATH,d_user_data['mailbox'])
        self.test_mailbox()
        
    def test_mailbox(self):
        mode = 'a' if os.path.exists(self.mailbox) else 'w'
        open(self.mailbox, mode).close()
    def deliver_message(self, summary_json_dumped):
        mode = 'a' if os.path.exists(self.mailbox) else 'w'
        with open(self.mailbox, mode) as mailbox_writer:
            mailbox_writer.writelines([summary_json_dumped + "\n"])
class UserManager():
    def __init__(self):
        self.all_user = {}
        self.all_user_name = {}
        self.load_users()
    def load_users(self):
        with open(config['program']['user']['database']['path'], 'r') as user_database:
            self.all_user = json.load(user_database)['lauchat']
            self.all_user_name = [
                list(get_json_element(user, ['username'], ['data', 'name'], ['data', 'mailbox'], ['data', 'role']))
                for user in self.all_user
            ]
    def find_friend(self, name):
        for user in self.all_user_name:
            if name == user[0] or name == user[1]:
                return {"username": user[0], "name": user[1], 'mailbox': user[2], 'role': user[3]}
        return None
    def authenticate(self, username, password):
        self.load_users()
        for user in self.all_user:
            usern, passwd, userdata = get_json_element(user, ['username'], ['password'], ['data'])
            if usern == username and password == passwd:
                userdata['username'] = usern
                return User(userdata)
            else:
                continue
        return False

class Program():
    def __init__(self):
        self.Commands = {
            "exit": {
                "do": self.set_exit,
                "description": "Exit app"
            },
            "commands": {
                "do": self.print_commands,
                "description": "Print this help"
            },
            "help": {
                "do": self.print_commands,
                "description": "Print this help"
            }
        }
        self.current_program = Program
        self.exit_signal = False
        self.run()
    def print_commands(self):
        print("\n{} commands\n".format(self.__class__.__name__)+
              "\n".join(["{}: {}".format(command,command_info['description']) for command, command_info in self.Commands.items()])+
              "\n")
        return False
    def set_exit(self):
        self.exit_signal = True
        return True
    def get_keyboard_input(self, prompt):
        message = input(prompt)
        #print(message in self.Commands, self.Commands)
        if message in self.Commands:
            command = message
            action = self.Commands[command]['do']
            return action()
        else:
            return message
    def run(self):
        while not self.exit_signal:
            self.user_manager = UserManager()
            authenticated = False
            while not authenticated:
                print("Login")
                username = self.get_keyboard_input("Username: ")
                #print("exit signal", self.exit_signal)
                if not self.exit_signal:
                    if username:
                        authenticated = self.user_manager.authenticate(username, input("Password: "))
                        if not authenticated:
                            print("Wrong user credentials, retry another.\n")
                else:
                    break
            if not self.exit_signal:
                self.session = Chat( authenticated, self.user_manager)
                program_exit_code = self.session.run()
                if program_exit_code == "close":
                    break
        
    @staticmethod
    def notification_agent(program_chat):
        print("Enable notification for {}".format(program_chat.user.name))
        last_message = {}
        while not program_chat.is_logout and not program_chat.exit_signal:
            with open(program_chat.user.mailbox, 'r') as mailbox_reader:
                last_lines = tail(mailbox_reader, 1)
                if len(last_lines): # history exsist
                    # print(last_lines)
                    new_message = json.loads(last_lines[0])
                    if new_message['from'] != program_chat.user.username and new_message != last_message:
                        last_message = new_message
                        Chat.print_history_message(new_message)
                else: # new mailbox, no history
                    pass # dont do anything
            time.sleep(1)
        print("Close notification for", program_chat.user.name)
        return 0 # return to close thread after logout
class Chat(Program):
    @staticmethod
    def print_history_message(message):
        print("[{}:{}]>{}".format(datetime.datetime.fromtimestamp(message['time']), message['from_name'], message['message']))
    def __init__(self, user, usermgr):
        self.Commands = {
            "logout": {
                "do": self.set_logout,
                "description": "Logout for new session."
            },
            "exit": {
                "do": self.set_exit,
                "description": "Exit app."
            },
            "send to": {
                "do": self.set_destination,
                "description": "Set receiver."
            },
            "commands": {
                "do": self.print_commands,
                "description": "Print this help"
            },
            "help": {
                "do": self.print_commands,
                "description": "Print this help"
            },
            "history": {
                "do": self.load_history,
                "description": "Read history on conversation"
            }, 
            "reply": {
                "do": self.reply,
                "description": "Reply last sent message"
            }, 
        }
        self.usermgr = usermgr
        self.user = user
        self.current_program = Chat
        self.exit_signal = False
        self.is_logout = False
        self.destination_user = None
    
    def load_history(self):
        n_load = max(int(input("History length: ")), 1)
        history = []
        n = 0
        with open(self.user.mailbox, 'r') as my_mailbox_reader:
            all_mails = my_mailbox_reader.readlines()
            all_mails.reverse()
            for line in all_mails:
                message = json.loads(line)
                if [self.user.name, self.destination_user.name].sort() == [message['from'], message['to']].sort():
                    history.append(message)
                    n += 1
                if n == n_load:
                    break
            history.reverse()
            for message in history:
                Chat.print_history_message(message)
    def reply(self):
        with open(self.user.mailbox, 'r') as my_mailbox_reader:
            l_last_mail = tail(my_mailbox_reader, 1)
            if l_last_mail:
                last_message = json.loads(l_last_mail[0])
                to_user = last_message['from'] if last_message['from'] != self.user.username else last_message['to']
                self.set_destination(to_user)
            else:
                print("No previous message to reply")
        
    def set_destination(self, to_user=None):
        to_user = input("Send to: ") if not to_user else to_user
        result = self.usermgr.find_friend(to_user)
        if result:
            self.destination_user = User(result)
            if self.destination_user.name == self.user.name:
                print("To yourself\n")
            else:
                print("To {}\n".format(to_user))
        else:
            print(to_user, 'not found')
    def set_logout(self):
        self.is_logout = True
        self.exit_signal = True
    def show_banner(self):
        all_banners = config['program']['chat']['banner']['format']['username']
        banner = random.choice(all_banners)
        print(banner.format(self.user.name) + '\n')
    def run(self):
        self.show_banner()
        noti_thread = threading.Thread(target=Program.notification_agent, args=(self,))
        noti_thread.start()
        noti_thread.join(0)
        self.set_destination(self.user.username)
        while not self.exit_signal:
            content = self.get_keyboard_input(config['s_prompt_word'])
            if self.exit_signal:
                continue
            else:
                Message(self, self.user, self.destination_user, content)
        print("Bye {}.\n".format(self.user.name))
        return "logout" if self.is_logout else "close"
    

# main app here
if __name__ == "__main__":
    Program()
