import sqlite3
from pathlib import Path

dbPath = '/home/pi/Desktop/PatokaProject/resources/month.db'

def mainLoop():
    con = sqlite3.connect(dbPath)
    cur = con.cursor()

    try:
        cur.execute('CREATE TABLE monthly(day INTEGER PRIMARY KEY, curtemp, hitemp, lotemp, totalrain24)')
    except:
        pass

    cur.execute("SELECT MAX(tempouthi), MIN(tempoutlo) from daily LIMIT 1")
    data = cur.fetchall()
    cur.execute(f'SELECT tempout FROM daily WHERE time >=(SELECT MAX(time) FROM daily) LIMIT 1')
    data2 = cur.fetchall()

    cur.execute("SELECT ROUND(SUM(rainfallin), 2) FROM daily")
    totalRain = cur.fetchall()

    cur.execute("INSERT INTO monthly(curtemp, hitemp, lotemp, totalrain24) VALUES (?, ?, ?, ?)", (data2[0][0], data[0][0], data[0][1], totalRain[0][0]))
    cur.execute('DELETE FROM daily')

    con.commit()
    con.close()
if __name__ == '__main__':
    mainLoop()