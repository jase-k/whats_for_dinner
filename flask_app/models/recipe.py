from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request

class Recipe:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = f"{data['first_name']} {data['last_name']}" #Joined with the creator id
        self.title = data['title']
        self.instructions = data['instructions']
        self.premium = data['premium']

    @staticmethod
    def addRecipeToDB(data):
        query = "INSERT INTO recipes (created_at, updated_at, creator_id, title, instructions, premium) VALUES(NOW(), NOW(), %(user_id)s, %(title)s, %(instructions)s, %(premium)s)"

        id = MySQLConnection().query_db(query, data)

        return id
    
    @classmethod
    def getRecipeById(cls, id):
        #Join User info, reviews
        pass


