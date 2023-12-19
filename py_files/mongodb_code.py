# Import libraries
from pymongo.mongo_client import MongoClient
import pandas as pd
import re

# Function to connect to MongoDB Database
def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    uri = "mongodb+srv://dev:knowledge@cluster0.sbemqrk.mongodb.net/?retryWrites=true&w=majority"

    try:
        # Create a new client and connect to the server
        client = MongoClient(uri)
    except:
        return -1

    try:
        db = client.project_names
    except:
        db = client["project_names"]

    return db

# Function to check whether the data already exists or not
def data_exists(collection, projectName):
    # Remove all characters except letters and numbers from project name
    projectName = re.sub(r'[\W_]+', '', projectName)

    # Convert the string to lowercase
    projectName = projectName.lower()

    if collection.count_documents({"ProjectName": projectName}, limit = 1):
        return True
    else:
        return False

# Function to load the data into MongoDB Database
def load_data(collection, projectName, df):
    # Remove all characters except letters and numbers from project name
    projectName = re.sub(r'[\W_]+', '', projectName)

    # Convert the string to lowercase
    projectName = projectName.lower()

    # Reset indexes of the Pandas Dataframe
    df = df.reset_index()

    # Load data into the database
    collection.insert_one({"ProjectName": projectName, "Data": df.to_dict('records')})

# Function to fetch the data from MongoDB Database
def fetch_data(collection, projectName):
    # Remove all characters except letters and numbers from project name
    projectName = re.sub(r'[\W_]+', '', projectName)

    # Convert the string to lowercase
    projectName = projectName.lower()

    # Fetch data from the database
    data_from_db = collection.find_one({"ProjectName": projectName})

    # Convert the fetched data into a Pandas Dataframe
    df = pd.DataFrame(data_from_db["Data"])

    # Get a list having names of all the columns present in the dataframe
    column_names = list(df.columns)

    # Set the index of the Pandas Dataframe
    df = df.set_index(column_names)

    return df