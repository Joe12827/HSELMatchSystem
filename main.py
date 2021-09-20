# Joe Wesnofske
# Made in 2019
# Using discord.py rewrite

import discord
import json
import requests
import time

from VarsityEsports import Tournament

client = discord.Client()

toornamentId = ''
global rosterName
global toornamentIds
global toornamentNames
global fullToornamentName
global toornamentNamesFull
toornamentIds = []
toornamentNames = []
toornamentNamesFull = []
fullToornamentName = ''

commandPrefix = '!'

# Open files for toornament data
toornamentIdsFile = open('H:\mybotdatacache\Toornament Id List.json' , 'r')
toornamentIdsFile = json.load(toornamentIdsFile)
for x in range(len(toornamentIdsFile)):
    toornamentIds.append(toornamentIdsFile[x])

toornamentNamesFile = open('H:\mybotdatacache\Toornament Names.json' , 'r')
toornamentNamesFile = json.load(toornamentNamesFile)
for x in range(len(toornamentNamesFile)):
    toornamentNames.append(toornamentNamesFile[x])

toornamentNamesFullFile = open('H:\mybotdatacache\Toornament Names Full.json' , 'r')
toornamentNamesFullFile = json.load(toornamentNamesFullFile)
for x in range(len(toornamentNamesFullFile)):
    toornamentNamesFull.append(toornamentNamesFullFile[x])

# Get data for standings
tournamentStandingsFullList = []
print('Starting Standings Cache (Slow)')
for x in range(len(toornamentIds)):
    tournamentObject = Tournament(toornamentIds[x])
    tournamentStandingsFullList.append(tournamentObject.getStandings())
    print('Standings Cache ' + toornamentIds[x] + ' Done')
print('All Standings Cache Done')


