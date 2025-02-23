import sqlite3
import json
from resources import constants

dbPath = constants.dbPath

def fileToSql(filePath: str, sensorGroup: str):
    #Sensor group is to determine between USGS and WeatherLink
    #Possible sensorGroup values are the keys from sqlValues.json
    #Loads the file using json
    with open(filePath, 'r') as file:
            values = json.load(file)

    #Turns the json into a comma seperated list(No brackets) to insert into the SQL

    sql = ''

    for value in values[sensorGroup]:
        if value == None:
            value = 'null'
        sql += f'{value}, '

    #Removes the ending comma and space. Returns the final output
    sql = sql[:-2]
    return sql

def listToSql(list: list):
    sql = ''

    for value in list:
        if value == None:
            value = 'null'
        sql += f'{value}, '

    #Removes the ending comma and space. Returns the final output
    sql = sql[:-2]
    return sql


def checkTableExists(tableName: str, dbPath: str = dbPath) -> bool:

    #Checks if a table exists in the SQLite3 database.

    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name=?;
    """, (tableName, ))

    exists = cursor.fetchone() is not None
    conn.close()
    
    return exists

def createUSGS(dbPath: str = dbPath):

    #Creates an SQLite3 for the usgs table if it does not exist.
    
    if not checkTableExists("usgs"):
        conn = sqlite3.connect(dbPath)

        cursor = conn.cursor()
        cursor.execute("CREATE TABLE usgs ( ? )")

        conn.commit()
        conn.close()

def createWeatherLink(dbPath: str = dbPath):

    #Check to see if the weatherlink table exists. If it does'nt, it makes a cursor and opens the values file

    if not checkTableExists("weatherlink"):
        conn = sqlite3.connect(dbPath)

        cursor = conn.cursor()

        sql = fileToSql("resources/sqlValues.json", 'weatherlink')

        #Creates the weatherlink table and commits it to the database. Closes the database at the end

        cursor.execute('CREATE TABLE weatherlink ( ? )'.replace("?", sql))

        conn.commit()
        conn.close()

def insertData(data: list, table: str, dbPath:str = dbPath):

    #Connects to the database and creates a cursor
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    if checkTableExists(table):
        
        #Turns the json and list data into SQL useable data
        valuesSql = fileToSql("resources/sqlValues.json", table)
        dataSql = listToSql(data)

        #Prepares the sql statement and adds in the values and data
        sql = f"INSERT INTO {table} (#) VALUES (?)"
        sql = sql.replace('#', valuesSql)
        sql = sql.replace("?", dataSql)

        #Executes the sql statement and commits it to the database
        cursor.execute(sql)

        conn.commit()
        conn.close()
    elif not checkTableExists("weatherlink"):
        createWeatherLink()
        insertData(data, table)
    elif not checkTableExists('usgs'):
        createUSGS()
        insertData(data, table)
    
def getValues(startUnix: int, endUnix: int, table: str, values: list, dbPath:str = dbPath):
    #Connects to the database and creates a cursor
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()

    if checkTableExists(table):

        #Converts the values to useable sql code
        sqlValues = listToSql(values)

        #Formats the sql, executes it, and returns it to where the function was called
        sql = f"SELECT {sqlValues} from {table} WHERE CAST(ts as INT) <= {startUnix} AND CAST(ts as INT) >= {endUnix}"
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()

        return data
    elif not checkTableExists(table):
        return 'done'


if __name__ == "__main__":
    createWeatherLink(dbPath)