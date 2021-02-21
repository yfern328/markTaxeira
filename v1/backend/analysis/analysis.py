import pandas
import pdb

#this method reads a JSON file, organizes columns, and outputs to CSV
def write_JSON_to_CSV():

    playerUniverse = pandas.read_json("./temp/players.json").transpose()

    #not needed for this data output
    del playerUniverse["headshotLink"]
    del playerUniverse["teamLogoLink"]

    #Tanner Dodson joins the Shohei Ohtani club;
    #is classified as OF, RP (need to account for extra columns from scrape due to oddity) #fixed in second extract--not needed
    #del playerUniverse["2020_RBIp"]
    #del playerUniverse["2020_K"]
    #del playerUniverse["2021_RBIp"]
    #del playerUniverse["2021_K"]

    #print(df.keys())

    #reorder the columns
    playerUniverse = playerUniverse.reindex(columns = ['name', 'rank', 'team', 'position', '2020_fpts', '2021_fpts', 'outlook',
            '2020_AB', '2020_R', '2020_HR', '2020_RBI', '2020_BBb', '2020_Kb', '2020_SB', '2020_AVG', '2020_OBP', '2020_SLG', '2020_OPS',
            '2021_AB', '2021_R', '2021_HR', '2021_RBI', '2021_BBb', '2021_Kb', '2021_SB', '2021_AVG', '2021_OBP', '2021_SLG', '2021_OPS',
            '2020_G', '2020_GS', '2020_IP', '2020_BBp', '2020_Kp', '2020_W', '2020_SV', '2020_HD', '2020_ERA', '2020_WHIP', '2020_K/9',
            '2021_G', '2021_GS', '2021_IP', '2021_BBp', '2021_Kp', '2021_W', '2021_SV', '2021_HD', '2021_ERA', '2021_WHIP', '2021_K/9'])


    #rename the columns
    playerUniverse.columns = ['Name', 'Rank', 'Team', 'Position', '2020_FPTS', 'PROJ_FPTS', 'Outlook',
            '2020_AB', '2020_R', '2020_HR', '2020_RBI', '2020_BBb', '2020_Kb', '2020_SB', '2020_AVG', '2020_OBP', '2020_SLG', '2020_OPS',
            'PROJ_AB', 'PROJ_R', 'PROJ_HR', 'PROJ_RBI', 'PROJ_BBb', 'PROJ_Kb', 'PROJ_SB', 'PROJ_AVG', 'PROJ_OBP', 'PROJ_SLG', 'PROJ_OPS',
            '2020_G', '2020_GS', '2020_IP', '2020_BBp', '2020_Kp', '2020_W', '2020_SV', '2020_HD', '2020_ERA', '2020_WHIP', '2020_K/9',
            'PROJ_G', 'PROJ_GS', 'PROJ_IP', 'PROJ_BBp', 'PROJ_Kp', 'PROJ_W', 'PROJ_SV', 'PROJ_HD', 'PROJ_ERA', 'PROJ_WHIP', 'PROJ_K/9']

    print(playerUniverse)
    #pdb.set_trace()
    playerUniverse.to_csv("./temp/playerUniverse.csv", index=False)
