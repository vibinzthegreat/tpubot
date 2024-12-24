import hikari
import lightbulb
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

gpulink = 'https://www.techpowerup.com/gpu-specs/'
cpulink = 'https://www.techpowerup.com/cpu-specs/'

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get(gpulink)
print(driver.current_window_handle)
driver.switch_to.new_window("tab")
driver.get(cpulink)
print(driver.current_window_handle)

window_handles = driver.window_handles

bot = lightbulb.BotApp(intents=hikari.Intents.ALL, token=input("your token here(change this line to your token if you do not want to save the token every time):   "), prefix='%')

# Define the wait object for future use
wait = WebDriverWait(driver, 10)  # 10 seconds timeout for waiting

@bot.command
@lightbulb.command('ping', 'says pong')
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx):
    await ctx.respond('pong!')

# Update the XPaths as needed
gpu_input_xpath = "/html/body/div/div[3]/div[1]/form/section/div/fieldset[3]/div/input"
gpu_link_xpath = "/html/body/div/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/a"

# These elements might be used for both CPU and GPU, so you may want to find them again in each function
@bot.command
@lightbulb.option("text", "text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command('gpu', "lists gpu's")
@lightbulb.implements(lightbulb.PrefixCommand)
async def gpu(ctx):
    driver.switch_to.window(window_handles[0])
    
    # Wait for the input element to be present on the page
    try:
        elem = wait.until(EC.presence_of_element_located((By.XPATH, gpu_input_xpath)))
        elem.send_keys(ctx.options.text)
        
        # Wait for the result link to be clickable
        result_elem = wait.until(EC.element_to_be_clickable((By.XPATH, gpu_link_xpath)))
        await ctx.respond(result_elem.get_attribute('href'))
    
    except selenium.common.exceptions.NoSuchElementException:
        await ctx.respond("No GPU found! Please try again. The proper format is skuname(gt/gtx/rtx) + model number + suffix(xt/super/ti).")

    except selenium.common.exceptions.TimeoutException:
        await ctx.respond("Timed out waiting for GPU input or results. Please try again later.")
    
    finally:
        elem.clear()


@bot.command
@lightbulb.option("text", "text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command('cpu', "lists cpu spec link")
@lightbulb.implements(lightbulb.PrefixCommand)
async def cpu(ctx):
    driver.switch_to.window(window_handles[1])
    
    # Wait for the input element to be present on the page
    try:
        elem = wait.until(EC.presence_of_element_located((By.XPATH, gpu_input_xpath)))  # Same XPath as GPU input
        elem.send_keys(ctx.options.text)
        
        # Wait for the result link to be clickable
        result_elem = wait.until(EC.element_to_be_clickable((By.XPATH, gpu_link_xpath)))  # Same XPath as GPU link
        await ctx.respond(result_elem.get_attribute('href'))
    
    except selenium.common.exceptions.NoSuchElementException:
        await ctx.respond("No CPU found! Please try again. The proper format is skuname + model number + suffix. If that does not work, make sure there are spaces where needed.")

    except selenium.common.exceptions.TimeoutException:
        await ctx.respond("Timed out waiting for CPU input or results. Please try again later.")
    
    finally:
        elem.clear()


bot.run()
