MITRE ATT&CK Scoring Algorithm and Dashboard

Table of Contents

1. Overview
2. Prerequisites
Using Visual Studio Code (VSCode):
Using Jupyter Notebook:
3. Installation	
4. Dataset
5. Running the Scoring Algorithm
6. Running the Dashboard
7. Usage
8. Troubleshooting
---------------------------------------------------------------------------------------------------------------------------

1. Overview

This project consists of two components:
    1.	Scoring Algorithm: A Python script that calculates a complexity score, prevalence score, and threat actor score for techniques from the MITRE ATT&CK framework.
    2.	Dashboard: A web-based dashboard, built using Dash and Plotly, that visualizes the scoring results, including a 3D globe for tactics by region, heatmaps, bar charts, and pie charts.

------------------------------------------------------------------------------------------------------------------------------------

2. Prerequisites

Before you begin, ensure you have the following installed:
    ●	Python 3.7+
    ●	pip (Python package installer)
    ●	Visual Studio Code (VSCode) (Recommended for editing and running Python scripts)
    ●	Jupyter Notebook (Optional but useful for interactive data exploration and testing)

You will need the following Python libraries:
    ●	pandas
    ●	dash
    ●	plotly
    ●	random

To install the required libraries, run the following command:

    pip install pandas dash plotly

Using Visual Studio Code (VSCode):
    1.	Install VSCode from here.
    2.	Install the Python extension in VSCode for an enhanced coding experience (syntax highlighting, IntelliSense, and running scripts directly).
    3.	Open your project folder in VSCode, and you can run the script directly in the terminal by pressing F5 or using the Run button.

Using Jupyter Notebook:

Install Jupyter by running:

    pip install notebook

  1.	Launch Jupyter by typing the following on the terminal: jupyter notebook
  2.	You can now interactively test your Python scripts in a notebook environment, which is great for data exploration and visualization testing. Simply copy-paste your code into a notebook cell and execute it.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

3. Installation
    1.	Clone this repository or download the scripts manually to your local machine.
    2.	Ensure you have installed all the required Python packages as mentioned above.

Place the dataset (a CSV file) at the specified location. By default, the file path is set to:
makefile
C:\Users\FV2.csv

  3.	Replace this path with the location where your dataset is stored, or modify the script to use your preferred path.

------------------------------------------------------------------------------------------------------------------------------------

4. Dataset
The algorithm expects a CSV file with the following columns:
    ●	tactics: List of tactics involved in the technique (comma-separated values).
    ●	permissions required: Privilege level (e.g., Administrator).
    ●	is sub-technique: Boolean indicating whether the entry is a sub-technique.
    ●	defenses bypassed: Defenses bypassed by the technique (comma-separated values).
    ●	relationship citations: List of relationship citations (comma-separated values).
    ●	created_x: Date of creation of the entry (format: %d-%b-%y).
    ●	Region: Region of the attack or technique.
Ensure that your dataset follows this format for the algorithm to work properly.

------------------------------------------------------------------------------------------------------------------------------------

5. Running the Scoring Algorithm
To calculate the complexity score, prevalence score, and the threat actor score, follow these steps:
  1.	Open the Python script scoring_algo.py.
Ensure that the path to the dataset (FV2.csv) is correct. Modify the following line as needed:

      file_path = r'C:\Users\FV2.csv'  # Replace with your file path

  2.	Run the script from the command line:

      python algo.py

  3.	The script will process the dataset, calculate the scores, and save the results to a new CSV file at the same location as the original file.

------------------------------------------------------------------------------------------------------------------------------------

6. Running the Dashboard To visualize the scoring results with the dashboard:
   
  1.	Open the dashboard.py file.
Ensure that the path to the dataset in the dashboard script is correct. Modify the following line as needed:

    file_path = r'C:\Users\FV2.csv'  # Replace with your file path
  
  2.	Run the dashboard script from the command line:

    python dashboard.py

  3.	Open a web browser and navigate to http://127.0.0.1:8050/. The dashboard will be available at this address.

------------------------------------------------------------------------------------------------------------------------------------

7. Usage
The dashboard provides various interactive visualizations:
  ●	3D Globe: Displays the tactics used by the country, with randomized coordinates for better visualization.
  ●	Bar Chart: Displays the top 10 techniques by threat actor score.
  ●	Pie Chart: Shows the distribution of techniques by region.
  ●	Heat Map: Visualizes defenses bypassed against tactics.
  ●	Line Chart: Displays the cumulative prevalence score over time by region.
Use the dropdown filters to interact with different aspects of the dataset and visualize the results dynamically.

------------------------------------------------------------------------------------------------------------------------------------

8. Troubleshooting
  ●	Dataset Issues: Ensure your CSV file has the correct columns and data format. The code will fail if the dataset does not follow the expected structure.
  ●	Dashboard Not Running: If the dashboard doesn’t load, ensure that no other service is using port 8050. Try changing the port number in the app.run_server() call if needed.
