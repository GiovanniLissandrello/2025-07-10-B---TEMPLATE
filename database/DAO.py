from database.DB_connect import DBConnect
from model.arco import Arco
from model.categoria import Categoria
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategorie():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from categories c"

        cursor.execute(query)

        for row in cursor:
            results.append(Categoria(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(idcategoria):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from products p 
                    where p.category_id = %s"""

        cursor.execute(query, (idcategoria,))

        for row in cursor:
            results.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArchi(anno1,anno2,idcategoria,idMap):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.product_id as id1, t2.product_id as id2, (t1.vendite + t2.vendite) as peso
                    from (select p.product_id , sum(oi.quantity) as vendite
                    from products p, orders o, order_items oi 
                    where p.product_id = oi.product_id  
                    and o.order_id = oi.order_id
                    and o.order_date between %s and %s
                    and p.category_id = %s
                    group by p.product_id) t1,
                    (select p.product_id , sum(oi.quantity) as vendite
                    from products p, orders o, order_items oi 
                    where p.product_id = oi.product_id  
                    and o.order_id = oi.order_id
                    and o.order_date between %s and %s
                    and p.category_id = %s
                    group by p.product_id ) t2
                    where t1.vendite <= t2.vendite
                    and t1.product_id != t2.product_id """

        cursor.execute(query, (anno1,anno2,idcategoria,anno1,anno2,idcategoria))

        for row in cursor:
            results.append(Arco(idMap[row["id1"]], idMap[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results

