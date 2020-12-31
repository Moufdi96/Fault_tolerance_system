import json

def loadJsonFile(path):
    jsonText = ''    
    with open(path, "r") as stable_memory:
        jsonText = stable_memory.read()
        dataBase = json.loads(jsonText)
    return dataBase

def saveData(path,newDataVector,mean):
    dataBase = loadJsonFile(path)
    with open("/home/moufdi/GitHubProjects/Projet_mutlithreading/stableMemory.json", "w") as stable_memory:
        dataBase.append((newDataVector,mean))
        json.dump(dataBase,stable_memory)