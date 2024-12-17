import mysql.connector

class Users:
	
	def __init__(self):
		print("User")

	def delete(self, id):
		db_name="webschool_test"
		table_name="users"
		mydb = mysql.connector.connect(
			host="localhost",
			user="root",
			password="",
			database=db_name
		)
		mycursor = mydb.cursor()
		sql = f"DELETE FROM {table_name} WHERE id='{id}'"
		mycursor.execute(sql)
		mydb.commit()
		print(mycursor.rowcount, "record deleted.")
		return mycursor.rowcount > 0
	
	def update(self, id, user):
		print([user])
		db_name="webschool_test"
		table_name="users"
		mydb = mysql.connector.connect(
			host="localhost",
			user="root",
			password="",
			database=db_name
		)
		mycursor = mydb.cursor()
		sql = f"""
  			UPDATE {table_name} 
  				SET password='{user["password"]}',
      				email='{user["email"]}',
          			phone='{user["phone"]}',
             		name='{user["name"]}' 
               		WHERE id='{id}'
                 """
		mycursor.execute(sql)
		mydb.commit()
		print(mycursor.rowcount, "record update.")
		return mycursor.rowcount > 0
  
	def all(self):
		db_name="webschool_test"
		table_name="users"
		mydb = mysql.connector.connect(
			host="localhost",
			user="root",
			password="",
			database=db_name
		)
		mycursor = mydb.cursor()
		sql = f"SELECT * FROM {table_name}"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		return myresult
    
	def find(self,id):
		db_name="webschool_test"
		table_name="users"
		mydb = mysql.connector.connect(
			host="localhost",
			user="root",
			password="",
			database=db_name
		)
		mycursor = mydb.cursor()
		sql = f"SELECT * FROM {table_name} WHERE id='{id}'"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		return myresult
    
	def add(self, user):
		print(user["name"])
		db_name="webschool_test"
		table_name="users"
		connection = mysql.connector.connect(
			host="localhost",
			user="root",
			password="",
			database=db_name,
       		charset="utf8mb4"
		)
		cursor = connection.cursor()
		sql = f"INSERT INTO `{table_name}` (name, password, email, phone) VALUES (%s, %s, %s, %s)"
		val = (user["name"], user["password"], user["email"], user["phone"])
		cursor.execute(sql, val)
		connection.commit()
		print(cursor.rowcount, "record inserted.")
		user_added = cursor.rowcount > 0		
		cursor.close()
		connection.close()
		return user_added
		