#Module qui regroupe l'ensemble des fonctions pour scrapper les infos utiles sur le site BWF Software Tournament
import bs4 as bs
import requests
import pandas as pd
import numpy as np

from simulation import *


def get_tournament_list_men_singles(playerId,player_name,week_id):
    url_player = 'https://bwf.tournamentsoftware.com/ranking/player.aspx?id='+week_id+'&player='+str(playerId)

    response = requests.get(url_player)
    content = response.text

    soup = bs.BeautifulSoup(content, 'html.parser')

    tables = soup.find_all('table', attrs={'class':'ruler'})

    player_tournaments_results = []

    for table in tables:
        caption = table.find('caption')
        if "Men's Singles results of "+player_name in caption.text:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                cols = tr.find_all('td')
                if len(cols)>=6:
                    #0: Tournament, 1: Week, 2: Result, 3: Points, 4: Matches 5: Used for calculation
                    link_to_matchs = cols[4].find('a').get('href')
                    used_for_calculation = len(cols[5].find_all('img'))>=1
                    
                    year = cols[1].text.strip().split('-')[0]
                    week = cols[1].text.strip().split('-')[1]
                    tournament_name = cols[0].text.strip()
                    print(tournament_name)
                    if year == '2022':
                        details_tournament = df_2022_tournaments_list[df_2022_tournaments_list['Tournament']==tournament_name]
                        week = details_tournament['Week'].iloc[0]
                    elif year == '2023':
                        details_tournament = df_2023_tournaments_list[df_2023_tournaments_list['Tournament']==tournament_name]
                        week = details_tournament['Week'].iloc[0]

                    player_tournaments_results.append([year,week,tournament_name,cols[2].text.strip(),cols[3].text.strip(),used_for_calculation,link_to_matchs])

    df_player_tournaments_results = pd.DataFrame(player_tournaments_results,columns=['Year','Week','Tournament','Result','Points','Calculation','Matches'])

    df_player_tournaments_results['Points'] = df_player_tournaments_results['Points'].astype('int')
    df_player_tournaments_results['Week'] = df_player_tournaments_results['Week'].astype('int')
    df_player_tournaments_results = df_player_tournaments_results.sort_values(by=['Week'], ascending=True)
    df_player_tournaments_results.reset_index(drop=True,inplace=True)

    return df_player_tournaments_results

def get_tournament_list_women_singles(playerId,player_name,week_id):
    url_player = 'https://bwf.tournamentsoftware.com/ranking/player.aspx?id='+week_id+'&player='+str(playerId)

    response = requests.get(url_player)
    content = response.text

    soup = bs.BeautifulSoup(content, 'html.parser')

    tables = soup.find_all('table', attrs={'class':'ruler'})

    player_tournaments_results = []

    for table in tables:
        caption = table.find('caption')
        if "Women's Singles results of "+player_name in caption.text:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                cols = tr.find_all('td')
                if len(cols)>=6:
                    #0: Tournament, 1: Week, 2: Result, 3: Points, 4: Matches 5: Used for calculation
                    link_to_matchs = cols[4].find('a').get('href')
                    used_for_calculation = len(cols[5].find_all('img'))>=1

                    year = cols[1].text.strip().split('-')[0]
                    week = cols[1].text.strip().split('-')[1]
                    tournament_name = cols[0].text.strip()
                    if year == '2022':
                        details_tournament = df_2022_tournaments_list[df_2022_tournaments_list['Tournament']==tournament_name]
                        week = details_tournament['Week'].iloc[0]
                    elif year == '2023':
                        details_tournament = df_2023_tournaments_list[df_2023_tournaments_list['Tournament']==tournament_name]
                        week = details_tournament['Week'].iloc[0]

                    player_tournaments_results.append([year,week,tournament_name,cols[2].text.strip(),cols[3].text.strip(),used_for_calculation,link_to_matchs])

    df_player_tournaments_results = pd.DataFrame(player_tournaments_results,columns=['Year','Week','Tournament','Result','Points','Calculation','Matches'])

    df_player_tournaments_results['Points'] = df_player_tournaments_results['Points'].astype('int')
    df_player_tournaments_results['Week'] = df_player_tournaments_results['Week'].astype('int')
    df_player_tournaments_results = df_player_tournaments_results.sort_values(by=['Week'], ascending=True)
    df_player_tournaments_results.reset_index(drop=True,inplace=True)

    return df_player_tournaments_results


