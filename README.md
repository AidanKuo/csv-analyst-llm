# CSV Analyst Bot

## Overview

This app uses streamlit ui and OpenAI's API to create an analyst bot that takes a clean dataset and can give the user insights/visualizations through python code after the user asks a business related question.

## Features

### Csv Upload

A core feature of this project is the ability to upload a cleaned CSV in order to read and make inferences on the data given.

![](img\csvupload.png)

### Data Preview

Providing a data preview helps guide users with what questions might provide the best answers with the data given.

![](img\datapreview.png)

### Question Box

A question box is provided where the user can ask questions to the bot in relation to the csv file the user has already given.

![](img\questionbox.png)

### Tailored insights

After a question has been asked, the bot will create a visualization based on the code it created which best fits the question asked and outputs the code it created, a visualization, and a summary of an answer to the question.

![](img\usage.png)