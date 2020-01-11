import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class DbUtils:

# -----------------------GOODS------------METHODS-------------
    def insert_good(prod_id, units_count, order_id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("insert into GOODS(UNITS_COUNT, PRODUCT_UNIT_ID, ORDER_ID) values(?, ?, ?)", (units_count, prod_id, order_id))
        conn.commit()
        return cursor.lastrowid

    def select_goods(order_id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT G.ID, G.UNITS_COUNT, G.PRODUCT_UNIT_ID, G.ORDER_ID, P.NAME, PU.PRICE
                             FROM GOODS AS G 
                             JOIN PRODUCT_UNITS AS PU ON
                             PU.ID = G.PRODUCT_UNIT_ID
                             JOIN PRODUCTS AS P ON
                             PU.PRODUCT_ID = P.ID
                             WHERE G.ORDER_ID = ?;''', [order_id])
        return cursor.fetchall()

# -----------------------ORDERS------------METHODS-------------

    def insert_order(status, user_id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("insert into ORDERS(STATUS, USER_ID) values(?, ?)", (status, user_id))
        conn.commit()
        return cursor.lastrowid

# -----------------------PRODUCTS------------METHODS-------------
    def select_products():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID, NAME, FACTORY_ID, PRODUCT_TYPE_ID, CALORIE_CONTENT, EXPIRATION_DATE, DIMENSION, WEIGHT, PICTURE FROM PRODUCTS WHERE IS_DELETE = '0';")
        return cursor.fetchall()

    def select_products_id(name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM PRODUCTS WHERE IS_DELETE = '0' AND NAME = ?;", [name])
        return cursor.fetchall()

    def select_products_names_find(find):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        find = '%' + find + '%'
        cursor.execute("SELECT P.NAME, PT.TYPE_NAME FROM PRODUCTS AS P JOIN PRODUCT_TYPES AS PT ON P.PRODUCT_TYPE_ID = PT.ID WHERE P.IS_DELETE = '0' AND P.NAME LIKE '%s' ;" % find)
        return cursor.fetchall()

    def select_products_names():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT P.NAME, PT.TYPE_NAME
        FROM PRODUCTS AS P JOIN 
        PRODUCT_TYPES PT ON
        P.PRODUCT_TYPE_ID = PT.ID
        WHERE P.IS_DELETE = '0';''')
        return cursor.fetchall()

    def select_product_id(id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID, NAME, FACTORY_ID, PRODUCT_TYPE_ID, CALORIE_CONTENT, EXPIRATION_DATE, DIMENSION, WEIGHT, PICTURE FROM PRODUCTS WHERE IS_DELETE = '0' AND ID = ?;", [id])
        return cursor.fetchall()

    def insert_product(name, factory_id, product_type_id, calorie_content, expiration_date, dimension, weight, picture):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("insert into PRODUCTS(NAME, FACTORY_ID, PRODUCT_TYPE_ID, CALORIE_CONTENT, EXPIRATION_DATE, DIMENSION, WEIGHT, PICTURE, IS_DELETE) values(?, ?, ?, ?, ?, ?, ?, ?, '0')", (name, factory_id, product_type_id, calorie_content, expiration_date, dimension, weight, picture))
        conn.commit()
        return cursor.lastrowid
    
    def delete_product(id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE PRODUCTS SET IS_DELETE = '1' WHERE ID = ?;", (id))
        conn.commit()

    def update_product_img(id, picture):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE PRODUCTS SET PICTURE = ?  WHERE ID = ?", (picture, id))
        conn.commit()

    def update_product(id, name, factory_id, product_type_id, calorie_content, expiration_date, dimension, weight):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE PRODUCTS SET NAME = ?, FACTORY_ID = ?, PRODUCT_TYPE_ID = ?, CALORIE_CONTENT = ?, EXPIRATION_DATE = ?, DIMENSION = ?, WEIGHT = ? WHERE ID = ?", (name, factory_id, product_type_id, calorie_content, expiration_date, dimension, weight, id))
        conn.commit()

    def update_product_pic(id, name, factory_id, product_type_id, calorie_content, expiration_date, dimension, weight, picture):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE PRODUCTS SET NAME = ?, FACTORY_ID = ?, PRODUCT_TYPE_ID = ?, CALORIE_CONTENT = ?, EXPIRATION_DATE = ?, DIMENSION = ?, WEIGHT = ?, PICTURE = ? WHERE ID = ?", (name, factory_id, product_type_id, calorie_content, expiration_date, dimension, weight, picture, id))
        conn.commit()

# -----------------------PRODUCT_UNITS------------METHODS-------------
    def select_product_units():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID, PRODUCT_ID, QUANTITY, MANUFACTURE_DATE, RELEVANCE, PRICE FROM PRODUCT_UNITS WHERE IS_DELETE = '0';")
        return cursor.fetchall()

    def select_product_units_all():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT    P.ID, P.NAME, P.FACTORY_ID, 
                                    P.PRODUCT_TYPE_ID, P.CALORIE_CONTENT, 
                                    P.EXPIRATION_DATE, P.DIMENSION, P.WEIGHT, P.PICTURE,

                                    PU.ID,
                                    PU.QUANTITY, 
                                    PU.MANUFACTURE_DATE,
                                    PU.RELEVANCE,
                                    PU.PRICE
                            FROM    PRODUCT_UNITS AS PU JOIN
                                        PRODUCTS AS P ON
                                            PU.PRODUCT_ID = P.ID
                            WHERE   PU.IS_DELETE = '0';''')
        return cursor.fetchall()

    # def select_products():
    #     conn = sqlite3.connect("mydatabase.db")
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT ID, NAME, FACTORY_ID, PRODUCT_TYPE_ID, CALORIE_CONTENT, EXPIRATION_DATE, DIMENSION, WEIGHT, PICTURE FROM PRODUCTS WHERE IS_DELETE = '0';")
    #     return cursor.fetchall()

    def insert_product_units(product_id, quantity, manufacture_date, relevance, price):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("insert into PRODUCT_UNITS(PRODUCT_ID, QUANTITY, MANUFACTURE_DATE, RELEVANCE, PRICE, IS_DELETE) values(?, ?, ?, ?, ?, '0')", (product_id, quantity, manufacture_date, relevance, price))
        conn.commit()
    
    def delete_product_units(id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE PRODUCT_UNITS SET IS_DELETE = '1' WHERE ID = ?;", (id))
        conn.commit()

    def update_product_units(id, product_id, quantity, manufacture_date, relevance):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE PRODUCT_UNITS SET PRODUCT_ID = ?, QUANTITY = ?, MANUFACTURE_DATE = ?, RELEVANCE = ? WHERE ID = ?", (product_id, quantity, manufacture_date, relevance, id))
        conn.commit()

# -----------------------PRODUCT_INGREDIENT------------METHODS-------------
    def select_product_ingredient():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID, PRODUCT_ID, INGREDIENT_ID FROM PRODUCT_INGREDIENT;")
        return cursor.fetchall()

    def select_product_ingredient(prod_id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT    INGREDIENT_NAME
                            FROM    INGREDIENTS JOIN 
                                    ( SELECT  INGREDIENT_ID
                                        FROM PRODUCT_INGREDIENT
                                        WHERE PRODUCT_ID = ?) AS PI ON
                                        ID = PI.INGREDIENT_ID
                                            ;''', [prod_id])
        return cursor.fetchall()

    def insert_product_ingredients(product_id ,ingredients):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()

        ing_str = ""
        for i in range(len(ingredients)):
            ing_str += "'"+ ingredients[i] + "'"
            if i < len(ingredients) - 1:
                ing_str += ", "
        cursor.execute("SELECT ID FROM INGREDIENTS WHERE IS_DELETE = '0' AND INGREDIENT_NAME IN (%s);" % ing_str)
        ing_id = cursor.fetchall()
        for i in range(len(ing_id)):
            cursor.execute("insert into PRODUCT_INGREDIENT(PRODUCT_ID, INGREDIENT_ID) values(?, ?)", (product_id, ing_id[i][0]))
        conn.commit()
    
    def delete_product_ingredient(id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PRODUCT_INGREDIENT WHERE PRODUCT_ID = ?;", [id])
        conn.commit()

    def update_product_ingredient(id, product_id ,ingredient_id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE PRODUCT_INGREDIENT SET PRODUCT_ID = ?, INGREDIENT_ID = ? WHERE ID = ?", (product_id, ingredient_id, id))
        conn.commit()

# -----------------------INGREDIENTS------------METHODS-------------
    def select_ingredients():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID, INGREDIENT_NAME, DIMENSION FROM INGREDIENTS WHERE IS_DELETE = '0';")
        return cursor.fetchall()

    def select_ingredients_name():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT INGREDIENT_NAME FROM INGREDIENTS WHERE IS_DELETE = '0';")
        return cursor.fetchall()

    def select_ingredients_id(ingredients):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        ing_str = ""
        for i in range(len(ingredients)):
            ing_str += "'"+ ingredients[i] + "'"
            if i < len(ingredients) - 1:
                ing_str += ", "
        cursor.execute("SELECT ID FROM INGREDIENTS WHERE IS_DELETE = '0' AND INGREDIENT_NAME IN (%s);" % ing_str)
        return cursor.fetchall()

    def insert_ingredients(ingredient_name, dimension):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("insert into INGREDIENTS(INGREDIENT_NAME, DIMENSION, IS_DELETE) values(?, ?, '0')", (ingredient_name, dimension))
        conn.commit()
    
    def delete_ingredients(id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE INGREDIENTS SET IS_DELETE = '1' WHERE ID = ?;", (id))
        conn.commit()

    def update_ingredients(id, ingredient_name, dimension):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE INGREDIENTS SET INGREDIENT_NAME = ?, DIMENSION = ? WHERE ID = ?", (ingredient_name, dimension, id))
        conn.commit()

# -----------------------PRODUCT_TOPE------------METHODS-------------
    def select_product_types():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID, TYPE_NAME FROM PRODUCT_TYPES WHERE IS_DELETE = '0';")
        return cursor.fetchall()

    def select_product_types_names():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT TYPE_NAME FROM PRODUCT_TYPES WHERE IS_DELETE = '0';")
        return cursor.fetchall()

    def select_product_types_name(id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT TYPE_NAME FROM PRODUCT_TYPES WHERE IS_DELETE = '0' AND ID = ?;", [id])
        return cursor.fetchall()

    def select_product_types_id(type_name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM PRODUCT_TYPES WHERE IS_DELETE = '0' AND TYPE_NAME = ?;", [type_name])
        return cursor.fetchall()

    def insert_product_types(type_name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("insert into PRODUCT_TYPES(TYPE_NAME, IS_DELETE) values(?, '0')", [type_name])
        conn.commit()
    
    def delete_product_types(id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE PRODUCT_TYPES SET IS_DELETE = '1' WHERE ID = ?;", (id))
        conn.commit()

    def update_product_types(id, type_name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE PRODUCT_TYPES SET TYPE_NAME = ? WHERE ID = ?", (type_name, id))
        conn.commit()

# ------------------FACTORIES----METHODS-------------------
    def select_factories():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fact.ID, fact.LOCATION, fact.FACTORY_NAME, \
        fact.MANUFACTURER_ID, man.COMPANY_NAME FROM FACTORIES as fact JOIN MANUFACTURERS AS man \
        ON fact.MANUFACTURER_ID = man.ID WHERE fact.IS_DELETE = 0 AND man.IS_DELETE = 0;")
        return cursor.fetchall()

    def select_factories_names():
            conn = sqlite3.connect("mydatabase.db")
            cursor = conn.cursor()
            cursor.execute("SELECT FACTORY_NAME  FROM FACTORIES WHERE IS_DELETE = 0;")
            return cursor.fetchall()

    def select_factories_name(id):
            conn = sqlite3.connect("mydatabase.db")
            cursor = conn.cursor()
            cursor.execute("SELECT FACTORY_NAME  FROM FACTORIES WHERE IS_DELETE = 0 AND ID = ?;", [id])
            return cursor.fetchall()

    def select_factories_id(fact_name):
            conn = sqlite3.connect("mydatabase.db")
            cursor = conn.cursor()
            cursor.execute("SELECT ID FROM FACTORIES WHERE IS_DELETE = 0 AND FACTORY_NAME = ?;", [fact_name])
            return cursor.fetchall()

    def insert_factory(location, fact_name, manuf_name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM MANUFACTURERS WHERE COMPANY_NAME = ?;", [manuf_name])
        result = cursor.fetchone()
        if result[0] is not None:
            cursor.execute("insert into FACTORIES(LOCATION, FACTORY_NAME, MANUFACTURER_ID, IS_DELETE) values(?,?,?, '0')", (location, fact_name, result[0]))
            conn.commit()


    def update_factory(id, location, fact_name, manuf_name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID FROM MANUFACTURERS WHERE COMPANY_NAME = ?;", [manuf_name])
        result = cursor.fetchone()
        if result[0] is not None:
            cursor.execute("UPDATE FACTORIES SET LOCATION = ?, FACTORY_NAME = ?, MANUFACTURER_ID = ? WHERE ID = ?", (location, fact_name,result[0] , id))
            conn.commit()

    def delete_factory(id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE FACTORIES SET IS_DELETE = '1' WHERE ID = ?;", (id))
        conn.commit()


# -------------MANUFACTURERS---METHODS---------------------------
    def insert_manufacturer(email, comp_name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("insert into MANUFACTURERS(EMAIL, COMPANY_NAME, IS_DELETE) values(?,?, '0')", (email, comp_name))
        conn.commit()

    def select_manufacturers():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT ID, EMAIL, COMPANY_NAME FROM MANUFACTURERS WHERE IS_DELETE = '0';")
        return cursor.fetchall()

    def select_manufacturers_name():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COMPANY_NAME FROM MANUFACTURERS WHERE IS_DELETE = '0';")
        return cursor.fetchall()

    def delete_manufacturer(id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE MANUFACTURERS SET IS_DELETE = '1' WHERE ID = ?;", (id))
        conn.commit()

    def update_manufacturer(id, email, comp_name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE MANUFACTURERS SET EMAIL = ?, COMPANY_NAME = ? WHERE ID = ?", (email, comp_name, id))
        conn.commit()

# --------------------USERS----METHODS--------------------------
    def insert_user(login, password, email, user_type, full_name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        cursor.execute("insert into USERS(LOGIN, PASSWORD, EMAIL, USER_TYPE, FULL_NAME, IS_DELETE) values(?,?,?,?,?, '0')", (login, password_hash, email, user_type, full_name))
        conn.commit()

    def update_user(id, login, password_hash, email, user_type, full_name):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        if password_hash == "":
            cursor.execute("UPDATE USERS SET LOGIN = ?, \
            EMAIL = ?, USER_TYPE = ?, FULL_NAME = ? WHERE ID = ?", (login, email, user_type, full_name, id))
       
        else:
            cursor.execute("UPDATE USERS SET LOGIN = ?, PASSWORD = ?, \
            EMAIL = ?, USER_TYPE = ?, FULL_NAME = ? WHERE ID = ?", (login, password_hash, email, user_type, full_name, id))
        conn.commit()
        
    def select_users():
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT ID, LOGIN, EMAIL, USER_TYPE, FULL_NAME FROM USERS WHERE IS_DELETE = '0';''')
        return cursor.fetchall()

    def select_user_full(login):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT ID, LOGIN, EMAIL, USER_TYPE, FULL_NAME FROM USERS WHERE IS_DELETE = '0' AND LOGIN = ?;''', [login])
        return cursor.fetchall()

    def delete_user(id):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE USERS SET IS_DELETE = '1' WHERE ID = ?;", (id))
        conn.commit()

    def get_user_password(login):
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        cursor.execute('SELECT PASSWORD FROM USERS WHERE LOGIN = ? ;', [login])
        result = cursor.fetchone()
        if result is not None:
                return result[0]
        else:
            return None

        
