import os
import random
import uuid

from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

from server.models.Transaction import Transaction

load_dotenv()


class DatabaseClient:
    """
    This class is used to connect directly to the Mongo Database.
    """

    def __init__(self):
        self.__cluster = MongoClient(os.getenv("MONGO_CLUSTER_URL"))
        self.__database = self.__cluster[os.getenv("MONGO_DATABASE")]
        self.__collection = self.__database[os.getenv("MONGO_COLLECTION")]

    def __generateId(self) -> str:
        """
        Returns a new and unused random id
        """
        newId = uuid.uuid1()
        while self.__collection.find_one({"_id": newId}):
            newId = uuid.uuid1()
        return newId.hex

    def getTransaction(self, transactionId: str) -> Transaction:
        """
        Returns a dictionary object of the league or an Error object if not retrieved
        https://docs.mongodb.com/manual/reference/method/db.collection.findOne/
        """
        response = self.__collection.find_one({"_id": transactionId})
        # response will be None if not found
        if response:
            return Transaction(response["_id"], response["amount"], response["note"], response["category"],
                               response["isIncome"], response["date"].date())
        else:
            # TODO return Error(f"Could not find a transaction with ID: {transactionId}")
            return None

    def addTransaction(self, amount: float, note: str, category: str, isIncome: bool, date: datetime.date) -> str:
        """
        Adds a transaction with a new generated ID to the database
        Returns the new transaction's ID or an Error object if not inserted
        https://docs.mongodb.com/manual/reference/method/db.collection.insertOne/
        """
        # if date is null, set current time as date
        # NOTE: PyMongo does not support just dates, so we must convert to a datetime (we use max time)
        # source: https://stackoverflow.com/questions/30553406/python-bson-errors-invaliddocument-cannot-encode-object-datetime-date2015-3
        if not date:
            date = datetime.combine(datetime.now(), datetime.max.time())
        else:
            date = datetime.combine(date, datetime.max.time())
        # construct default transaction object
        transaction = {"_id": self.__generateId(), "amount": amount, "note": note, "category": category,
                       "isIncome": isIncome, "date": date}
        response = self.__collection.insert_one(transaction)
        if response.acknowledged:
            return response.inserted_id
        else:
            # TODO return Error("Could not insert transaction into database.")
            return "error"

    def updateTransaction(self, transactionId: str, newNote: str):
        """
        Updates a transaction with given id
        Returns a Document object or an Error object if not updated
        https://docs.mongodb.com/manual/reference/method/db.collection.update/
        https://specify.io/how-tos/mongodb-update-documents
        """
        transaction = self.getTransaction(transactionId)
        if not transaction:
            return None
        else:
            transaction["note"] = newNote
            response = self.__collection.update({"_id": transactionId}, transaction)
            if response:
                return response
            else:
                # TODO return Error("Could not update league.")
                return None

    def deleteTransaction(self, transactionId: str) -> bool:
        """
        Deletes the transaction with the given ID
        Returns None if successfully deleted or an Error if not.
        https://docs.mongodb.com/manual/reference/method/db.collection.remove/
        """
        response = self.__collection.remove({"_id": transactionId})
        if response["n"] == 1:
            # successfully deleted 1 league
            return True
        else:
            # could not delete the league
            return False
