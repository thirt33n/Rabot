import discord
import os
import requests
import json
import random
from replit import db
from stay_awake import stay_awake


client = discord.Client()

hi_words = ['*hi','*hello','*Hi','*Hello','*hey','*Hey','*yo','*Yo','*wassup']            #the greetings

Reminders=[]                                                  #the reminders list

hi_resp =['Hiya','How are you','What do you want?','You are a simp','Hey!','Whatup','Imma busy rn']   #rabot replies

rep_words = ['fine','good','bad','great',"awesome"]                                             #other user words


reply_1 = ["That's great!",                                                    #Rabt's words 
"Hope it is that way",
"That's good but don't you have other things to do? ",
"All right!"
"Okay"
]

def addition(Reminders):                                                       #reminder additions
  if "add" in db.keys():
    add = db["add"]
    add.append(Reminders)
    db["add"] = add
  else:
    db["add"] = [add]


def simprate(name):
  s=name +" is "+str(random.randint(0,100))+"% simp"
  return s
  


def deletion(i):                                                               #reminder delete
  add = db["add"]
  if len(add) > i:
    del add[i]
  db["add"] = add
  



def get_inspired():                                                         #api call
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  inspire = json_data[0]['q']
  return (inspire)

def dad_jokes():
  resp = requests.get("https://icanhazdadjoke.com/slack")
  #resp = requests.get("https://us-central1-dadsofunny.cloudfunctions.net/DadJokes")
  json_dd = json.loads(resp.text)
  joke = json_dd['attachments'][0]['fallback']
  return (joke) 

def insults():
  get = requests.get("https://insult.mattbas.org/api/en/insult.json")
  json_return = json.loads(get.text)
  insult = json_return['insult']
  return(insult)

@client.event
async def on_ready():
  print("On the field as {0.user}"
  .format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return
  options = Reminders
  if "add" in db.keys():
    options = options + db["add"]

  #if any(word in message.content for word in Reminders):                                  #bunch of 
   # await message.channel.send(random.choice(options))

  if message.content.startswith('*inspire'):
    inspire = get_inspired()
    await message.channel.send(inspire) 
  
  if message.content.startswith('*joke'):
    haha = dad_jokes()
    await message.channel.send(haha)

  if message.content.startswith('*bye'):
    await message.channel.send('So long Sucker')

  if any(word in message.content for word in hi_words):
    await message.channel.send(random.choice(hi_resp))

  if (message.content == "*tell"):
    await message.channel.send(random.choice(options))
  
  if(message.content == "*tell all"):
    for option in options:
      k=option
      await message.channel.send((k))

  if any(word in message.content for word in rep_words):
    await message.channel.send(random.choice(reply_1))
  
  

  if ( message.content == "siddharth"):
    await message.channel.send("The boss")

  if (message.content == "*thanks"):
    await message.channel.send("Welcome")

  if(message.content == "*help"):
    await message.channel.send('\t\tRABOT HERE \nUse the * before a random greeting like Hi or hello to talk to me\n\nUse *inspire to make me give some advice for your worthless lives\n Use *remind + <text>  to save any message of your choice\n Use *tell to view one of your saved messages and *tell all to view all of your saved messages \n Use *clear + index of the text you want to delete to clear it\nUse *simp and mention someone to know how simp they are(I know I copy from other bots)\n Use *insult for insults and *joke for jokes(duh)!\n \n\n\n\t\t\tMore "updates" on the way' )

  if message.content.startswith("*remind"):
    addons = message.content.split("*remind ",1)[1]
    addition(addons)
    await message.channel.send("Aight I'll keep that in mind")


  if message.content.startswith("*insult"):
    k = insults()
    await message.channel.send(k)


  if message.content.startswith("*simp"):
    name_of_guy = message.content.split("*simp ",1)[1]
    t=simprate(name_of_guy)
    await message.channel.send(t)



  if message.content.startswith("*clear"):
    add = []
    if "add"in db.keys():
      index = int(message.content.split("*clear", 1)[1])
      deletion(index)
      add = db["add"]
    #await message.channel.send(add)
  
  #if message.content.startswith("*tell"):
   # index1 = int(message.content.split("*tell", 1)[1])
   # tell_1 = Reminders[index1-2]
    #await message.channel.send(tell_1)

stay_awake()



client.run(os.getenv('token'))
