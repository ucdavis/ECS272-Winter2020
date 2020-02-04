# Assignment 4: Interactive Visualization System

For this assignment, you will implement a system that integrates interactive visualizations with advanced data analytics methods (e.g., ML and NLP) for exploring a complex dataset of your choice. You should work in __teams of 2 students__ for this assignment.


## Requirement
The interactive visualization system to be implemented must incorporate at least one of the following data analytics methods:

* Dimensionality reduction
* Clustering
* Factor analysis
* Natural language processing

You should choose the proper data analytics method(s) based on your dataset.

For visualization, the system needs to have a dashboard consisting 3 linked views, including both an overview and detail view of the analysis results. Similar to Assignment 2, one of the views must be using an advanced visualization method (i.e., it cannot be a scatter plot, bar chart, pie chart or other similar basic plots).

In addition, the dashboard needs to have two types of user interaction:

* __Interaction Type 1__: Widgets for configuring/adjusting the parameters of the data analytics method
* __Interaction Type 2__: Selection of items in the overview for displaying extra information about the selected items in the detail view. The interaction for selection can be mouse click, mouse over, zooming, or lasso selection.

For example, if K-Means clustering is used for analyzing a multidimensional dataset, the dashboard should have a widget for users to control the value of _k_ (the number of clusters should be in the result), and the clustering results can be displayed in the overview visualization with a lasso selection (see an [example](https://bl.ocks.org/skokenes/a85800be6d89c76c1ca98493ae777572) here).


For system implementation, you can use either JavaScript or Python. You can also use a server-client architecture for implementing the system, which you can Javascript for the visualization frontend and Python for the server backend.

## Resource

You can select a dataset from the list below or use any other dataset that you want:

* [List of historical ballot measures in SF](https://data.sfgov.org/City-Management-and-Ethics/List-of-Historical-Ballot-Measures/xzie-ixjw)
* [The Movie Database (metadata for 5,000 movies)](https://www.kaggle.com/tmdb/tmdb-movie-metadata)
* [Student alcohol consumption link](https://www.kaggle.com/uciml/student-alcohol-consumption)
* [Pokemon dataset link](https://www.kaggle.com/alopez247/pokemon)
* [freeCodeCamp 2017 Survey](https://www.kaggle.com/fccuser/the-freecodecamp-2017-new-coder-survey)
* [Young people survey link](https://www.kaggle.com/miroslavsabo/young-people-survey)


__JavaScript__ data analysis libraries:
* [ml.js](https://github.com/mljs/ml) - Dimensionality reduction and clustering
* [supercluster](https://github.com/mapbox/supercluster) - geospatial point clustering
* [compromise](https://github.com/spencermountain/compromise) and [NLP.js](https://github.com/axa-group/nlp.js) - NLP

__Python__ data analysis libraries: 
* [Scikit-learn](https://scikit-learn.org/) - Machine learning for data mining and analysis
* [Prince](https://github.com/MaxHalford/Prince) - Factor analysis
* [Natural Language Toolkit](https://www.nltk.org/) - NLP

## Submission
To submit, push all your source codes to the forked repository you used for Assignment 1 and 3. For this assignment, you do not need to create a pull request. Instead, submit the hyperlink to your repository in UCD Canvas.
After submission, please make an appointment to meet with the TA for grading this assignment. Please be prepared to answer questions about the tasks you did for this assignment, which is listed below with the grading breakdown: 

* Data Analysis Method (30 pts)
* Overview Visualization (10 pts)
* Detailed Visualization (10 pts)
* Third Visualization (10 pts) - Either an additional overview or detail, or another linked view.
* System Design and Interactions (40 pts)
  * Selecting data points within the overview
  * Views are linked together
  * Application of data analysis method makes sense
  * System design makes sense
