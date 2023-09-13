from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import os
os.system("cls") #clear screen from previous sessions
import time
import json # for cookies

from enum import Enum # that one is for You, my dear reader, code readability from NAKIGOE.ORG
class Status(Enum):
    SUCCESS = 0
    FAILURE = 1

COOKIES_PATH = 'auth/cookies.json'
LOCAL_STORAGE_PATH = 'auth/local_storage.json'
USER_AGENT = "My Standard Browser and my standard Device" # Replace with your desired user-agent string. You can find your current browser's user-agent by searching "What's my user-agent?" in a search engine
options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("start-maximized")
options.page_load_strategy = 'eager' #do not wait for images to load
options.add_argument(f"user-agent={USER_AGENT}")
options.add_experimental_option("detach", True)

s = 10 #time to wait for a single component on the page to appear, in seconds; increase it if you get server-side errors «try again later»
counter = 0

driver = webdriver.Edge(options=options)
action = ActionChains(driver)
wait = WebDriverWait(driver,s)

def custom_wait(driver, timeout, condition_type, locator_tuple):
    wait = WebDriverWait(driver, timeout)
    return wait.until(condition_type(locator_tuple))

# use eternal_wait only for a few critical elements, like login fields and for page successful load indicators 
# use eternal_wait for a critical server response indicator, it is more effective than time.sleep(seconds)!
def eternal_wait(driver, timeout, condition_type, locator_tuple): # timeout is symbolic here since it is eternal loop
    while True:
        try:
            element = WebDriverWait(driver, timeout).until(
                condition_type(locator_tuple)
            )
            return element
        except:
            print(f"\n\nWaiting for the element(s) {locator_tuple} to become {condition_type}…")
            time.sleep(0.5) # just to display a message
            continue

#cover letter
text_file = open("cover-letter-ru.txt", "r")
MESSAGE = text_file.read()
text_file.close()

#simple answer to all questions, showcase of all my works!
text_file = open("links-list.txt", "r")
answer = text_file.read()
text_file.close()

USERNAME = "nakigoetenshi@gmail.com"
PASSWORD = "Super_Mega_Password"
LOGIN_PAGE = "https://hh.ru/account/login"
JOB_SEARCH_QUERY = "Java"
LOGIN_PAGE = "https://hh.ru/account/login"
EXCLUDE = "испанский, немецкий, Minecraft, Unity, blender, wordpress, 1C, 1С, bitrix, erlang, angular, laravel, sharepoint, react, React.JS, vue, Vue.JS, typescript, Rust, golang, go, java, delphi, автор, кредит, медсестра, медбрат, врач, полицейский, мойщик, упаковщик, сборщик, приемщик, приёмщик, часовщик, помощник, повар, сушист, хостес, бар, бармен, официант, бариста, курьер, продажа, маникюр, педикюр, электрик, электромонтёр, слесарь, кассир, грузчик, швея, игр, игра, игры, покер, казино, беттинг, гемблинг, гэмблинг, вейп, вейпинг, games, gambling, gamble, tobacco, vape, vaping"
REGION = "global"
SEARCH_LINK = "https://hh.ru/"
MIN_SALARY = "200000"
ONLY_WITH_SALARY = True

def load_data_from_json(path): return json.load(open(path, 'r'))
def save_data_to_json(data, path): os.makedirs(os.path.dirname(path), exist_ok=True); json.dump(data, open(path, 'w'))

def add_cookies(cookies): [driver.add_cookie(cookie) for cookie in cookies]
def add_local_storage(local_storage): 
    [driver.execute_script(f"window.localStorage.setItem({json.dumps(k)}, {json.dumps(v)});") for k, v in local_storage.items()]

def success():
    try:
        custom_wait(driver, s, EC.presence_of_element_located, (By.XPATH, '//a[@data-qa="mainmenu_myResumes"]'))
        return True
    except:
        return False

def navigate_and_check(probe_page):
    driver.get(probe_page)
    time.sleep(5)
    if success(): # return True if you are loggged in successfully independent of saving new cookies, check the successful log in indicator
        save_data_to_json(driver.get_cookies(), COOKIES_PATH)
        save_data_to_json({key: driver.execute_script(f"return window.localStorage.getItem('{key}');") for key in driver.execute_script("return Object.keys(window.localStorage);")}, LOCAL_STORAGE_PATH)
        return True
    else: 
        return False

