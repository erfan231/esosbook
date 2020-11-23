from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import re
import database

#Christmas Gifts
# fiction-list = "https://www.booktopia.com.au/books-online/fiction/cF-p1.html?sorter=sortorder-en-dsc"



url = 'https://www.booktopia.com.au/books-online/christmas-essentials/l205-p1.html'

request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

webpage = urlopen(request).read()
#print(webpage)

soup = bs(webpage, "lxml")
books = soup.select(".product-details")


with open("code.html", "w+") as file:


    for book in books:
        # book title
        book_title = book.select("a")
        #at = book_title.find("origin")
        for title in book_title:
            file.write("{} \n".format(str(title)))

       
        # book description
        book_description = book.select(".review-quote")
        for desc in book_description:
            decode_desc = desc.text.replace("\n", "")
            print(decode_desc)
