import aiohttp
import asyncio 
import bs4 
import re 
from pandas import read_excel 
import time 
from function import *

Link = "https://scholar.google.com/citations?hl=en&user=lB5LhOQAAAAJ"

async def fetch_all_data(url):



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
            img_link = "https://scholar.google.com"+str(img_["src"])
            print('img' , img_link)
            citations = soup.find("td" , {'class' :'gsc_rsb_std'}).get_text()
            print("name_tag" , name)
            print("affiliation" , affiliation)
            print("email" , email)
            print('citations' , citations)

            

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


