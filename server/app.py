from server.clients.DatabaseClient import DatabaseClient
from server.enums.Category import Category

if __name__ == "__main__":
    dbClient = DatabaseClient()
    result = dbClient.addTransaction(None, 4.20, "test transaction", Category.BILL)
    print(result)