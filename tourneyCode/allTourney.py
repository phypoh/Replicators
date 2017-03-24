#This file contains all the functions implementations.

import psycopg2

import config


class Toorn:

    def __init__(self, toorAPI):
        self.myInsert = 'INSERT INTO ' + config.table + \
                        '(creator, dserver, toorid, skillreq, createdat, gamemode, region)' \
                        'VALUES (%s, %s, %s, %s, %s, %s, %s) '
        self.cli = toorAPI
        self.myDelete = "DELETE FROM " + config.table + \
                        " WHERE creator = '%s'"
        self.myUpdate = "UPDATE " + config.table + \
                        " SET dserver = '%s', skillreq = '%s'," \
                        " gamemode = '%s', region = '%s' " \
                        "WHERE creator = '%s' AND toorid = '%s'"


    ################## TOURNAMENT FUNCTIONS ##################

    def createT(self, dbCur, conn):

        #TODO: Get from User
        ############################ GET FROM USER ############################

        createdAt = '2017-03-21T17:19:54Z'    # get date of creation of tourney or today()
        gameMode = 'ranked'                   # get gameMode
        skillTier = 9                         # get SkillTier for Tourney applications or set as 0 : Requires integer

        name = 'NEWTEST'
        size = 10
        participant_type = 'team'               # Values: (single, team) in string format
        cordServer = 'Halcyon Hackers'          # Get Discord ServerName
        organizerName = 'Kashz'
        organizerCord = 'Kashz#7553'            # Get Discord name and tag.
        discordServer = 'PDSF'                  # Some Unique Discord Server name NOT INVITE URL.
        web = ''                                # Discord URL
        startDate = None                        # date in ISO8601
        endDate = None                          # date in ISO8601
        timeZone = ''                           # Organizer's timeZone in format of IANA tz database (see TZ column at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) Can make mapping of GMT + X to find this out.
        public = False                          # Values: (True, False)

        #Check for public
        if (public == True and (startDate == None or endDate == None)):
            print ('For Public Tourneys, Start and End Date is mandatory')
            ## ERROR : ASK START DATE / END DATE

        else:
            region = 'NA'                           # Values: (EU, NA, EA, SEA, etc.) in string format
            desc = 'Testing Bot'                    # Enter Description
            rules = 'No Rules'                      # Rules for Tourney
            prize = '6k Ice'                        # Tourney Prize
            matchFormat = 'one'                     # Values: (none, one, home_away, bo3, bo5, bo7, bo9, bo11) in string format

            ############################ PRE-SET VARIABLES ############################
            discipline = 'vainglory'
            full_name = cordServer + ' Tourney'
            playedOnline = True
            country = None
            checkIn = False
            participant_nationality = False

            resToorApi = (self.cli).create_tournament(discipline, name, size, participant_type, full_name, organizerName,
                              web, startDate, endDate, timeZone, playedOnline, public, region, country, desc,
                              rules, prize, checkIn, participant_nationality, matchFormat)

            if (resToorApi['id']):
                tID = resToorApi['id']
                print ('Successfully created!', tID)

            # PUT DATA IN POSTGRES DATABASE
                try:
                    dbCur.execute(self.myInsert, (organizerCord, discordServer, tID, skillTier, createdAt, gameMode, region))
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
            else:
                print ('Error')

    def getT(self, dbCur):
        tID = []

        # TODO: Get from DISCORD
        ############################ GET FROM DISCORD API ############################
        cordName = 'Kashz#7553'  # Person invoking the command.

        ############################ GET FROM POSTGRES ############################
        try:
            dbCur.execute("SELECT toorid FROM " + config.table + " WHERE creator = '" + cordName + "'")
            rows = dbCur.fetchall()

            for item in range(len(rows)):
                tID.append(rows[item][0])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        ############################ GET FROM TOURNAMENT API ############################
        for item in tID:
            res = (self.cli).get_tournament(item, 0)
            print (res)

    def editT(self, dbCur, conn):

        # TODO: MESSES UP SOMEPLACE IN COMMITTING CHANGES TO POSTGRES; Need to VERIFY.
        ############################ GET FROM DISCORD API ############################

        tID = ''

        # TODO: Get from DISCORD
        ############################ GET FROM DISCORD API ############################
        cordName = 'Kashz#7553'  # Person invoking the command.
        dserver = 'PDSF'       # Get the server from where the command is invoked.

        ############################ GET FROM POSTGRES ############################
        try:
            # This should fetch ONLY one Tournament ID as it searches with DICORDSERVER AND CREATOR - so only one tourney per server is allowed.
            dbCur.execute("SELECT toorid FROM " + config.table + " WHERE creator = '" + cordName + "' AND dserver = '" + dserver+ "'")
            rows = dbCur.fetchall()

            for item in range(len(rows)):
                tID = rows[item][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        print (tID)

        # TODO: Get from User
        ############################ GET FROM USER ############################
        gameMode = 'ranked'  # get gameMode
        skillTier = 9  # get SkillTier for Tourney applications or set as 0 : Requires integer

        name = 'nameChanged! '
        size = 10
        cordServer = 'Halcyon Hackers'  # Get Discord ServerName
        organizerName = 'Kashz'
        organizerCord = 'Kashz#7553'  # Get Discord name and tag.
        discordServer = 'PDSF???'
        web = ''  # Discord URL
        startDate = None  # date in ISO8601
        endDate = None  # date in ISO8601
        timeZone = ''  # Organizer's timeZone in format of IANA tz database (see TZ column at https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) Can make mapping of GMT + X to find this out.
        public = False  # Values: (True, False)

        # Check for public
        if (public == True and (startDate == None or endDate == None)):
            print('For Public Tourneys, Start and End Date is mandatory')
            ## ERROR : ASK START DATE / END DATE

        else:
            region = 'NA'  # Values: (EU, NA, EA, SEA, etc.) in string format
            desc = 'Testing Bot'  # Enter Description
            rules = 'No Rules'  # Rules for Tourney
            prize = '6k Ice'  # Tourney Prize
            matchFormat = 'one'  # Values: (none, one, home_away, bo3, bo5, bo7, bo9, bo11) in string format

            ############################ PRE-SET VARIABLES ############################
            full_name = cordServer + ' Tourney'
            playedOnline = True
            country = None
            checkIn = False
            participant_nationality = False

            resToorApi = (self.cli).edit_tournament(tID, name, size, full_name, organizerName, web, startDate, endDate,
                                                    timeZone, playedOnline, public, region, country, desc, rules, prize,
                                                    checkIn, participant_nationality, matchFormat)

            if (resToorApi['id']):
                print('Successfully updated!', tID)

                # UPDATE DATA IN POSTGRES DATABASE
                # 'UPDATE %s ('UPDATE %s (skillreq, gamemode, region)' \
                #       'VALUES (%s, %s, %s)' \
                #       'WHERE toorid = %s'

                #self.myInsert = 'UPDATE ' + config.table + \
                #                '(creator, dserver, toorid, skillreq, createdat, gamemode, region)' \
                #                'VALUES (%s, %s, %s, %s, %s, %s, %s) '
            try:



                dbCur.execute(self.myUpdate % (discordServer, skillTier, gameMode, region, organizerCord, tID))
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

    def deleteT(self, dbCur, conn):

        tID = []

        # TODO: Get from DISCORD
        ############################ GET FROM DISCORD API ############################
        cordName = 'Kashz#7553' #Person invoking the command.

        ############################ DELETING FROM TOURNAMENT API ############################
        try:
            dbCur.execute("SELECT toorid FROM " + config.table + " WHERE creator = '" + cordName + "'")
            rows = dbCur.fetchall()

            for item in range(len(rows)):
                tID.append(rows[item][0])
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        for item in tID:
            try:
                dbCur.execute(self.myDelete % (cordName))
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

        for item in tID:
            res = (self.cli).delete_tournament(item)
            if ('code 204' in res):
                print('Successfully Deleted')

    def getMyT(self):
        res = (self.cli).my_tournaments()
        print (res)

    ################## MATCHES FUNCTIONS ##################

    def getM(self):
        pass

    def editM(self):
        pass

    def getMResult(self):
        pass

    def editMResult(self):
        pass

    def MbyDisciplines(self):
        pass

    ################## GAMES FUNCTIONS ##################

    def getG(self):
        pass

    def editG(self):
        pass

    def getGResult(self):
        pass

    def editGResult(self):
        pass

    ################## PARTICIPANTS FUNCTIONS ##################

    def getToorIDPostgres(self, dbCur, discordServer):
        try:
            # This should fetch ONLY one Tournament ID as it searches with DICORDSERVER so only one tourney per server is allowed.
            dbCur.execute("SELECT toorid FROM " + config.table + " WHERE dserver = '" + discordServer + "'")
            return (dbCur.fetchone()[0])
        except (Exception, psycopg2.DatabaseError) as error:
            return (error)


    def createP(self, dbCur):

        team = []
        teamName = ''
        # TODO: Get from User
        ############################ GET FROM USER ############################
        discordServer = 'PDSF'  # Server of Discord the user is in.
        boolTeam = input('team: t/f?: ') # Whether adding one participant or a team of participants
        region = 'NA'  # Ask region

        if (boolTeam == 'True'):
            teamSize = int(input('teamsize: ')) # Ask TeamSize
            teamName = input('teamName: ') #Ask user for Team Name

            for i in range(teamSize):
                ign = input('Enter IGN: ')
                team.append({'name': ign, 'email': None, 'country':region})
        else:
            ############################ GET FROM DISCORD API ############################
            ign = input("ign: ") #IGN of user

        ############################ GET ToorID FROM POSTGRES ############################
        tID = self.getToorIDPostgres(dbCur,discordServer)


        if not (teamName == ''):
            ign = teamName
        res = (self.cli).create_participant(tID, ign, None, region, team)
        print (res)

    def getAllP(self, dbCur):

        # TODO: Get from User
        ############################ GET FROM USER ############################
        discordServer = 'PDSF'  # Server of Discord the user is in.

        ############################ GET ToorID FROM POSTGRES ############################
        tID = self.getToorIDPostgres(dbCur, discordServer)

        allP = []
        res = (self.cli).participants(tID, True,False,'alphabetic')
        for item in res:
            allP.append({'id': item['id'], 'name': item['name']})
        print (allP)
        return allP

    def getOneP(self, dbCur):

        # TODO: Get from User
        ############################ GET FROM USER ############################
        discordServer = 'PDSF'  # Server of Discord the user is in.

        ############################ GET ToorID FROM POSTGRES ############################
        tID = self.getToorIDPostgres(dbCur, discordServer)

        idP = input('Enter id: ')

        res = (self.cli).get_participant(tID, idP)
        print (res)

    def deleteP(self, dbCur):

        # TODO: Get from User
        ############################ GET FROM USER ############################
        discordServer = 'PDSF'  # Server of Discord the user is in.

        ############################ GET ToorID FROM POSTGRES ############################
        tID = self.getToorIDPostgres(dbCur, discordServer)

        listOfP = self.getAllP(dbCur)

        # TODO: Get from User, Convert Name to ID.
        ############################ GET FROM USER ############################
        p2Delete = input('Delete ID: ') #Ask user to enter Name

        res = (self.cli).delete_participant(tID, p2Delete)
        if ('code 204' in res):
            print('Successfully Deleted')

    ################## SCHEDULES FUNCTIONS ##################

    def getSch(self):
        pass

    ################## STAGES FUNCTIONS ##################

    def getSta(self):
        pass

    def getTSta(self):
        pass

    def getAllSta(self):
        pass
