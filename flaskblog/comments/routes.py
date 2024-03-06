from flask import request, jsonify, Blueprint
from flaskblog import db
from flaskblog.models import Comment

comments = Blueprint('comments', __name__) 

@comments.route("/api/comments", methods = ['POST'])
def new_comment():

    method = request.method
    
    if method == "POST":
        
        contents = request.get_json()

        ID = contents['id']
        TEXT = contents['text']
        BLOG_ID = contents['blog_id']

        comment = Comment(id = ID, text = TEXT, blog_id = BLOG_ID)

        try:
            db.session.add(comment)
            db.session.commit() 
        except Exception as e:
            return jsonify(message = str(e))

        return jsonify({"response" : "Successfull"})
    
@comments.route("/api/comments/<id>", methods = ['GET', 'PUT'])
def comment_changes(id):

    method = request.method

    comments = Comment.query.filter(Comment.id == id).first()
    if(comments is None):
        json_data = jsonify(message = "Nothing in Database")
        return json_data

    if method == "GET":
        json_data = jsonify(id=comments.id, text=comments.text, blog_id=comments.blog_id)
        return json_data
    
    if method == "PUT":
        
        contents = request.get_json()

        TEXT = contents['text']
        
        if TEXT != "":
            comments.text = TEXT

        try:
            db.session.commit() 
        except Exception as e:
            return jsonify({"Error occurred: " : str(e)})

        json_data = jsonify(text=comments.text)
        return json_data
    
    
@comments.route("/api/comments/blog/<blog_id>", methods = ['GET'])
def fetch_comment(blog_id):

    method = request.method

    if method == "GET":
        result = Comment.query.first()  
        if(result is None):
            json_data = jsonify(message = "Nothing in Database")
            return json_data
        
        comments = Comment.query.filter(Comment.blog_id == blog_id).all()

        comments_list = [{'id': comment.id, 'text': comment.text, 'blog_id': comment.blog_id} for comment in comments]
        return jsonify(comments_list)
    
    
@comments.route("/api/comments/blog/<blog_id>/comments", methods = ['DELETE'])
def delete_blog_comments(blog_id):

    comments = Comment.query.filter(Comment.blog_id == blog_id).all()
    if(len(comments) == 0):
            json_data = jsonify(message = "Nothing in Database")
            return json_data

    method = request.method
    
    if method == "DELETE":

        try:
            for comment in comments:
                db.session.delete(comment)
                db.session.commit()
        except Exception as e:
            return jsonify(message = str(e))

        return jsonify(message = "Successfull")