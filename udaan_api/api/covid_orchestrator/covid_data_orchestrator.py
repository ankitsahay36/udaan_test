from api.data_access.mongo_access import MongoConnection
user_collection = "user"
risk_audit_collection = "risk_audit"
admin_collection = "admin"
covid_data_coll = "covid_data"


class CovidController:
    mongo_connector = MongoConnection()
    client = mongo_connector.client()

    # def __init__(self):
    #     pass
    def register_user(self, data):
        collection_cl = CovidController.mongo_connector.get_collection_client(user_collection)
        try:
            users = CovidController.mongo_connector.get(user_collection)
            _id = len(users)+1
            data["_id"] = _id
            data["userId"] = _id
            collection_cl.insert_one(data)
            return {"userId": _id}
        except:
            raise Exception("db connection failed")
# """
# {"userId": "1", "symptoms": ["fever", "cold", "cough"], "travelHistory": true, "contactWithCovidPatient": true}
# No symptoms, No travel history, No contact with covid positive patient - Risk = 5%
# Any one symptom, travel history or contact with covid positive patient is true - Risk = 50%
# Any two symptoms, travel history or contact with covid positive patient is true - Risk = 75%
# Greater than 2 symptoms, travel history or contact with covid positive patient is true - Risk = 95%
# """
    def risk_check(self, data):
        collection_cl = CovidController.mongo_connector.get_collection_client(risk_audit_collection)
        try:
            n_symptoms = len(data['symptoms'])
            t_history = data['travelHistory']
            contact_p = data['contactWithCovidPatient']
            # if
            collection_cl.insert(data)

            if n_symptoms == 0 and not t_history and not contact_p:
                risk_percentage = 5
            elif n_symptoms == 1 and not t_history and not contact_p:
                risk_percentage = 10
            elif n_symptoms == 1 and (t_history or contact_p):
                risk_percentage = 50
            elif n_symptoms == 2 and (t_history or contact_p):
                risk_percentage = 75
            elif n_symptoms > 2 and (t_history or contact_p):
                risk_percentage = 95


            print(data)
            return {"riskPercentage": risk_percentage}
        except Exception as e:
            raise Exception("db connection failed")

    def register_admin(self, data):
        collection_cl = CovidController.mongo_connector.get_collection_client(admin_collection)
        try:
            users = CovidController.mongo_connector.get(admin_collection)
            _id = len(users) + 1
            data["_id"] = _id
            data["adminId"] = _id
            collection_cl.insert_one(data)
            return {"adminId": _id}
        except:
            raise Exception("db connection failed")

    def admin_report(self, data):
        # collection_cl = CovidController.mongo_connector.get_collection_client(user_collection)
        collection_cl_audit = CovidController.mongo_connector.get_collection_client(risk_audit_collection)

        try:
            user_data = CovidController.mongo_connector.get(user_collection, {"userId": data["userId"]})
            if len(user_data) == 0:
                raise Exception("No User Found with given user id")
            audit_data = CovidController.mongo_connector.get(risk_audit_collection, {"userId": data["userId"]})
            if len(user_data) == 0:
                raise Exception("No User Found with given user id in covid data")
            audit_data = audit_data[0]
            audit_data['adminId'] = data["adminId"]
            audit_data["result"] = data["result"]

            collection_cl_audit.update_one(data, {"userId": data["userId"]})
            return {"updated": True}
        except Exception as e:
            raise Exception(str(e))





