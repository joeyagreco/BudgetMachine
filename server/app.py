import datetime

from server.clients.DatabaseClient import DatabaseClient
from server.enums.Category import Category

if __name__ == "__main__":
    dbClient = DatabaseClient()
    # result = dbClient.addTransaction(datetime.date(1997, 3, 9), 4.20, "test transaction", Category.BILL)
    # result = dbClient.addTransaction(None, 4.20, "test transaction", Category.BILL)
    # result = dbClient.updateTransaction("2d885c91c40d11eba5dd00d861588225", "updatedNoteHere")
    # result = dbClient.getTransaction("2d885c91c40d11eba5dd00d861588225")
    result = dbClient.deleteTransaction("2d885c91c40d11eba5dd00d861588225")
    print(result)