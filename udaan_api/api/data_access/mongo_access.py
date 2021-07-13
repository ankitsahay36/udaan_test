from pymongo import MongoClient


class MongoConnection:
    def __init__(self):
        self.host = "localhost"
        self.port = "27017"
        self.db = "udaan_test"
        self.mongo_string = "mongodb://" + self.host + ":" +self.port + "/" +self.db

    def client(self):
        self._client = MongoClient(self.mongo_string)
        return self._client

    def get(self, collection_name, query={}):
        cl = self._client[self.db][collection_name]
        data = cl.find(query)
        final_data = []
        for d in data:
            del d["_id"]
            final_data.append(d)

        return final_data

    def get_collection_client(self, collection_name):
        return self._client[self.db][collection_name]



if __name__ == "__main__":
    cli = MongoConnection()
    client_ob = cli.client()
    coll_client = cli.get_collection_client("user")
    coll_client.insert_one({"user_id": 1})
    print(cli.get("user"))
