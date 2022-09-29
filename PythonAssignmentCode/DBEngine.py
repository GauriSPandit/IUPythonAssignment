import sqlalchemy as db
from Exceptions import SQLQueryException

"""
    This class models a database engine allowing insert queries on data
    to store data in sqlite database
"""
class DBEngine():

    #Create connection on instantiation
    def __init__(self, filename):
        self.__conn = db.create_engine('sqlite:///output/' + filename).connect()

    #Method to insert trainng data
    def insert_training_data(self, row):

        if self.__conn.closed:
            raise SQLQueryException("Failed to create database connection!")
        else:
            self.__conn.execute("INSERT INTO training_data (x, y1, y2, y3, y4) VALUES (" + str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "," + str(row[4]) + ")")

    #Method to insert ideal data
    def insert_ideal_data(self, row):

        if self.__conn.closed:
            raise SQLQueryException("Failed to create database connection!")
        else:
            query = "INSERT INTO ideal_data (x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24, y25, y26, y27, y28,"
            query += "y29, y30, y31, y32, y33, y34, y35, y36, y37, y38, y39, y40, y41, y42, y43, y44, y45, y46, y47, y48, y49, y50) VALUES (" + str(row[0]) + "," + str(row[1]) + ","
            query += str(row[2]) + "," + str(row[3]) + "," + str(row[4]) + "," + str(row[5]) + "," + str(row[6]) + "," + str(row[7]) + "," + str(row[8]) + "," + str(row[9]) + "," + str(row[10]) + ","
            query += str(row[11]) + "," + str(row[12]) + "," + str(row[13]) + "," + str(row[14]) + "," + str(row[15]) + "," + str(row[16]) + "," + str(row[17]) + "," + str(row[18]) + "," + str(row[19]) + ","
            query += str(row[20]) + "," + str(row[21]) + "," + str(row[22]) + "," + str(row[23]) + "," + str(row[24]) + "," + str(row[25]) + "," + str(row[26]) + "," + str(row[27]) + "," + str(row[28]) + ","
            query += str(row[29]) + "," + str(row[30]) + "," + str(row[31]) + "," + str(row[32]) + "," + str(row[33]) + "," + str(row[34]) + "," + str(row[35]) + "," + str(row[36]) + ","
            query += str(row[37]) + "," + str(row[38]) + "," + str(row[39]) + "," + str(row[40]) + "," + str(row[41]) + "," + str(row[42]) + "," + str(row[43]) + "," + str(row[44]) + ","
            query += str(row[45]) + "," + str(row[46]) + "," + str(row[47]) + "," + str(row[48]) + "," + str(row[49]) + "," + str(row[50]) + ")"
            self.__conn.execute(query)

    #Method to insert test data
    def insert_test_data(self, x_datapoint, y_datapoint):

        if self.__conn.closed:
            raise SQLQueryException("Failed to create database connection!")
        else:
            self.__conn.execute("INSERT INTO test_data (x, y) VALUES (" + str(x_datapoint) + "," + str(y_datapoint) + ")")

    def update_test_data(self, x_datapoint, deviation, y_function):
        self.__conn.execute("UPDATE test_data SET delta_y=" + str(deviation) + ", ideal_func='" + y_function + "' WHERE x=" + str(x_datapoint))

    def select(query):
        return 0
    
    def close(self):
        self.__conn.close()