from django.shortcuts import render
from .models import QueryForm
from .models import Authors
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import aiohttp
import asyncio
import bs4
import re
# from http import requests
from pandas import read_excel
from function import *

sort_by_date = False
# Create your views here.
def home(request):
    return render(request, 'index.html')

@csrf_exempt
def get_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        return HttpResponseRedirect(form.data)
    else:
         form = QueryForm()
    return render('results.html')

def sort_papers(request, id, link):

    # global name,affiliation,email,img_link,citations

    # author = Authors.objects.get(author_id=id)
    # Link = author.link
    # # Link = "https://scholar.google.com/citations?hl=en&user=lB5LhOQAAAAJ"

    # async def fetch_all_data(url):

    #     global name, citations, img_link, email, affiliation


    #     async with aiohttp.ClientSession() as session:

    #         async with session.get(url) as response:

    #             # name = url[to_cut:]

    #             status = response.status
    #             response = await response.text()

    #             if status == 429:
    #                 print("too many request to server , error code : 429")

    #             # if verbose:
    #             #     print(response, status)


    #             soup = bs4.BeautifulSoup(response , 'html.parser')

    #             name  = soup.find("div" , {'id' : 'gsc_prf_in'}).get_text()
    #             affiliation = soup.find("div" ,{'class' : 'gsc_prf_il'}).get_text()
    #             email = soup.find("div" , {'id':'gsc_prf_ivh'}).get_text()
    #             email = email[len("Verified email at "):]
    #             img = soup.find("div" , {'id' : 'gsc_prf_pua'})
    #             img_ = img.find("img")
    #             gimg = str(img_["src"])
    #             if(gimg[0]!='h'):
    #                 img_link = "https://scholar.google.com"+gimg
    #             else:
    #                 img_link = gimg

    #             citations = soup.find("td" , {'class' :'gsc_rsb_std'}).get_text()
                

    #             # Pname = name
    #             # Paffiliation = affiliation
    #             # Pemail = email
    #             # Pimg_link = img_link
    #             # Pcitations = citations

                
    #             print('img' , img_link)
    #             print("name_tag" , name)
    #             print("affiliation" , affiliation)
    #             print("email" , email)
    #             print('citations' , citations)

    # def print_all_pages():

    #     # f = init_file()

    #     # pages = create_links(n)

    #     tasks = []
    #     loop = asyncio.new_event_loop()

    #     try:
            

    #         tasks.append(loop.create_task(fetch_all_data(Link)))

    #         loop.run_until_complete(asyncio.wait(tasks))

    #     except KeyboardInterrupt:

    #         print("Program Terminated by User")

    #         print("<---Bye--->")

    #     loop.close()
    #     # close_file(f)

    # print_all_pages()
    
    # context = {'name' : name, 'affiliation' : affiliation, 'email' : email, 'citations' : citations, 'img_link' : img_link}
    
    # return render(request, 'profile.html', context)


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

    context = {'id': id ,'name' : name, 'affiliation' : affiliation, 'email' : email, 'citations' : citations, 'img_link' : img_link, 'list': lt}

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

def crawler_run(request):
    ind=0
    # field = input()
    ID = 0
    authIdForHTML = []
    linksForHTML = []
    namesForHTML = []
    pfpLinksForHTML = []
    emailsForHTML = []
    affiliationsForHTML = []
    citationsForHTML = []


    Authors.objects.all().delete()
    
    field = request.POST['fieldSearch']
    nameList = []
    web_site = 'https://scholar.google.com/'
    base_url = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="
    to_cut = len(base_url)
    def download_subpage(link):
        r1=requests.get(web_site + link)
        return r1.text


    def data_not_available(url ):
        print("Data not available for " +str(url))
    def create_links():
        return base_url+field

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

        # all.append(URL)
        # all = cut(all, n)

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

                name = url
            
                status = response.status
                response = await response.text()

                if status == 429:
                    print("too many request to server , error code : 429")

                # if verbose:
                #     print(name, status)


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

                        # authIdForHTML.append(ID)
                        # ID = ID + 1

                        # studiesForHTML.append(Data[3])


                        # a = await store_in_list(L,name , Data)

                        # await save_in_file(f,name , Data)

                    # ind+=1

            


    def print_all_pages():
        pages = create_links()
        tasks = []
        names = []
        print(pages)
        loop = asyncio.new_event_loop()

        try:

            tasks.append(loop.create_task(fetch_all_data(pages)))

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



    print_all_pages()

    for x in range(len(namesForHTML)):
        authIdForHTML.append(x)

    dataList = zip(authIdForHTML, namesForHTML, linksForHTML, pfpLinksForHTML, emailsForHTML, affiliationsForHTML, citationsForHTML)
    
    print(emailsForHTML)
    print(citationsForHTML)
    print("hhihihihihihi",dataList)
    
    for auth_id, name, plink, pfplink, email, affiliation, citations in dataList :
            Authors.objects.create(author_id = auth_id, author_name = name, link = plink, pfp_link = pfplink, email = email, affiliation = affiliation, citations = citations)
            print("hi")
            print(Authors.objects.get(author_id=auth_id))

    dataList = zip(authIdForHTML, namesForHTML, linksForHTML, pfpLinksForHTML, emailsForHTML, affiliationsForHTML, citationsForHTML)
    

    return render(request, "results.html", context={'dataList':dataList})


    
def results(request):
    return render('results.html')


def get_profile(request, id):
    dbData = Authors.objects.get(author_id=id)
    context = {'data': dbData}
    return render(request, 'profile.html', context)