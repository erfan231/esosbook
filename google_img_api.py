
import re
import json
from urllib.request import urlopen

class image_url:
    def __init__(self):
        pass

    def get_url(self, book_name):
        a = book_name.split(" ")
        book_name_value = ""
        for x in range(len(a)):
            book_name_value += a[x]+"+"

        new_value = book_name_value[:-1]
        url = "https://www.googleapis.com/books/v1/volumes?q={}&callback=handleResponse".format(new_value)
        return url


ask = str(input("Enter book name: "))
a = image_url()   
response = urlopen(a.get_url(ask))
links = re.findall('"((http)?://.*?)"', str(response.read()))
if len(links) >= 1:
    pic_url = links[0][0] #save to db (pic_url)
    print(pic_url)
else:
    print("Invalid book name")



#https://www.googleapis.com/books/v1/volumes?q=zero+to++one&callback=handleResponse

#img links, thorugh the above url
"""
 "imageLinks": {
          "smallThumbnail": "http://books.google.com/books/content?id=M22fAwAAQBAJ&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api",
          "thumbnail": "http://books.google.com/books/content?id=M22fAwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"
"""

