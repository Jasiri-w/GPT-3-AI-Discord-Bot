# General Imports
import os
from datetime import datetime
from keep_alive import keep_alive

# GPT-3 AI Api import
import openai

# Discord
import discord

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_story(story):
  return """Write a vividly descriptive story about a {}""".format(
      story.capitalize()
  )

#prompt = input("Generate a story about...")

def ai_request(prompt):
  start_time = datetime.now()
  response = openai.Completion.create(
    model = "text-davinci-002",
    prompt = prompt,
    temperature = 0.9,
    max_tokens = 350,
    top_p = 1,
    frequency_penalty = 0,
    presence_penalty = 0.6,
  )
  req_time = datetime.now() - start_time
  res = response.choices[0].text + "\nTime Taken:" + str(req_time) + "\nLength: " + str(len(response.choices[0].text))
  print(res)
  return res

# All Discord API code is below

client = discord.Client()
commands = """

These are all the commands available:

$AI ~ This allows you to send any command for the GTP-3 AI to follow. e.g. 'Write an email boasting over an old teacher that never believed in me.' or 'Write a dismal conversation between to AI going through an existential crisis.' Always finish with a fullstop

$AI-Story ~ This generates a story based on your prompt. Make your prompt complete the sentence 'Write a vivid story about...' e.g 'a man with three legs in the Sahara'

$AI-Commands ~ View the list of commands
$AI-List ~ View the list of commands

Written by Suave -> Updated
"""

@client.event
async def on_ready():
  print("We're ready and online. Succesfully logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if(message.author == client.user):
    return

  print("\nRequest submitted by ", message.author)
  if message.content.startswith('$AI '):
    user_prompt = message.content[3:]
    await message.channel.send(ai_request(user_prompt))
  elif message.content.startswith('$AI-Story'):
    user_prompt = message.content[9:]
    await message.channel.send(ai_request(generate_story(user_prompt)))
  elif message.content.startswith('$AI-Commands') or message.content.startswith('$AI-List'):
    await message.channel.send(commands)


def main():
  keep_alive()
  client.run(os.getenv("DISCORD_TOKEN_GPT"))

# Start Script
main()