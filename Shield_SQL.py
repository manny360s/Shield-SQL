from selenium import webdriver
from time import sleep
import requests
import time

# Makes Text Type Slow
def slow_type(text, delay=0.1):
    for character in text:
        print(character, end='', flush=True)
        time.sleep(delay)
    print()
 
def scanAll(URL,value):
    scanURL(URL)
    scanForm(URL,value)
# Scans The URL For Sql Vulnerability
def scanURL(URL):
    # Malicious Characters Being added to the URL
    injections = ["\"'"]
    for injection in injections:
        r = requests.get(URL + injection)
    # Vulnerability Check
        if r.status_code == 200 and "SQL" in r.text:
            res = print(f"SQL Injection Vulnerability Found In Url In {URL}")
            return res
    res = print("Vulnerability Not Found In URL")
    return res
# Scans The Form For Sql Vulnerability     
def scanForm(URL,value):
    if value == "N/A":
        return 
    # Web Driver That Makes A Demo Website
    driver = webdriver.Chrome()
    driver.get(URL)
    input_list = []
    # Searchs For All Forms And Inputs
    login_inputs = driver.find_elements('css selector','input[type="text"], input[type="password"], input[type="email"]')
    try:
        # Figures Out If There Is Any Forms Or Inputs
        for input_elem in login_inputs:
            input_id = input_elem.get_attribute("id")  
            input_list.append(input_id)
        if not input_list:
            res = print("No input forms found on the page, or company has hidden forms")
            return res
        else:
            #Prints Malicious Characters Into Forms
            for c in "\"'", "admin' -":
                for input in input_list:
                    elem = driver.find_element('css selector',f'#{input}')
                    elem.send_keys(c)
                # Finds The Submit Button And Clicks It
                elem = driver.find_element('css selector', f'input[type="submit"][value="{value}"]')
                elem.click()
                sleep(5.0)
                 # Vulnerability Check
                paragraphs = driver.find_elements('css selector', "p")
                for paragraph in paragraphs:
                     if "Syntax error" or "you have an error in your sql syntax;" or "warning: mysql" in paragraph.text:
                        res = print(f"SQL Injection Vulnerability Found in Form of {URL}")
                        return res
    except:
        res = print("Vulnerability Not Found In Form")        
        driver.quit()
        return res

if __name__ == "__main__":
    slow_type("Welcome To Sheild SQL", 0.05)
    slow_type("Please Enter The URL You Want To Scan:", 0.05)
    URL = str(input(""))
    slow_type("Now Enter The Name Of The Submit Button (Ex: Login)", 0.05)
    slow_type("Also If You're Just Testing The URL Enter N/A:", 0.05)
    value = str(input(""))
    scanAll(URL,value)