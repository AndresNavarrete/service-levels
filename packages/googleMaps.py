from googlemaps import Client
from packages.enums import Google_Modes
import json

### Docs https://github.com/googlemaps/google-maps-services-python
class GoogleMaps:

   def __init__(self, apiKey):
      self.gmaps = Client(key=apiKey)

class Geocoder(GoogleMaps):
   
   def getCoordinates(self, location):
      response = self.getGeocodeResponse(location)
      formattedAddress = response[0]["formatted_address"]
      lat = response[0]["geometry"]["location"]["lat"]
      lng = response[0]["geometry"]["location"]["lng"]
      coordResponse = {
         "location_input": location,
         "lat": lat,
         "lng": lng,
         "formatted_address": formattedAddress
         }
      return coordResponse

   def getGeocodeResponse(self, location):
      geocodeResult = self.gmaps.geocode(location)
      return geocodeResult

class Directions(GoogleMaps):
   # https://developers.google.com/maps/documentation/directions/get-directions

   # TODO: Add transit with only bus.

   def getDirections(self, origin, destination, mode, departure_time, only_bus):
      directionsResponse = self.getDirectionsResponse(origin, destination, mode, departure_time, only_bus)
      if not directionsResponse:
         return self.getDefaultResponse() 
      trip = directionsResponse[0]["legs"][0]
      steps = self.getStepsInformation(trip, mode)
      wait_time, walk_time, travel_time = self.getDesagregatedTime(trip, steps, mode)

      response = {
         "distance": trip["distance"]["value"],
         "duration": trip["duration"]["value"],
         "end_address": trip["end_address"],
         "end_location_lat": trip["end_location"]["lat"],
         "end_location_lng": trip["end_location"]["lng"],
         "start_address": trip["start_address"],
         "start_location_lat": trip["start_location"]["lat"],
         "start_location_lng": trip["start_location"]["lng"],
         "wait_time": wait_time,
         "walk_time": walk_time,
         "travel_time": travel_time,
         "transfers": self.getTransferNumber(steps),
         "steps": steps
      }
      return response

   def getDirectionsResponse(self, origin, destination, mode, departure_time, only_bus = False):
      if only_bus:
         transit_mode = Google_Modes.bus
      else:
         transit_mode = None
      directionsResponse = self.gmaps.directions(
         origin,
         destination,
         mode = mode,
         transit_mode = transit_mode,
         departure_time = departure_time)
      self.saveRawResponse(directionsResponse)
      return directionsResponse
   
   def saveRawResponse(self, response):
      with open('resources/raw/directions.json', 'w') as outfile:
         json.dump(response, outfile)

   def getDefaultResponse(self):
      return {
         "distance": None,
         "duration": None,
         "end_address": None,
         "end_location_lat": None,
         "end_location_lng": None,
         "start_address": None,
         "start_location_lat": None,
         "start_location_lng": None,
         "wait_time": None,
         "walk_time": None,
         "travel_time": None,
         "transfers": None,
         "steps": []
      }


   def getStepsInformation(self, trip, mode):
      steps = list()
      if mode != "transit":
         return steps
      for step in trip["steps"]:
         stepInfo = self.getNewStep(step)
         steps.append(stepInfo)
      return steps
   
   def getNewStep(self, step):
      stepInfo = {
         "distance": step["distance"]["value"],
         "duration": step["duration"]["value"],
         "travel_mode": step["travel_mode"],
         "instruction": step["html_instructions"],
         "headway": 0,
      }
      if step["travel_mode"] == "TRANSIT":
         stepInfo["headway"] = step["transit_details"]["headway"]
         
      return stepInfo
   
   def getDesagregatedTime(self, trip, steps, mode):
      wait_time = 0
      walk_time = 0
      travel_time = 0
      if mode in ("driving", "walking"):
         travel_time = trip["duration"]["value"]
      if mode == "transit":
         walk_time = sum([step["duration"] for step in steps if step["travel_mode"] == "WALKING"])
         travel_time = sum([step["duration"] for step in steps if step["travel_mode"] in ("TRANSIT", "DRIVING")])
         wait_time = max(trip["duration"]["value"] - walk_time - travel_time, 0)
      return wait_time, walk_time, travel_time
   
   def getTransferNumber(self, steps):
      transfers = 0
      for step in steps:
         if step["travel_mode"] == "TRANSIT":
            transfers += 1
      return max(0, transfers - 1)



