from flask import request, jsonify, Blueprint
from flaskblog import db
from flaskblog.models import Reaction
from enum import Enum

reactions = Blueprint('reactions', __name__) 

class ReactionType(Enum):
    LIKE = 1
    LOVE = 2
    HATE = 3

class TargetType(Enum):
    BLOG = 1
    COMMENT = 2
    

@reactions.route("/api/reactions/add", methods = ['POST'])
def new_reaction():

    method = request.method
    
    if method == "POST":
        
        contents = request.get_json()

        ID = contents['id']
        TYPE = ReactionType(contents['type']).name
        TARGET_TYPE = TargetType(contents['target_type']).name
        TARGET_ID = contents['target_id']
        BLOG_ID = contents['blog_id']
        COMMENT_ID = contents['comment_id']

        comment = Reaction(id = ID, type = TYPE, target_type = TARGET_TYPE, target_id = TARGET_ID, 
                           blog_id = BLOG_ID, comment_id = COMMENT_ID)
        
        try:
            db.session.add(comment)
            db.session.commit() 
        except Exception as e:
            return jsonify(message = str(e))
        
        return jsonify({"response" : "Successfull"})
    
@reactions.route("/api/reactions/delete/<id>", methods = ['DELETE'])
def delete_reaction(id):

    reactions1 = Reaction.query.filter(Reaction.target_id == id).first()
    if(reactions is None):
        json_data = jsonify(message = "Nothing in Database")
        return json_data

    method = request.method
    
    if method == "DELETE":
        
        if(reactions1.target_type == 1):
            try:
                reactions2 = Reaction.query.filter(Reaction.blog_id == id).first()
                db.session.delete(reactions2)
                db.session.commit()
            except Exception as e:
                return jsonify(message = str(e))
        elif(reactions1.target_type == 2):
            try:
                reactions2 = Reaction.query.filter(Reaction.comment_id == id).first()
                db.session.delete(reactions2)
                db.session.commit()
            except Exception as e:
                return jsonify(message = str(e))
        
        return jsonify({"response" : "Successfull"})