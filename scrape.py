#   Yash Parag Butala
#   27-Nov-2020
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import MySQLdb
from bs4 import BeautifulSoup
import time

#database details. Dumped to MySQL
HOST = "localhost"      
USERNAME = "root"
PASSWORD = ""
DATABASE = "scrape_data"

d = webdriver.Firefox()
d.get('https://www.investing.com/equities/tata-consultancy-services-historical-data')
try:  #attempt to dismiss banners that could block later clicks
    WebDriverWait(d, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".closer"))).click()
    d.find_element_by_css_selector('.closer').click()
except:
    pass
d.find_element_by_id('widgetFieldDateRange').click() #show the date picker
sDate  = d.find_element_by_id('startDate')  # set start date input element into variable
sDate.clear()                               #clear existing entry
sDate.send_keys('04/01/2016')               #add custom entry
eDate = d.find_element_by_id('endDate')     #repeat for end date
eDate.clear()
eDate.send_keys('11/27/2020')
d.find_element_by_id('applyBtn').click()    #submit changes
time.sleep(10)                              #wait for page to reload after clicking the button
num_rows = len (d.find_elements_by_xpath("//*[@id='curr_table']/tbody/tr"))         #get dimenions of the table.  
num_cols = len (d.find_elements_by_xpath("//*[@id='curr_table']/tbody/tr[2]/td"))   #Id of the table is 'curr_table' which is found by inspect element

date = []           
price = []
print(num_rows,num_cols)
#tore date and prices as list.
for i in range(1,num_rows):
	c1 = d.find_element_by_xpath("//*[@id='curr_table']/tbody/tr["+str(i)+"]/td[1]").text
	c2 = d.find_element_by_xpath("//*[@id='curr_table']/tbody/tr["+str(i)+"]/td[2]").text
#	print(c1,c2)
	date.append(c1)
	price.append(c2)


#connect to db and dump data
db = MySQLdb.connect(HOST, USERNAME, PASSWORD, DATABASE)
query="INSERT INTO tcs(date,price) VALUES(%s,%s)"
cursor = db.cursor()
for i in range(len(date)):
    cursor.execute(query,(str(date[i]),str(price[i])))
    db.commit()

print('done')
