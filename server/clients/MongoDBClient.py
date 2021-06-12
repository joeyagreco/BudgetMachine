import os
import uuid
from typing import List

from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

from server.models.Transaction import Transaction
from server.models.Year import Year
from server.util import YamlProcessor

load_dotenv()


class MongoDBClient:
    """
    This class is used to connect directly to the Mongo Database.
    """

    def __init__(self):
        self.__cluster = MongoClient(os.getenv("MONGO_CLUSTER_URL"))
        self.__database = self.__cluster[os.getenv("MONGO_DATABASE")]
        # check if we want TEST or PROD data
        self.__transactionCollection = self.__database[os.getenv("MONGO_COLLECTION_TRANSACTIONS_TEST")]
        self.__yearCollection = self.__database[os.getenv("MONGO_COLLECTION_YEARS_TEST")]
        if YamlProcessor.getVariable("PRODUCTION_DATA"):
            self.__transactionCollection = self.__database[os.getenv("MONGO_COLLECTION_TRANSACTIONS_PROD")]
            self.__yearCollection = self.__database[os.getenv("MONGO_COLLECTION_YEARS_PROD")]

    def __generateId(self) -> str:
        """
        Returns a new and unused random id
        """
        newId = uuid.uuid1()
        while self.__transactionCollection.find_one({"_id": newId}):
            newId = uuid.uuid1()
        return newId.hex

    def __mapToTransaction(self, data: dict) -> Transaction:
        """
        Maps the given data to a Transaction and returns it.
        """
        return Transaction(data["_id"], data["amount"], data["note"], data["category"],
                           data["isIncome"], data["date"].date())

    def getTransaction(self, transactionId: str, **params) -> Transaction:
        """
        Returns a dictionary object of the league or an Error object if not retrieved
        https://docs.mongodb.com/manual/reference/method/db.collection.findOne/
        PARAMS:
        NOMAP: bool: If True, will not map response to a Transaction object {Default: false}
        """
        noMap = params.get("noMap", False)
        response = self.__transactionCollection.find_one({"_id": transactionId})
        # response will be None if not found
        if response:
            return response if noMap else self.__mapToTransaction(response)
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
        response = self.__transactionCollection.insert_one(transaction)
        if response.acknowledged:
            return response.inserted_id
        else:
            # TODO return Error("Could not insert transaction into database.")
            return "error"

    def updateTransaction(self, updatedTransaction: Transaction):
        """
        Updates a transaction with given id
        Returns a Document object or an Error object if not updated
        https://docs.mongodb.com/manual/reference/method/db.collection.update/
        https://specify.io/how-tos/mongodb-update-documents
        """
        transaction = self.getTransaction(updatedTransaction.getTId(), noMap=True)
        if not transaction:
            return None
        else:
            transaction["amount"] = updatedTransaction.getAmount()
            transaction["category"] = updatedTransaction.getCategory()
            transaction["note"] = updatedTransaction.getNote()
            transaction["isIncome"] = updatedTransaction.getIsIncome()
            transaction["date"] = datetime.combine(updatedTransaction.getDate(), datetime.max.time())
            response = self.__transactionCollection.update({"_id": updatedTransaction.getTId()}, transaction)
            if response:
                return response
            else:
                # TODO return Error("Could not update transaction.")
                return None

    def deleteTransaction(self, transactionId: str) -> bool:
        """
        Deletes the transaction with the given ID
        Returns None if successfully deleted or an Error if not.
        https://docs.mongodb.com/manual/reference/method/db.collection.remove/
        """
        response = self.__transactionCollection.remove({"_id": transactionId})
        if response["n"] == 1:
            # successfully deleted 1 league
            return True
        else:
            # could not delete the league
            return False

    def getAllTransactions(self, **params) -> List[Transaction]:
        """
        Returns a list of all Transaction objects
        PARAMS:
        LIMIT: int: Limits the amount of entries returned {DEFAULT: 0}
        """
        limit = params.get("limit", 0)
        cursor = self.__transactionCollection.find({}).limit(limit)
        allTransactions = list()
        for document in cursor:
            allTransactions.append(self.__mapToTransaction(document))
        return allTransactions

    def addYear(self, year: Year):
        """
       Adds a Year with a new generated ID to the database
       Returns the new Year's ID or an Error object if not inserted
       https://docs.mongodb.com/manual/reference/method/db.collection.insertOne/
       """
        bankWrappers = dict()
        # unwrap all BankWrappers and put them into a dict
        for month in year.getBankWrappers().keys():
            # unwrap all Banks and put them into a list
            banks = list()
            for bank in year.getBankWrappers()[month].getBanks():
                bankDict = dict()
                bankDict["amount"] = bank.getAmount()
                bankDict["category"] = bank.getCategory()
                banks.append(bankDict)
            bankWrappers["banks"] = banks
            bankWrappers["month"] = month
        # construct default Year object
        year = {"_id": self.__generateId(), "year": year.getYear(), "bankWrappers": bankWrappers}
        response = self.__yearCollection.insert_one(year)
        if response.acknowledged:
            return response.inserted_id
        else:
            # TODO return Error("Could not insert Year into database.")
            return "error"
