from selenium import webdriver
import time  
from selenium.webdriver.common.keys import Keys 
import chromedriver_binary
from selenium.webdriver.common.by import By
import pymongo
import datetime


client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['freight_provider']
collection = db['test_scrap_data']


def data_set_none(database_data):
    if 'name' not in database_data:
        database_data["name"]=None

    if 'ratings' not in database_data:
        database_data["ratings"]=None

    if 'address' not in database_data:
        database_data["address"]=None

    if 'mobile' not in database_data:
        database_data["mobile"]=None

    if 'website' not in database_data:
        database_data["website"]=None

    if 'shortaddress' not in database_data:
        database_data["shortaddress"]=None
    
    if 'claim' not in database_data:
        database_data["claim"]=None

    return database_data

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://www.google.com/maps/search/near+me+freight+provider")

while True:
    main_box = driver.find_elements(by=By.CLASS_NAME, value="a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd")
    print(len(main_box))
    print(main_box)
    main_box[0].click()
    time.sleep(5)
    list_box = driver.find_elements(by=By.CLASS_NAME, value="Ymd7jc")
    k=0
    for list_element in list_box:
        database_data = {}
        print(k)
        try:
            list_element.click()
            time.sleep(3)
            get_name = driver.find_elements(by=By.CLASS_NAME, value="x3AX1-LfntMc-header-title-title")
            for element in get_name:
                if element.is_displayed():
                    print(element.text)
                    database_data["name"]=element.text
                    print("h1", database_data)
            # validation for dulicate
            fined_name = collection.find_one({'name':element.text})
            if fined_name:
                print("h1")
                pass
            else:
                print("h2")
                get_address = driver.find_elements(by=By.CLASS_NAME, value='CsEnBe')
                print("h3",len(get_address))
                for i in range(len(get_address)):
                    # Get all Data in same class For example address, mobile, website, claim
                    data = get_address[i].get_attribute('aria-label')
                    # split all data in ':'
                    split_data = data.split(": ")
                    
                    if 'Address'in split_data:
                        database_data["address"]=split_data[1]

                    elif 'Phone' in split_data:
                        print(split_data[1])
                        split_data[1]=split_data[1].replace(" ", "")
                        database_data["mobile"]=split_data[1]

                    elif 'Website' in split_data:
                        split_data[1]=split_data[1].strip()
                        database_data["website"]=split_data[1]

                    elif 'Plus code' in split_data:
                        database_data["shortaddress"]=split_data[1]

                    elif 'Claim this business' in split_data:
                        database_data["claim"]='Claim this business'
                
                get_rating = driver.find_elements(by=By.CLASS_NAME, value='aMPvhf-fI6EEc-KVuj8d')
                for element in get_rating:
                    if element.is_displayed():
                        print(element.text)
                        database_data["ratings"]=element.text
                
                database_data = data_set_none(database_data)
                
                print(database_data)
                collection.insert_one(database_data)
            k+=1
        except Exception as e:
            pass
            k+=1

    get_name = driver.find_elements(by=By.CLASS_NAME, value="xoLGzf-LgbsSe")
    get_name[0].click()
    time.sleep(2)

    next_btn = driver.find_elements(by=By.ID, value="ppdPk-Ej1Yeb-LgbsSe-tJiF1e")
    try:
        next_btn[0].click()
        time.sleep(2)
    except:
        break


