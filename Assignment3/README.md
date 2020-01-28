# Assignment 3: Visualization Dashboard

In this assignment, you will be learning how to implement a dashboard with two visualization views. You can use either JavaScript with [D3.js](https://d3js.org) or Python with [Dash](https://dash.plot.ly/?_ga=2.191292847.426805754.1574706741-53947978.1573166595) to do this assignment. 

Before coding, please go over one of the following tutorials:
* D3: [Introduction](https://d3js.org/#introduction), [Bar Chart Example](http://bost.ocks.org/mike/bar/), [Selection](http://bost.ocks.org/mike/selection/), [Update Patterns](https://www.d3indepth.com/enterexit/)
* Dash: Dash Tutorial [Part 1](https://dash.plot.ly/installation), [2](https://dash.plot.ly/getting-started), and [3](https://dash.plot.ly/getting-started-part-2).

If you need to learn more about JavaScript or Python, you can refer to [A re-introduction to JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/A_re-introduction_to_JavaScript) or [Python Basics](https://www.learnpython.org/).


## Datasets

In this assignment, you can choose one of the following datasets:

* [LAX Passenger Counts by Terminal](https://data.lacity.org/A-Prosperous-City/Los-Angeles-International-Airport-Passenger-Traffi/g3qu-7q2u)
* [Film Locations in San Francisco](https://data.sfgov.org/Culture-and-Recreation/Film-Locations-in-San-Francisco/yitu-d5am)
* [List of Historical Ballot Measures in San Francisco](https://data.sfgov.org/City-Management-and-Ethics/List-of-Historical-Ballot-Measures/xzie-ixjw)
* [Louisville Restaurant Health Inspections](https://data.louisvilleky.gov/dataset/restaurant-inspection-data)
* [SF Crime Dataset](https://www.kaggle.com/roshansharma/sanfranciso-crime-dataset)
* [Global Terrorism Database](https://www.kaggle.com/START-UMD/gtd)
  
To use a dataset, download data file from one of the URLs above and put it in the "datasets" folder under the Assignment 3 directory. (Note: __DO NOT__ add or commit the data file to the Git repository).


### Coding Template

To help you get started, you can use a template for setting up the application and load the dataset. For D3.js, you can use the "D3-template" in the Assignment 3 folder. For Dash, you can use the example in the [Dash Tutorial Part 3](https://dash.plot.ly/getting-started-part-2).


## Requirement

Your task is then to implement a visualization dashboard. The design of this dashboard should facilitate analysis of the dataset in an effective or interesting way. This dashboard must have two visualization views. Your visualizations should include one basic and one advanced visualization methods. The two visualizations should depict different dimensions or aspects of the dataset to be examined. You can also support visual analysis techniques, such as context + focus. For instance, a bubble chart can be used as a primary view while selecting a bubble, a bar chart may be used to display extra information.


### Examples of basic visualization methods
* Bar chart
* Pie or donut chart
* Line and area chart
* 2D heatmap or matrix view
* Scatter plot or bubble chart
* Node-link diagram
* Geographical map

### Examples of more advanced visualization methods
* Parallel set or parallel coordinates plot
* Sankey or alluvial diagram
* Star coordinates or plot
* Chord diagram
* Stream graph
* Arc diagram

For each view, you need to provide one or more visual interface widgets (e.g., a dropdown menu or slider) for changing the parameters of the visualization. For examples, a drop-down menu can be provided for selecting the data dimension that maps to the x-axis of a scatter plot or the color encoding used in a 2D heatmap.

## Submission
To submit this assignment, follow the procedures below:
* Create a new folder inside the Assignment 3 directory in the forked repository for Assignment 1. The name of the folder should be the same as your UC Davis email account name (without ' @ucdavis.edu'). 
* Put all your codes inside this folder, and use "git add" to add all your codes, and then commit.
* After commit and push all the codes to your own repository, create a pull request by following the same procedure used for Assignment 1 (see instructions [here](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork)). 
* To complete your submission, submit the hyperlink of the pull request in UCD Canvas. 
