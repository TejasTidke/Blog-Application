from flask import request, jsonify, Blueprint
from flaskblog import db
from flaskblog.models import Blog
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, OperationalError

blogs = Blueprint('blogs', __name__) 

@blogs.route("/api/blogs/search/<str_title>", methods = ['GET'])
def searh_blog(str_title):

    method = request.method

    if method == "GET":
        result = Blog.query.first()  
        if(result is None):
            json_data = jsonify(message = "Nothing in Database")
            return json_data

        blogs = Blog.query.filter(Blog.title == str_title).all()

        if(len(blogs) == 0):
            json_data = jsonify(message = "No Blog with the given title")
            return json_data

        blogs_list = [{'id': blog.id, 'title': blog.title, 'content': blog.content} for blog in blogs]
        return jsonify(blogs_list)

    
@blogs.route("/api/blogs", methods = ['GET', 'POST'])
def new_blog():

    method = request.method

    if method == "GET":
        result = Blog.query.first()  
        if(result is None):
            json_data = jsonify(message = "Nothing in Database")
            return json_data
        
        blogs = Blog.query.all()
        
        blogs_list = [{'id': blog.id, 'title': blog.title, 'content': blog.content} for blog in blogs]
        return jsonify(blogs = blogs_list)
    
    if method == "POST":
        
        contents = request.get_json()

        ID = contents['id']
        TITLE = contents['title']
        CONTENT = contents['content']

        blog = Blog(id = ID, title = TITLE, content = CONTENT)
        
        try:
            db.session.add(blog)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"Eror Occured: ", str(e)})
 
        return jsonify({"response" : "Successfull"})
    
    
@blogs.route("/api/blogs/<blog_id>", methods = ['GET', 'PUT', 'DELETE'])
def changes_blog(blog_id):

    try:
        blogs = Blog.query.get(blog_id)
    except Exception as e:
            return jsonify({"Error Occured " : str(e)})

    if blogs is None:
        json_data = jsonify(message = "This Blog is not present")
        return json_data

    method = request.method

    if method == "GET":
        json_data = jsonify(id=blogs.id, title=blogs.title, content=blogs.content)
        return json_data

    
    if method == "PUT":
        
        result = Blog.query.first()  
        if(result is None):
            json_data = jsonify(message = "Nothing in Database")
            return json_data
        
        contents = request.get_json()

        TITLE = contents['title']
        CONTENT = contents['content']

        if TITLE != "":
            blogs.title = TITLE
        if CONTENT != "":
            blogs.content =  CONTENT

        try:
            db.session.commit() 
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"Eror Occured: ", str(e)})

        json_data = jsonify(id=blogs.id, title=blogs.title, content=blogs.content)
        return json_data
    
    
    if method == "DELETE":
       
        result = Blog.query.first() 
        
        if(result is None):
            json_data = jsonify(message = "Nothing in Database")
            return json_data
        
        try:
            db.session.delete(blogs)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"Error Occured " : str(e)})
        except Exception as e:
            return jsonify({"Error Occured " : str(e)})
        except OperationalError as e:
            return jsonify({"Error Occured " : str(e)})
        
        return jsonify({"response" : "Successfull"})

