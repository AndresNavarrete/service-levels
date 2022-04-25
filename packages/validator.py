from packages.enums import User_Modes


class Validator:

    def __init__(self, input):
        self.input = input
        self.all_ids = []
        self.avialable_modes = [
            User_Modes.car,
            User_Modes.transit,
            User_Modes.bus,
            User_Modes.walk
        ]

    def validate_input(self):
        for request in self.input.requests:
            self.validate_mode(request)
            self.validate_id(request)
            self.validate_origin(request)
            self.validate_destination(request)

    def validate_mode(self, request):
        if request["Modo"] in self.avialable_modes:
            return
        msg = "Invalid mode. id {} mode {}".format(request["ID"], request["Modo"])
        raise ValueError(msg)
    
    def validate_id(self, request):
        if request["ID"] in self.all_ids:
            msg = "Duplicated ID. id {}".format(request["ID"])
            raise ValueError(msg)
        self.all_ids.append(request["ID"])
    
    def validate_origin(self, request):
        if request["Origen_str"] != None:
            return
        if request["Origen_Lat"] == None or request["Origen_Lng"] == None:
            msg = "Invalid origin. id {}".format(request["ID"])
            raise ValueError(msg)
    
    def validate_destination(self, request):
        if request["Destino_str"] != None:
            return
        if request["Destino_Lat"] == None or request["Destino_Lng"] == None:
            msg = "Invalid destination. id {}".format(request["ID"])
            raise ValueError(msg)
        
