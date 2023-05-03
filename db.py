import sqlite3
def init_db():
    db = sqlite3.connect('orders.db')
    cur = db.cursor()
    return cur,db
def create_table(cur:sqlite3.Cursor,db:sqlite3.Connection):
    cur.execute("""CREATE TABLE IF NOT EXISTS CUSTOMERS
                   (COFFEETYPE varchar(255),
                   SUGAR VARCHAR(255),
                   CUPSIZE VARCHAR(255))""")

def insert_val(coffeetype:str,sugar:str,cupsize:str,timeoforder:str,cur:sqlite3.Cursor,db:sqlite3.Connection):
    cur.execute("""INSERT INTO CUSTOMERS VALUES(?,?,?)""",(coffeetype,sugar,cupsize))
    db.commit()

def exit_on_db(cur:sqlite3.Cursor,db:sqlite3.Connection):
    cur.close()
