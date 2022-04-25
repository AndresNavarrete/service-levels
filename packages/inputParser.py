import pandas
import json


class InputParser:

    def __init__(self, inputPath):
        self.inputPath = inputPath
        self.inputData = None
        self.loadInput()
    
    def loadInput(self):
        df = pandas.read_excel(self.inputPath)
        input = df.to_json(orient='records')
        self.requests = json.loads(input)
