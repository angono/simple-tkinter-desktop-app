import sqlite3


class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db) 
        self.cur = self.con.cursor()

        product_sql = """
            CREATE TABLE IF NOT EXISTS product(
                id integer PRIMARY KEY AUTOINCREMENT,
                ref_code char,
                name char,
                unit_price char,
                quantity char,
                total_price real,
                created_date text
            )
        """
        self.cur.execute(product_sql)
        self.con.commit()


    # product table
    def fetch_products(self):
        self.cur.execute("SELECT * FROM product ORDER BY id DESC") 
        rows = self.cur.fetchall()
        return rows 

    def count_product(self):
        self.cur.execute("SELECT COUNT (*) FROM product")
        rows = self.cur.fetchall()
        return rows 

    def search_products(self, name, unit_price, quantity, total_price):
        self.cur.execute("SELECT * FROM product WHERE name=? OR unit_price=? OR quantity=? OR total_price=?", 
            (name, unit_price, quantity, total_price))
        rows = self.cur.fetchall()
        return rows 

    def insert_products(self, ref_code, name, unit_price, quantity, total_price, created_date):
        self.cur.execute("INSERT INTO product VALUES(NULL, ?, ?, ?, ?, ?, ?)", 
            (ref_code, name, unit_price, quantity, total_price, created_date))
        self.con.commit()
            
    def update_products(self, id, ref_code, name, unit_price, quantity, total_price, created_date):
        self.cur.execute("UPDATE product SET ref_code=?, name=?, unit_price=?, quantity=?, total_price=?, created_date=? WHERE id=?", 
            (ref_code, name, unit_price, quantity, total_price, created_date, id,))
        self.con.commit()

    def remove_products(self, id):
        self.cur.execute("DELETE FROM product WHERE id=?", (id,))
        self.con.commit()

    
result = Database("product_database.db")
print(result)


