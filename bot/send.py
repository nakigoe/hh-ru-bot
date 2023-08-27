from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import os
os.system("cls") #clear screen from previous sessions
import time
import json # for cookies

cookies_path = 'auth/cookies.json'
local_storage_path = 'auth/local_storage.json'
user_agent = "My Usual Browser on a Usual Device" # Replace with your desired user-agent string. You can find your current browser's user-agent by searching "What's my user-agent?" in a search engine
options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("start-maximized")
options.page_load_strategy = 'eager' #do not wait for images to load
options.add_argument(f"user-agent={user_agent}")
options.add_experimental_option("detach", True)

s = 10 #time to wait for a single component on the page to appear, in seconds; increase it if you get server-side errors «try again later»
counter = 0

driver = webdriver.Edge(options=options)
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
job_search_query = "Assembly"
exclude = "испанский, немецкий, Minecraft, Unity, blender, wordpress, 1C, 1С, bitrix, erlang, angular, laravel, sharepoint, react, React.JS, vue, Vue.JS, typescript, Rust, golang, go, java, delphi, автор, кредит, медсестра, медбрат, врач, полицейский, мойщик, упаковщик, сборщик, приемщик, приёмщик, часовщик, помощник, повар, сушист, хостес, бар, бармен, официант, бариста, курьер, продажа, маникюр, педикюр, электрик, электромонтёр, слесарь, кассир, грузчик, швея, игр, игра, игры, покер, казино, беттинг, гемблинг, гэмблинг, вейп, вейпинг, games, gambling, gamble, tobacco, vape, vaping"
region = "global"
search_link = "https://hh.ru/"

def load_data_from_json(path): return json.load(open(path, 'r'))
def save_data_to_json(data, path): os.makedirs(os.path.dirname(path), exist_ok=True); json.dump(data, open(path, 'w'))

def add_cookies(cookies): [driver.add_cookie(cookie) for cookie in cookies]
def add_local_storage(local_storage): 
    [driver.execute_script(f"window.localStorage.setItem({json.dumps(k)}, {json.dumps(v)});") for k, v in local_storage.items()]

def success(): return True if wait.until(EC.presence_of_element_located((By.XPATH, '//a[@data-qa="mainmenu_myResumes"]'))) else False

def navigate_and_check(probe_page):
    driver.get(probe_page)
    time.sleep(3)
    if success(): # return True if you are loggged in successfully independent of saving new cookies
        save_data_to_json(driver.get_cookies(), cookies_path)
        save_data_to_json({key: driver.execute_script(f"return window.localStorage.getItem('{key}');") for key in driver.execute_script("return Object.keys(window.localStorage);")}, local_storage_path)
        return True
    else: 
        return False

def login():
    driver.get(login_page)
    time.sleep(3)

    show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="expand-login-by-password"]')))
    action.click(show_more_button).perform()
    
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-qa="login-input-username"]'))).send_keys(username)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="password"]'))).send_keys(password)

    time.sleep(10) # 10 senconds to enter the stupid possible antibot CAPTCHA
    
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-qa='account-login-submit']")))
    driver.execute_script('arguments[0].click()', login_button)
    
def check_cookies_and_login():
    driver.get(login_page) # you have to open some page first before trying to load cookies!
    time.sleep(3)
    
    if os.path.exists(cookies_path) and os.path.exists(local_storage_path):
        add_cookies(load_data_from_json(cookies_path))
        add_local_storage(load_data_from_json(local_storage_path))
        
        if navigate_and_check(search_link):
            return # it is OK, you are logged in
    
    login()
    time.sleep(3)
    navigate_and_check(search_link)

def scroll_to_bottom(): 
    reached_page_end= False
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    #expand the skills list:
    while not reached_page_end:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            reached_page_end = True
        else:
            last_height = new_height
            
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
    except:
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
        time.sleep(3)
        try:
            error = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="bloko-translate-guard"]')))
            if error: return 0 # resume submitted but there was a server error. Just try this specific job the next time!
        except:
            pass
        #wait until submitted to the server: 
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="vacancy-actions_responded"]')))
        counter += 1
        return 0
    except:
        return 1 #exit the function and provide an error return of 1 (do not increase the counter)
    
