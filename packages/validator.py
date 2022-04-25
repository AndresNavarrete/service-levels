from packages.enums import User_Modes


class Validator:

    def __init__(self, input):
        self.input = input
        self.ids = []
        self.modes = [
            User_Modes.car,
            User_Modes.transit,
            User_Modes.bus,
            User_Modes.walk
        ]

    def validateInput(self):
        for request in self.input.requests:
            self.validateMode(request)
            self.validateId(request)
            self.validateOrigin(request)
            self.validateDestination(request)

    def validateMode(self, request):
        if request["Modo"] in self.modes:
            return
        msg = "Invalid mode. id {} mode {}".format(request["ID"], request["Modo"])
        raise ValueError(msg)
    
    def validateId(self, request):
        if request["ID"] in self.ids:
            msg = "Duplicated ID. id {}".format(request["ID"])
            raise ValueError(msg)
        self.ids.append(request["ID"])
    
    def validateOrigin(self, request):
        if request["Origen_str"] != None:
            return
        if request["Origen_Lat"] == None or request["Origen_Lng"] == None:
            msg = "Invalid origin. id {}".format(request["ID"])
            raise ValueError(msg)
    
    def validateDestination(self, request):
        if request["Destino_str"] != None:
            return
        if request["Destino_Lat"] == None or request["Destino_Lng"] == None:
            msg = "Invalid destination. id {}".format(request["ID"])
            raise ValueError(msg)
        
