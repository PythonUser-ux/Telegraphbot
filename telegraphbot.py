import telebot
from telebot import types
import os
import re

telebot.apihelper.SESSION_TIME_TO_LIVE = 10 #5 *60

# files directory is the same of the .py file
os.chdir(os.path.dirname(__file__))

class BOT:
    def __init__(self, name, token, allowed=[], directory=None, other_commands=[]):
        self.name=name
        self.token=token
        self.allowed=allowed
        self.directory=directory
        self.other_commands=other_commands

        self._deep_degree=0
        self._conversation=[]
        self._start=False

        self.presentation=None
        self.start_markup=None
        self.start_markup_rows=[[]]
        self.init_message=None

        self.steps=[]
        self._bot=telebot.TeleBot(self.token, parse_mode = None)

        # the default directory is that of the source code
        if directory!=None:
            os.chdir(directory)

    def chat_step(self,order,message,question,answers,actions,unrecognized,next_steps=[]):
        if question!=None and self._deep_degree<order:
            self._bot.send_message(message.chat.id,question)
        if self._deep_degree==order:
            if message.text!=None:
                self._conversation.append(message.text)
            elif message.caption!=None:
                self._conversation.append(message.caption)
            else:
                self._conversation.append("__"+message.content_type+"__")


            # SAVING FILES

            if message.content_type=="photo":
                file_info = self._bot.get_file(message.photo[0].file_id)
                downloaded_file = self._bot.download_file(file_info.file_path)
                name_file="image.jpg"
                caption=message.caption
                if caption!=None:
                    name_file=caption+".jpg"
                with open(name_file, 'wb') as new_file:
                    new_file.write(downloaded_file)

            elif message.content_type=="voice":
                file_info = self._bot.get_file(message.voice.file_id)
                downloaded_file = self._bot.download_file(file_info.file_path)
                with open('new_file.ogg', 'wb') as new_file:
                    new_file.write(downloaded_file)

            elif message.content_type=="video":
                file_info = self._bot.get_file(message.video.file_id)
                downloaded_file = self._bot.download_file(file_info.file_path)
                with open('new_file.mp4', 'wb') as new_file:
                    new_file.write(downloaded_file)

            elif message.content_type=="audio":
                file_info = self._bot.get_file(message.audio.file_id)
                downloaded_file = self._bot.download_file(file_info.file_path)
                with open('new_file.m4a', 'wb') as new_file:
                    new_file.write(downloaded_file)

            elif message.content_type=="document":
                file_info = self._bot.get_file(message.document.file_id)
                downloaded_file = self._bot.download_file(file_info.file_path)
                with open('new_file.pdf', 'wb') as new_file:
                    new_file.write(downloaded_file)


        words=len(self._conversation)
        if words>order:
            for num, answer in enumerate(answers):
                    input=self._conversation[order]
                    if input==answer or re.fullmatch(answer, input):
                        if self._deep_degree==order:
                            actions[num](message)              # execute the action if active==True, otherwise it just returns the next step
                        if next_steps!=[]:
                            if next_steps[num]!=None:
                                next_steps[num](message)
                        return
            unrecognized(message)
            return
        return

        """
        order: degree of depth of the chat_step
        message: current user input
        question: message showed to the user at the beginning of the chat_step
        answers: ordered list of proper answers              Hint: it is possible to use Regex!
        actions: ordered list of the functions corresponding to the proper answers 
        unrecognized: default reply to non proper answers
        next_steps: list of all the sons of the chat_step
        """

    def lazy(self, message):
        pass

    def reset(self):                   # once called you need to start your bot again
        self._start=False
    
    def soft_reset(self):              # go back to the root node
        self._conversation=[]
        self._deep_degree=-1

    def unrecognized(self, message):
        self._bot.send_message(message.chat.id,"Unrecognized")
        self._conversation.pop()
        self._deep_degree-=1

    def keyboard_format(self, buttons=None):
        global markup
        if buttons!=None:
            for row in buttons:
                    row_btns=[]
                    for btn in row:
                        row_btns.append(types.KeyboardButton(btn))
                    markup.row(*row_btns)

    def polling(self):
        @self._bot.message_handler(commands=['start']+[command.name for command in self.other_commands])
        def commands_effects(message):
            if message.text=='/start':
                if (message.chat.id in self.allowed) or self.allowed==[]:
                    self._start=True
                    self._deep_degree=0
                    self._conversation=[]

                    if self.start_markup!=None:                 # for keyboard buttons
                        global markup
                        markup = types.ReplyKeyboardMarkup()
                        markup.add(*self.start_markup)
                        self.keyboard_format(self.start_markup_rows)
                    if self.presentation!=None:
                        self._bot.send_message(message.chat.id, self.presentation, reply_markup=markup)
                    if self.init_message!=None:
                        self._bot.send_message(message.chat.id, self.init_message)
            else:
                for command in self.other_commands:
                    if message.text == ('/'+command.name):
                        command.effect(message)
                        break



        @self._bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text'])
        def main_sender(message):
            if ((message.chat.id in self.allowed) or self.allowed==[]) and self._start:
                self.steps[0](message)
                self._deep_degree+=1
        self._bot.infinity_polling()

class Command:
    def __init__(self, name, effect):
        self.name=name
        self.effect=effect