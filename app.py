from flask import Flask,make_response,request,jsonify
from flask_mongoengine import MongoEngine
from config import DB_connection
from mongoengine import StringField
app = Flask(__name__)

conn = DB_connection()
DB_URI = "mongodb+srv://{}:{}@cluster0.1aksc.mongodb.net/{}?retryWrites=true&w=majority".format(conn.user_name,conn.password,conn.database_name)
app.config["MONGODB_HOST"] = DB_URI
print(DB_URI)

db = MongoEngine()
db.init_app(app)

class Book(db.Document):
    book_id = db.IntField()
    name = db.StringField()
    author = db.StringField()

    def to_json(self):
        return {
            "book_id" : self.book_id,
            "name" : self.name,
            "author" : self.author
        }

@app.route("/api/db_populate", methods = ['POST'])
def db_populate():
    Book1= Book(book_id = 1, name = "GOT", author = "George RR Martin")
    Book2= Book(book_id = 2, name = "LOR", author = "LOR_Writer")
    Book1.save()
    Book2.save()
    return make_response("",200)

@app.route("/api/books", methods = ['GET','POST'])
def api_books():
    if request.method == 'GET':
        books = []
        for book in Book.objects:
            books.append(book)
        return make_response(jsonify(books),200)
    elif request.method == 'POST':
        content = request.json
        book = Book(book_id = content['book_id'], name = content['name'], author = content['author'])
        book.save()
        return make_response("",201)

@app.route("/api/books/<book_id>", methods = ['GET','PUT','DELETE'])
def api_each_books(book_id):
    if request.method == 'GET':
        book_obj = Book.objects(book_id = book_id).first()
        if book_obj:
            return make_response(jsonify(book_obj.to_json()),200)
        else:
            return make_response("",404)
    elif request.method == 'PUT':
        content = request.json
        book_obj = Book.objects(book_id = book_id).first()
        book_obj.update( name = content['name'], author = content['author'])
        return make_response("",204)
    elif request.method == 'DELETE':
        book_obj = Book.objects(book_id = book_id).first()
        book_obj.delete()
        return make_response("",204)
        

if __name__ == "__main__":
    app.run()