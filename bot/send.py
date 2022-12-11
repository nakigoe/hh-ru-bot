'''
Автор: Ангел Максим Витальевич, то есть Nakigoe
Свежая версия всегда здесь: https://github.com/nakigoe/hh-ru-bot
Пишите, если Вы хотите получить уроки по C# и Питону: nakigoetenshi@gmail.com
1000 рублей 2 часа один урок

Ставьте звёзды и делитесь сноской на репозиторий со всеми!

Code is written by Maxim Angel, aka Nakigoe
You can always find the newest version at https://github.com/nakigoe/hh-ru-bot
contact me for Python and C# lessons at nakigoetenshi@gmail.com
$50 for 2 hours lesson

Put stars and share!!!
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.edge import service
import os
os.system("cls") #clear screen from previous sessions

options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("start-maximized")
# options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
my_service=service.Service(r'msedgedriver.exe')
options.page_load_strategy = 'eager' #do not wait for images to load
options.add_experimental_option("detach", True)

s = 5 #time to wait for a single component on the page to appear, in seconds; increase it if you get server-side errors «try again later»
counter = 0

driver = webdriver.Edge(service=my_service, options=options)
action = ActionChains(driver)
wait = WebDriverWait(driver,s)

#cover letter
text_file = open("cover-letter-ru.txt", "r")
message = text_file.read()
text_file.close()

#simple answer to all questions, showcase of all my works!
text_file = open("links-list.txt", "r")
answer = text_file.read()
text_file.close()

username = "nakigoetenshi@gmail.com"
password = "Super_Mega_Password"
login_page = "https://hh.ru/account/login"
job_search_query = "C#"
exclude = "1C, angular, php, sharepoint, react, vue, Rust, golang, go, java, vba, node.js, delphi, медсестра, медбрат, врач, полицейский, мойщик, упаковщик, сборщик, приемщик, приёмщик, часовщик, помощник, повар, сушист, хостес, бар, бармен, официант, бариста, курьер, продажа, маникюр, педикюр, электрик, электромонтёр, слесарь, кассир, грузчик, швея, игр, игра, игры, games, gambling, gamble, tobacco"
region = "global"

def select_all_countries():
    region_select_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="advanced-search-region-selectFromList"]')))
    driver.execute_script("arguments[0].click()", region_select_button)
    #select all countries:
    countries = driver.find_elements(By.XPATH, '//input[@name="bloko-tree-selector-default-name-0"]')
    for country in countries:
        driver.execute_script("arguments[0].click()", country)
    #submit selected countries:
    region_submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="bloko-tree-selector-popup-submit"]')))
    driver.execute_script("arguments[0].click()", region_submit_button)

def international_ok():
    try:
        international = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="relocation-warning-confirm"]')))
        driver.execute_script("arguments[0].click()", international)
    except TimeoutException:
        return #exit the function
    driver.refresh()

def check_cover_letter_popup():
    global counter
    try:
        cover_letter_popup = wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@data-qa="vacancy-response-popup-form-letter-input"]')))
        driver.execute_script('arguments[0].innerHTML = arguments[1]', cover_letter_popup, message)

        #experimenting with unresponsive button:
        cover_letter_popup.send_keys(Keys.ENTER) 
        action.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-submit-popup"]')))).perform()
        
        #unresponsive after another country popup:
        popup_cover_letter_submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-submit-popup"]')))
        driver.execute_script("arguments[0].click()", popup_cover_letter_submit_button)
        counter += 1
        return 1
    except TimeoutException:
        return 0 #exit the function
    
def answer_questions():
    try: 
        test_questions_presence = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-qa="task-body"]//textarea')))
        if test_questions_presence: 
            questions = driver.find_elements(By.XPATH, '//div[@data-qa="task-body"]//textarea')
            for question in questions:
                # driver.execute_script('arguments[0].innerHTML = arguments[1]', question, answer)
                question.send_keys(answer)
    except TimeoutException:
        return
    except StaleElementReferenceException:
        return
    
def fill_in_cover_letter():
    cover_letter_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-letter-toggle"]')))
    driver.execute_script("arguments[0].click()", cover_letter_button)
    
    cover_letter_text = wait.until(EC.element_to_be_clickable((By.XPATH, '//form[@action="/applicant/vacancy_response/edit_ajax"]/textarea')))
    driver.execute_script('arguments[0].innerHTML = arguments[1]', cover_letter_text, message)
    
    action.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-letter-submit"]')))).perform()
    
def click_all_jobs_on_the_page():
    global counter
    try:
        test_links_presence = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@data-qa="vacancy-serp__vacancy_response"]')))
    except TimeoutException:
        return
    except StaleElementReferenceException:
        return
    if test_links_presence: 
        job_links = driver.find_elements(By.XPATH, '//a[@data-qa="vacancy-serp__vacancy_response"]')
        for link in job_links:
            a = link.get_attribute('href')
            # Open a new window
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(a)            
            try:                            
                international_ok()
                answer_questions()
                fill_in_cover_letter()                
                #wait until submitted to the server:
                wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-qa="vacancy-response-letter-informer"]')))
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
        check_region = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-qa="advanced-search__selected-regions"]/div/div/div/span')))

        while check_region:
            clear_region = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-qa="advanced-search__selected-regions"]/div/div/div/button[@data-qa="bloko-tag__cross"]')))
            driver.execute_script("arguments[0].click()", clear_region)
            
            #check if multiple regions are selected from the previous searches
            try:
                check_region = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-qa="advanced-search__selected-regions"]/div/div/div/span')))
            except TimeoutException:
                return #exit the function

    except TimeoutException:
        return #exit the function

def login():
    driver.get(login_page)
    wait.until(EC.element_to_be_clickable((By.NAME, 'login'))).send_keys(username)

    show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-qa='expand-login-by-password']")))
    driver.execute_script('arguments[0].click()', show_more_button)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys(password)

    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-qa='account-login-submit']")))
    driver.execute_script('arguments[0].click()', login_button)

def advanced_search():
    action.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="advanced-search"]')))).perform()

    if region == "global":
        clear_region()
        #enable if you want to select certain countries, right now it selects ALL countries by default:
        #select_all_countries()

    advanced_search_textarea = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-qa="vacancysearch__keywords-input"]')))
    driver.execute_script('arguments[0].value = arguments[1]', advanced_search_textarea, job_search_query)

    exclude_these_results = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-qa="vacancysearch__keywords-excluded-input"]')))
    driver.execute_script('arguments[0].value = arguments[1]', exclude_these_results, exclude)
    
    no_agency = driver.find_element(By.XPATH, '//input[@data-qa="advanced-search__label-item_not_from_agency"]')
    driver.execute_script('arguments[0].click()', no_agency)

    quantity = driver.find_element(By.XPATH, '//input[@data-qa="advanced-search__items_on_page-item_100"]')
    driver.execute_script("arguments[0].click()", quantity)

    advanced_search_submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="advanced-search-submit-button"]')))
    driver.execute_script("arguments[0].click()", advanced_search_submit_button)
    
    #wait until the server sends results, server may be slow!
    driver.implicitly_wait(5) #wait for 5 seconds, just in case, for the server response

def main():
    global counter

    login()
    advanced_search()
    
    while counter < 200: #there is a limit of 200 resumes per day on hh.ru
        click_all_jobs_on_the_page()

        # Switch back to the first tab with search results
        driver.switch_to.window(driver.window_handles[0])

        #take in another hundred of results:
        next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="pager-next"]')))
        driver.execute_script("arguments[0].click()", next_page_button)

    # Close the only tab, will also close the browser.
    driver.close()
    driver.quit()

main() #run the script, starting from the main function