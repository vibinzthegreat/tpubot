import hikari
import time
import lightbulb
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

# LAUNCH DOTENV
load_dotenv() 

# VARIABLES

gputkn = os.getenv('GPUTOKEN')
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
gpulink = 'https://www.techpowerup.com/gpu-specs/'
bot = lightbulb.BotApp(intents=hikari.Intents.ALL, token=gputkn)
elems = driver.find_elements(By.XPATH, "/html/body/div/div[3]/div[1]/form/section/div/fieldset[3]/div/input")
names = driver.find_elements(By.XPATH, "/html/body/div/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/a")

# LAUNCH CHROME

chrome_options.add_argument("--headless")
driver.get(gpulink)

# BOT COMMANDS

@bot.command # PING COMMAND
@lightbulb.command('ping', 'says pong')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond('pong!')


@bot.command # GPU COMMAND
@lightbulb.option("text", "text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command('gpu', "lists gpu's")
@lightbulb.implements(lightbulb.SlashCommand)
async def gpu(ctx):
    for elem in elems:
        elem.send_keys(ctx.options.text)
    time.sleep(0.5)
    try:
        await ctx.respond(driver.find_element(By.XPATH, '/html/body/div/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/a').get_attribute('href'))

    except selenium.common.exceptions.NoSuchElementException:
        await ctx.respond("No GPU found! Please try again. the proper format is skuname(gt/gtx/rtx) + model number + suffix(xt/super/ti)")


    finally:
        elem.clear()


bot.run()
