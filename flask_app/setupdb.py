from web_package import db

# SCHEMA = os.path.join(os.getcwd(), "web_package/db", "schema.sql")

#Database Connectors/Disconnectors
# def connect_db():
#     return sqlite3.connect(DATABASE)
    
# def disconnect_db(connection):
#     connection.close()

# def init_db():
#     """Creates a Database and uses the SCHEMA file."""
#     try:
#         conn = connect_db()                      #Create the Database
#         f = open(SCHEMA)
#         conn.executescript(f.read())             #Create neccessary Tables
#         conn.commit()                            #Commit the changes
#     finally:                                     #Always executes this block
#         if globals().has_key("f"):
#             f.close()
#         if globals().has_key("conn"):
#             disconnect_db(conn)

if __name__ == '__main__':
    # init_db()
    db.create_all()
