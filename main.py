 #grab everything that has been said so far - done
  #grab the previous sentence -working only with periods
  #grab unread messages and display (or # of inputted previous messages) --> find function for finding number of unread messages in a channel
  #maybe have a callback of the last five sentences?
  #have to incorporate editted messages as well --> find function - done
  #maybe have instances of stories - like story objects
  #make deleting the previous message the actual message itself, not the pop function
  #start command for a new story?
  #end command for ending story and option to save?
  #what about storing the messages themselves in the list, and not the content? --> can check message id?


import discord
import os

bot = discord.Client()

sentence = []
whole_story = []

def addWord(msg):
  global sentence
  global whole_story

  if (msg.content==('.') or (msg.content=='!') or (msg.content==',') or (msg.content=='?') or (msg.content==':') or (msg.content=='(') or (msg.content==')')):
    sentence.append(msg.content)
    whole_story.append(msg.content)

  else:
    sentence.append(" ") 
    sentence.append(msg.content)
    whole_story.append(" ")
    whole_story.append(msg.content)

def deleteWord(msg):
  global sentence
  global whole_story

  if (msg.content==('.') or (msg.content=='!') or (msg.content==',') or (msg.content=='?') or (msg.content==':') or (msg.content=='(') or (msg.content==')')):
    sentence.pop(-1)
    whole_story.pop(-1)

  else:
    sentence.pop(-1)
    sentence.pop(-1)  
    whole_story.pop(-1)
    whole_story.pop(-1)

def refresh():
    global sentence
    global whole_story
    sentence.clear()
    whole_story.append(" |")

def findIndex():
  global whole_story
  whole_story.reverse()
  indexperiod = whole_story.index('.',1,)
 # indexexclam = whole_story.index('!')
  #indexquest = whole_story.index('?')
  whole_story.reverse()
  return (len(whole_story) - indexperiod)

# printing the final index


    

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    global sentence
    global whole_story
    if message.author == bot.user:
        return
    if message.content.startswith('->recap'):
      recap = "".join(map(str, sentence))
      await message.channel.send("One Word Story recap:" + recap)
      refresh()

    elif message.content.startswith('->allrecap'):
      all = "".join(map(str, whole_story))
      await message.channel.send("One Word Story full recap:" + all)

    elif message.content.startswith('->lastsentence'):
      lastsent = "".join(map(str, whole_story[findIndex():]))
      await message.channel.send("One Word Story last sentence:" + lastsent)
    elif message.content.startswith('->catchup'):
      catch = map(lambda x: x.content, await message.channel.history(limit=int(message.content.split()[1])).flatten())
      catchwords =  "".join(catch)
      await message.channel.send(catchwords)
   # 
    #  
    #  await message.channel.history().find(lambda m: m.author.id == users_id)

    elif message.content.startswith('->') and not (message.content.startswith('->recap'))  and not(message.content.startswith('->allrecap')) and not(message.content.startswith('->lastsentence')):
      addWord(message)
      await message.delete()

    else:
      addWord(message)

@bot.event
async def on_message_delete(message):
  deleteWord(message)

@bot.event
async def on_message_edit(before, after):
  deleteWord(before)
  addWord(after)
      
bot.run(os.getenv('TOKEN'))