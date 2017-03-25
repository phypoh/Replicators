import psycopg2
import psycopg2.extras

import config
import toornament as tourney
from allTourney import Toorn

conn = ''
cur = ''
cli = ''
Tnew = ''

#Basic Startup Functions
def initializeStuff():

    # Connects to Postgres DB.
    # Makes client of toornament API.

    try:
        global conn, cur, cli, Tnew
        conn = psycopg2.connect("host= %s dbname= %s user= %s password= %s" % (config.host, config.db, config.user, config.pwd))
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cli = tourney.ToornamentClient(config.cID, config.cSec, config.toorKey)
        Tnew = Toorn(cli)
        print("Connected ...")
    except:
        print("Error!")

#Initializes Tourney Table with attributes.
# Db Schema
#  ------------------------------------------------------------------------------------------------------------
# | id | creator     | dserver     | toorid      | skillreq | createdat | finished | gamemode    | region      |
# | int| varchar(50) | varchar(50) | varchar(50) | int      | date      | bool     |varchar(50) | varchar(10)  |
#  ------------------------------------------------------------------------------------------------------------
def createMainTable():
    query = "CREATE TABLE %s (" \
            "id SERIAL, " \
            "creator VARCHAR(50) NOT NULL, " \
            "dserver VARCHAR(50) NOT NULL, " \
            "toorid VARCHAR(50) PRIMARY KEY NOT NULL, " \
            "skillreq INTEGER, " \
            "createdat DATE, " \
            "finished BOOLEAN DEFAULT FALSE, " \
            "gamemode VARCHAR(50) NOT NULL, " \
            "region VARCHAR(10) NOT NULL)"
    cur.execute(query % (config.table))
    conn.commit()

#Testing & Debugging
def fetchTableSchema():
    query = "SELECT * FROM %s"
    cur.execute(query % (config.table))
    colnames = [desc[0] for desc in cur.description]
    print (colnames)

def fetchAllRows():
    query = "SELECT * FROM %s"
    cur.execute(query % (config.table))
    rows = cur.fetchall()
    print (rows)

def printBlock():
    print("\n1. createTournament\t| 2. editTournament\t| 3. getTournamentByID\t| 4. deleteTournament\t| 5. getMyTournaments"
          "\n6. createParticipant\t| 7. getOneParticipant\t| 8. getAllParticipants\t| 9. deleteParticipant\n| 10.\t|"
          "99. Exit\t | 100. getAllRows\t|")


#[Main Code Execution begins here]
if __name__ == '__main__':

    initializeStuff()
    #createMainTable() #Creates a new database as I could not work with the one Spies created.
    #fetchTableSchema()
    fetchAllRows()

    inp = 100
    while inp>0:
        printBlock()
        inp = int(input("Choice: "))
        if inp == 1:
            Tnew.createT(cur, conn) #print ('createTournament')
        elif inp ==2:
            Tnew.editT(cur,conn) #print('editTournament')
        elif inp == 3:
            Tnew.getT(cur) #print('getTournamentByID')
        elif inp == 4:
            Tnew.deleteT(cur, conn) #print('deleteTournament')
        elif inp == 5:
            Tnew.getMyT() #print('getMyTournaments')


        elif inp == 6:
            Tnew.createP(cur) #print('createParticipant')
        elif inp == 7:
            Tnew.getOneP(cur)  # print('getOneParticipant')
        elif inp == 8:
            Tnew.getAllP(cur)  # print('getAllParticipants')
        elif inp == 9:
            Tnew.deleteP(cur)  # print('deleteParticipant')



        elif inp == 99: # Exit
            inp = -1
        elif inp == 100: #fetches all rows from POSTGRES
            fetchAllRows()
    print('End')