# from selenium import webdriver
from selenium import webdriver

from time import sleep 
# browser = webdriver.Safari()

from selenium import webdriver

from time import sleep 
from selenium.webdriver.firefox.options import Options


from collections import deque

lt_iit = deque([])
lt_nit = deque([])
lt_iiit = deque([])


lt_queue = [lt_iit,lt_nit,lt_iiit]

global_list = []

# lt_iiit.append("arun")
# lt_nit.append("manish")
# lt_iit.append("maqsood")

link_iit = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=iit"
link_nit = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=nit"
link_iiit = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=iiit"


link_list= [link_iit ,link_nit,link_iiit]

list_bool = [True,True,True]
options = Options()
# options.headless = True
browser = webdriver.Firefox(options=options)
# browser.get(link_iit)


def parsing(link_index):
	browser.get(link_list[link_index])
	#run scrape code and fill the list by appending list_queue[list_index]

	# def get_list():
	try:
		if browser.find_element_by_class_name('gs_btnPR'):
			browser.find_element_by_class_name('gs_btnPR').click()
			sleep(1)
	except NoSuchElementException:
		list_bool[list_index] = False

	link_list[link_index] = browser.current_url



#code to fill global_list


def fill_global_list():
	if global_list>0:
		return global_list
	while len(global_list)<10:

		if len(lt_queue[0])>0:

			iiit = lt_queue[0].popleft()
			global_list.append(iiit)

		if len(lt_queue[1])>0:
			nit = lt_queue[1].popleft()
			global_list.append(nit)

		if len(lt_queue[2])>0:
			iit = lt_queue[2].popleft()
			global_list.append(iit)

		if len(lt_queue[0])<=0 and len(lt_queue[1])<=0 and len(lt_queue[2])<=0:
			break

	if len(lt_queue[2])<=0:
		if list_bool[2]==True:
			parsing(2)

	if len(lt_queue[0])<=0:
		if list_bool[0]==True:
			parsing(0)

	if len(lt_queue[1])<=0:
		if list_bool[1]==True:
			parsing(1)

	if len(global_list)<=0:
		fill_global_list()

	if True not in list_bool and (len(lt_queue[0])<=0 and len(lt_queue[1])<=0 and len(lt_queue[2])<=0):
		return None

	return global_list






print(global_list)


browser.quit()



# from time import sleep 
# from selenium.webdriver.firefox.options import Options
# from selenium.common.exceptions import NoSuchElementException  

# options = Options()
# # options.headless = True
# # browser = webdriver.Safari()

# # op = webdriver.ChromeOptions()
# # op.add_argument('headless')
# link = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=iit"
# browser = webdriver.Firefox(options=options)
# browser.get(link)
# # browser.maximize_window()

# # sample = "deep learning"
# # browser.find_element_by_id("keywords").send_keys(sample)
# while True:
# 	try:
# 		if browser.find_element_by_class_name('gs_btnPR'):
# 			browser.find_element_by_class_name('gs_btnPR').click()
# 			sleep(1)
# 	except NoSuchElementException:
# 		break

# # finally:

# browser.quit() 