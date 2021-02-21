import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pdb
import json

def autodrive():

    #create webdriver instance
    browser = webdriver.Chrome(executable_path=os.getenv("CHROMEDRIVER_PATH"))

    #create conditional waiter
    waiter = WebDriverWait(browser, 20)

    #access ESPN Fantasy URL
    browser.get(os.getenv("ESPN_FANTASY_BASEBALL_URL"))

    try:
        login(browser, waiter)

        browser.get(os.getenv("ESPN_FANTASY_PROJECTIONS_URL"))
        print("Navigating to Projections page...")

        playerData = {}
        playerData = getAllPlayerData(browser, waiter, playerData)
        writePlayerDataToJSON(playerData)
    finally:
        #keepBrowserOpen()
        browser.quit()

#login method accepts a webdriver instance and waiter instance;
#logs-in to ESPN automatically using specified credentials
def login(browser, waiter):

    print("Logging in to ESPN using credentials...")

    #wait until profile icon loads; then click
    profile_icon = waiter.until(EC.presence_of_element_located((By.ID, "global-user-trigger")))
    profile_icon.click()

    #initiate login
    login_link = browser.find_element_by_xpath("//a[@data-affiliatename='espn']")
    login_link.click()

    #switch target to login modal
    login_iframe = browser.switch_to_frame("disneyid-iframe")

    #locate input fields and submit button for un/pw
    email = browser.find_element_by_xpath("//span/input[@type='email']")
    password = browser.find_element_by_xpath("//span/input[@type='password']")
    login_button = browser.find_element_by_xpath("//button[@type='submit']")

    #clear out the fields
    email.clear()
    password.clear()

    #enter info and login
    email.send_keys(os.getenv("LOGIN_EMAIL"))
    password.send_keys(os.getenv("LOGIN_PASSWORD"))
    login_button.click()
    print("Login successful!")
    time.sleep(10)

    #wait until page re-loads with profile icon
    #waiter.until(EC.presence_of_element_located((By.ID, "global-user-trigger")))

#clicks button that selects all players instead of just Batters
def setProjectionsPage(browser, waiter):
    allPlayersButton = waiter.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filterSlotIds"]/label[1]')))
    allPlayersButton.click()
    time.sleep(10)


