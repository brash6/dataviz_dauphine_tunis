## Project requirements

The module evaluation wil be done with a technical project assignment. This project will be done in groups of 2 using the best practices of software engineering collaboration. 

The students have to develop a data application using [panel](https://panel.holoviz.org/index.html). They are expected to work using Github and to give a link of both the deployed app link and the github repository in which it's developed.

(Panel enables easy deployment and hosting using github for example, checkout : https://panel.holoviz.org/user_guide/Running_in_Webassembly.html)

The final grade will depend on : 

- Code cleanness and readability
- Project structure
- Commits and PRs relevance in the Github repo
- Relevance of the dashboard from a business perspective 
- Respect of data viz best practices 
- Beauty of the visualisations

## Project description

The project purpose is to answer a business question related to [the following dataset](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams) (Student's performance in exams) : 

<strong>How can we explain and predict both math, reading and writing scores of high school students in the United States ?</strong>

The data application is expected to have : 

- A home page from which every dashboards are accessible 
- A dashboard enabling the user to explore the dataset : This dashboard should have a side bar in which the user can select different filters (columns of the dataset). The plots (bar plots, scatter plots, box plots, line plots, etc.) should be efficiently designed and each one should give a relevant amount of information.  
- A dashboard to present the results of your analysis and your answer to the business question. Regression, Clustering, Neural Networks, etc, use the Machine Learning algorithms/models you want to answer the question. This dashboard can also be interactive with filters and widgets. 
- A third optional dashboard to present further analysis

Each dashboard should have a "Refresh dashboard" button. 
They can also include in-dashboard widgets triggering functions live on modification.

## Resources

- Panel website : https://panel.holoviz.org/
- Panel discourse : https://discourse.holoviz.org/c/panel/5
- Bokeh discourse : https://discourse.bokeh.org/
- awesome-panel github repository : https://github.com/awesome-panel/awesome-panel