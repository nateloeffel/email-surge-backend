from dotenv import load_dotenv
from linkedin_scraper import actions
from person import Person
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
load_dotenv()

email = os.getenv('LINKEDIN_EMAIL')
password = os.getenv('LINKEDIN_PASSWORD')
chrome_options = Options()
# chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--load-extension={0}".format("./capsolver_extension"))

url = "https://www.linkedin.com/in/nateloeffel"
driver = webdriver.Chrome(options=chrome_options)
actions.login(driver, email, password)
person = Person(linkedin_url=url, driver=driver)
response = person.serialize_person()
# print(response)