def login():
    driver.get(LOGIN_PAGE)

    show_more_button = eternal_wait(driver, s, EC.element_to_be_clickable, (By.XPATH, '//button[@data-qa="expand-login-by-password"]'))
    action.click(show_more_button).perform()
    
    login_field = eternal_wait(driver, s, EC.element_to_be_clickable, (By.XPATH, '//input[@data-qa="login-input-username"]'))
    password_field = eternal_wait(driver, s, EC.element_to_be_clickable, (By.XPATH, '//input[@type="password"]'))
    
    login_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    
    login_button = eternal_wait(driver, s, EC.element_to_be_clickable, (By.XPATH, "//button[@data-qa='account-login-submit']"))
    click_and_wait(login_button,5) 
    
def check_cookies_and_login():
    driver.get(LOGIN_PAGE) # you have to open some page first before trying to load cookies!
    
    if os.path.exists(COOKIES_PATH) and os.path.exists(LOCAL_STORAGE_PATH):
        add_cookies(load_data_from_json(COOKIES_PATH))
        add_local_storage(load_data_from_json(LOCAL_STORAGE_PATH))
        
        if navigate_and_check(SEARCH_LINK): # store fresh cookies after successful login 
            return # it is OK, you are logged in
    
    login()
    navigate_and_check(SEARCH_LINK) # store fresh cookies after successful login 

def scroll_to_bottom(delay=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            break
        last_height = new_height
            
def click_and_wait(element, delay=1):
    action.move_to_element(element).click().perform()
    time.sleep(delay)

def js_click(driver, element):
    try:
        if element.is_displayed() and element.is_enabled():
            # Scroll the element into view
            driver.execute_script("arguments[0].scrollIntoView();", element)
            
            # Move to the element to ensure it's in the viewport
            action.move_to_element(element).perform()
            
            # Click the element
            driver.execute_script("arguments[0].click();", element)
            
            # Ensure the element has focus
            driver.execute_script("arguments[0].focus();", element)
            
        else:
            print(f"{element} element is not visible or not enabled for clicking.")
    except Exception as e:
        print(f"An error occurred while clicking the element: {str(e)}")
         
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

def check_cover_letter_popup(message):
    global counter
    try:
        cover_letter_popup = wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[@data-qa="vacancy-response-popup-form-letter-input"]')))
        set_value_with_event(cover_letter_popup, message)

        #experimenting with unresponsive button:
        action.click(wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-submit-popup"]')))).perform()
        
        #unresponsive after another country popup:
        popup_cover_letter_submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-submit-popup"]')))
        driver.execute_script("arguments[0].click()", popup_cover_letter_submit_button)
        time.sleep(3)
        try:
            error = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="bloko-translate-guard"]')))
            if error: return Status.SUCCESS # resume submitted but there was a server error. Just try this specific job the next time!
        except:
            pass
        #wait until submitted to the server: 
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="vacancy-actions_responded"]')))
        counter += 1
        return Status.SUCCESS
    except:
        return Status.FAILURE #exit the function and provide an error return of 1 (do not increase the counter)
    
def set_value_with_event(element, value):
    # Click to focus
    action.move_to_element(element).click().perform()
    
    # Clear the existing value
    driver.execute_script("arguments[0].value = '';", element)
    
    # Use JavaScript to simulate human typing
    driver.execute_script("""
    var setValue = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
    var element = arguments[0];
    var value = arguments[1];
    
    setValue.call(element, value);
    
    var event = new Event('input', { bubbles: true });
    element.dispatchEvent(event);
    """, element, value)