toornamentAllGameData = []
toornamentGameDataTemp = []
toornamentData = []


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(commandPrefix + 'help'):
        try:
            await message.delete()
        except:
            print('Sent in Direct Message')
            
        helpEmbed = discord.Embed(colour=discord.Colour.blurple())

        helpEmbed.add_field(name=commandPrefix + "match Club Name: Roster Name", value='Find latest match data for a given roster')
        helpEmbed.add_field(name=commandPrefix + "standings", value='Find standings for a specific game')

        helpEmbed.set_footer(text="Made possible by Joey Dubz and his internet provider")

        await message.channel.send(embed=helpEmbed)
        

    if message.content == commandPrefix + 'members':
        guild = message.guild
        x = guild.member_count
        await message.channel.send(x)
        print(x)


    if message.content == commandPrefix + "standings":
        try:
            await message.delete()
        except:
            print('Sent in Direct Message')
            
        commandGiver = '{0.author}'.format(message)

        embed = discord.Embed(
            title=str('Use "' + commandPrefix + 'standings x" to get the standings for a game'),
            colour=discord.Colour.red()
        )
        for x in range(len(toornamentNames)):
            embed.add_field(name=x+1, value=str(toornamentNamesFull[x]), inline=True)

        embed.set_author(name='HSEL Standings Discord System', icon_url='https://mobile.varsityesports.com/images/hsel_jumbo.png')
        embed.set_footer(text="Made possible by Joey Dubz and his internet provider")

        await message.channel.send(embed=embed)


    if message.content.startswith(commandPrefix + 'standings '):
        try:
            await message.delete()
        except:
            print('Sent in Direct Message')
            
        commandName = commandPrefix + 'standings '
        commandAndMessage = str(message.content)
        toornamentNumber = commandAndMessage.replace(commandName, '')
        print(toornamentNumber)

        try:  # Test to see if input was an int
            toornamentNumber = int(toornamentNumber)
        except ValueError:
            await message.channel.send("Please use a tournament number between 1 and " + str(len(toornamentIds)))
            return

        if toornamentNumber >= 1 and toornamentNumber <= len(toornamentIds):
            toornamentStandingsId = toornamentIds[toornamentNumber - 1]  # Standing embed has first toornament start at 1 (not 0)
            toornamentStandingsName = toornamentNamesFull[toornamentNumber - 1]

            toornamentStandingsId = int(toornamentStandingsId)

            tournamentStandingsMainList = tournamentStandingsFullList[toornamentNumber - 1]

            print(toornamentStandingsId)

            embed = discord.Embed(
                title=str(toornamentStandingsName + ' Standings (Top 10)'),
                colour=discord.Colour.red()
            )

            embed.set_author(name='HSEL Standings Discord System', icon_url='https://mobile.varsityesports.com/images/hsel_jumbo.png')
            embed.set_footer(text="Made possible by Joey Dubz and his internet provider")

            for x in range(2,-1,-1):
                topPlayers = ''
                for y in range(10):  # takes top 10 teams
                    try:
                        if len(tournamentStandingsMainList[1][x][1][y][1]) <= 25:
                            topPlayers += tournamentStandingsMainList[1][x][1][y][1] + '\n' + '\n' + '\n'
                        else:
                            topPlayers += tournamentStandingsMainList[1][x][1][y][1] + '\n' + '\n'
                    except:
                        print('No player found')
                try:
                    embed.add_field(name=str(tournamentStandingsMainList[1][x][0]), value=(topPlayers), inline=True)
                except:
                    print('Empty Standings List')

            await message.channel.send(embed=embed)

        else:
            await message.channel.send("Please use a tournament number between 1 and " + str(len(toornamentIds)))

    # Start of HSELMatchBot

    if message.content.startswith(commandPrefix + 'match '):
        await message.add_reaction('✔')
        commandGiver = '{0.author}'.format(message)
        print(commandGiver)

        commandName = commandPrefix + 'match '
        commandAndRoster = str(message.content)
        rosterName = commandAndRoster.replace(commandName, '')

        msg = rosterName.format(message)

        for x in range(len(toornamentIds)):
            # Made to only run on my machine
            with open("H:\mybotdatacache\\" + str(toornamentNames[x]) + 'ToornamentData.json') as toornamentDataFile:
                toornamentDataTemp = json.load(toornamentDataFile)

            toornamentDataStrTemp = str(toornamentDataTemp)

            if rosterName in toornamentDataStrTemp:
                global toornamentData
                global toornamentId
                toornamentData = toornamentDataTemp
                toornamentId = str(toornamentIds[x])
                toornamentName = str(toornamentNames[x])

                isPlayoffs = False
                if "'stage_number': 4" in toornamentDataStrTemp:
                    isPlayoffs = True
                break
            else: toornamentId = 'none'

        toornaments = []
        toornaments = requests.get('https://mobile.varsityesports.com/api/toornament').json()
        for x in range(len(toornamentIds)):
            if toornamentId == toornaments[x]["id"]:
                fullToornamentName = toornaments[x]["name"]
                print(fullToornamentName)
                break

        if toornamentId == 'none':
            await message.channel.send('Unable to find roster. Make sure it is correct!')
            try:
                await message.delete()
            except:
                print('Sent in Direct Message')
            print("No roster found.")
            return

        global gameConnectionId
        gameConnectionId = 0
        if toornamentId == "0000000000000": #league of legends
            gameConnectionId = 11

        if toornamentId == "2745251605683224576": #rl
            gameConnectionId = 12

        if toornamentId == "2745219818095149056": #ow
            gameConnectionId = 13

        if toornamentId == "2745257243593342976": #hs
            gameConnectionId = 14

        if toornamentId == "2745255184153886720": #csgo
            gameConnectionId = 15

        if toornamentId == "2745245145646383104": #r6 pc
            gameConnectionId = 16
        if toornamentId == "2745248836230004736": #r6 ps4
            gameConnectionId = 16
        if toornamentId == "2745247067001896960": #r6 xbox
            gameConnectionId = 16

        if toornamentId == "0000000000": #paladins
            gameConnectionId = 17

        if toornamentId == "2785700766919540736": #smite
            gameConnectionId = 18

        if toornamentId == "0000000000": #cod wwII
            gameConnectionId = 19

        if toornamentId == "0000000000": #Injustice 2
            gameConnectionId = 20

        if toornamentId == "0000000000": #Dota 2
            gameConnectionId = 21

        if toornamentId == "0000000000": #Heroes of the Storm
            gameConnectionId = 22

        if toornamentId == '2745253579684020224': #smash
            gameConnectionId = 23

        if toornamentId == '2745259770527031296': #fortnite
            gameConnectionId = 24

        rosterMatchList = []
        matchIdList = []
        matchIdRoundNumber = []
        matchIdStageNumber = []
        playoffRoundIds = []
        playoffRoundNumbers = []
        latestPlayoffRoundNumber = 0
        latestRoundNumber = 0
        matchIdRoundNumberStr = ''
        latestRoundNumberId = ''

        if isPlayoffs == False:
            for x in range(len(toornamentData)):
                try:
                    for i in toornamentData[x]["opponents"]:
                        if rosterName in i["participant"]["name"]:
                            matchIdList.append(toornamentData[x]["id"])

                            matchIdRoundNumber.append(toornamentData[x]["round_number"])
                            matchIdStageNumber.append(toornamentData[x]["stage_number"])

                            rosterMatchList.append(toornamentData[x])
                except:
                    print ('Null')

        if isPlayoffs == True:
            for x in range(len(toornamentData)):
                try:
                    for i in toornamentData[x]["opponents"]:
                        if rosterName in i["participant"]["name"]:
                            if toornamentData[x]["stage_number"] == 4:
                                matchIdList.append(toornamentData[x]["id"])

                                matchIdRoundNumber.append(toornamentData[x]["round_number"])
                                matchIdStageNumber.append(toornamentData[x]["stage_number"])
                                rosterMatchList.append(toornamentData[x])
                except:
                    print ('Null')

        if matchIdList == []:
            await message.delete()
            await message.channel.send(rosterName + ' did not make playoffs.')
            return

        latestRoundNumber = max(matchIdRoundNumber)
        for x in range(len(matchIdRoundNumber)):
            matchIdRoundNumberStr += str(matchIdRoundNumber[x])

        latestRoundIndex = matchIdRoundNumberStr.find(str(latestRoundNumber))

        latestRoundNumberId = matchIdList[latestRoundIndex]

        matchData = requests.get("https://mobile.varsityesports.com/api/toornament/" + toornamentId + "/match/" + str(
            latestRoundNumberId)).json()

        matchLink = "https://ves.highschoolesportsleague.com/tournament/" + toornamentId + "/match/" + str(
            latestRoundNumberId) + "/edit"
        
        teamNumber = ''
        rosterIdList = []
        clubIdList = []

        for x in range(2):
            rosterIdList.append(matchData["opponents"][x]["rosterId"])
            clubIdList.append(matchData["opponents"][x]["clubId"])

        global clubID
        clubID = ''

        for x in range(2):
            if matchData["opponents"][x]["participant"]["name"] == rosterName:

                clubID = str(matchData["opponents"][x]["clubId"])

        enemyRosterName = ''

        if clubIdList[0] == clubID:
            enemyRosterId = rosterIdList[1]
            enemyClubId = clubIdList[1]
            enemyPosition = 1
            enemyRosterName = matchData["opponents"][1]["participant"]["name"]
        else:
            enemyRosterId = rosterIdList[0]
            enemyClubId = clubIdList[0]
            enemyPosition = 0
            enemyRosterName = matchData["opponents"][0]["participant"]["name"]

        rosterData = str(requests.get("https://mobile.varsityesports.com/api/club/" + str(enemyClubId) + "/roster/" + str(enemyRosterId)).json())

        index = 0
        loopNumber = 0
        playerNumber = ''
        playerIdList = []
        global playerVELinks
        playerVELinks = []

        while "userId" in rosterData:
            loopNumber += 1
            index = rosterData.find("userId")
            rosterData = rosterData[index + 1:]
            cutOff = rosterData.find(",")
            playerIdList.append(rosterData[9:cutOff - 1])
        del playerIdList[0]

        for x in range(len(playerIdList)):
            playerVELinks.append('https://mobile.varsityesports.com/users/profile/' + (playerIdList[x]))

        if toornamentId == '2745257243593342976' or toornamentId == '2745259770527031296' or toornamentId == '2745253579684020224' or toornamentId == '2745231753238880256' or toornamentId == '2869227017663250432' or toornamentId == '2869248536377081856':#check if its a solo games
            enemyNameAndRoster = matchData["opponents"][enemyPosition]["participant"]["name"]
            soloNameCutOff = enemyNameAndRoster.find(":")
            enemyName = enemyNameAndRoster[soloNameCutOff+2:]

            for x in range(len(playerIdList)):
                playerGameconnectionsData = requests.get("https://mobile.varsityesports.com/api/user/" + playerIdList[x] + "/gameconnections").json()
                for y in range(len(playerGameconnectionsData)):
                    if playerGameconnectionsData[y]["inGameName"] == enemyName:
                        playerVELinks = ''
                        playerVELink = ('https://mobile.varsityesports.com/users/profile/' + (playerIdList[x]))
                        
                        if isPlayoffs == False:
                            embed = discord.Embed(
                                title=str('Regular season week ' + str(latestRoundNumber) + '\n' + rosterName + "   vs. \n" + enemyRosterName),
                                colour=discord.Colour.red()
                            )
                        else:
                            embed = discord.Embed(
                                title=str('Playoff round ' + str(latestRoundNumber) + '\n' + rosterName + "   vs. \n" + enemyRosterName),
                                colour=discord.Colour.red()
                            )

                        embed.set_author(name=fullToornamentName, icon_url='https://mobile.varsityesports.com/images/hsel_jumbo.png')
                        embed.set_footer(text=commandAndRoster + "\nMade possible by Joe and his internet provider")
                        embed.add_field(name="Match Link", value=matchLink, inline=False)
                        embed.add_field(name=str(enemyName), value=playerVELink)
                        await message.delete()
                        await message.channel.send(embed=embed)
                        break

        else: #if NOT solo game (team game)
            global playerNameList
            playerNameList = []

            if isPlayoffs == False:
                embed = discord.Embed(
                    title=str('Regular season round ' + str(latestRoundNumber) + '\n' + rosterName + "   vs. \n" + enemyRosterName),
                    colour=discord.Colour.red()
                )
            else:
                embed = discord.Embed(
                    title=str('Playoff round ' + str(latestRoundNumber) + '\n' + rosterName + "   vs. \n" + enemyRosterName),
                    colour=discord.Colour.red()
                )

            embed.set_author(name=fullToornamentName, icon_url='https://mobile.varsityesports.com/images/hsel_jumbo.png')
            embed.set_footer(text=commandAndRoster + "\nMade possible by Joey Dubz and his internet provider")
            embed.add_field(name="Match Link", value=matchLink, inline=False)

            for x in range(len(playerIdList)):
                gameConnectionInfo = requests.get("https://mobile.varsityesports.com/api/user/" + playerIdList[x] + "/gameconnections").json()

                for y in range(len(gameConnectionInfo)):
                    if gameConnectionInfo[y]["gamesId"] == str(gameConnectionId):
                        global playerName
                        playerNameList.append(gameConnectionInfo[y]["inGameName"])

                embed.add_field(name=str(playerNameList[x]), value=playerVELinks[x])
            try:
                await message.delete()
            except:
                print('Sent in Direct Message')
            await message.channel.send(embed=embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-------------')

client.run('TOKEN')
