from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getY():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct YEAR(s.`datetime`) as y
                           from sighting s 
                           order by `datetime` DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["y"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getS(y):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []
        query = """select distinct shape
                       from sighting s 
                       where s.shape is not null and year(s.`datetime`) = %s
                       order by shape"""
        cursor.execute(query, (y,))

        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getN(y, s):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []
        query = """select distinct *
                        from sighting 
                        where shape = %s and year(`datetime`) = %s"""
        cursor.execute(query, (s, y))
        for row in cursor:
            result.append(Sighting(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getA(y, s):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        result = []
        query = """with tavola as(select s.id as id, s.state as st, s.longitude  as lon
                    from sighting s
                    where shape = %s and year(`datetime`) = %s)
                    select t1.id as idd, t2.id as idd2, t1.lon as l1, t2.lon as l2 
                    from tavola t1, tavola t2
                    where t1.st = t2.st and t1.lon < t2.lon"""
        cursor.execute(query, (s, y))
        for row in cursor:
            result.append((row["idd"], row["idd2"], row["l1"], row["l2"]))
        cursor.close()
        cnx.close()
        return result
