import os
import uuid
from typing import List, Dict

from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

from server.models.Bank import Bank
from server.models.Month import Month
from server.models.Transaction import Transaction
from server.models.Year import Year
from server.util import YamlProcessor
from server.util.Logger import Logger

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
            # log all data
            Logger.log("YEARS", self.__yearCollection.find({}))
            Logger.log("TRANSACTIONS", self.__transactionCollection.find({}))


    def __generateId(self) -> str:
        """
        Returns a new and unused random id
        """
        newId = uuid.uuid1()
        while self.__transactionCollection.find_one({"_id": newId}):
            newId = uuid.uuid1()
        return newId.hex

    @staticmethod
    def __mapToTransaction(data: dict) -> Transaction:
        """
        Maps the given data to a Transaction and returns it.
        """
        return Transaction(data["_id"], data["amount"], data["note"], data["category"],
                           data["isIncome"], data["date"].date())

    @staticmethod
    def __mapFromTransactionToDict(transaction: Transaction) -> Dict:
        """
        Maps the given Transaction object to a dictionary and returns it.
        """
        return {"_id": transaction.getTId(), "amount": transaction.getAmount(),
                "note": transaction.getNote(), "category": transaction.getCategory(),
                "isIncome": transaction.getIsIncome(), "date": datetime.combine(transaction.getDate(), datetime.max.time())}

    @staticmethod
    def __mapFromYearToDict(year: Year) -> Dict:
        """
        Maps the given Year object to a dictionary and returns it.
        """
        months = dict()
        for monthNum in year.getMonths().keys():
            month = year.getMonths()[monthNum]
            banks = list()
            for bank in month.getBanks():
                bankDict = {"amount": bank.getAmount(), "category": bank.getCategory()}
                banks.append(bankDict)
            monthDict = {"month": month.getMonth(), "banks": banks}
            months[str(monthNum)] = monthDict
        return {"_id": year.getYId(), "year": year.getYear(), "months": months}

    @staticmethod
    def __mapToYear(data: dict) -> Year:
        """
        Maps the given data to a Year and returns it.
        """
        months = dict()
        for monthNum in data["months"].keys():
            month = data["months"][monthNum]
            banks = month["banks"]
            bankList = list()
            for bank in banks:
                bankList.append(Bank(bank["amount"], bank["category"]))
            monthObj = Month(month["month"], bankList)
            months[monthNum] = monthObj

        return Year(data["_id"], data["year"], months)

    def getTransaction(self, transactionId: str, **params) -> Transaction:
        """
        Returns a dictionary object of the transaction or an Error object if not retrieved
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
        response = self.__transactionCollection.update({"_id": updatedTransaction.getTId()}, self.__mapFromTransactionToDict(updatedTransaction))
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
        # deconstruct default Year object
        year = self.__mapFromYearToDict(year)
        year["_id"] = self.__generateId()
        response = self.__yearCollection.insert_one(year)
        if response.acknowledged:
            return response.inserted_id
        else:
            # TODO return Error("Could not insert Year into database.")
            return "error"

    def getAllYears(self, **params) -> List[Year]:
        """
        Returns a list of all Year objects
        PARAMS:
        LIMIT: int: Limits the amount of entries returned {DEFAULT: 0}
        """
        limit = params.get("limit", 0)
        cursor = self.__yearCollection.find({}).limit(limit)
        allYears = list()
        for document in cursor:
            allYears.append(self.__mapToYear(document))
        return allYears

    def getYear(self, yearId: str, **params) -> Year:
        """
        Returns a dictionary object of the year or an Error object if not retrieved
        https://docs.mongodb.com/manual/reference/method/db.collection.findOne/
        PARAMS:
        NOMAP: bool: If True, will not map response to a Year object {Default: false}
        """
        noMap = params.get("noMap", False)
        response = self.__yearCollection.find_one({"_id": yearId})
        # response will be None if not found
        if response:
            return response if noMap else self.__mapToYear(response)
        else:
            # TODO return Error(f"Could not find a year with ID: {yearId}")
            return None

    def updateYear(self, updatedYear: Year):
        """
        Updates a year with given id
        Returns a Document object or an Error object if not updated
        https://docs.mongodb.com/manual/reference/method/db.collection.update/
        https://specify.io/how-tos/mongodb-update-documents
        """
        response = self.__yearCollection.update({"_id": updatedYear.getYId()}, self.__mapFromYearToDict(updatedYear))
        if response:
            return response
        else:
            # TODO return Error("Could not update year.")
            return None
