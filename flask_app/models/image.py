from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request
from abc import ABC, abstractclassmethod, abstractmethod
import os


class Image(ABC): 
    def __init__(self, data): 
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.file_path = os.path.relpath(data['file_path'],  os.getcwd()+"/flask_app/static").replace('\\', '/')
    
    def __str__(self) -> str:
        return f"IMAGE INSTANCE STARTS:id: {self.id}, \n created_at: {self.created_at}, updated_at: {self.updated_at}, user_id = {self.user_id}, \n file_path: {self.file_path} $IMAGE INSTANCE ENDS"

    @classmethod
    @abstractmethod
    def deleteImage(cls, image_id):
        pass #Should Delete from Database and Server Storage

    @classmethod
    @abstractmethod
    def getImageById(image_id):
        pass #Should retrieve the file path from the database and get the photo from storage. .. Returns and instance of Image

    @staticmethod
    @abstractmethod 
    def insertImageToDB(data):
        pass #Should Save image to server files and add file path to the database

class ProfileImage(Image):
    def __init__(self, data):
        super().__init__(data)
    
    @classmethod
    def deleteImage(cls, image_id):
        image = cls.getImageById(image_id)

        #Deletes from DataBase
        query = f"DELETE FROM profile_images WHERE id = {image.id}"

        #Deletes from Server Files #Returning 0 means it's returnning the default photo and shouldn't be deleted.
        if not image.id == 0:
            os.remove(os.path.join(os.getcwd()+"/flask_app/static", image.file_path))

        MySQLConnection().query_db(query)


    @staticmethod
    def insertImageToDB(user_id, file):
    
        #Get last id of image database
        query = "SELECT id FROM profile_images ORDER BY id DESC LIMIT 1"
        last_image_id = MySQLConnection().query_db(query)

        #protects from an error if no other photos are in the database
        if not len(last_image_id) == 0:
            filename = f"{user_id}-{last_image_id[0]['id']+1}.png"
        else: 
            filename = f"{user_id}-1.png"
            

        #Stores profile_picture on disk and saves file path
        cwd = os.getcwd()
        print("CURRENT DIRECTORY BEFORE CHANGE: ", os.getcwd()+f"/flask_app/static/imgs/usercontent/{user_id}/")
        filepath =  os.getcwd()+f"/flask_app/static/imgs/usercontent/{user_id}/"
        if not os.path.exists(filepath):
            os.chdir(os.getcwd()+f"/flask_app/static/imgs/usercontent/")
            print("CURRENT DIRECTORY durring CHANGE: ", os.getcwd())
            os.makedirs(filepath) 
            os.chdir(cwd)
            print("CURRENT DIRECTORY AFTER CHANGE: ", os.getcwd)
        
        #saves file to disk
        filepath = os.path.join(filepath, filename).replace('\\', '/') #filepath comes back with both '/'s and '\'s. We need to replace them to match and be used by html files. 

        print('FILEPATH: ', filepath)
        file.save(filepath)

        #Insert Image to Database
        query = f"INSERT INTO profile_images(created_at, updated_at, user_id, file_path) VALUES(NOW(), NOW(), {user_id}, '{filepath}')"
        id = MySQLConnection().query_db(query)

        return id

    @classmethod
    def getImageById(cls, id):

        query = f"SELECT * from profile_images WHERE id = {id}"
        
        db_data = MySQLConnection().query_db(query)
        print("Data from user DB", len(db_data))

        if len(db_data) > 0:
            image = cls(db_data[0])
            return image
        else: 
            filepath = os.getcwd()+"/flask_app/static/imgs/user/profile_holder.png"
            data = {
                'id' : 0,
                'created_at' : None,
                'updated_at' : None,
                'user_id' : None,
                'file_path' : filepath.replace('\\', '/')
            }
            return cls(data)



class RecipeImage(Image):
    def __init__(self, data):
        super().__init__(data)
        self.recipe_id = data['recipe_id']
    
    @classmethod
    def deleteImage(cls, image_id):
        image = cls.getImageById(image_id)

        #Deletes from Server Files
        os.remove(os.path.join(os.getcwd()+"/flask_app/static", image.file_path))

        #Deletes from DataBase
        query = f"DELETE FROM recipe_images WHERE id = {image.id}"
        MySQLConnection().query_db(query)


    @staticmethod
    def insertImageToDB(user_id, recipe_id, file):
        #Get last id of image database
        query = "SELECT id FROM recipe_images ORDER BY id DESC LIMIT 1"
        last_image_id = MySQLConnection().query_db(query)

        #protects from an error if no other photos are in the database
        if not len(last_image_id) == 0:
            filename = f"{user_id}-{last_image_id[0]['id']+1}r.png"
        else: 
            filename = f"{user_id}-1r.png"
            
        filepath =  os.getcwd()+f"/flask_app/static/imgs/usercontent/{user_id}/"
        
        if not os.path.exists(filepath):
            #Stores recipe_picture on disk and saves file path
            cwd = os.getcwd()
            os.chdir(os.getcwd()+f"/flask_app/static/imgs/usercontent/")
            os.makedirs(filepath) 
            os.chdir(cwd)
        
        #filepath comes back with both '/'s and '\'s. We need to replace them to match and be used by html files. 
        filepath = os.path.join(filepath, filename).replace('\\', '/') 

        #saves file to disk
        file.save(filepath)

        #Insert Image to Database
        query = f"INSERT INTO recipe_images(created_at, updated_at, user_id, recipe_id, file_path) VALUES(NOW(), NOW(), {user_id}, {recipe_id}, '{filepath}')"
        id = MySQLConnection().query_db(query)

        return id

    @classmethod
    def getImageById(cls, id):

        query = f"SELECT * from recipe_images WHERE id = {id}"
        
        db_data = MySQLConnection().query_db(query)

        if len(db_data) > 0:
            image = cls(db_data[0])
            return image
        else:
            return False

    #Replace with recipe pulling in images 
    @classmethod
    def getRecipeImages(cls, recipe_id):
        query = f"SELECT * FROM recipe_images WHERE recipe_id = {recipe_id}"

        db_data = MySQLConnection().query_db(query)

        images = []
        for row in db_data:
            images.append(cls(row))

        return images