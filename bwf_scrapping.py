#Module qui regroupe l'ensemble des fonctions pour scrapper les infos utiles sur le site BWF Software Tournament
import bs4 as bs
import urllib.request
import pandas as pd
import numpy as np

from simulation import *


def get_tournament_list_men_singles(playerId,player_name,week_id):
    url_player = 'https://bwf.tournamentsoftware.com/ranking/player.aspx?id='+week_id+'&player='+str(playerId)

    source = urllib.request.urlopen(url_player).read()
    soup = bs.BeautifulSoup(source,'lxml')

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

    source = urllib.request.urlopen(url_player).read()
    soup = bs.BeautifulSoup(source,'lxml')

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

    source = urllib.request.urlopen(url_player).read()
    soup = bs.BeautifulSoup(source,'lxml')

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

    source = urllib.request.urlopen(url_player).read()
    soup = bs.BeautifulSoup(source,'lxml')

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

    source = urllib.request.urlopen(url_player).read()
    soup = bs.BeautifulSoup(source,'lxml')

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

    source = urllib.request.urlopen(url_world_ranking).read()
    soup = bs.BeautifulSoup(source,'lxml')

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