import os
import random
import discord
from dotenv import load_dotenv
import responses

class ResponseSet:
  def __init__(self, keywords, rep, score):
    self.keywords = keywords
    self.rep = rep
    self.score = score

# needs a score of 2 or more to qualify
responseConnection = [
ResponseSet(["hungry", "food", "i want", "i am", "im", "what should i", "eat", "lunch", "dinner", "snack", "breakfast"], responses.recipes, 0),
ResponseSet(["im", "lonly", "bored", "linked", "linkedin", "friend", "whos on", "dont have", "no friends"], responses.linkedin, 0),
ResponseSet(["i need", "motivation", "im procrastinating", "im going to", "procrastinate"], responses.modivation, 0),
ResponseSet(["tell me about yourself", "who are you", "about", "slackbot"], responses.about, 0),
ResponseSet(["any advice", "for me", "give me", "advice"], responses.warnings, 0),
ResponseSet(["give me", "fun", "fact", "knowledge"], responses.fact, 0),
]

# message fully matches one of the options to qualify
responseConnectionSolo = [
(["hello", "hi"], responses.hello),
(["sj help"], responses.helping),
(["slackbot", "slackbot jr", "slackbot jr.", "sj"], responses.summoned),
(["f"], responses.F), #time it so it only responsed once and not after every respect paid
]

def cleanUpScores():
    for i in responseConnection:
        i.score = 0

def patternRecog(data):
    data = str.lower(data.replace("'", "").replace("\"", "").replace(":", "").replace(";", "").replace(",", "").replace(".", "").replace("?", "").replace("!", ""))
    for i in responseConnection:
            for j in i.keywords:
                if data.find(j) != -1:
                    i.score = i.score + 1
    
    #tempWords = data.split()
    #words = []
    #for word in tempWords:
    #    word = str.lower(word.replace("'", "").replace("\"", "").replace(":", "").replace(";", "").replace(",", "").replace(".", "").replace("?", "").replace("!", ""))
    #    words.append(word)
    #for word in words:
    #    for i in responseConnection:
    #        for j in i.keywords:
    #            if(word == j):
    #                i.score = i.score + 1
    
    maxScore = 0
    bestAnsIndex = -1
    index = 0
    for i in responseConnection:
        if i.score > maxScore and i.score >= 2:
            maxScore = i.score
            bestAnsIndex = index
        index = index + 1
    if(bestAnsIndex != -1):
       return True, random.choice(responseConnection[bestAnsIndex].rep)
    return False, "Bananas"
    

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

print("Slackbot Jr., reporting for duty.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    for i in responseConnectionSolo:
        for j in i[0]:
            if str.lower(message.content) == j:
                response = random.choice(i[1])
                await message.channel.send(response)
    match, response = patternRecog(message.content)
    if match == True:
        await message.channel.send(response)
    cleanUpScores()
    
client.run(TOKEN)



# Sources
# https://medium.com/bad-programming/making-a-cool-discord-bot-in-python-3-e6773add3c48#:~:text=Making%20a%20Cool%20Discord%20Bot%20in%20Python%203,...%205%20Adding%20useful%20Functions%20&%20Examples.
# https://realpython.com/how-to-make-a-discord-bot-python/


# Link to add to server
# https://discord.com/api/oauth2/authorize?client_id=804487971511992350&permissions=0&scope=bot