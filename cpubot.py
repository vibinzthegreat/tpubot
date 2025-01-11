import hikari
import time
import lightbulb
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# VARIABLES

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
gpulink = 'https://www.techpowerup.com/cpu-specs/'
bot = lightbulb.BotApp(intents=hikari.Intents.ALL, token=("your token here"))

# LAUNCH CHROME

driver.get(gpulink)

# VARS FOR SELENIUM

elems = driver.find_elements(By.XPATH, "/html/body/div/div[3]/div[1]/form/section/div/fieldset[3]/div/input")
names = driver.find_elements(By.XPATH, "/html/body/div/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/a")


# BOT COMMANDS

@bot.command # PING COMMAND
@lightbulb.command('pong', 'says ping')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond('ping!')


@bot.command # CPU COMMAND
@lightbulb.option("text", "text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command('cpu', "Lists cpu's")
@lightbulb.implements(lightbulb.SlashCommand)
async def gpu(ctx):
    for elem in elems:
        elem.send_keys(ctx.options.text)
    time.sleep(0.5)
    try:
        await ctx.respond(driver.find_element(By.XPATH, '/html/body/div/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/a').get_attribute('href'))

    except selenium.common.exceptions.NoSuchElementException:
        await ctx.respond("No CPU found! Please try again. The proper format is prefix + model number + suffix. Make sure to add spaces!")


    finally:
        elem.clear()


bot.run()