def answer_questions():
    #create radio-buttons answers here!!!
    try: 
        test_questions_presence = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-qa="task-body"]//textarea')))
        if test_questions_presence: 
            try:
                questions = driver.find_elements(By.XPATH, '//div[@data-qa="task-body"]//textarea')
                for question in questions:
                    question.send_keys(answer)
            except:
                pass
    except:
        return
    
def fill_in_cover_letter():
    global counter
    scroll_to_bottom()
    try:
        cover_letter_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-letter-toggle"]')))
        driver.execute_script("arguments[0].click()", cover_letter_button)
        
        cover_letter_text = wait.until(EC.element_to_be_clickable((By.XPATH, '//form[@action="/applicant/vacancy_response/edit_ajax"]/textarea')))
        driver.execute_script('arguments[0].innerHTML = arguments[1]', cover_letter_text, message)
        
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-letter-submit"]')))
        driver.execute_script("arguments[0].removeAttribute('disabled')", submit_button) #remove 'disabled' attribute
        action.double_click(submit_button).perform()
        time.sleep(3)
        try:
            error = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="bloko-translate-guard"]')))
            if error: return 0 # resume submitted but there was a server error. Just try this specific job the next time!
        except:
            pass
        #wait until submitted to the server:
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-qa="vacancy-response-letter-informer"]')))
        counter += 1
        return 0
    except:
        return 1
    
def click_all_jobs_on_the_page():
    global counter
    scroll_to_bottom()
    try:
        test_links_presence = wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(., "Откликнуться")]')))
    except:
        return
    if test_links_presence: 
        job_links = driver.find_elements(By.XPATH, '//a[contains(., "Откликнуться")]')
        for link in job_links:
            a = link.get_attribute('href')
            # Open a new window
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(a) 
            time.sleep(3)
            international_ok() # the problematic code to click the international popup
            
            #check for a loading error (server might be overloaded)
            # try:
            #     test_error_message = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="bloko-translate-guard"]')))
            # except:
            #   pass 
            # if test_error_message != None and test_error_message.get_attribute('innerHTML') == "Произошла ошибка, попробуйте ещё раз":
            #     action.double_click(wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="vacancy-response-link-top"]')))).perform()     
                   
            if fill_in_cover_letter() == 0:
                driver.close()
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                continue
            elif check_cover_letter_popup() == 0:
                driver.close()
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                continue
            else:  
                try:
                    answer_questions()
                    if check_cover_letter_popup() == 0:
                        driver.close()
                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[0])
                        continue
                    fill_in_cover_letter()
                    driver.close()
                    time.sleep(1)
                    
                except:
                    driver.close()
                    time.sleep(1)
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
            except:
                return #exit the function

    except:
        return #exit the function

def advanced_search():
    action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="advanced-search"]')))).perform()

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
    time.sleep(3)

def main():
    global counter

    check_cookies_and_login()
    time.sleep(3)
    advanced_search()
    
    while counter < 200: #there is a limit of 200 resumes per day on hh.ru
        click_all_jobs_on_the_page()

        # Switch back to the first tab with search results
        driver.switch_to.window(driver.window_handles[0])

        try:
            #take in another hundred of results:
            next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="pager-next"]')))
            driver.execute_script("arguments[0].click()", next_page_button)
        except:
            os.system("cls") #clear screen from unnecessary logs since the operation has completed successfully
            print("It's either the hh.ru server has become undresponsive or you have reached the hh.ru limit of 200 resumes per day or all the links within the current search query have been clicked. \n 1) check if hh.ru is alive and responsive \n 2) check if you have reached the limit \n 3) check if you have clicked all the links available for the job search query. In that case change the 'job_search_query = ' value. \n \n Sincerely Yours, \n NAKIGOE.ORG")
            break

    # Close the only tab, will also close the browser.
    driver.close()
    driver.quit()

main() #run the script, starting from the main function