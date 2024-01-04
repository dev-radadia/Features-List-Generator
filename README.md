# Features-List-Generator

## Description:
The main objective of this project is to build a Features List Generator tool using the power of Generative AI. The program should be capable of generating a list of necessary modules and submodules required in a project (The user will provide the project name).
The project will be made from scratch using suitable Python Libraries and APIs. 

## Features:
This tool should be able to carry out the following tasks:
1. The user will provide the project name for which they want a list of features.
2. If the features list for the given project name is already present in the MongoDB Database then the program will fetch the data from there, otherwise, the program will generate the names of the most common modules and submodules required for the project using PaLM API.
3. The program will then display the features list on the screen.
4. If the user wants the download the result then it will map the result into an Excel sheet with a suitable format.

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
