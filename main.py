from packages.serviceLevelManager import ServiceLevelManager

if __name__ == '__main__':
    path = "resources/request.xlsx"
    apiKey = ""
    app = ServiceLevelManager(path, apiKey)
    app.execute()
