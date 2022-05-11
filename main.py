from packages.serviceLevelManager import ServiceLevelManager

if __name__ == '__main__':
    path = "resources/request.xlsx"
    apiKey = "AIzaSyCDEBZ-YilN6CRFnPoiiVJaKk_6VXZNiBA"
    app = ServiceLevelManager(path, apiKey)
    app.execute()
