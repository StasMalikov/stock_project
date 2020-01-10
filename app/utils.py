from app.db_utils import DbUtils

class Utils:
    def get_products():
        tmp = DbUtils.select_products()
        result = []
        for i in range(len(tmp)):
            result.append(Product(tmp[i]))
        return result

    def get_prod_units():
        tmp = DbUtils.select_product_units_all()
        result = []
        for i in range(len(tmp)):
            result.append(ProductUnit(tmp[i]))
        return result

    def get_product_id(id):
        tmp = DbUtils.select_product_id(id)
        return Product(tmp[0])
    
    def clear_select(select0, non_select0):
        if isinstance(select0, str):
            select = set()
            select.add(select0)
        else:
            select = set(select0)
        
        non_select = set()
        for i in range(len(non_select0)):
            non_select.add(non_select0[i][0])
        return list(non_select.difference(select))

class Product:
    def __init__(self, obj):
        self.id = obj[0]
        self.name = obj[1]
        self.factory = DbUtils.select_factories_name(obj[2])[0][0]
        self.product_type = DbUtils.select_product_types_name(obj[3])[0][0]
        self.calories = obj[4]
        self.expiration = obj[5]
        self.dimension = obj[6]
        self.weight = obj[7]
        self.picture = obj[8]
        self.ingridients = []
        tmp = DbUtils.select_product_ingredient(obj[0])
        for i in range(len(tmp)):
            self.ingridients.append(tmp[i][0])

class ProductUnit:
    def __init__(self, obj):
        self.id = obj[0]
        self.name = obj[1]
        self.factory = DbUtils.select_factories_name(obj[2])[0][0]
        self.product_type = DbUtils.select_product_types_name(obj[3])[0][0]
        self.calories = obj[4]
        self.expiration = obj[5]
        self.dimension = obj[6]
        self.weight = obj[7]
        self.picture = obj[8]
        self.ingridients = []
        tmp = DbUtils.select_product_ingredient(obj[0])
        for i in range(len(tmp)):
            self.ingridients.append(tmp[i][0])

        self.unit_id = obj[9]
        self.quantity = obj[10]
        self.manufacture_date = obj[11] 
        self.relevance = obj[12]
        self.price = obj[13]