def answer_questions():
    global counter
    # Radio-buttons and Checkboxes bypass:
    try:
        # Find all the UL containers (Modify the selector as per your needs)
        ul_containers = driver.find_elements(By.XPATH, '//div[@data-qa="task-body"]/ul')

        # Iterate over each UL container
        for ul in ul_containers:
            # Find all radio buttons and checkboxes within the current UL
            input_elements = ul.find_elements(By.XPATH, './/input[@type="radio" or @type="checkbox"]')

            # Click the last input element in the list
            if input_elements:
                driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", input_elements[-1])
    except:
        pass
    
    # fill in all text areas with the portfolio links from the links-list.txt file:
    try: 
        test_questions_presence = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-qa="task-body"]//textarea')))
        if test_questions_presence: 
            try:
                questions = driver.find_elements(By.XPATH, '//div[@data-qa="task-body"]//textarea')
                for question in questions:
                    set_value_with_event(question, answer)
                
                submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-submit-popup"]')))
                driver.execute_script("arguments[0].removeAttribute('disabled')", submit_button) #remove 'disabled' attribute
                action.click(submit_button).perform()
                time.sleep(3)
                try:
                    error = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="bloko-translate-guard"]')))
                    if error: return Status.SUCCESS # resume submitted but there was a server error. Just try this specific job the next time!
                except:
                    pass
                # wait until submitted to the server: 
                wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="vacancy-actions_responded"]')))
                counter += 1
                return Status.SUCCESS
            except:
                return Status.FAILURE
    except:
        return Status.FAILURE
    
def fill_in_cover_letter(message):
    global counter
    scroll_to_bottom()
    try:
        cover_letter_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-letter-toggle"]')))
        driver.execute_script("arguments[0].click()", cover_letter_button)
        
        cover_letter_text = wait.until(EC.element_to_be_clickable((By.XPATH, '//form[@action="/applicant/vacancy_response/edit_ajax"]/textarea')))
        set_value_with_event(cover_letter_text, message)
        
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="vacancy-response-letter-submit"]')))
        driver.execute_script("arguments[0].removeAttribute('disabled')", submit_button) #remove 'disabled' attribute
        action.click(submit_button).perform()
        time.sleep(3)
        try:
            error = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="bloko-translate-guard"]')))
            if error: return Status.SUCCESS # resume submitted but there was a server error. Just try this specific job the next time!
        except:
            pass
        #wait until submitted to the server:
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-qa="vacancy-response-letter-informer"]')))
        counter += 1
        return Status.SUCCESS
    except:
        return Status.FAILURE
    
def click_all_jobs_on_the_page():
    global counter
    scroll_to_bottom()
    #wait for the page to load dynamically
    eternal_wait(driver, 10, EC.presence_of_element_located, (By.XPATH, '//div[@data-qa="vacancies-search-header"]'))
    try:
        job_links = custom_wait(driver, 10, EC.presence_of_all_elements_located, (By.XPATH, '//a[contains(., "Откликнуться")]'))
    except:
        return Status.FAILURE
    
    for link in job_links:
        a = link.get_attribute('href')
    # for i in range(1): # this line is for debug
    #     a = "https://hh.ru/applicant/vacancy_response?vacancyId=85935747" # this line is for debug, comment out two lines above to test a specific job application
        
        # Open a new window
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(a) 
        time.sleep(3)
        international_ok() # the problematic code to click the international popup  
        
        # get the company name and the job title, attach them to Your message
        try:
            company_name = custom_wait(driver, 10, EC.presence_of_element_located, (By.XPATH, '//a[@data-qa="vacancy-company-name"]')).text
        except:
            pass
        try:
            vacancy_title = custom_wait(driver, 10, EC.presence_of_element_located, (By.XPATH, '//h1[@data-qa="vacancy-title"]')).text
        except:
            pass
        if company_name and vacancy_title:
            customized_message = f"Здравствуйте, {company_name}!\nПрошу рассмотреть мою кандидатуру на вакансию\n«{vacancy_title}».\n\n{MESSAGE}"
        elif company_name:
            customized_message = f"Здравствуйте, {company_name}!\n\n{MESSAGE}"
        elif vacancy_title:
            customized_message = f"Здравствуйте!\nПрошу рассмотреть мою кандидатуру на вакансию\n«{vacancy_title}».\n\n{MESSAGE}"
        else: customized_message = MESSAGE
        
        if fill_in_cover_letter(customized_message) == Status.SUCCESS:
            driver.close()
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])
            continue
        elif check_cover_letter_popup(customized_message) == Status.SUCCESS:
            driver.close()
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[0])
            continue
        else:  
            try:
                answer_questions()
                driver.close()
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                continue
                
            except: # something is off with the page, just switch to the next dream job in the list 
                driver.close()
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[0])
                continue

