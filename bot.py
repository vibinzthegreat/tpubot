import hikari
import time
import lightbulb
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
gpulink = 'https://www.techpowerup.com/gpu-specs/'
cpulink = 'https://www.techpowerup.com/cpu-specs/'
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get(gpulink)
driver.switch_to.new_window("tab")
driver.get(cpulink)





bot = lightbulb.BotApp(intents=hikari.Intents.ALL, token=input("your token here(change this line to your token if you do not want to save the token every time):   "), prefix='%')


@bot.command
@lightbulb.command('ping', 'says pong')
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx):
    await ctx.respond('pong!')

elems = driver.find_elements(By.XPATH, "/html/body/div/div[3]/div[1]/form/section/div/fieldset[3]/div/input")
names = driver.find_elements(By.XPATH, "/html/body/div/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/a")


@bot.command
@lightbulb.option("text", "text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command('gpu', "lists gpu's")
@lightbulb.implements(lightbulb.PrefixCommand)
async def gpu(ctx):
    driver.switch_to.window("https://www.techpowerup.com/gpu-specs/")
    for elem in elems:
        elem.send_keys(ctx.options.text)
    time.sleep(0.5)
    try:
        await ctx.respond(driver.find_element(By.XPATH, '/html/body/div/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/a').get_attribute('href'))

    except selenium.common.exceptions.NoSuchElementException:
        await ctx.respond("No GPU found! Please try again. the proper format is skuname(gt/gtx/rtx) + model number + suffix(xt/super/ti)")


    finally:
        elem.clear()


@bot.command
@lightbulb.option("text", "text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command('cpu', "lists cpu spec link")
@lightbulb.implements(lightbulb.PrefixCommand)
async def gpu(ctx):
    driver.switch_to.window("https://www.techpowerup.com/cpu-specs/")
    for elem in elems:
        elem.send_keys(ctx.options.text)
    time.sleep(0.5)
    try:
        await ctx.respond(driver.find_element(By.XPATH, '/html/body/div/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/a').get_attribute('href'))

    except selenium.common.exceptions.NoSuchElementException:
        await ctx.respond("No CPU found! Please try again. the proper format is skuname + model number + suffix. if that does not work make sure there are spaces where needed")


    finally:
        elem.clear()

bot.run()
