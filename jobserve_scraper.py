from select import select
from turtle import position
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time

# , wfh_only

def get_jobs(keywords):

    browser = webdriver.Edge()
    browser.maximize_window() # For maximizing window
    browser.implicitly_wait(20)
    browser.get("https://www.jobserve.com/gb/en/Job-Search/")
    jobs = []
    
    # fill in keywords search box
    keywords_field = browser.find_element(By.NAME, "ctl00$main$srch$ctl_qs$txtKey")
    keywords_field.send_keys(keywords)
    

    # select location Within 100 miles
    mile_field = Select(browser.find_element(By.ID, "selRad"))
    mile_field.select_by_visible_text('Within 100 miles')

    # search
    search_click = browser.find_element(By.NAME, "ctl00$main$srch$ctl_qs$btnSearch")
    search_click.click()

    ## Job page ##
    
    #Filter out jobs with no salary/rate recorded

    browser.find_element(By.XPATH, "//*[@id='CHECKBOXSAL1']").click()
    browser.find_element(By.XPATH, "//*[@id='CHECKBOXSAL11']").click()
    browser.find_element(By.XPATH, "//*[@id='refinebutton']").click()


    # Going through each job
    
    jobs = browser.find_element_by_tag_name("html")
    jobs_data = []
    
    results_num = browser.find_element(By.XPATH, "//span [@ class='resultnumber']").text
    results_num = int(results_num.replace(',',''))
    
    i = 0
     
    while i <= 500:
        
        try:
            position = browser.find_element(By.XPATH, "//a [@ id='td_jobpositionlink']").get_attribute("textContent")
            contract = browser.find_element(By.XPATH, "//span[@ id='td_job_type']").get_attribute("textContent")
            rate = browser.find_element(By.XPATH, "//*[@id='md_rate']").get_attribute("textContent")
            location = browser.find_element(By.XPATH, "//span[@ id='md_location']").get_attribute("textContent")
            recruiter = browser.find_element(By.XPATH, "//span[@ id='md_recruiter']").get_attribute("textContent")
            reference = browser.find_element(By.XPATH, "//span[@ id='md_ref']").get_attribute("textContent")
            description = browser.find_element(By.XPATH, '//*[@id="md_skills"]').get_attribute("textContent")
        except (NoSuchElementException, StaleElementReferenceException):
            pass       

                
        data = {'Position': position,
                'Job Type': contract,
                'Rate': rate,
                'Location': location,
                'Recruiter': recruiter,
                'Reference': reference,
                'Description':description
        }
                

        jobs_data.append(data)
                            
        jobs.send_keys(Keys.DOWN)
        browser.implicitly_wait(20)
        time.sleep(1)
           
        #print(jobs_data)

        i += 1
        print(i)
        
    return pd.DataFrame(jobs_data)

    



    #job_list = browser.find_element(By.CLASS_NAME, "jobItem")
    #for job in range(0, len(job_list)):
    #    if job_list.is_displayed():
    #        job_list.click()

    #'Industry': browser.find_element(By.ID, "md_industry").text,
    #            'Rate': browser.find_element(By.ID, "md_rate").text}