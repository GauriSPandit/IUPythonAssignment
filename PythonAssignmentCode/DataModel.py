import math
import pandas as pd
from Exceptions import FileNotFoundException
from DBEngine import *
import VisualizationEngine as engine

"""
    This class models a data model which can be used to perform
    regression analysis using least square method
"""
class DataModel():
    def __init__(self):
        self.__trainingData = None
        self.__idealData = None
        self.__leastIdealData = None
        self.__testData = None
        self.__regressedData = []

    """
        This method loads training dataset into data member
        Data set is stored as pandas dataframe. It further saves
        the data in the SQLITE database
        :param filename: Training dataset file name
    """
    def train(self, filename):
        try:
            self.__trainingData = pd.read_csv(filename)
        except:
            raise FileNotFoundException("Failed to open " + filename)

        # trainingData = self.__trainingData.values.tolist()

        # DB = DBEngine("database.db")
        # for row in trainingData:
        #      DB.insert_training_data(row)
        # print("Training data saved successfully!")
        
        #DB.close()

    """
        This method loads reads the ideal data from the csv file and 
        store the same within class as pandas dataframe. Further, it
        finds four most ideal functions to be used for regression.
        The same is stored as pandas dataframe in __leastIdealData property
        Further, ideal dataset is inserted into the database
        :param filename: Ideal dataset file name
    """
    def idealise(self, filename):
        #Get all y datasets
        df = pd.read_csv(filename)
        self.__idealData = df

        newDF = df.drop('x', axis=1)

        #Calculate mean for each ideal dataset
        mean = newDF.mean().values.tolist()

        #Convert dataframe to 2D matrix
        data_table = newDF.values.tolist()
        squared_deviations = {}

        #Initialize squared deviation for each dataset
        for index in range(1,51):
            squared_deviations["y" + str(index)] = 0
        
        #Loop through matrix to calcuate sum of squared dev. for each dataset
        for rowIndex in range(0,len(data_table)):
            #Extract a row
            row = data_table[rowIndex]

            #Add squared dev. for each dataset index to the sum
            for colIndex in range(0,len(row)):
                squared_deviations["y" + str(colIndex + 1)] = squared_deviations["y" + str(colIndex + 1)] + math.pow(row[colIndex] - mean[colIndex], 2)
        
        #Sort dictionary of sum over squared deviations in ascending order
        sorted_squared = sorted(squared_deviations.items(), key=lambda x: x[1])

        #Filter the dataframe to presere 4 ideal datasets with least sum of squared deviations
        self.__leastIdealData = self.__idealData[['x', sorted_squared[0][0], sorted_squared[1][0], sorted_squared[2][0], sorted_squared[3][0]]]

        # idealData = self.__idealData.values.tolist()
        # DB = DBEngine("database.db")
        # for row in idealData:
        #      DB.insert_ideal_data(row)
        # print("Ideal data saved successfully!")

    """
        This method leads test dataset from csv file, stores the same
        in pandas dataframe, and processes each datapoint to calculate
        deviations and map ideal functions.
        :param filename: Test dataset file name
    """
    def test(self, filename):
        #Store test data
        self.__testData = pd.read_csv(filename)
        #Map test data to list
        self.__processTestData()
        print("Test data saved successfully!")
    
    """
        This method perform regression on test datapoints and maps the same
        with ideal functions. Stores the datapoints in list
    """
    def __processTestData(self):

        test_data = self.__testData.values.tolist()
        #DB = DBEngine("database.db")

        #Process each datapoint
        for index in range(0, len(test_data)):
            test_x = test_data[index][0]
            test_y = test_data[index][1]

            #Get ideal and training dataset matching test datapoint
            ideal_data = self.__leastIdealData.loc[self.__leastIdealData['x'] == test_x].values.tolist()[0]
            training_data = self.__trainingData.loc[self.__trainingData['x'] == test_x].values.tolist()[0]

            #DB.insert_test_data(test_x, test_y)
            
            max_deviation = -10000
            max_index = 0
            for idealIndex in range(1, len(ideal_data)):
                test_ideal_dev = test_y - ideal_data[idealIndex]
                calculated_deviation = self.__getMaxDeviation(training_data, ideal_data[idealIndex]) * math.sqrt(2)

                if test_ideal_dev < calculated_deviation and calculated_deviation > max_deviation:
                    max_deviation = calculated_deviation
                    max_index = idealIndex

            if max_deviation != -10000:
                #DB.update_test_data(test_x, max_deviation, self.__leastIdealData.columns.values[max_index])
                print("Test_x: " + str(test_x) + " | Test_y: " + str(test_y) + " | Dev: " + str(max_deviation) + " | ideal_index: " + self.__leastIdealData.columns.values[max_index])
                point = {}
                point["x"] = test_x
                point["y"] = test_y
                point["dev"] = max_deviation
                point["ideal_function"] =  self.__leastIdealData.columns.values[max_index]
                self.__regressedData.append(point)
        #DB.close()
    
    #Method to plot data on graphs
    def visualize(self):
        engine.plotTrainingAndIdealData(self.__trainingData, self.__leastIdealData)
        engine.plotTestData(self.__regressedData, self.__leastIdealData)

    def __getMaxDeviation(self, trainingData, idealFunction):
        maxValue = math.inf * -1

        for value in trainingData:
            if idealFunction - value > maxValue:
                maxValue = idealFunction - value

        return maxValue

    def gettrainingData(self):
        return self.__trainingData

    def getregressedData(self):
        return self.__regressedData

    def getidealData(self):
        return self.__idealData


def main():
    tmp = DataModel()
    tmp.train("data\\train.csv")
    tmp.idealise("data\\ideal.csv")
    tmp.test("data\\test.csv")
    tmp.visualize()
main()