def get_tournament_list_men_doubles(playerId,player_name,player_partner_name,week_id):
    url_player = 'https://bwf.tournamentsoftware.com/ranking/player.aspx?id='+week_id+'&player='+str(playerId)

    response = requests.get(url_player)
    content = response.text

    soup = bs.BeautifulSoup(content, 'html.parser')

    tables = soup.find_all('table', attrs={'class':'ruler'})

    player_tournaments_results = []

    for table in tables:
        caption = table.find('caption')
        if "Men's Doubles results of "+player_name+' / '+player_partner_name in caption.text:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                cols = tr.find_all('td')
                if len(cols)>=6:
                    #0: Tournament, 1: Week, 2: Result, 3: Points, 4: Matches 5: Used for calculation
                    link_to_matchs = cols[4].find('a').get('href')
                    used_for_calculation = len(cols[5].find_all('img'))>=1

                    year = cols[1].text.strip().split('-')[0]
                    week = cols[1].text.strip().split('-')[1]
                    tournament_name = cols[0].text.strip()
                    if year == '2022':
                        details_tournament = df_2022_tournaments_list[df_2022_tournaments_list['Tournament']==tournament_name]
                        week = details_tournament['Week'].iloc[0]
                    elif year == '2023':
                        details_tournament = df_2023_tournaments_list[df_2023_tournaments_list['Tournament']==tournament_name]
                        week = details_tournament['Week'].iloc[0]

                    player_tournaments_results.append([year,week,tournament_name,cols[2].text.strip(),cols[3].text.strip(),used_for_calculation,link_to_matchs])

    df_player_tournaments_results = pd.DataFrame(player_tournaments_results,columns=['Year','Week','Tournament','Result','Points','Calculation','Matches'])
    
    df_player_tournaments_results['Points'] = df_player_tournaments_results['Points'].astype('int')
    df_player_tournaments_results['Week'] = df_player_tournaments_results['Week'].astype('int')
    df_player_tournaments_results = df_player_tournaments_results.sort_values(by=['Week'], ascending=True)
    df_player_tournaments_results.reset_index(drop=True,inplace=True)

    return df_player_tournaments_results

def get_tournament_list_women_doubles(playerId,player_name,player_partner_name,week_id):
    url_player = 'https://bwf.tournamentsoftware.com/ranking/player.aspx?id='+week_id+'&player='+str(playerId)

    response = requests.get(url_player)
    content = response.text

    soup = bs.BeautifulSoup(content, 'html.parser')

    tables = soup.find_all('table', attrs={'class':'ruler'})

    player_tournaments_results = []

    for table in tables:
        caption = table.find('caption')
        if "Women's Doubles results of "+player_name+' / '+player_partner_name in caption.text:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                cols = tr.find_all('td')
                if len(cols)>=6:
                    #0: Tournament, 1: Week, 2: Result, 3: Points, 4: Matches 5: Used for calculation
                    link_to_matchs = cols[4].find('a').get('href')
                    used_for_calculation = len(cols[5].find_all('img'))>=1

                    year = cols[1].text.strip().split('-')[0]
                    week = cols[1].text.strip().split('-')[1]
                    tournament_name = cols[0].text.strip()
                    if year == '2022':
                        details_tournament = df_2022_tournaments_list[df_2022_tournaments_list['Tournament']==tournament_name]
                        week = details_tournament['Week'].iloc[0]
                    elif year == '2023':
                        details_tournament = df_2023_tournaments_list[df_2023_tournaments_list['Tournament']==tournament_name]
                        week = details_tournament['Week'].iloc[0]

                    player_tournaments_results.append([year,week,tournament_name,cols[2].text.strip(),cols[3].text.strip(),used_for_calculation,link_to_matchs])

    df_player_tournaments_results = pd.DataFrame(player_tournaments_results,columns=['Year','Week','Tournament','Result','Points','Calculation','Matches'])
    
    df_player_tournaments_results['Points'] = df_player_tournaments_results['Points'].astype('int')
    df_player_tournaments_results['Week'] = df_player_tournaments_results['Week'].astype('int')
    df_player_tournaments_results = df_player_tournaments_results.sort_values(by=['Week'], ascending=True)
    df_player_tournaments_results.reset_index(drop=True,inplace=True)

    return df_player_tournaments_results

