from flask import *
from database import init_db, db_session
from models import *
from datetime import datetime
from sqlalchemy import desc 

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "7TAD0FIOoNvSzHJqww=="

# TODO: Fill in methods and routes
@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        user = request.form["username"] 
        pw = request.form["password"]
        username_user = db_session.query(User).where(User.username==user).first()
        if username_user is None or username_user.password != pw:
            flash("Wrong username or password.", "error")
            return render_template("signin.html")
        else: 
            session["username"] = user
            return redirect(url_for('browse'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else: 
        while True:
            name = request.form["name"]
            username = request.form["username"] 
            pw_1 = request.form["password"]
            pw_2 = request.form["password2"]
            bio = request.form["bio"]
            if db_session.query(User).where(User.username==username).first() is not None:
                flash("That username is already taken.", "error")
                return render_template("signup.html")
            elif pw_1 != pw_2:   
                flash("The passwords don't match. Try again.", "error")
                return render_template("signup.html")
            else:
                new_user = User(name, username, pw_1, bio)
                session["username"] = username
                db_session.add(new_user)
                db_session.commit()
                return redirect(url_for('browse'))     

@app.route("/browse")
def browse():
    reviews = db_session.query(Reviews).order_by(desc(Reviews.timestamp)).all()
    books = []
    length = 0
    for review in reviews:
        length += 1
        books.append(db_session.query(Books).where(review.book_id==Books.id).first())
    return render_template("browse.html", reviews=reviews, books=books, length=length)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        user = db_session.query(User).where(User.username==session["username"]).first()
        library = db_session.query(Libraries).where(Libraries.username==session["username"]).all()
        user_books = []
        for book in library:
            user_books.append(db_session.query(Books).where(Books.id==book.book_id).first())
        return render_template("profile.html", user=user, user_books=user_books)
    else: 
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        image = request.form["image"]
        content = request.form["content"]
        new_book = Books(title, author, image)
        db_session.add(new_book)
        book_id = db_session.query(Books.id).where((Books.author==author) and (Books.title==title))
        new_review = Reviews(book_id, content, datetime.now(), session["username"], rating)
        db_session.add(new_review)
        db_session.commit()
        library = Libraries(session["username"], book_id)
        db_session.add(library)
        db_session.commit()
        return redirect(url_for('browse'))     

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("signin"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
