from database import Users, User_Books

user = Users.query.filter_by(username="erfanSSS").first()

books = user.books

print(user.books.count())


for x in range(user.books.count()):
    print(user.books[x].book_name)