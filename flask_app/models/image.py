from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, request
import os


class Image: 
    def __init__(self, data): 
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner_user_id = data['owner_user_id']
        self.file_path = os.path.relpath(data['file_path'],  os.getcwd()+"/flask_app/static").replace('\\', '/')
    
    def __str__(self) -> str:
        return f"IMAGE INSTANCE STARTS:id: {self.id}, \n created_at: {self.created_at}, updated_at: {self.updated_at}, owner_user_id = {self.owner_user_id}, \n file_path: {self.file_path} $IMAGE INSTANCE ENDS"

    def deleteSelf(self):
        #Deletes from Disk
        
        os.remove(os.path.join(os.getcwd()+"/flask_app/static", self.file_path))

        #Deletes from DataBase
        query = f"DELETE FROM images WHERE id = {self.id}"
        MySQLConnection().query_db(query)

        query = f"UPDATE users SET profile_image_id = 0"



    @staticmethod
    def insertImageToDB(data):
        #Get last id of image database
        query = "SELECT id FROM images ORDER BY id DESC LIMIT 1"
        last_image_id = MySQLConnection().query_db(query)

        #protects from an error if no other photos are in the database
        if not len(last_image_id) == 0:
            filename = f"{data['id']}-{last_image_id[0]['id']+1}.png"
        else: 
            filename = f"{data['id']}-{1}.png"
            

        #Stores profile_picture on disk and saves file path
        cwd = os.getcwd()
        print("CURRENT DIRECTORY BEFORE CHANGE: ", os.getcwd()+f"/flask_app/static/imgs/usercontent/{data['id']}/")
        filepath =  os.getcwd()+f"/flask_app/static/imgs/usercontent/{data['id']}/"
        if not os.path.exists(filepath):
            os.chdir(os.getcwd()+f"/flask_app/static/imgs/usercontent/")
            print("CURRENT DIRECTORY durring CHANGE: ", os.getcwd())
            os.makedirs(filepath) 
            os.chdir(cwd)
            print("CURRENT DIRECTORY AFTER CHANGE: ", os.getcwd)
        
        #saves file to disk
        filepath = os.path.join(filepath, filename).replace('\\', '/') #filepath comes back with both '/'s and '\'s. We need to replace them to match and be used by html files. 

        print('FILEPATH: ', filepath)
        data['profile_picture'].save(filepath)

        #Insert Image to Database
        query = f"INSERT INTO images(created_at, updated_at, owner_user_id, file_path) VALUES(NOW(), NOW(), {data['id']}, '{filepath}')"
        id = MySQLConnection().query_db(query)

        return id

    @classmethod
    def deleteImage(cls, photo_id):
        image = cls.getImageById(photo_id)
        image.deleteSelf()

    @classmethod
    def getImageById(cls, id):
        if not id: 
            return False
            
        query = f"SELECT * from images WHERE id = {id}"
        print(os.getcwd())
        image = MySQLConnection().query_db(query)


        if not len(image) == 0:
            image = cls(image[0])
            return image
        else: 
            flash('Image not Found! Please contact us if problem persists', 'file')
            return False

        
    @classmethod
    def getProfileImage(cls, id):
        image = cls.getImageById(id)
        print('CURRENT WORKING FROM PROFILE IMAGE', os.getcwd())
        if image: 
            return image
        else: 
            filepath = os.getcwd()+"/flask_app/static/imgs/user/profile_holder.png"
            data = {
                'id' : None,
                'created_at' : None,
                'updated_at' : None,
                'owner_user_id' : None,
                'file_path' : filepath.replace('\\', '/')
            }
            

            return cls(data)
