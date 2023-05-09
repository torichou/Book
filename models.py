"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

# TODO: Complete your models
"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""
class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)
    name = Column("name", TEXT, nullable=False)
    bio = Column("bio", TEXT, nullable=False)
    
    def __init__(self, name, username, password, bio):
        self.username = username
        self.password = password
        self.name = name
        self.bio = bio
        
        
    def __repr__(self):
        return "@" + self.username

class Reviews(Base):
    # TODO: Complete the class
    __tablename__ = "reviews"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    content = Column("content", TEXT, nullable=False)
    timestamp = Column("timestamp", TEXT, nullable=False)
    username = Column("username", ForeignKey("users.username"))
    rating = Column("rating", INTEGER, nullable=False)
    book_id = Column("book_id", INTEGER, ForeignKey("users.username"))

    def __init__(self, book_id, content, timestamp, username, rating):
        self.content = content
        self.timestamp = timestamp
        self.username = username
        self.rating = rating
        self.book_id = book_id

    def __repr__(self):
        return "@" + self.username + "\n" + self.rating + "\n" + self.content + "\n" + self.timestamp

class Books(Base):
    # TODO: Complete the class
    __tablename__ = "books"

    # Columns 
    id = Column("id", INTEGER, primary_key=True)
    title = Column("title", TEXT, nullable=False)
    author = Column("author", TEXT, nullable=False)
    image = Column("image", TEXT, nullable=False)

    def __init__(self, title, author, image):
        self.title = title
        self.author = author
        self.image = image
        
    def __repr__(self):
        return self.title + " by " + self.author

class Libraries(Base):
    # TODO: Complete the class
    __tablename__ = "libraries"

    # Columns
    username = Column("username", ForeignKey("users.username"), primary_key=True)
    book_id = Column("book_id", ForeignKey("books.id"), primary_key=True)

    def __init__(self, username, book_id):
        self.username = username
        self.book_id = book_id