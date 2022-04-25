import pandas

class OutputParser:

    def __init__(self, outputPath):
        self.outputPath = outputPath
        self.steps = []
        self.trips = []
    
    def addTrip(self, request, response):
        newTrip = {
            "id": request["ID"],
            "modo": request["Modo"],
            "hora": request["Hora"],
            "origen_direccion": response["start_address"],
            "origen_lat": response["start_location_lat"],
            "origen_lng": response["start_location_lng"],
            "destino_direccion": response["end_address"],
            "destino_lat": response["end_location_lat"],
            "destino_lng": response["end_location_lng"],
            "transbordos": response["transfers"],
            "distancia_m": response["distance"],
            "tiempo_total_seg": response["duration"],
            "tiempo_espera_seg": response["wait_time"],
            "tiempo_caminata_seg": response["walk_time"],
            "tiempo_viaje_seg": response["travel_time"],
        }
        self.trips.append(newTrip)
        for step in response["steps"]:
            self.addStep(step, request["ID"])
    
    def addStep(self, step, tripId):
        newStep = {
            "viaje_id": tripId,
            "modo": step["travel_mode"],
            "distancia_m": step["distance"],
            "tiempo_total_seg": step["duration"],
            "tiempo_espera_seg": step["headway"],
            "indicacion": step["instruction"]
        }
        self.steps.append(newStep)
    
    def writeExcel(self):
        trips = pandas.DataFrame(self.trips)
        steps = pandas.DataFrame(self.steps)
        with pandas.ExcelWriter(self.outputPath) as writer:  
            trips.to_excel(writer, sheet_name='Viajes')
            steps.to_excel(writer, sheet_name='Etapas')

