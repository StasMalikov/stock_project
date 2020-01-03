from app.db_utils import DbUtils

class Utils:
    def get_products():
        tmp = DbUtils.select_products()
        result = []
        for i in range(len(tmp)):
            result.append(Product(tmp[i]))
        return result

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