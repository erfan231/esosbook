import sqlite3 

connection = sqlite3.connect("database.db") #db directory/name
cursor = connection.cursor()

def create_new_column():
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id integer ,name text)") #make new table with it's columns
    connection.commit() # push the code

    sql_command = ("ALTER TABLE '{table_name}' ADD column '{column_name}' '{data_type}'") #make new column to existing db/table
    base_command = sql_command.format(table_name="users", column_name="new_column_name", data_type="Varchar")

    cursor.execute(base_command)
    connection.commit()
    connection.close()



#create_new_column()


#don't forget to update your class definitions(sqlalchemy) the changes you make here :)


"""
if data_type == "Integer":
data_type_formatted = "INTEGER"
elif data_type == "String":
data_type_formatted = "VARCHAR(100)"
"""
