# Features-List-Generator

## Description:
This is a Features List Generator tool integrated with the power of Generative AI. This tool is capable of generating a list of necessary modules and submodules required to build a project (The user provides the project name).
The program is made from scratch using suitable Python Libraries and APIs. 

## Features:
This tool can carry out the following tasks:
1. The user provides the name of the project for which they want a list of features.
2. If the features list for the given project name is already present in the MongoDB Database then the program fetches the data from there, otherwise, the program generates the names of the most common modules and submodules required for building the project using PaLM API.
3. The program then displays the features list on the screen.
4. If the user wants to download the result, it maps the data into an Excel sheet with a suitable format.

## Technology Stack:
### Programming Language:
Python 3.10.3
### Python Libraries:
Google, Flask, Pandas
### API:
PaLM API (_Python Module:_ google.generativeai)
### Web Development:
HTML, CSS, JavaScript
### Database:
MongoDB
