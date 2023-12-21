# Import libraries
import google.generativeai as palm
import pandas as pd
from collections import defaultdict

# Configure API
palm.configure(api_key = 'AIzaSyA3L1x80yxEpJ4_b9Mlw0O1YqeSNEr314c')

# Initialize global variables
featuresList = None
temperature = 0
candidateCount = 1

# FUNCTIONS
# Function to initialize the model using PaLM API
def control_model(temperature, candidateCount):
  controlPrompt = '''I'm using you as a modules generator tool in my application.
                    Therefore, your soul task is to generate a list of modules and submodules for an application.
                    You need to give the output in a fixed format provided, i.e. all the outputs you generate will be having the same format.
                    Use a clear and concise table format with name of a module followed by its corresponding submodules separated with commas in each line.
                    Your response should not contain any extra information.'''

  try:
    response = palm.chat(prompt = controlPrompt, temperature = temperature, candidate_count = candidateCount).last
  except:
    control_model(temperature = temperature, candidateCount = candidateCount)

# Function to generate text using PaLM API
def generate_features_list(projectName, temperature, candidateCount):
  prompt = "Generate a long features list for the following project: " + projectName + ". Use a clear and concise table format with name of a module followed by its corresponding submodules separated with commas in each line. Your response should not contain any extra information."
  try:
    response = palm.generate_text(prompt = prompt, temperature = temperature, candidate_count = candidateCount).result
    return response
  except:
    return generate_features_list(projectName = projectName, temperature = temperature, candidateCount = candidateCount)

# Function for DFS traversal of graph
def dfs_traversal(node, featuresGraph, visited, featuresEncoding, modules, lst):
  visited[node] = True

  leafNode = True
  for neighbour in featuresGraph[node]:
    if not visited[neighbour]:
      leafNode = False
      dfs_traversal(node = neighbour, featuresGraph = featuresGraph, visited = visited, featuresEncoding = featuresEncoding, modules = modules, lst = lst + [featuresEncoding[neighbour]])

  if leafNode:
    modules.append(lst)

# Function to create Pandas DataFrame
def create_dataframe(features):
  # Split the features list linewise
  features = features.splitlines()
  try:
    # Remove the extra information from the features list
    features = features[2:]
  except:
    return -1

  # Create a graph by splitting features list into modules and submodules
  featuresGraph = defaultdict(list)
  featuresEncoding = {}
  idx = 1
  for feature in features:
    feature = feature.split("|")
    try:
      moduleName, submoduleNames = feature[1], feature[2]
    except:
      return -1
    
    moduleName = moduleName.strip(" *")
    if moduleName not in featuresEncoding.values():
      featuresEncoding[idx] = moduleName
      featuresGraph[0].append(idx)
      idx = idx + 1

    keyList = list(featuresEncoding.keys())
    valList = list(featuresEncoding.values())
    moduleNo = keyList[valList.index(moduleName)]

    submoduleNames = submoduleNames.split(",")
    for submoduleName in submoduleNames:
      submoduleName = submoduleName.strip(" *")
      if submoduleName != moduleName:
        featuresEncoding[idx] = submoduleName
        featuresGraph[moduleNo].append(idx)
        idx = idx + 1

  # DFS trarversal of graph
  visited = [False] * idx
  visited[0] = True
  modules = []
  rowIdx = 1
  for neighbour in featuresGraph[0]:
    dfs_traversal(node = neighbour, featuresGraph = featuresGraph, visited = visited, featuresEncoding = featuresEncoding, modules = modules, lst = [rowIdx] + [featuresEncoding[neighbour]])
    rowIdx = rowIdx + 1

  # Regularize the columns
  totalColumns = len(max(modules, key = len))
  for lst in modules:
    residualEntries = totalColumns - len(lst)
    lst.extend([''] * residualEntries)

  # Name the columns
  columns = ["SR.NO.", "MODULE NAME", "FEATURES"]
  for i in range(1, totalColumns-2):
    columnName = "SUBFEATURES - " + str(i)
    columns.append(columnName)

  # Create Pandas DataFrame
  df = pd.DataFrame(modules, columns = columns)

  # Set the index of the Pandas Dataframe
  df = df.set_index(columns)

  return df

# Main function
def main(projectName):
  global featuresList, temperature, candidateCount

  # control_model(temperature = temperature, candidateCount = candidateCount)

  featuresList = generate_features_list(projectName = projectName, temperature = temperature, candidateCount = candidateCount)

  dataFrame = create_dataframe(features = featuresList)
  
  return dataFrame