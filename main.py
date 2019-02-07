from fbchat import Client
from fbchat.models import *
import requests
import re
from bs4 import BeautifulSoup
import random as r

from os import environ
from flask import Flask
from haiku import haikufy

#app = Flask(__name__)
#app.run(environ.get('PORT'))



LOGIN=environ.get('LOGIN')
PASSWORD=environ.get('PASSWORD')
THREAD=environ.get('THREAD')
OWNER=environ.get('OWNER')
SPIKER=environ.get('SPIKER')
class CustomClient(Client):
    
    def q_send(self,text):
        self.send(Message(text=text), thread_id=THREAD, thread_type=ThreadType.GROUP)
    def get_spiker(self):
        return "\n\n".join(SPIKER.split(","))
    def get_power(self):
        r=requests.get("https://powerlisting.fandom.com/wiki/special:random")
        soup = BeautifulSoup(r.text, 'html.parser')
        p=soup.p
        h1=soup.h1
        return str(r.url+"\n\n*"+h1.text+"*\n\n"+p.text)


    def get_user_name(self,id):
        return self.fetchUserInfo(id)[id].first_name

    def get_nickname(self,id):
        self.nicknames=client.fetchGroupInfo(THREAD)[THREAD].nicknames
        user=self.nicknames[id]
        return(user)
        #return(f'url{u.url}, first_name{u.first_name}, last_name{u.last_name}, is_friend{u.is_friend}, gender{u.gender}, affinity{u.affinity}, nickname{u.nickname}, own_nickname{u.own_nickname}, color{u.color}, emoji{u.emoji}')
    def get_IQ(self,id):
        prog = re.compile("\d*IQ")
        result = prog.search(self.get_nickname(id))
        return result[0]
    def get_help(self):
        return '''pomoc
!power - wylosuj moc
!IQ [get|set|add|sub] [person?] [amount?]
        '''

    def get_id_from_mention(self,mention):
        try:
            out=mention.thread_id
        except IndexError:
            pass
        return out

    def onMessage(self, message_object, author_id, thread_id, thread_type, **kwargs):
        if(thread_id!=THREAD):
            return True
        haiku=haikufy(message_object.text):
        if(haiku):
            self.q_send(haiku+"-"+self.get_user_name(author_id))
        if(message_object.text.startswith("!close") and author_id==OWNER):
            self.q_send("shutting down :(")
            self.logout()
        if(message_object.text.startswith("!spiker")):
            self.q_send(self.get_spiker())
        if(message_object.text.startswith("good bot")):
            self.q_send(":) <3")
        if(message_object.text.startswith("!help")):
            self.q_send(self.get_help())
        if(message_object.text.startswith("!power")):
            self.q_send(self.get_power())
        if(message_object.text.startswith("!nickname")):
            self.q_send(f'Your nickname:{self.get_nickname(author_id)}')
        if(message_object.text.startswith("!id")):
            self.q_send(f'Your id:{author_id}')
        if(message_object.text.startswith("!coinflip")):
            self.q_send("heads" if r.random()<0.5 else "tails")
        if(message_object.text.startswith("!IQ")):
            
            text=message_object.text.split(" ")
            command=""
            user=""
            points=""
            try:
                command=text[1]
            except IndexError:
                print("no command")
                pass
            try:
                user=text[2]
            except IndexError:
                print("no person")
                pass
            try:
                prog = re.compile("\d+")
                string=" ".join(text[1:])
                result = prog.search(string)
                points=result[0]
            except IndexError:
                print("no points")
                pass
            except TypeError:
                print("no points")
                pass
            
            if(command=="get"):
                self.nicknames=client.fetchGroupInfo(THREAD)[THREAD].nicknames
                if(user != "" and "@" in user):
                    user_id=self.get_id_from_mention(message_object.mentions[0])
                    self.q_send(f'{self.get_user_name(user_id)} has {self.get_IQ(user_id)}')
                else: 
                    self.q_send(f'You have {self.get_IQ(author_id)}')
            if(command=="set"):
                if(user != "" and "@" in user):
                    user_id=self.get_id_from_mention(message_object.mentions[0])
                    nickname=self.get_nickname(user_id)
                    IQ=self.get_IQ(user_id)
                    new_nickname=nickname.replace(IQ,points+"IQ")
                    self.changeNickname(new_nickname, user_id, thread_id=THREAD, thread_type=ThreadType.GROUP)
                else:
                    user_id=author_id
                    nickname=self.get_nickname(user_id)
                    IQ=self.get_IQ(user_id)
                    new_nickname=nickname.replace(IQ,points+"IQ")
                    self.changeNickname(new_nickname, user_id, thread_id=THREAD, thread_type=ThreadType.GROUP)
            if(command=="add"):
                if(user != "" and "@" in user):
                    user_id=self.get_id_from_mention(message_object.mentions[0])
                    nickname=self.get_nickname(user_id)
                    IQ=self.get_IQ(user_id)
                    IQ=int(IQ[:-2])
                    new_nickname=nickname.replace(str(IQ),str(int(points)+IQ))
                    self.changeNickname(new_nickname, user_id, thread_id=THREAD, thread_type=ThreadType.GROUP)
                else:
                    user_id=author_id
                    nickname=self.get_nickname(user_id)
                    IQ=self.get_IQ(user_id)
                    IQ=int(IQ[:-2])
                    new_nickname=nickname.replace(str(IQ),str(int(points)+IQ))
                    self.changeNickname(new_nickname, user_id, thread_id='', thread_type=ThreadType.GROUP)
        pass
        def onMessageDelivered(msg_ids=None, delivered_for=None, thread_id=None, thread_type=ThreadType.GROUP, ts=None, metadata=None, msg=None):
            pass
        def onMessageError(exception=None, msg=None):
            pass 
        def onMessageSeen(seen_by=None, thread_id=None, thread_type=ThreadType.GROUP, seen_ts=None, ts=None, metadata=None, msg=None):
            pass
        def onMessageUnsent(mid=None, author_id=None, thread_id=None, thread_type=None, ts=None, msg=None):
            pass

client = CustomClient(LOGIN, PASSWORD)
client.listen()
client.logout()