def get_tournament_list_mixed_doubles(playerId,player_name,player_partner_name,week_id):
    url_player = 'https://bwf.tournamentsoftware.com/ranking/player.aspx?id='+week_id+'&player='+str(playerId)

    response = requests.get(url_player)
    content = response.text

    soup = bs.BeautifulSoup(content, 'html.parser')

    tables = soup.find_all('table', attrs={'class':'ruler'})

    player_tournaments_results = []

    for table in tables:
        caption = table.find('caption')
        if "Mixed Doubles results of "+player_name+' / '+player_partner_name in caption.text:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                cols = tr.find_all('td')
                if len(cols)>=6:
                    #0: Tournament, 1: Week, 2: Result, 3: Points, 4: Matches 5: Used for calculation
                    link_to_matchs = cols[4].find('a').get('href')
                    used_for_calculation = len(cols[5].find_all('img'))>=1

                    year = cols[1].text.strip().split('-')[0]
                    week = cols[1].text.strip().split('-')[1]
                    tournament_name = cols[0].text.strip()
                    if year == '2022':
                        details_tournament = df_2022_tournaments_list[df_2022_tournaments_list['Tournament']==tournament_name]
                        week = details_tournament['Week'].iloc[0]
                    elif year == '2023':
                        details_tournament = df_2023_tournaments_list[df_2023_tournaments_list['Tournament']==tournament_name]
                        week = details_tournament['Week'].iloc[0]

                    player_tournaments_results.append([year,week,tournament_name,cols[2].text.strip(),cols[3].text.strip(),used_for_calculation,link_to_matchs])

    df_player_tournaments_results = pd.DataFrame(player_tournaments_results,columns=['Year','Week','Tournament','Result','Points','Calculation','Matches'])
    
    df_player_tournaments_results['Points'] = df_player_tournaments_results['Points'].astype('int')
    df_player_tournaments_results['Week'] = df_player_tournaments_results['Week'].astype('int')
    df_player_tournaments_results = df_player_tournaments_results.sort_values(by=['Week'], ascending=True)
    df_player_tournaments_results.reset_index(drop=True,inplace=True)

    return df_player_tournaments_results

#Fonction qui va scrapper la liste des semaines de classement disponibles sur le site de la bwf ainsi que les id de semaines associés
def get_world_ranking_weeks():
    url_world_ranking = 'https://bwf.tournamentsoftware.com/ranking/ranking.aspx?rid=70'

    df_options_weeks = pd.DataFrame(columns=['options_weeks','weeks_ids'])

    response = requests.get(url_world_ranking)
    content = response.text

    soup = bs.BeautifulSoup(content, 'html.parser')

    ranking_week = soup.find('select')
    weeks = ranking_week.find_all('option')

    for option in weeks:
        if option.text.strip().split('/')[2]=='2023':
            df_options_weeks.loc[len(df_options_weeks)]=[option.text.strip(),option['value'].strip()]

    df_options_weeks['weeks_ids'] = df_options_weeks['weeks_ids'].astype('int')
    df_options_weeks = df_options_weeks.sort_values(by=['weeks_ids'], ascending=True)
    df_options_weeks['weeks_ids'] = df_options_weeks['weeks_ids'].astype('str')
    df_options_weeks.reset_index(drop=True,inplace=True)

    return df_options_weeks

