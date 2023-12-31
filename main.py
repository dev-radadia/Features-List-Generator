# Import libraries
from flask import Flask, render_template, send_file, request
import pandas as pd
from io import BytesIO

# Import helper files
import py_files

# Create Flask app instance
app = Flask(__name__, template_folder = "templates")

# Connect to MongoDB Database
db = py_files.mongodb_code.get_database()

# Check if there was a failure connecting to MongoDB Server
if(isinstance(db, int)):
    # Keep trying to establish a successful connection with the MongoDB Server
    while(isinstance(db, int)):
        db = py_files.mongodb_code.get_database()

# Connect to a Collection in the MongoDB Database
try:
    mongodbCollection = db.dataframes
except:
    mongodbCollection = db["dataframes"]
    

@app.route('/')
# 'home' page function
def home():
    return render_template("home.html")

# @app.route('/getdata/<string:pjname>', methods=['POST']) 
# # Function to fetch 'projectName' variable value from JavaScript file
# def getdata(pjname):
#     global projectName
    
#     # Load the JSON string into a Python string variable
#     projectName = json.loads(pjname)

#     return('/')

@app.route('/generate')
# 'generate' page function
def generate():
    # Get the variable from query string
    projectName = request.args.get('value')

    # Check whether the required data exists in the MongoDB Database
    if py_files.mongodb_code.data_exists(collection = mongodbCollection, projectName = projectName):
        # Fetch the Pandas Dataframe from the MongoDB Database
        dataFrame = py_files.mongodb_code.fetch_data(collection = mongodbCollection, projectName = projectName)
    else:
        # Generate Pandas Dataframe for the given project
        dataFrame = py_files.genai_code.main(projectName = projectName)

        # Check if a valid Pandas Dataframe was generated or not
        if(isinstance(dataFrame, int)):
            return render_template("home.html")

        # Load the generated Pandas Dataframe into the MongoDB Database
        py_files.mongodb_code.load_data(collection = mongodbCollection, projectName = projectName, df = dataFrame)
    
    # Name the Excel file
    excelFilename = "features_list-" + projectName + ".xlsx"
    excelFilename = excelFilename.replace(" ", "_")

    return render_template("generate.html", data = {'pjname': projectName, 'table': dataFrame, 'filename': excelFilename})

@app.route("/download", methods=["GET"])
# Function to send Excel File object to JavaScript file
def download_excel():
    # Get the variable from query string
    projectName = request.args.get('value')

    # Fetch the Pandas Dataframe from the MongoDB Database
    dataFrame = py_files.mongodb_code.fetch_data(collection = mongodbCollection, projectName = projectName)

    # Create an in-memory buffer for the Excel Sheet
    output = BytesIO()

    # Write the DataFrame to Excel
    writer = pd.ExcelWriter(output)
    dataFrame.to_excel(writer, sheet_name = projectName, index = True)
    writer.close()
    output.seek(0)

    # Name the Excel file
    excelFilename = "features_list-" + projectName + ".xlsx"
    excelFilename = excelFilename.replace(" ", "_")

    # Create a Response object with the Excel file data
    response = send_file(output, download_name = excelFilename)

    return response

if __name__ == "__main__":
    # Run the app in debug mode if the script is run directly and specify the port number
    app.run(debug = True, port = 3000)
