import aiohttp
import asyncio 
import bs4 
import re 
from pandas import read_excel 
import time 
from function import *


link = "https://www.ieor.iitb.ac.in/people/research_scholars"


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

            name  = soup.find("div" , {'class' : 'field-item even'})

            text = name.find_all('a')

            name_list = []

            for t in text:

            	name_list.append([str(t.get_text()) ,t['href'] ])
            print(name_list)

           	
            

def print_all_pages():

    tasks = []
    loop = asyncio.new_event_loop()

    try:
        

        tasks.append(loop.create_task(fetch_all_data(link)))

        loop.run_until_complete(asyncio.wait(tasks))

    except KeyboardInterrupt:

        print("Program Terminated by User")

        print("<---Bye--->")

    loop.close()
    # close_file(f)

print_all_pages()
