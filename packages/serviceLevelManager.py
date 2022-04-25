from packages.enums import User_Modes, Google_Modes
from packages.googleMaps import Directions
from packages.inputParser import InputParser
from packages.outputParser import OutputParser
import dateparser

class ServiceLevelManager:

    def __init__(self, inputPath, apiKey):
        self.inputPath = inputPath
        self.input = InputParser(inputPath)
        outputPath = inputPath[:-5] + "_Completed.xlsx"
        self.output = OutputParser(outputPath)
        self.directions = Directions(apiKey)
        self.responses = []
    
    def execute(self):
        self.getAllServiceLevels()
        self.fillOutput()
        self.writeOutput()

    def getAllServiceLevels(self):
        for request in self.input.requests:
            origin = self.getOrigin(request)
            destination = self.getDestination(request)
            mode = self.getMode(request)
            hour = request["Hora"]
            departure = "Next Monday at {}".format(hour)
            date = dateparser.parse(departure)
            only_bus = request["Modo"] == User_Modes.bus

            response = self.directions.getDirections(origin, destination, mode, date, only_bus)
            self.responses.append(response)

    def getOrigin(self, request):
        if request["Origen_str"] == None:
            return (request["Origen_Lat"], request["Origen_Lng"])
        return request["Origen_str"]
    
    def getDestination(self, request):
        if request["Destino_str"] == None:
            return (request["Destino_Lat"], request["Destino_Lng"])
        return request["Destino_str"]
    
    def getMode(self, request):
        if request["Modo"] == User_Modes.car:
            mode = Google_Modes.car
        if request["Modo"] == User_Modes.transit or request["Modo"] == User_Modes.bus:
            mode = Google_Modes.transit
        if request["Modo"] == User_Modes.walk:
            mode = Google_Modes.walk
        
        return mode
    
    def fillOutput(self):
        for request, response in zip(self.input.requests, self.responses):
            self.output.addTrip(request, response)

    def writeOutput(self):
        self.output.writeExcel()
