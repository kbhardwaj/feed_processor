import pickle

class StoreIOService():
    
    def __init__(self):
        pass

    def store(self, filename, data):
        try: 
            storageFile = open(filename, 'wb') 
            pickle.dump(data, storageFile) 
            storageFile.close() 
        except: 
            print("Something went wrong")

    def get(self, filename):
        return pickle.load( open(filename, "rb") )

    def append(self, filename, data):
        existingData = self.get(filename)

        for k, v in data.items():
            if not existingData.get(k):
                existingData[k] = v

        self.store(filename, existingData)

storeIOService = StoreIOService()