#gets player data from the current page and then creates a dictionary with the projections
def getPlayerData(browser, waiter):

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    playerTables = soup.find_all("div", {"class": "jsx-2175038926 full-projection-table"})

    #for formatting in debugger
    #playerTables[0].find("div", {"class": "jsx-4259148104 player-info-secondary"}).find("span", {"class": "player-teamname"}).get_text()
    #playerTables[0].find("div", {"class": "jsx-317977224 player__fullprojections__stats"})
    #playerTables[0].find("div", {"class": "jsx-317977224 player__fullprojections__stats"}).find_all("th", {"class": "Table__TH"})[1].get_text()

    players = {}

    for playerTable in playerTables:

        playerName = playerTable.find("a").get_text()
        rank = playerTable.find("div", {"class": "jsx-2810852873 table--cell ranking tar"}).get_text()

        #headshot = playerTable.find("div", {"class": "Image__Wrapper aspect-ratio--child"}).find("img")["src"]
        headshot = playerTable.find("div", {"class": "jsx-4259148104 player-headshot"}).find("img")["src"]
        teamLogo = playerTable.find("div", {"class": "jsx-4259148104 player-info-secondary"}).find("img")["src"]
        playerStats = playerTable.find("div", {"class": "jsx-317977224 player__fullprojections__stats"})
        y1 = playerStats.find_all("tr", {"class": "Table__TR Table__TR--sm Table__odd"})[0].find_all("td")[0].get_text().split(" ")[0]
        y2 = playerStats.find_all("tr", {"class": "Table__TR Table__TR--sm Table__odd"})[1].find_all("td")[0].get_text().split(" ")[0]
        statHeader = playerStats.find_all("th", {"class": "Table__TH"})
        statRow = playerStats.find_all("tr", {"class": "Table__TR Table__TR--sm Table__odd"})
        playerPosition = playerTable.find("div", {"class": "jsx-4259148104 player-info-secondary"}).find("span", {"class": "position-eligibility"}).get_text()
        statHeaderTag = "p"

        #check if the position of the player is a batter (Shohei Ohtani is treated as batter with projections)
        if(("P" not in playerPosition) or (playerName == "Shohei Ohtani") or (playerName == "Tanner Dodson")):
            statHeaderTag = "b"

        players[rank] = {
        #playerObj = {
            "name": playerName,
            "rank": rank,
            "headshotLink": headshot,
            "teamLogoLink": teamLogo,
            "team": playerTable.find("div", {"class": "jsx-4259148104 player-info-secondary"}).find("span", {"class": "player-teamname"}).get_text(),
            "position": playerPosition,

            #2020 Stats
            f"{y1}_{statHeader[1].get_text()}": statRow[0].find_all("td")[1].get_text(),
            f"{y1}_{statHeader[2].get_text()}": statRow[0].find_all("td")[2].get_text(),
            f"{y1}_{statHeader[3].get_text()}": statRow[0].find_all("td")[3].get_text(),

            f"{y1}_{statHeader[7].get_text()}": statRow[0].find_all("td")[7].get_text(),
            f"{y1}_{statHeader[8].get_text()}": statRow[0].find_all("td")[8].get_text(),
            f"{y1}_{statHeader[9].get_text()}": statRow[0].find_all("td")[9].get_text(),
            f"{y1}_{statHeader[10].get_text()}": statRow[0].find_all("td")[10].get_text(),
            f"{y1}_{statHeader[11].get_text()}": statRow[0].find_all("td")[11].get_text(),
            f"{y1}_{statHeader[12].get_text()}": statRow[0].find_all("td")[12].get_text(),

            #2021 Projected Stats
            f"{y2}_{statHeader[1].get_text()}": statRow[1].find_all("td")[1].get_text(),
            f"{y2}_{statHeader[2].get_text()}": statRow[1].find_all("td")[2].get_text(),
            f"{y2}_{statHeader[3].get_text()}": statRow[1].find_all("td")[3].get_text(),

            f"{y2}_{statHeader[7].get_text()}": statRow[1].find_all("td")[7].get_text(),
            f"{y2}_{statHeader[8].get_text()}": statRow[1].find_all("td")[8].get_text(),
            f"{y2}_{statHeader[9].get_text()}": statRow[1].find_all("td")[9].get_text(),
            f"{y2}_{statHeader[10].get_text()}": statRow[1].find_all("td")[10].get_text(),
            f"{y2}_{statHeader[11].get_text()}": statRow[1].find_all("td")[11].get_text(),
            f"{y2}_{statHeader[12].get_text()}": statRow[1].find_all("td")[12].get_text(),

            "outlook": playerTable.find("div", {"class": "full-projection-player-outlook__content mt2 n8"}).get_text()
        }

        #account for the fact that BB and K are both pitcher and hitter stats; create distinct column names by appending statHeaderTag
        if(statHeaderTag == "p"):
            players[rank][f"{y1}_{statHeader[4].get_text()}{statHeaderTag}"] = statRow[0].find_all("td")[4].get_text()
            players[rank][f"{y1}_{statHeader[5].get_text()}{statHeaderTag}"] = statRow[0].find_all("td")[5].get_text()
            players[rank][f"{y1}_{statHeader[6].get_text()}"] = statRow[0].find_all("td")[6].get_text()
            players[rank][f"{y2}_{statHeader[4].get_text()}{statHeaderTag}"] = statRow[1].find_all("td")[4].get_text()
            players[rank][f"{y2}_{statHeader[5].get_text()}{statHeaderTag}"] = statRow[1].find_all("td")[5].get_text()
            players[rank][f"{y2}_{statHeader[6].get_text()}"] = statRow[1].find_all("td")[6].get_text()
        else:
            players[rank][f"{y1}_{statHeader[4].get_text()}"] = statRow[0].find_all("td")[4].get_text()
            players[rank][f"{y1}_{statHeader[5].get_text()}{statHeaderTag}"] = statRow[0].find_all("td")[5].get_text()
            players[rank][f"{y1}_{statHeader[6].get_text()}{statHeaderTag}"] = statRow[0].find_all("td")[6].get_text()
            players[rank][f"{y2}_{statHeader[4].get_text()}"] = statRow[1].find_all("td")[4].get_text()
            players[rank][f"{y2}_{statHeader[5].get_text()}{statHeaderTag}"] = statRow[1].find_all("td")[5].get_text()
            players[rank][f"{y2}_{statHeader[6].get_text()}{statHeaderTag}"] = statRow[1].find_all("td")[6].get_text()



        print(f"Added {playerName}!")

    return players

#merges current player page data with previously fetched player data
def addPlayers(browser, waiter, playerData):
    players = getPlayerData(browser, waiter)
    newPlayerData = {**playerData, **players}
    return newPlayerData

#gets the data for all the players on the projection page
def getAllPlayerData(browser, waiter, playerData):

    setProjectionsPage(browser, waiter)
    next_button = browser.find_element_by_xpath('//*[@id="fitt-analytics"]/div/div[5]/div[2]/div[3]/div/div/div/div/div[51]/button[2]')

    #while((next_button.get_attribute("disabled") == None)) & (int(next_button.get_attribute("data-nav-item")) <= 5)):  #just for testing upto a page number

    pages_extracted = []

    while(next_button.get_attribute("disabled") == None):
        print("Fetching Player Data from Page...")

        currentPage = int(next_button.get_attribute("data-nav-item"))

        if(currentPage not in pages_extracted):
            playerData = addPlayers(browser, waiter, playerData)
            pages_extracted.append(currentPage)

        print(f"Extrated: {pages_extracted}")
        print("Navigating to Next page...")
        next_button.click()
        time.sleep(10)

    #extract data for the last page
    playerData = addPlayers(browser, waiter, playerData)
    print("Finished fetching player data...")
    time.sleep(10)

    return playerData

#writes the current players dictionary to a JSON file
def writePlayerDataToJSON(playerData):

    print("Writing data to JSON file...")

    with open('./temp/players.json', 'w', encoding='utf-8') as f:
        json.dump(playerData, f, ensure_ascii=False, indent=4)

    print("Successfully wrote data to JSON file!")


#method just keeps the browser open instead of quitting when finished with task
def keepBrowserOpen():
    while(True):
        pass

#method for outputting page source to text file for parsing and debugging
def writePageSourceToText(browser):
    #pdb.set_trace()

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    file = open("./temp/projectionsPage.txt", "w")
    file.write(str(soup.prettify()))
    file.close()
