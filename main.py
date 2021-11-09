import discord
import os
import requests
import json
import random
from replit import db
from stay_awake import stay_awake


client = discord.Client()

hi_words = [
    '*hi', '*hello', '*Hi', '*Hello', '*hey', '*Hey', '*yo', '*Yo', '*wassup'
]  #the greetings

Reminders = []  #the reminders list

hi_resp = [
    'Hiya', 'How are you', 'What do you want?', 'You are a simp','Will you shut up man' ,'Hey!',
    'Whatup', 'Imma busy rn'
]  #rabot replies

rep_words = ['*fine', '*good', '*bad', '*great', "*awesome"]  #other user words
link = 'https://discord.com/api/oauth2/authorize?client_id=789088446743576577&permissions=0&scope=bot'

reply_1 = [
    "That's great!",  #Rabt's words 
    "Hope it is that way",
    "That's good but don't you have other things to do? ",
    "All right!"
    "Okay"
]


def addition(Reminders):  #reminder additions
    if "add" in db.keys():
        add = db["add"]
        add.append(Reminders)
        db["add"] = add
    else:
        db["add"] = [add]



def simprate(name):
    s = name + " is " + str(random.randint(0, 100)) + "% simp"
    return s


def deletion(i):  #reminder delete
    add = db["add"]
    if len(add) > i:
        del add[i]
    db["add"] = add


def get_inspired():  #api call
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    inspire = json_data[0]['q']
    return (inspire)


def weather(city):
    link1='https://api.openweathermap.org/data/2.5/weather?q='
    ct=city
    link2='&units=metric&APPID='
    my_secret = os.environ['apikey']
    fulllink=link1+ct+link2+my_secret
    res = requests.get(fulllink)
    jj_data = json.loads(res.text)
    desc = jj_data['weather'][0]['description']
    temp = jj_data['main']['temp']
    return(desc,temp)




def memes():
    respy = requests.get("https://meme-api.herokuapp.com/gimme")
    jsonn = json.loads(respy.text)
    title = jsonn['title']
    meme = jsonn['url']
    return (title, meme)


def dad_jokes():
    resp = requests.get("https://icanhazdadjoke.com/slack")
    #resp = requests.get("https://us-central1-dadsofunny.cloudfunctions.net/DadJokes")
    json_dd = json.loads(resp.text)
    joke = json_dd['attachments'][0]['fallback']
    return (joke)



def insults(name):
    get = requests.get("https://insult.mattbas.org/api/en/insult.json")
    json_return = json.loads(get.text)
    insult = json_return['insult']
    stri = name + ", " + insult
    return (stri)





@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game("with *help"))
    print("On the field as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #much = sidlist
    #global much
    options = Reminders
    if "add" in db.keys():
      options = options + db["add"]

    #if "join" in db.keys():
    #  much = much +db["join"]

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

    if (message.content == "*tell all"):
        for option in options:
            k = option
            await message.channel.send((k))

    if(message.content.startswith('*weather')):
          cc = message.content.split("*weather ", 1)[1]
          descr,temp= weather(cc)
          #andis = "Chances of : "
          te = str(temp)+" C "
          fullsentence = descr
          await message.channel.send((fullsentence))
          await message.channel.send("temperature: "+ te)


      

    if (message.content == "*meme"):
        tit, mem = memes()
        await message.channel.send(tit)
        await message.channel.send(mem)

    if any(word in message.content for word in rep_words):
        await message.channel.send(random.choice(reply_1))



    if (message.content == "*thanks"):
        await message.channel.send("Welcome")

    if (message.content == "*help"):
        await message.channel.send(
            '\t\tRABOT HERE\n\nUse the * before a random greeting like Hi or hello to talk to me\n\nUse *inspire to make me give some advice for your worthless lives\n\nUse *remind + <text>  to save any message of your choice\n\nUse *tell all to view all of your saved messages\n\n Use *clear + index of the text you want to delete to clear it\n\nUse *simp and mention someone to know how simp they are(I know I copy from other bots)\n\nUse *insult for insults and *joke for jokes(duh)!\n\nType *meme for memes\n\n\n\n\nPS: If you would like to add this bot into another server use the link below!\nhttps://discord.com/api/oauth2/authorize?client_id=789088446743576577&permissions=0&scope=bot\n \n\n\n\t\t\t'
        )

    if message.content.startswith("*remind"):
        addons = message.content.split("*remind ", 1)[1]
        addition(addons)
        await message.channel.send("Aight I'll keep that in mind")

  
    if message.content.startswith("*insult"):
        der_name = message.content.split("*insult ", 1)[1]
        k = insults(der_name)
        await message.channel.send(k)

 

    if message.content.startswith("*simp"):
        name_of_guy = message.content.split("*simp ", 1)[1]
        t = simprate(name_of_guy)
        await message.channel.send(t)

    if message.content.startswith("*clear"):
        add = []
        if "add" in db.keys():
            index = int(message.content.split("*clear", 1)[1])
            deletion(index)
            add = db["add"]
        #await message.channel.send(add)

        if message.content.startswith("*sclear"):
            sidlist = []
            if "join" in db.keys():
                ind = int(message.content.split("*sclear", 1)[1])
                deletion(ind)
                join = db["join"]
    #if message.content.startswith("*tell"):
    # index1 = int(message.content.split("*tell", 1)[1])
    # tell_1 = Reminders[index1-2]
    #await message.channel.send(tell_1)

stay_awake()

client.run(os.getenv('token'))
