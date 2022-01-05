from django.shortcuts import render
from .models import QueryForm
from .models import Authors
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from collections import deque


import aiohttp
import asyncio
import bs4
import re
# from http import requests
from pandas import read_excel
from function import *

from selenium import webdriver

from time import sleep 
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException  

authIdForHTML = []
linksForHTML = []
namesForHTML = []
pfpLinksForHTML = []
emailsForHTML = []
affiliationsForHTML = []
citationsForHTML = []
lt_iit = deque([])
lt_nit = deque([])
lt_iiit = deque([])
link_list = []
list_bool = [True,True,True]

base_url = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="
sort_by_date = False

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)

# Create your views here.
def home(request):
    return render(request, 'index.html')

@csrf_exempt
def first_page(request):
    Authors.objects.all().delete()
    # if(not browser):
    #     browser.quit()
    field = request.POST['fieldSearch']
    return crawler_run(request, str(base_url+field))

# def next_page(request):
#     if browser.find_element_by_class_name('gs_btnPR'):
#             browser.find_element_by_class_name('gs_btnPR').click()
#     return crawler_run(request, browser.current_url)



def sort_papers(request, id, link):

    author = Authors.objects.get(author_id=id)
    Link = link

    global name,affiliation,email,img_link,citations,lt


    async def fetch_all_data(url):

        global name, citations, img_link, email, affiliation, lt


        async with aiohttp.ClientSession() as session:

            async with session.get(url) as response:

                # name = url[to_cut:]

                status = response.status
                response = await response.text()

                if status == 429:
                    print("too many request to server , error code : 429")

                # if verbose:
                #     print(response, status)


                soup = bs4.BeautifulSoup(response , 'html.parser')

                name  = soup.find("div" , {'id' : 'gsc_prf_in'}).get_text()
                affiliation = soup.find("div" ,{'class' : 'gsc_prf_il'}).get_text()
                email = soup.find("div" , {'id':'gsc_prf_ivh'}).get_text()
                email = email[len("Verified email at "):]
                img = soup.find("div" , {'id' : 'gsc_prf_pua'})
                img_ = img.find("img")
                img_link = str(img_["src"])
                if(img_link[5]!=':'):
                    img_link = "https://scholar.google.com"+img_link 
                print('img' , img_link)
                citations = soup.find("td" , {'class' :'gsc_rsb_std'}).get_text()
                print("name_tag" , name)
                print("affiliation" , affiliation)
                print("email" , email)
                print('citations' , citations)

                lt = []

                table  = soup.find("table" , {'id' : 'gsc_a_t'})
                # list_ = table.find_all('td')

                list_ = soup.find_all("a" , {'id' , "gsc_a_at"})

                for it in list_:

                    lt.append(it.get_text())


                print(lt)



                

    def print_all_pages():

        # f = init_file()

        # pages = create_links(n)

        tasks = []
        loop = asyncio.new_event_loop()

        try:
            

            tasks.append(loop.create_task(fetch_all_data(Link)))

            loop.run_until_complete(asyncio.wait(tasks))

        except KeyboardInterrupt:

            print("Program Terminated by User")

            print("<---Bye--->")

        loop.close()
        # close_file(f)

    print_all_pages()

    context = {'id': id, 'name' : name, 'affiliation' : affiliation, 'email' : email, 'citations' : citations, 'img_link' : img_link, 'list': lt}

    return render(request, 'profile.html', context)        



def create_profile(request, id):
    sort_ = "&view_op=list_works&alert_preview_top_rm=2&sortby=pubdate"
    author = Authors.objects.get(author_id=id)
    if(sort_by_date):
        link = str(author.link) + sort_
    else:
        link = str(author.link)
    return sort_papers(request, id, link)

