from server.clients.DatabaseClient import DatabaseClient

if __name__ == "__main__":
    dbClient = DatabaseClient()
    result = dbClient.addTransaction(None, 4.20, "test transaction", 3)
    print(result)