import os

import discord
import langid
import requests
from discord import app_commands

API_KEY = os.environ['APIKEY']
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

TL_txt = ' '
sendtxt = ' '
request = ' '
response = ' '
target_lang = 'JA'
target_lang_EN = 'EN'
formality = 'prefer_less'


@client.event
async def on_ready():
  # 起動したらターミナルにログイン通知が表示される
  print('ログインしました')
  await tree.sync()


@tree.command(name="solaire", description="Summon Solaire ソラールを召喚")
async def test_command(interaction: discord.Interaction):
  await interaction.response.send_message(
    "I am Solaire of Astora, an adherent to the Lord of Sunlight. 俺はアストラのソラール。見ての通り、太陽の神の信徒だ。"
  )


@client.event
async def on_message(message):
  if message.author.bot or message.channel.id != 1051127361350942730:
    return
  elif len(message.content) >= 150:
    await message.reply("文字数制限を超過しました。Character limit exceeded.")
  else:
    sendtxt = TLapi(message.content)
    await message.reply(sendtxt, mention_author=False)


def TLapi(TL_txt):
  ISO = langid.classify(TL_txt)[0]
  ISO = ISO.upper()
  if target_lang == ISO:
    params = {
      'auth_key': API_KEY,
      'text': TL_txt,
      'target_lang': target_lang_EN,
      'formality': formality,
      'source_lang': target_lang
    }

  else:
    params = {
      'auth_key': API_KEY,
      'text': TL_txt,
      'target_lang': target_lang,
      'formality': formality
    }

  request = requests.post("https://api-free.deepl.com/v2/translate",
                          data=params)

  response = request.json()
  result = (response['translations'][0]['text'])
  return (result)


client.run(os.getenv['TOKEN'])
