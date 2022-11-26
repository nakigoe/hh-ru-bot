'''
Автор: Ангел Максим Витальевич, то есть Nakigoe
Свежая версия всегда здесь: https://github.com/nakigoe/hh-ru-bot
Пишите, если Вы хотите получить уроки по C# и Питону: nakigoetenshi@gmail.com
1000 рублей 2 часа один урок

Ставьте звёзды и делитесь сноской на репозиторий со всеми!

Code written by Maxim Angel, aka Nakigoe
You can always find the newest version at https://github.com/nakigoe/hh-ru-bot
contact me for Python and C# lessons at nakigoetenshi@gmail.com
$50 for 2 hours lesson

Put some stars and share!!!
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
import time
s = 4 #time to wait for a single component on the page to appear, in seconds; increase it if you get server-side errors «try again later»
counter = 0
driver = webdriver.Chrome("chromedriver")

text_file = open("cover-letter-ru.txt", "r")
message = text_file.read()
text_file.close()

username = "nakigoetenshi@gmail.com"
password = "super_mega_password"
login_page = "https://hh.ru/account/login"
job_search_query = "C#"
region = "global"

def select_all_countries():
    region_select_button = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="advanced-search-region-selectFromList"]')))
    driver.execute_script("arguments[0].click()", region_select_button)
    #select all countries:
    countries = driver.find_elements(By.XPATH, '//input[@name="bloko-tree-selector-default-name-0"]')
    for country in countries:
        driver.execute_script("arguments[0].click()", country)
    #submit selected countries:
    region_submit_button = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="bloko-tree-selector-popup-submit"]')))
    driver.execute_script("arguments[0].click()", region_submit_button)

def international_ok():
    try:
        international = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="relocation-warning-confirm"]')))
        driver.execute_script("arguments[0].click()", international)
    except TimeoutException:
        return #exit the function

def check_cover_letter_popup():
    try:
        cover_letter_popup = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//textarea[@data-qa="vacancy-response-popup-form-letter-input"]')))
        driver.execute_script('arguments[0].innerHTML = arguments[1]', cover_letter_popup, message)
        popup_cover_letter_submit_button = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-submit-popup"]')))
        driver.execute_script("arguments[0].click()", popup_cover_letter_submit_button)
        global counter
        counter += 1
        return 1
    except TimeoutException:
        return 0 #exit the function

def click_all_jobs_on_the_page():
    global counter

    job_links = driver.find_elements(By.XPATH, '//a[@data-qa="vacancy-serp__vacancy_response"]')
    for link in job_links:
        a = link.get_attribute('href')
        # Open a new window
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(a)
        try:
            # the page opening is already a response!
            international_ok()
            cover_letter_button = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-letter-toggle"]')))
            driver.execute_script("arguments[0].click()", cover_letter_button)
            cover_letter_text = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//form[@action="/applicant/vacancy_response/edit_ajax"]/textarea')))
            driver.execute_script('arguments[0].innerHTML = arguments[1]', cover_letter_text, message)
            cover_letter_submit_button = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-letter-submit"]')))
            driver.execute_script("arguments[0].click()", cover_letter_submit_button)
            #wait until submitted to the server:
            WebDriverWait(driver,s).until(EC.presence_of_element_located((By.XPATH, '//div[@data-qa="vacancy-response-letter-informer"]')))
            counter +=1
            driver.close()
        except TimeoutException:
            if check_cover_letter_popup() == 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue 
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue
        driver.switch_to.window(driver.window_handles[0])

def clear_region():
    try:
        check_region = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-qa="advanced-search__selected-regions"]/div/div/div/span')))

        while check_region:
            clear_region = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-qa="advanced-search__selected-regions"]/div/div/div/button[@data-qa="bloko-tag__cross"]')))
            driver.execute_script("arguments[0].click()", clear_region)
            
            #check if multiple regions are selected from the previous searches
            try:
                check_region = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//div[@data-qa="advanced-search__selected-regions"]/div/div/div/span')))
            except TimeoutException:
                return #exit the function

    except TimeoutException:
        return #exit the function

driver.get(login_page)
WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.NAME, 'login'))).send_keys(username)

show_more_button = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-qa='expand-login-by-password']")))
driver.execute_script('arguments[0].click()', show_more_button)

WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys(password)

login_button = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-qa='account-login-submit']")))
driver.execute_script('arguments[0].click()', login_button)

advanced_search_switch = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="advanced-search"]')))
driver.execute_script('arguments[0].click()', advanced_search_switch)

if region == "global":
    clear_region()
    
    #enable if you want to select certain countries, right now it selects ALL countries by default:
    #select_all_countries()

advanced_search_textarea = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//input[@data-qa="vacancysearch__keywords-input"]')))
driver.execute_script('arguments[0].value = arguments[1]', advanced_search_textarea, job_search_query)

no_agency = driver.find_element(By.XPATH, '//input[@data-qa="advanced-search__label-item_not_from_agency"]')
driver.execute_script('arguments[0].click()', no_agency)

quantity = driver.find_element(By.XPATH, '//input[@data-qa="advanced-search__items_on_page-item_100"]')
driver.execute_script("arguments[0].setAttribute('value','300')", quantity)
driver.execute_script("arguments[0].click()", quantity)

advanced_search_submit_button = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="advanced-search-submit-button"]')))
driver.execute_script("arguments[0].click()", advanced_search_submit_button)

while counter < 200: #there is a limit of 200 resumes per day on hh.ru
    click_all_jobs_on_the_page()

    # Switch back to the first tab with search results
    driver.switch_to.window(driver.window_handles[0])

    #take in another hundred of results:
    next_page_button = WebDriverWait(driver,s).until(EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="pager-next"]')))
    driver.execute_script("arguments[0].click()", next_page_button)

# Close the only tab, will also close the browser.
driver.close()
