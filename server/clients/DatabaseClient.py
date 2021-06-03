import os
import random
import uuid

from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

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
        Will be between 100000-999999 [always 6 digits]
        """
        newId = uuid.uuid1()
        while self.__collection.find_one({"_id": newId}):
            newId = uuid.uuid1()
        return newId.hex

    def getTransaction(self, transactionId: int):
        """
        Returns a dictionary object of the league or an Error object if not retrieved
        https://docs.mongodb.com/manual/reference/method/db.collection.findOne/
        """
        response = self.__collection.find_one({"_id": transactionId})
        # response will be None if not found
        if response:
            return response
        else:
            return Error(f"Could not find a transaction with ID: {transactionId}")

    def addTransaction(self, date: object, amount: float, note: str, category: str) -> str:
        """
        Adds a transaction with a new generated ID to the database
        Returns the new transaction's ID or an Error object if not inserted
        https://docs.mongodb.com/manual/reference/method/db.collection.insertOne/
        """
        # if date is null, set current time as date
        if not date:
            date = datetime.now()
        # construct default transaction object
        transaction = {"_id": self.__generateId(), "date": date, "amount": amount, "note": note, "category": category}
        response = self.__collection.insert_one(transaction)
        if response.acknowledged:
            return response.inserted_id
        else:
            # return Error("Could not insert transaction into database.")
            return "error"

    # def updateLeague(self, leagueId: int, leagueName: str, years):
    #     """
    #     Updates a league with given parameters
    #     Returns a Document object or an Error object if not updated
    #     https://docs.mongodb.com/manual/reference/method/db.collection.update/
    #     https://specify.io/how-tos/mongodb-update-documents
    #     """
    #     league = self.getLeague(leagueId)
    #     if isinstance(league, Error):
    #         return league
    #     else:
    #         league["leagueName"] = leagueName
    #         league["years"] = years
    #         response = self.__collection.update({"_id": leagueId}, league)
    #         if response:
    #             return response
    #         else:
    #             return Error("Could not update league.")
    #
    # def deleteLeague(self, leagueId: int):
    #     """
    #     Deletes the league with the given ID
    #     Returns None if successfully deleted or an Error if not.
    #     https://docs.mongodb.com/manual/reference/method/db.collection.remove/
    #     """
    #     response = self.__collection.remove({"_id": leagueId})
    #     if response["n"] == 1:
    #         # successfully deleted 1 league
    #         return None
    #     else:
    #         # could not delete the league
    #         return Error("Could not delete league.")
    #
    # def deleteWeek(self, leagueId: int, year: int):
    #     """
    #     Deletes the most recent week of the year in the league with the given ID
    #     Returns league if successfully deleted or an Error if not.
    #     https://docs.mongodb.com/manual/reference/method/db.collection.update/
    #     https://specify.io/how-tos/mongodb-update-documents
    #     """
    #     league = self.getLeague(leagueId)
    #     if isinstance(league, Error):
    #         return league
    #     else:
    #         league["years"][str(year)]["weeks"] = league["years"][str(year)]["weeks"][:-1]
    #         response = self.__collection.update({"_id": leagueId}, league)
    #         if response:
    #             league = self.getLeague(leagueId)
    #             return league
    #         else:
    #             return Error("Could not delete week.")