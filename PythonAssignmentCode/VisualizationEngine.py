from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column

"""
    This function plots training and ideal datafunction on graphs
    using one to one mapping on index values
    :param trainingDF: Pandas dataframe containing 4 training datasets
    :param idealDF: Pandas dataframe containing 4 selected ideal dataset
"""

# Few dummy changes are added for replicating push on git branch

def plotTrainingAndIdealData(trainingDF, idealDF):
    
    graphs = []
    val = 1

    for index in range(4):
        graphs.append(createGraph(trainingDF, idealDF, val))
        val += 1
    
    output_file("training_and_ideal_viz.html")
    show(column(graphs))

"""
    This function returns a graph of training and ideal data
    Ideal data is presented on line
    Training data as scatter points
    :param trainingDF: Pandas dataframe containing training datasets
    :param idealDF: Pandas dataframe containing ideal datasets
    :index : Index value of pandas dataframe column to extract values from
"""
def createGraph(trainingDF, idealDF, index):

    heading = "Training Dataset " + trainingDF.columns.values[index]
    heading += " vs Ideal Dataset " + idealDF.columns.values[index]
    
    graph = figure(title= heading, x_axis_label='X', y_axis_label='Y')
    graph.scatter(trainingDF['x'], trainingDF[trainingDF.columns.values[index]], fill_color="red", legend_label="Training")
    graph.line(idealDF["x"], idealDF[idealDF.columns.values[index]], legend_label="Ideal")

    return graph

"""
    This function returns a graph of training and ideal data
    Ideal data is presented on line
    Training data as scatter points
    :param regressedDF: List of datapoints where each datapoint is a dictionary
                        having structure: {'x': value, 'y': value, 'dev': value, 'ideal_function': value}
    :param idealDF: Pandas dataframe containing ideal datasets
"""
def plotTestData(regressedDF, idealDF):

    graphs = []

    for datapoint in regressedDF:
        graphs.append(createPointGraph(datapoint, idealDF))
    
    output_file("test_data_viz.html")
    show(column(graphs))

"""
    This function returns a graph of test data and ideal data
    Ideal data is presented on line
    Test data as scatter points
    :param datapoint: Test datapoint dictionary having following structure: {'x': value, 'y': value, 'dev': value, 'ideal_function': value}
    :param idealDF: Pandas dataframe containing ideal datasets
"""
def createPointGraph(datapoint, idealDF):

    datapointStr = "(" + str(datapoint["x"]) + "," + str(datapoint["y"]) + ")"
    heading = "Test point " + datapointStr + " with ideal function " + datapoint["ideal_function"]

    graph = figure(title=heading, x_axis_label='X', y_axis_label='Y')
    graph.line(idealDF["x"], idealDF[datapoint["ideal_function"]], legend_label="Ideal Function")

    graph.scatter([datapoint["x"]], [round(datapoint["y"], 4)], fill_color="red", legend_label="Test Datapoint", size = 10)
    return graph