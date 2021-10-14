import re
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request

class Menu: 
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.updated_at = data["updated_at"]
        self.created_at = data["created_at"]
    
    def to_json(self):
        json = {
            "id" : self.id,
            "name" : self.name,
            "updated_at" : self.updated_at,
            "created_at" : self.created_at
        }
        return json
    
    @classmethod
    def getMenuById(cls, id = None):
        if not id:
            return None
        query = f"SELECT * FROM menus WHERE id = {id}"
        db_data = MySQLConnection().query_db(query)
        if db_data: 
            return cls(db_data[0])
        else:
            return None
    
    @staticmethod
    def updateMenu(id, menu_name) -> None:
        query = f"UPDATE menus SET name = '{menu_name}', updated_at = NOW() WHERE id = {id}"
        MySQLConnection().query_db(query)

    @staticmethod
    def createNew(menu_name) -> int:
        query = f"INSERT INTO menus (created_at, updated_at, name) VALUES(NOW(), NOW(), '{menu_name}')"
        id = MySQLConnection().query_db(query)
        return id
