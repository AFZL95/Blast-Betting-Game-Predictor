from selenium import webdriver
from datetime import datetime
import time

browser=webdriver.Chrome(r"C:\Users\FZL\Desktop\Blast Betting Game Predictor\Dependencies\chromedriver.exe")


#go to site
browser.get("http://1fifa90.com/games/crash/index")

#login
time.sleep(5)
browser.find_element_by_id("mail").send_keys("onlyfbaccount@gmail.com")
browser.find_element_by_id("pass").send_keys("P566XN7xJCybsT9tgkSv")
time.sleep(2)
browser.find_element_by_class_name("action-button").click()
time.sleep(10)
browser.find_element_by_id("play_button").click()
time.sleep(5)
browser.find_element_by_class_name("lang_67").click()
time.sleep(3)

def writeToHistoryFile(recordList):
	with open("C:\\Users\FZL\Desktop\Blast Betting Game Predictor\First things First (Data Collecting)\history.csv","a") as myfile:
		for eachColumn in recordList:
			myfile.write(eachColumn+",")
		myfile.write("\n")
	
def checkForFirstLine(firstRecord):
	aa=[]
	while str(firstRecord.text).split("\n")[0]=="-":
		time.sleep(2)
		
	# if str(firstRecord.text).split("\n")[0]!="-":
	return (list([str(datetime.now())]+str(firstRecord.text).split("\n")))
	# else:
		# time.sleep(2)
		# return checkForFirstLine(firstRecord)


history=[]
aa=[]
recordRows=browser.find_elements_by_xpath("//div[contains(@class,'table-body')]/div[contains(@class,'crash-row')]")
for eachRow in recordRows[1:]:
	if str(eachRow.text).split("\n")[0]!="-":
		history.append([str(datetime.now())]+str(eachRow.text).split("\n"))

for eachRecrod in reversed(history):
	writeToHistoryFile(eachRecrod)	
	
while 1:
	firstRecord = browser.find_element_by_xpath("//div[contains(@class,'table-body')]/div[contains(@class,'crash-row')]")
	newRecord=checkForFirstLine(firstRecord)
	print((newRecord))
	writeToHistoryFile(newRecord)
	time.sleep(5)
	try:
		browser.find_element_by_xpath('//*[@id="disconnect_screen"]/table/tbody/tr/td/center/a').click()
		time.sleep(10)
		browser.find_element_by_id("play_button").click()
		time.sleep(5)
		browser.find_element_by_class_name("lang_67").click()
		time.sleep(3)	
	except:
		pass

