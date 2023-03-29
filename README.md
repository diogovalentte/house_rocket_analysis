# House Rocket Analysis
## OBJECTIVE:
1. Do an exploratory analysis on a dataset with the objective of getting insights and hypotesis.
2. Answer the requests of an imaginary CEO of the House Rocket company.
3. Create a simple web app to visualize the data with maps, tables, and filters.
---

## The source dataset:
The dataset is from **[Kaggle](https://www.kaggle.com)** and can be found **[here](https://www.kaggle.com/harlfoxem/housesalesprediction)** with the dataset schema description.

Dataset description: "This dataset contains home sales prices for King County, which includes Seattle. It includes homes sold between May 2014 and May 2015.
It's a great dataset for evaluating simple regression models."

---

## Imaginary business questions:
The House Rocket works with buying and selling houses. The CEO of House Rocket asked us to analyze the dataset with multiple available houses for purchase and answer four questions:
1. Which houses should House Rocket buy and by which price?
2. Once the houses are bought, for what price should they be sold?
3. What is the best time of the year to sell the houses?
4. The House Rocket should renovate the houses to increase the selling price? What parts of the houses should the House Rocket renovate? What is the price increase given for each renovation option?
---

## Analysis:
The dataset analysis is divided into three Python notebooks:

### 1.0-Data_Exploratory:
In this analysis the dataset has been explored with the following objectives:
1. Identify the duplicated or missing values from the dataset and treat them if necessary.
2. Calculate descriptive statistics of the dataset.
3. Identify outliers on the dataset and treat them if necessary.
4. Identify the correlation between the houses features and the house price.

### 2.0-Main_Questions:
In this analysis, the [CEO business questions](#imaginary-business-questions) are answered. In addition to that, we generate a table with the recommended houses to buy, at what price to sell them if they are renovated or not, and the possible profit.

### 3.0-Hypotheses:
In this analysis, we create and answer our own hypothesis about the dataset.

---
## Web App:
The web app is a dashboard with the main insights, data samples, maps, and filters to use.

---
## How to start the dashboard or the notebooks environment:
1. Install the Python dependencies:
```sh
pip install -r requirements.txt
```
2. Start the dashboard. Will show the URL of the dashboard. Copy and paste on your web browser:
```sh
./init.sh dashboard
```
3. Start the environment to see and execute the notebooks:
```sh
./init.sh notebooks
```