def profile_check(request, id):
    global sort_by_date
    sort_by_date = not sort_by_date
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def crawler_run(request, searchLink):
    ind=0
    # field = input()
    ID = 0
    # field = request.POST['fieldSearch']
    # global browser
    nameList = []
    web_site = 'https://scholar.google.com/'
    base_url = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="
    to_cut = len(base_url)
    def download_subpage(link):
        r1=requests.get(web_site + link)
        return r1.text


    def data_not_available(url ):
        print("Data not available for " +str(url))
    # def create_links():
    #     return base_url+field

    async def find_and_extract_data_name(soup):

        central_table = soup.find(id = "gsc_prf_w")
        description = central_table.find("div" , {'class' : "gsc_prf_il"})
        fields = []

        for field in central_table.find("div" , {'class' : "gsc_prf_il" , 'id' : "gsc_prf_int"} ).contents:
            if isinstance(field , bs4.element.NavigableString):
                continue

            if isinstance(field , bs4.element.Tag):
                fields.append(field.text)

        corner_table = soup.find("div",{"class":"gsc_rsb_s gsc_prf_pnl"})

        try:
            # num_cit_index = list(corner_table.find_all("td" , {"class":"gsc_rsb_std"}))
            num_cit_index=list(corner_table.find_all("td", {"class":"gsc_rsb_std"}))
            hist = corner_table.find("div" , {"class":"gsc_md_hist_b"}).contents

        except:
            raise ValueError


        for i in range(len(hist)):
            if isinstance(hist[i] , bs4.element.Tag):
                hist.append(hist[i])

        num_cit = num_cit_index[0].text
        h_index = num_cit_index[2].text
        ii0_index = num_cit_index[4].text
        n6 = hist[-6].text
        n5 = hist[-5].text
        n4 = hist[-4].text
        n3 = hist[-3].text
        n2 = hist[-2].text
        n1 = hist[-1].text
        Data = [num_cit , h_index , ii0_index , fields , n6,n5,n4,n3,n2,n1]
        return Data


    def create_linksName(x):

        all = []

        URL = base_url
        for a in x:
            URL += a + "+"



        return URL[:len(URL)-1]


    async def fetch_all_data(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                name = url[to_cut:]
                status = response.status

                response = await response.text()
                soup = bs4.BeautifulSoup(response , 'html.parser')

                for tag in  soup.find_all("h3" , {'class' : 'gs_ai_name'}):
                    # print(tag.text)
                    name = [x for x in str(tag.text).split()]
                    print(name)
                    namesForHTML.append(' '.join([str(e) for e in name]))
                    nameList.append(create_linksName(name))
                    

    async def fetch_all_data_name(url):



        async with aiohttp.ClientSession() as session:

            async with session.get(url) as response:
                global authIdForHTML
                global linksForHTML
                

                name = url
            
                status = response.status
                response = await response.text()

                if status == 429:
                    print("too many request to server , error code : 429")

                soup = bs4.BeautifulSoup(response , 'html.parser')

                result = soup.find("h3" , {'class' : 'gs_ai_name'})

                if result is None:

                    data_not_available(f,name)
                else :

                    link = result.find('a' , href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
                    linksForHTML.append("https://scholar.google.com"+str(link))
                    print("LINK:  " + "https://scholar.google.com"+str(link))
                

                    L = []

                    async with session.get(web_site+link) as subresponse:
                        
                        global namesForHTML
                        global pfpLinksForHTML
                        global emailsForHTML
                        global affiliationsForHTML
                        global citationsForHTML
                        print("request: " + name + " with status: " + str(subresponse.status))

                        html = await subresponse.text()
    
                        soup = bs4.BeautifulSoup(html ,'html.parser')
                        Data = await find_and_extract_data_name(soup)
                        # soup = bs4.BeautifulSoup(download_subpage(link), 'html.parser')
                        print(Data, "Data")
                        central_table=soup.find(id="gsc_prf_w")
                        img=central_table.find(id="gsc_prf_pup-img")
                        pimg = img["src"]
                        pfpLinksForHTML.append(pimg)

                        affiliation = soup.find("div" ,{'class' : 'gsc_prf_il'}).get_text()
                        email = soup.find("div" , {'id':'gsc_prf_ivh'}).get_text()
                        email = email[len("Verified email at "):]
                        img = soup.find("div" , {'id' : 'gsc_prf_pua'})
                        img_ = img.find("img")
                        gimg = str(img_["src"])
                        citations = soup.find("td" , {'class' :'gsc_rsb_std'}).get_text()

                        print("hello "+email)
                        print(affiliation)
                        emailsForHTML.append(email)
                        citationsForHTML.append(citations)
                        affiliationsForHTML.append(affiliation)

                        # affiliation = [affiliation.split(" ")]
                        # for a in affiliation:
                        #     if a.uppercase

            


    def print_all_pages(url):
        # pages = create_links()
        tasks = []
        names = []
        # print(pages)
        loop = asyncio.new_event_loop()

        try:

            tasks.append(loop.create_task(fetch_all_data(url)))

            loop.run_until_complete(asyncio.wait(tasks))

        except KeyboardInterrupt:

            print("Program Terminated by User")

            print("<---Bye--->")

        loop.close()

        loop = asyncio.new_event_loop()

        try:
            for page in nameList:

                names.append(loop.create_task(fetch_all_data_name(page)))


                loop.run_until_complete(asyncio.wait(names))

        except KeyboardInterrupt:

            print("Program Terminated by User")

            print("<---Bye--->")

        loop.close()
    
    # browser.get(searchLink)
    
    global lt_iit 
    global lt_nit 
    global lt_iiit


    lt_queue = [lt_iit,lt_nit,lt_iiit]

    global_list = []

    # lt_iiit.append("arun")
    # lt_nit.append("manish")
    # lt_iit.append("maqsood")

    link_iit = searchLink + " iit"
    link_nit = searchLink + " nit"
    link_iiit = searchLink + " iiit"

    global link_list
    link_list= [link_iit, link_nit, link_iiit]
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    global list_bool
    # global browser
    # options = Options()
    # options.headless = True
    # browser = webdriver.Firefox(options=options)
    # browser.get(link_iit)


    def parsing(link_index):
        # global browser
        browser.get(link_list[link_index])
        #run scrape code and fill the list by appending list_queue[list_index]
        print_all_pages(link_list[link_index])
        dataList = zip(namesForHTML, linksForHTML, pfpLinksForHTML, emailsForHTML, affiliationsForHTML, citationsForHTML)
        # print("hihsaidhasihdihsai", set(dataList))
        lt_queue[link_index] = deque(dataList)
        print(lt_queue[link_index])
        # def get_list():
        try:
            if browser.find_element_by_class_name('gs_btnPR'):
                browser.find_element_by_class_name('gs_btnPR').click()
                sleep(1)
        except NoSuchElementException:
            list_bool[link_index] = False

        link_list[link_index] = browser.current_url



    #code to fill global_list


    def fill_global_list():
        # print("hiehello",lt_queue)
        if len(global_list)>0:
            return global_list
        while len(global_list)<10:

            if len(lt_queue[0])>0:

                iit = lt_queue[0].popleft()
                print("IIT: ",iit)

                global_list.append(iit)

            if len(lt_queue[1])>0:
                nit = lt_queue[1].popleft()
                print("NIT: ",nit)

                global_list.append(nit)

            if len(lt_queue[2])>0:
                iiit = lt_queue[2].popleft()
                print("IIIT: ",iiit)
                global_list.append(iiit)

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

        if True not in list_bool or (len(lt_queue[0])<=0 and len(lt_queue[1])<=0 and len(lt_queue[2])<=0):
            return None

        else:
            return global_list




    fill_global_list()

    print("helloooooooooooooooooooo", global_list)


    # browser.quit()

    # print_all_pages(searchLink)

    # for x in range(len(namesForHTML)):
    #     authIdForHTML.append(x)

    # dataList = zip(namesForHTML, linksForHTML, pfpLinksForHTML, emailsForHTML, affiliationsForHTML, citationsForHTML)
    
    # print(emailsForHTML)
    # print(citationsForHTML)
    # print("hhihihihihihi",dataList)
    
    for name, plink, pfplink, email, affiliation, citations in global_list :
            Authors.objects.create(author_name = name, link = plink, pfp_link = pfplink, email = email, affiliation = affiliation, citations = citations)

    # authIdForHTML = list(Authors.objects.values_list('author_id', flat=True))
    # authIdForHTML = authIdForHTML[:10][::-1]
    dataList = Authors.objects.all()
    dataList = dataList[:10][::-1]
    print(dataList)
    
    # dataList = zip(authIdForHTML, namesForHTML, linksForHTML, pfpLinksForHTML, emailsForHTML, affiliationsForHTML, citationsForHTML)
    

    return render(request, "results.html", context={'dataList':dataList})

def next_page(request):
    global_list = []
    ind=0
    # field = input()
    ID = 0
    # field = request.POST['fieldSearch']
    nameList = []
    web_site = 'https://scholar.google.com/'
    base_url = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="
    to_cut = len(base_url)
    def download_subpage(link):
        r1=requests.get(web_site + link)
        return r1.text


    def data_not_available(url ):
        print("Data not available for " +str(url))
    # def create_links():
    #     return base_url+field

    async def find_and_extract_data_name(soup):

        central_table = soup.find(id = "gsc_prf_w")
        description = central_table.find("div" , {'class' : "gsc_prf_il"})
        fields = []

        for field in central_table.find("div" , {'class' : "gsc_prf_il" , 'id' : "gsc_prf_int"} ).contents:
            if isinstance(field , bs4.element.NavigableString):
                continue

            if isinstance(field , bs4.element.Tag):
                fields.append(field.text)

        corner_table = soup.find("div",{"class":"gsc_rsb_s gsc_prf_pnl"})

        try:
            # num_cit_index = list(corner_table.find_all("td" , {"class":"gsc_rsb_std"}))
            num_cit_index=list(corner_table.find_all("td", {"class":"gsc_rsb_std"}))
            hist = corner_table.find("div" , {"class":"gsc_md_hist_b"}).contents

        except:
            raise ValueError


        for i in range(len(hist)):
            if isinstance(hist[i] , bs4.element.Tag):
                hist.append(hist[i])

        num_cit = num_cit_index[0].text
        h_index = num_cit_index[2].text
        ii0_index = num_cit_index[4].text
        n6 = hist[-6].text
        n5 = hist[-5].text
        n4 = hist[-4].text
        n3 = hist[-3].text
        n2 = hist[-2].text
        n1 = hist[-1].text
        Data = [num_cit , h_index , ii0_index , fields , n6,n5,n4,n3,n2,n1]
        return Data


    def create_linksName(x):

        all = []

        URL = base_url
        for a in x:
            URL += a + "+"



        return URL[:len(URL)-1]


    async def fetch_all_data(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                name = url[to_cut:]
                status = response.status

                response = await response.text()
                soup = bs4.BeautifulSoup(response , 'html.parser')

                for tag in  soup.find_all("h3" , {'class' : 'gs_ai_name'}):
                    # print(tag.text)
                    name = [x for x in str(tag.text).split()]
                    print(name)
                    namesForHTML.append(' '.join([str(e) for e in name]))
                    nameList.append(create_linksName(name))
                    

    async def fetch_all_data_name(url):



        async with aiohttp.ClientSession() as session:

            async with session.get(url) as response:
                global authIdForHTML
                global linksForHTML
                

                name = url
            
                status = response.status
                response = await response.text()

                if status == 429:
                    print("too many request to server , error code : 429")

                soup = bs4.BeautifulSoup(response , 'html.parser')

                result = soup.find("h3" , {'class' : 'gs_ai_name'})

                if result is None:

                    data_not_available(f,name)
                else :

                    link = result.find('a' , href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
                    linksForHTML.append("https://scholar.google.com"+str(link))
                    print("LINK:  " + "https://scholar.google.com"+str(link))
                

                    L = []

                    async with session.get(web_site+link) as subresponse:
                        
                        global namesForHTML
                        global pfpLinksForHTML
                        global emailsForHTML
                        global affiliationsForHTML
                        global citationsForHTML
                        print("request: " + name + " with status: " + str(subresponse.status))

                        html = await subresponse.text()
    
                        soup = bs4.BeautifulSoup(html ,'html.parser')
                        Data = await find_and_extract_data_name(soup)
                        # soup = bs4.BeautifulSoup(download_subpage(link), 'html.parser')
                        print(Data, "Data")
                        central_table=soup.find(id="gsc_prf_w")
                        img=central_table.find(id="gsc_prf_pup-img")
                        pimg = img["src"]
                        pfpLinksForHTML.append(pimg)

                        affiliation = soup.find("div" ,{'class' : 'gsc_prf_il'}).get_text()
                        email = soup.find("div" , {'id':'gsc_prf_ivh'}).get_text()
                        email = email[len("Verified email at "):]
                        img = soup.find("div" , {'id' : 'gsc_prf_pua'})
                        img_ = img.find("img")
                        gimg = str(img_["src"])
                        citations = soup.find("td" , {'class' :'gsc_rsb_std'}).get_text()

                        print("hello "+email)
                        print(affiliation)
                        emailsForHTML.append(email)
                        citationsForHTML.append(citations)
                        affiliationsForHTML.append(affiliation)

                        # affiliation = [affiliation.split(" ")]
                        # for a in affiliation:
                        #     if a.uppercase

            


    def print_all_pages(url):
        # pages = create_links()
        tasks = []
        names = []
        # print(pages)
        loop = asyncio.new_event_loop()

        try:

            tasks.append(loop.create_task(fetch_all_data(url)))

            loop.run_until_complete(asyncio.wait(tasks))

        except KeyboardInterrupt:

            print("Program Terminated by User")

            print("<---Bye--->")

        loop.close()

        loop = asyncio.new_event_loop()

        try:
            for page in nameList:

                names.append(loop.create_task(fetch_all_data_name(page)))


                loop.run_until_complete(asyncio.wait(names))

        except KeyboardInterrupt:

            print("Program Terminated by User")

            print("<---Bye--->")

        loop.close()
    
    # browser.get(searchLink)
    
    global lt_iit 
    global lt_nit
    global lt_iiit


    lt_queue = [lt_iit,lt_nit,lt_iiit]

    global_list = []

    global lt_iit 
    global lt_nit 
    global lt_iiit

    # lt_iiit.append("arun")
    # lt_nit.append("manish")
    # lt_iit.append("maqsood")

    link_iit = searchLink + " iit"
    link_nit = searchLink + " nit"
    link_iiit = searchLink + " iiit"


    global link_list
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    global list_bool
    # global browser
    # options = Options()
    # options.headless = True
    # browser = webdriver.Firefox(options=options)
    # browser.get(link_iit)


    def parsing(link_index):
        browser.get(link_list[link_index])
        #run scrape code and fill the list by appending list_queue[list_index]
        print_all_pages(link_list[link_index])
        dataList = zip(namesForHTML, linksForHTML, pfpLinksForHTML, emailsForHTML, affiliationsForHTML, citationsForHTML)
        # print("hihsaidhasihdihsai", set(dataList))
        lt_queue[link_index] = deque(dataList)
        print(lt_queue[link_index])
        # def get_list():
        try:
            if browser.find_element_by_class_name('gs_btnPR'):
                browser.find_element_by_class_name('gs_btnPR').click()
                sleep(1)
        except NoSuchElementException:
            list_bool[link_index] = False

        link_list[link_index] = browser.current_url



    #code to fill global_list


    def fill_global_list():
        # print("hiehello",lt_queue)
        if len(global_list)>0:
            return global_list
        while len(global_list)<10:

            if len(lt_queue[0])>0:

                iit = lt_queue[0].popleft()
                print("IIT: ",iit)

                global_list.append(iit)

            if len(lt_queue[1])>0:
                nit = lt_queue[1].popleft()
                print("NIT: ",nit)

                global_list.append(nit)

            if len(lt_queue[2])>0:
                iiit = lt_queue[2].popleft()
                print("IIIT: ",iiit)
                global_list.append(iiit)

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

        if True not in list_bool or (len(lt_queue[0])<=0 and len(lt_queue[1])<=0 and len(lt_queue[2])<=0):
            return None

        else:
            return global_list




    fill_global_list()

    print("helloooooooooooooooooooo", global_list)


    # browser.quit()

    # print_all_pages(searchLink)

    # for x in range(len(namesForHTML)):
    #     authIdForHTML.append(x)

    # dataList = zip(namesForHTML, linksForHTML, pfpLinksForHTML, emailsForHTML, affiliationsForHTML, citationsForHTML)
    
    # print(emailsForHTML)
    # print(citationsForHTML)
    # print("hhihihihihihi",dataList)
    
    for name, plink, pfplink, email, affiliation, citations in global_list :
            Authors.objects.create(author_name = name, link = plink, pfp_link = pfplink, email = email, affiliation = affiliation, citations = citations)

    # authIdForHTML = list(Authors.objects.values_list('author_id', flat=True))
    # authIdForHTML = authIdForHTML[:10][::-1]
    dataList = Authors.objects.all()
    dataList = dataList[:10][::-1]
    print(dataList)
    
    # dataList = zip(authIdForHTML, namesForHTML, linksForHTML, pfpLinksForHTML, emailsForHTML, affiliationsForHTML, citationsForHTML)
    

    return render(request, "results.html", context={'dataList':dataList})

    
def results(request):
    return render('results.html')


def get_profile(request, id):
    dbData = Authors.objects.get(author_id=id)
    context = {'data': dbData}
    return render(request, 'profile.html', context)