def get_race_paris_2024_men_singles(last_week):

    url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id="+last_week+"&category=472&C472FOC=&p=1&ps=100"

    response = requests.get(url)
    content = response.text

    soup = bs.BeautifulSoup(content, 'html.parser')

    table = soup.find('table', attrs={'class':'ruler'})
    table_rows = table.find_all('tr')

    men_singles_ranking = []

    for tr in table_rows:
        cols = tr.find_all('td')
        if len(cols) >= 4:
            #0:rank, 1: previous rank, 3: country 3 letters, 4: player, 6: memberId, 7: Points, 8: Tournaments, 9: Confederation, 10: country
            try:
                previous_rank = cols[1].get('title').split('Previous rank: ')[1]
            except:
                previous_rank = None
            link = cols[4].find('a').get('href')
            men_singles_ranking.append([cols[0].text,previous_rank,cols[3].text,cols[4].text.split('] ')[1],cols[6].text,cols[7].text,cols[8].text,cols[9].text,cols[10].text,link.split('&player=')[1]])
            
            
    df_men_singles_ranking = pd.DataFrame(men_singles_ranking,columns=['Rank','Previous Rank','Short Country','Player','MemberId','Points','Tournaments','Confederation','Country','PlayerId'])

    df_men_singles_ranking['Rank'] = df_men_singles_ranking['Rank'].astype('int')
    df_men_singles_ranking = df_men_singles_ranking.sort_values(by=['Rank'], ascending=True)
    df_men_singles_ranking['Rank'] = df_men_singles_ranking['Rank'].astype('str')
    df_men_singles_ranking.reset_index(drop=True,inplace=True)

    df_race_men_singles = pd.DataFrame(columns=['Race Rank','Country','Player','Points','Tournaments','Country order','Confederation'])

    for i in range(len(df_men_singles_ranking)):
        playerId = df_men_singles_ranking['PlayerId'].iloc[i]

        player_name = df_men_singles_ranking['Player'].iloc[i]

        url_player = 'https://bwf.tournamentsoftware.com/ranking/player.aspx?id='+last_week+'&player='+str(playerId)

        response = requests.get(url_player)
        content = response.text

        soup = bs.BeautifulSoup(content, 'html.parser')

        tables = soup.find_all('table', attrs={'class':'ruler'})

        player_tournaments_results = []

        for table in tables:
            caption = table.find('caption')
            if "Men's Singles results of "+player_name in caption.text:
                table_rows = table.find_all('tr')
                for tr in table_rows:
                    cols = tr.find_all('td')
                    if len(cols)>=6:
                        #0: Tournament, 1: Week, 2: Result, 3: Points, 4: Matches 5: Used for calculation
                        link_to_matchs = cols[4].find('a').get('href')
                        used_for_calculation = len(cols[5].find_all('img'))>=1

                        player_tournaments_results.append([cols[1].text.strip().split('-')[0],cols[1].text.strip().split('-')[1],cols[0].text.strip(),cols[2].text.strip(),cols[3].text.strip(),used_for_calculation,link_to_matchs])

        df_player_tournaments_results = pd.DataFrame(player_tournaments_results,columns=['Year','Week','Tournament','Result','Points','Calculation','Matches'])

        df_player_tournaments_results['Week'] = df_player_tournaments_results['Week'].astype('int')
        df_player_tournaments_results['Points'] = df_player_tournaments_results['Points'].astype('int')
        df_player_tournaments_results = df_player_tournaments_results.sort_values(by=['Week'], ascending=True)
        df_player_tournaments_results.reset_index(drop=True,inplace=True)
        df_player_tournaments_results = df_player_tournaments_results[(df_player_tournaments_results['Year'] == '2023') | (df_player_tournaments_results['Year'] == '2024')]
        df_player_tournaments_results = df_player_tournaments_results[df_player_tournaments_results['Week']>=18]
        
        
        df_race_men_singles.loc[len(df_race_men_singles)] = [i+1,df_men_singles_ranking['Country'].iloc[i],df_men_singles_ranking['Player'].iloc[i],df_player_tournaments_results['Points'].sum(),len(df_player_tournaments_results.index),'',df_men_singles_ranking['Confederation'].iloc[i]]

    df_race_men_singles.sort_values('Points',ascending=False,inplace=True)
    df_race_men_singles.reset_index(drop=True,inplace=True)
    df_race_men_singles['Race Rank'] = [i for i in range(1,len(df_race_men_singles)+1)]

    df_race_men_singles.to_excel('./RACE_TO_PARIS/Men_Singles_Race_to_Paris.xlsx',index=False)

    return df_race_men_singles


