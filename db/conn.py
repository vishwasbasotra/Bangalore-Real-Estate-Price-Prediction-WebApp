from tkinter import EXCEPTION
import MySQLdb
from colorama import Cursor
import mysql.connector


class database:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host="127.0.0.1",
                port='3306',
                user="root",
                password="training@123",
                db="houses",
                auth_plugin='mysql_native_password'
            )
        except Exception as e:
            raise Exception("Error in establishing connection with database")

    def sign_log(self, input_data):
        name = input_data.name
        email = input_data.email
        password = input_data.password
        try:
            cursor = self.db.cursor()
            if name=="":
                exists_query = f"""select exists(select * from users where 
                            email = '{email}' and password = '{password}')"""
                ex_flag = cursor.execute(exists_query)
                if not ex_flag["exists"]:
                    return "User doesn't exist, please sign in"
                else:
                    return "Login Successful"
            else:
                exists_query = f"""select exists(select * from users where 
                            email = '{email}' and password = '{password}')"""
                ex_flag = cursor.execute(exists_query)
                if ex_flag["exists"]:
                    return "Login Successful"
                else:
                    query = "INSERT INTO users(name, email, password) VALUES('{name}', '{email}', '{password})'"
                    cursor.execute(query)
                    self.db.commit()
                    cursor.close()
                    return "Sign In Successful"

        except Exception as e:
            raise Exception("Error while signing or logging in")

    def insert_house_data(self, input_json):
        name = input_json['name']
        phone = input_json['phone']
        area = input_json['area']
        bhk = input_json['bhk']
        bath = input_json['bath']  
        location = input_json['location']
        price  = input_json['price']
        cursor = self.db.cursor()
        query = "INSERT INTO Houses(name, phone, area, bhk, bath, location, price) VALUES(%s,%s,%s,%s,%s,%s, %s)"
        values = (name, phone, area, bhk, bath, location, price)
        res = ""
        try:
            cursor.execute(query, values)
            self.db.commit()
            res = "Details entered successfully"
        except Exception as e:
            self.db.rollback()
            res = f"Error in entering details {e}"
        return res

    def populate_house_data(self, house_data):
        lst = []
        for house in house_data:
            house_dict = {
                "name": house['name'],
                "phone": house['phone'],
                "area": house['area'],
                "bhk": house['bhk'],
                "bath": house['bath'],
                "location": house['location'],
                "price": house['price']
            }

    def fetch_house_data(self):
        cursor = self.db.cursor()
        query = "SELECT * FROM Houses"
        result = cursor.execute(query)
        data = result.fetchall()
                




