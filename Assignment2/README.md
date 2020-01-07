# Assignment 2: Static Visualization

In this assignment, you need to choose a dataset and create three visualizations to show two different insights. For visualization, you can choose to use Jupyter Notebook (Python), Observable Notebook (JavaScript), or Tableau (GUI).  This is an individual assignment, so you may not work in groups. Your final submission will take the form of a report including the visualizations you created and the description of the insights you gained from the visualizations.

### Step 1: Choose a visualization tool 

* [Jupyter Notebook on Colab](https://colab.research.google.com/) (Python)
* [Observable Notebook](http://observablehq.com/) (JavaScript)
* [Tableau Public](https://public.tableau.com/en-us/s/) (GUI)

You can use one of these visualization tools based on your interest. If you're more interested in data analysis and exploration, we recommend using Python with Jupyter Notebook. If you're more interested in visualization design, user interface, and HCI, we recommend using JavaScript with Observable Notebook. If you are unsure or your major is not Computer Science, you can choose to use Tableau, which provides GUI for creating visualizations.

Two examples for visualization and analysis of a multidimensional dataset are provided:
*  [Examples in Colab](https://colab.research.google.com/drive/1PHrxxup8Iza3qbpeoSYwiQqexc96e-9H)
*  [Examples in Observable](https://observablehq.com/d/123f819bd5e5a92b)

Here are the tutorials for each of these tools:
* Colab: [Welcome To Colaboratory](https://colab.research.google.com/notebooks/welcome.ipynb#)
* Observable: [Five-Minute Introduction to Observable](https://observablehq.com/@observablehq/five-minute-introduction)
* Tableau: [Get Started with Tableau Desktop](https://help.tableau.com/current/guides/get-started-tutorial/en-us/get-started-tutorial-home.htm)
  

### Step 2: Choose a dataset from the list below

* [LAX Passenger Counts by Terminal](https://data.lacity.org/A-Prosperous-City/Los-Angeles-International-Airport-Passenger-Traffi/g3qu-7q2u)
* [Film Locations in San Francisco](https://data.sfgov.org/Culture-and-Recreation/Film-Locations-in-San-Francisco/yitu-d5am)
* [List of Historical Ballot Measures in San Francisco](https://data.sfgov.org/City-Management-and-Ethics/List-of-Historical-Ballot-Measures/xzie-ixjw)
* [Louisville Restaurant Health Inspections](https://data.louisvilleky.gov/dataset/restaurant-inspection-data)

#### Loading the data
For Observable notebook and Tableau, you can attach or load the dataset as CSV files.

For Colab, you can use the datasets stored in our data server for this assignment by using the following URLs (also see how to use "urllib.request" to load the datasets in the [Examples in Colab](https://colab.research.google.com/drive/1PHrxxup8Iza3qbpeoSYwiQqexc96e-9H)):
* LAX Passenger Counts by Terminal - http://stream.cs.ucdavis.edu/datasets/LAX_Terminal_Passengers.csv
* Film Locations in San Francisco - http://stream.cs.ucdavis.edu/datasets/SF_Flim_Locations.csv
* List of Historical Ballot Measures in San Francisco - http://stream.cs.ucdavis.edu/datasets/SF_Historical_Ballot_Measures.csv
* Louisville Restaurant Health Inspections - http://stream.cs.ucdavis.edu/datasets/Restaurant_Inspection.csv


### Step 3: Process the data

Next, you are going to load the chosen dataset to your selected tool for processing and visualization. For Jupyter and Observable, please refer to coding templates provided in the example folder. For Tableau, just use the GUI to load and process the data.

To process and transform the data for analysis, we recommend the following: 

* Jupyter Notebook: [Pandas](https://pandas.pydata.org/) (data processing and analysis library for Python)
* Observable: [Vega-Lite](https://vega.github.io/vega-lite/) (declarative grammars for data transformations and visualization)
* Tableau: its GUI provides basic operations for processing and transforming data; you can refer to [this tutorial](https://www.tutorialspoint.com/tableau/index.htm) to learn how to use Tableau if you want

### Step 4: Analyze and visualize the data


For visualizing the data, we recommend the following: 
* [Seaborn](https://seaborn.pydata.org/) or [Altair](https://altair-viz.github.io/) for Jupyter Notebook
* [Vega-Lite](https://vega.github.io/vega-lite/) for Observable Notebook
* For Tableau, just play with the GUI to create visualizations; if needed, please refer to the [tutorial on how to use Tableau](https://www.tutorialspoint.com/tableau/index.htm)

You can also use any other libraries for processing and visualizing the data with Python or JavaScript.

## Submission
For Colab and Observable notebooks, enable link sharing for your notebook and submit the link to Assignment 2 in UCD Canvas. For Tableau, you would need to submit a report containing the visualizations and explanation of your insights.