def clear_region():
    try:
        clear_region_buttons = custom_wait(driver, 10, EC.presence_of_all_elements_located, (By.XPATH, '//button[@data-qa="bloko-tag__cross"]'))
        for button in clear_region_buttons:
            js_click(driver, button)
    except:
        return #exit the function

def advanced_search():
    # this makes sure the user is logged in first!
    advanced_search_button = eternal_wait(driver, 10, EC.element_to_be_clickable, (By.XPATH, '//a[@data-qa="advanced-search"]'))
    
    js_click(driver, advanced_search_button)
    
    # waiting for the new page to load
    advanced_search_textarea = eternal_wait(driver, 10, EC.element_to_be_clickable, (By.XPATH, '//input[@data-qa="vacancysearch__keywords-input"]'))
    advanced_search_textarea.send_keys(JOB_SEARCH_QUERY)

    if REGION == "global":
        clear_region()
        #enable if you want to select certain countries, right now it selects ALL countries by default:
        #select_all_countries()
    
    try:
        exclude_these_results = custom_wait(driver, 10, EC.element_to_be_clickable, (By.XPATH, '//input[@name="excluded_text"]'))
        exclude_these_results.send_keys(EXCLUDE) # the text is long and JS is not working, a place for optimization
    except:
        pass
    
    try:
        no_agency = custom_wait(driver, 5, EC.element_to_be_clickable, (By.XPATH, '//input[@data-qa="advanced-search__label-item-label_not_from_agency"]'))
        js_click(driver, no_agency)
    except:
        pass
    
    salary = custom_wait(driver, 10, EC.element_to_be_clickable, (By.XPATH, '//input[@data-qa="advanced-search-salary"]'))
    salary.send_keys(MIN_SALARY)
    
    if ONLY_WITH_SALARY:
        salary_only_checkbox = custom_wait(driver, 10, EC.element_to_be_clickable, (By.XPATH, '//input[@name="only_with_salary"]'))
        js_click(driver, salary_only_checkbox)

    quantity = driver.find_element(By.XPATH, '//input[@data-qa="advanced-search__items_on_page-item_100"]')
    js_click(driver, quantity)

    advanced_search_submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="advanced-search-submit-button"]')))
    js_click(driver, advanced_search_submit_button) # there is an eternal_wait inside click_all_jobs_on_the_page() function right after that click!

def main():
    global counter

    check_cookies_and_login()
    advanced_search()
    
    while counter < 200: #there is a limit of 200 resumes per day on hh.ru
        if click_all_jobs_on_the_page() == Status.FAILURE:
            os.system("cls") #clear screen from unnecessary logs since the operation has completed
            print("It's either the hh.ru server has become undresponsive or all the links within the current search query have been clicked. \n 1) check if hh.ru is alive and responsive \n 2) check if you have clicked all the links available for the job search query. In that case, change the 'JOB_SEARCH_QUERY = ' value. \n \n Sincerely Yours, \n NAKIGOE.ORG\n")
            driver.close()
            driver.quit()

        # Switch back to the first tab with search results
        driver.switch_to.window(driver.window_handles[0])

        try:
            #take in another hundred of results:
            next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@data-qa="pager-next"]')))
            driver.execute_script("arguments[0].click()", next_page_button)
        except:
            os.system("cls") #clear screen from unnecessary logs since the operation has completed successfully
            print("It's either the hh.ru server has become undresponsive or all the links within the current search query have been clicked. \n 1) check if hh.ru is alive and responsive \n 2) check if you have clicked all the links available for the job search query. In that case change the 'JOB_SEARCH_QUERY = ' value. \n \n Sincerely Yours, \n NAKIGOE.ORG\n")
            driver.close()
            driver.quit()

    # Close the only tab, will also close the browser.
    os.system("cls") #clear screen from unnecessary logs since the operation has completed
    print("Congratulations!\n The script has completed successfully in one go!!! You've sent 200 resumes today, that is currently a limit on HH.RU\n Come again tomorrow! \n \n Sincerely Yours, \n NAKIGOE.ORG\n")

main() #run the script, starting from the main function