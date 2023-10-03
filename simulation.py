#Module qui regroupe l'ensemble des fonctions pour simuler la saison
import pandas as pd
import numpy as np
import plotly.graph_objects as go

#On initialise les dataframe avec la liste des tournois
df_2022_tournaments_list = pd.read_excel("./BWF_TOURNAMENTS/2022_BWF_TOURNAMENTS_LIST_WITH_DISTRIBUTION_AND_KEY_DATES_AND_MATCHING.xlsx")
df_2023_tournaments_list = pd.read_excel("./BWF_TOURNAMENTS/2023_BWF_TOURNAMENTS_LIST_WITH_DISTRIBUTION_AND_KEY_DATES_AND_MATCHING.xlsx")
#Dataframe avec estimation de classement
df_estimation_ranking_all = pd.read_excel("./averaged_points_ranking_all.xlsx",['men_singles','women_singles','men_doubles','women_doubles','mixed_doubles'])

#Fonction qui va estimer le classement du joueur en fonction des classements des années 2018,2019,2020,2023
def estimate_ranking(total_points,type_ranking,df_world_ranking_at_week):

    list_ranking = df_world_ranking_at_week['Points'].values
    closest_value = min(list_ranking, key=lambda x:abs(x-total_points))
    ranking = (np.where(list_ranking == closest_value)[0]+1)[0]

    if ranking<=10:
        distance_to_rank = round(list_ranking[0]-total_points)
        distance_to_rank = 'Gap to Top 1 : '+str(distance_to_rank)+' pts'
    elif ranking>10 and ranking<=20:
        distance_to_rank = round(list_ranking[9]-total_points)
        distance_to_rank = 'Gap to Top 10 : '+str(distance_to_rank)+' pts'
    elif ranking>20 and ranking<=30:
        distance_to_rank = round(list_ranking[19]-total_points)
        distance_to_rank = 'Gap to Top 20 : '+str(distance_to_rank)+' pts'
    elif ranking>30 and ranking<=50:
        distance_to_rank = round(list_ranking[29]-total_points)
        distance_to_rank = 'Gap to Top 30 : '+str(distance_to_rank)+' pts'
    elif ranking>50 and ranking<=70:
        distance_to_rank = round(list_ranking[49]-total_points)
        distance_to_rank = 'Gap to Top 50 : '+str(distance_to_rank)+' pts'
    elif ranking>70 and ranking<=100:
        distance_to_rank = round(list_ranking[69]-total_points)
        distance_to_rank = 'Gap to Top 70 : '+str(distance_to_rank)+' pts'
    elif ranking>100:
        distance_to_rank = round(list_ranking[99]-total_points)
        distance_to_rank = 'Gap to Top 100 : '+str(distance_to_rank)+' pts'

    return str(max(1,ranking-2))+"-"+str(ranking+2), distance_to_rank

#Fonction qui va renvoyer une liste de couleurs, une liste de tailles et une liste de formes pour les markers 
def get_viz_settings(df_ranking_over_weeks,year):
    markers_colors = []
    markers_sizes = []
    markers_shapes = []
    if year=='2022':
        df_tournaments_list = df_2022_tournaments_list
    elif year=='2023':
        df_tournaments_list = df_2023_tournaments_list

    for index, tournament_name in enumerate(df_ranking_over_weeks['Tournament']):
        if tournament_name=='No Tournament':
            if year == '2022':
                markers_colors.append('grey')
                markers_sizes.append(6)
                markers_shapes.append('circle')
            elif year == '2023':
                markers_colors.append('lightskyblue')
                markers_sizes.append(6)
                markers_shapes.append('circle')
        else:
            details_tournament = df_tournaments_list[df_tournaments_list['Tournament']==tournament_name]
            #Tournoi par équipe:
            if details_tournament['Team'].iloc[0]==1:
                markers_colors.append('purple')
                markers_shapes.append('hexagram')
            else:
                #Grade 1 tournaments
                if details_tournament[1].iloc[0]==13000:
                    markers_colors.append('gold')
                    markers_shapes.append('star')
                #Grade 2 tournaments
                elif details_tournament[1].iloc[0] in [12000,11000,9200]:
                    markers_colors.append('gold')
                    markers_shapes.append('hexagon')
                elif details_tournament[1].iloc[0] in [7000,5500]:
                    markers_colors.append('lightgrey')
                    markers_shapes.append('hexagon')
                #Grade 3 tournaments
                elif details_tournament[1].iloc[0] in [4000,2500,1700]:
                    markers_colors.append('sandybrown')
                    markers_shapes.append('star-diamond')

            #On va associer la taille au nombre de points gagné:
            points_earned = df_ranking_over_weeks['Points Earned'].iloc[index]
            if points_earned<1000:
                markers_sizes.append(7)
            elif points_earned>=1000 and points_earned<=2500:
                markers_sizes.append(9)
            elif points_earned>2500 and points_earned<=4000:
                markers_sizes.append(10)
            elif points_earned>4000 and points_earned<=5500:
                markers_sizes.append(11)
            elif points_earned>5500 and points_earned<=7000:
                markers_sizes.append(12)
            elif points_earned>7000 and points_earned<=9200:
                markers_sizes.append(13)
            elif points_earned>9200:
                markers_sizes.append(14)

    return markers_colors, markers_sizes, markers_shapes

#Fonction qui va renvoyer une liste du diminutif des catégories de tournois
def get_short_name_categories(df_tournaments_list):
    short_name_categories = []
    for i in range(len(df_tournaments_list)):
        if df_tournaments_list['Category'].iloc[i]=='HSBC BWF World Tour Super 1000':
            short_name_categories.append("S1000")
        elif df_tournaments_list['Category'].iloc[i]=='HSBC BWF World Tour Super 750':
            short_name_categories.append("S750")
        elif df_tournaments_list['Category'].iloc[i]=='HSBC BWF World Tour Super 500':
            short_name_categories.append("S500")
        elif df_tournaments_list['Category'].iloc[i]=='HSBC BWF World Tour Super 300':
            short_name_categories.append("S300")
        elif df_tournaments_list['Category'].iloc[i]=='BWF Tour Super 100':
            short_name_categories.append("S100")
        elif df_tournaments_list['Category'].iloc[i]=='International Challenge':
            short_name_categories.append("IC")
        elif df_tournaments_list['Category'].iloc[i]=='International Series':
            short_name_categories.append("IS")
        elif df_tournaments_list['Category'].iloc[i]=='Future Series':
            short_name_categories.append("FS")
        else:
            short_name_categories.append("")


    return short_name_categories
        
        
#Fonction qui va catégoriser les tournois
def get_category_tournaments(df_player_tournaments_results,df_tournaments_list):
    
    for i in range(len(df_player_tournaments_results)):
        #On regarde si les tournois sont par equipe
        df_tournament_details = df_tournaments_list[df_tournaments_list['Tournament']==df_player_tournaments_results['Tournament'].iloc[i]]
        df_player_tournaments_results.loc[i,'Team'] = df_tournament_details['Team'].values[0]
        df_player_tournaments_results.loc[i,'Matching Id'] = df_tournament_details['Matching Id'].values[0]
        #On regarde si ce sont des jeux continentaux
        if df_tournament_details['Category'].iloc[0]=='Continental Individual Games' or df_tournament_details['Category'].iloc[0]=='Multi-Sport Games':
            df_player_tournaments_results.loc[i,'Continental Games'] = 1
        else:
            df_player_tournaments_results.loc[i,'Continental Games'] = 0
        #On regarde si ce sont des championnats continentaux
        if df_tournament_details['Category'].iloc[0]=='Continental Individual Championships':
            df_player_tournaments_results.loc[i,'Continental Championships'] = 1
        else:
            df_player_tournaments_results.loc[i,'Continental Championships'] = 0
        #On regarde si c'est les championnats du monde
        if "World Championships" in df_tournament_details['Tournament'].iloc[0]:
            df_player_tournaments_results.loc[i,'World Championships'] = 1
        else:
            df_player_tournaments_results.loc[i,'World Championships'] = 0

    df_player_tournaments_results['Team'] = df_player_tournaments_results['Team'].astype('int')
    df_player_tournaments_results['Continental Games'] = df_player_tournaments_results['Continental Games'].astype('int')
    df_player_tournaments_results['Continental Championships'] = df_player_tournaments_results['Continental Championships'].astype('int')
    df_player_tournaments_results['World Championships'] = df_player_tournaments_results['World Championships'].astype('int')

    return df_player_tournaments_results

#Fonction qui renvoie la liste des tournois avec un attribut "Calculation"=True pour les tournois qui comptent pour le classement
def get_world_ranking(df_player_tournaments_results):
    #On les classe par ordre de points
    df_player_tournaments_results = df_player_tournaments_results.sort_values(by=['Points'], ascending=False)
    #On reset les indices
    df_player_tournaments_results.reset_index(drop=True,inplace=True)
    #Initialisation 
    df_player_tournaments_results['Calculation']=False
    df_tournaments_for_calculation = df_player_tournaments_results.iloc[0:1]
    #On parcourt tous les tournois et on vérifie qu'ils respectent les conditions pour le classement mondial
    for i in range(1,len(df_player_tournaments_results)):
        if len(df_tournaments_for_calculation)<10:
            df_tournaments_for_calculation = pd.concat([df_tournaments_for_calculation,df_player_tournaments_results.iloc[i:i+1]])
            #On regarde si un tournoi a été rejoué avant 52 semaines
            matching_id = df_player_tournaments_results['Matching Id'].iloc[i:i+1].values[0]
            if matching_id!=0 and df_tournaments_for_calculation['Matching Id'].value_counts()[matching_id]>1:
                #On garde le plus récent:
                index_matching_tournament = df_tournaments_for_calculation.index[df_tournaments_for_calculation['Matching Id']==matching_id].tolist()
                if df_tournaments_for_calculation.loc[index_matching_tournament[0],"Week"]<=df_tournaments_for_calculation.loc[index_matching_tournament[1],"Week"]:
                    df_tournaments_for_calculation.drop(index_matching_tournament[1], inplace=True)
                else:
                    df_tournaments_for_calculation.drop(index_matching_tournament[0], inplace=True)

            #On regarde si il y a deux tournois par equipe
            if df_tournaments_for_calculation['Team'].sum()>1:
                index_team = df_tournaments_for_calculation.index[df_tournaments_for_calculation['Team']==1].tolist()
                if df_tournaments_for_calculation.loc[index_team[0],"Points"]>=df_tournaments_for_calculation.loc[index_team[1],"Points"]:
                    df_tournaments_for_calculation.drop(index_team[1], inplace=True)
                else:
                    df_tournaments_for_calculation.drop(index_team[0], inplace=True)

            #On regarde si il y a deux jeux continentaux
            if df_tournaments_for_calculation['Continental Games'].sum()>1:
                index_cont_games = df_tournaments_for_calculation.index[df_tournaments_for_calculation['Continental Games']==1].tolist()
                if df_tournaments_for_calculation.loc[index_cont_games[0],"Points"]>=df_tournaments_for_calculation.loc[index_cont_games[1],"Points"]:
                    df_tournaments_for_calculation.drop(index_cont_games[0], inplace=True)
                else:
                    df_tournaments_for_calculation.drop(index_cont_games[1], inplace=True)

            #On regarde si il y a deux championnats continentaux
            if df_tournaments_for_calculation['Continental Championships'].sum()>1:
                index_cont_champ = df_tournaments_for_calculation.index[df_tournaments_for_calculation['Continental Championships']==1].tolist()
                if df_tournaments_for_calculation.loc[index_cont_champ[0],"Points"]>=df_tournaments_for_calculation.loc[index_cont_champ[1],"Points"]:
                    df_tournaments_for_calculation.drop(index_cont_champ[0], inplace=True)
                else:
                    df_tournaments_for_calculation.drop(index_cont_champ[1], inplace=True)

            #On regarde si il y a deux championnats du monde       
            if df_tournaments_for_calculation['World Championships'].sum()>1:
                index_world_champ = df_tournaments_for_calculation.index[df_tournaments_for_calculation['World Championships']==1].tolist()
                if df_tournaments_for_calculation.loc[index_world_champ[0],"Points"]>=df_tournaments_for_calculation.loc[index_world_champ[1],"Points"]:
                    df_tournaments_for_calculation.drop(index_world_champ[0], inplace=True)
                else:
                    df_tournaments_for_calculation.drop(index_world_champ[1], inplace=True)
    
    #On récupère les indices des tournois pour le calcul du classement
    index_tournaments_for_calculation = df_tournaments_for_calculation.index
    for idx in index_tournaments_for_calculation:
        df_player_tournaments_results.loc[idx,"Calculation"] = True
        
    return df_player_tournaments_results

#Fonction qui va renvoyer l'évolution du classement au fur et à mesure des semaines sans simulation, qui sera utilisé pour la viz'
def get_ranking_over_weeks(df_player_tournaments_results,type_ranking,df_world_ranking_at_week):
    #On récupère les catégories de tournois
    df_player_tournaments_results = get_category_tournaments(df_player_tournaments_results,df_2022_tournaments_list)
    df_player_tournaments_results = df_player_tournaments_results.sort_values(by=['Week'], ascending=True)

    #On va trouver la semaine la plus élevée parmis les simulations (resp. la plus petite)
    max_week =  df_player_tournaments_results['Week'].max()
    min_week =  df_player_tournaments_results.loc[df_player_tournaments_results['Calculation']==True,'Week'].min()

    total_points = df_player_tournaments_results.loc[df_player_tournaments_results['Calculation']==True,'Points'].sum()

    #On va calculer le nombre de points au fur et à mesure des semaines 
    points = [0]*52

    df_week_ranking = pd.DataFrame(columns = ['Week','Tournament','Result','Points Earned','Total Ranking Points','Estimated Ranking','Points to Top'])


    for week in range(1,min_week+1):
        points[week-1] = total_points
        estimate_rank, distance_to_rank = estimate_ranking(points[week-1],type_ranking,df_world_ranking_at_week)
        df_week_ranking.loc[len(df_week_ranking)]=[week,"No Tournament","",0,points[week-1],estimate_rank,distance_to_rank]
            
    for week in range(min_week+1,max_week+2):
        df_player_tournaments_results_simulated = df_player_tournaments_results[df_player_tournaments_results['Week']>=week]
        df_player_tournaments_results_simulated = get_world_ranking(df_player_tournaments_results_simulated)
        total_points = df_player_tournaments_results_simulated.loc[df_player_tournaments_results_simulated['Calculation']==True,'Points'].sum()
        points[week-1] = total_points
        estimate_rank, distance_to_rank = estimate_ranking(points[week-1],type_ranking,df_world_ranking_at_week)
        df_week_ranking.loc[len(df_week_ranking)]=[week,"No Tournament","",0,points[week-1],estimate_rank,distance_to_rank]
        
        df_week = df_player_tournaments_results[df_player_tournaments_results["Week"]==week-1]
        if len(df_week)>0:
            df_week_ranking.loc[week-2,'Tournament']=df_week['Tournament'].values[0]
            df_week_ranking.loc[week-2,'Result']=df_week['Result'].values[0]
            df_week_ranking.loc[week-2,'Points Earned']=df_week['Points'].values[0]
            
    for week in range(max_week+2,53):
        points[week-1] = 0
        estimate_rank, distance_to_rank = estimate_ranking(points[week-1],type_ranking,df_world_ranking_at_week)
        df_week_ranking.loc[len(df_week_ranking)]=[week,"No Tournament","",0,points[week-1],estimate_rank,distance_to_rank]

    return df_week_ranking

#Fonction qui va renvoyer une figure plotly pour la visualisation de l'évolution du ranking
def get_viz_ranking(df_week_ranking,year,name):
    markers_colors, markers_sizes, markers_shapes = get_viz_settings(df_week_ranking,year)

    custom_data = np.stack((df_week_ranking['Tournament'],df_week_ranking['Result'],df_week_ranking['Points Earned'],df_week_ranking['Estimated Ranking'],df_week_ranking['Points to Top']), axis=-1)

    fig = go.Figure(data=go.Scatter(x=df_week_ranking['Week'],
                                y=df_week_ranking['Total Ranking Points'],
                                customdata=custom_data,
                                name=name,
                                marker_color=markers_colors,
                                marker_size=markers_sizes,
                                marker_symbol = markers_shapes,
                                marker_opacity = 0.8,
                                line_color="rgba(182, 208, 226,0.4)",
                                fill="tozeroy",
                                fillcolor="rgba(182, 208, 226,0.2)"))

    fig.update_layout(title='Ranking Points Over Weeks',
                    xaxis_title="Week",
                    yaxis_title="Ranking Points",
                    hovermode=None
                    )

    fig.update_traces(mode="markers+lines",
                    hovertemplate = '<b>Week %{x}:</b>'+
                        '<br><b>Total Ranking Points</b>: %{y}'+
                        '<br><b>Estimated Ranking: %{customdata[3]}</b>'+
                        '<br><b>%{customdata[4]}</b>'+
                        '<br>'+
                        '<br>Tournament: %{customdata[0]}'+
                        '<br>Result: %{customdata[1]}'+
                        '<br>Points Earned: %{customdata[2]}'
                        )

    return fig

#Fonction qui va renvoyer l'évolution du classement au fur et à mesure des semaines sans simulation, qui sera utilisé pour la viz'
def get_ranking_over_weeks_simulated(df_player_tournaments_results,df_tournament_simulated,df_week_ranking,type_ranking,df_world_ranking_at_week):
    #On regarde la catégorie du tournois
    df_tournament_simulated = df_tournament_simulated.sort_values(by=['Week'], ascending=True)
    df_tournament_simulated.reset_index(drop=True,inplace=True)
    df_tournament_simulated = get_category_tournaments(df_tournament_simulated,df_2023_tournaments_list)

    #On va trouver la semaine la plus élevée parmis les simulations (resp. la plus petite)
    max_week = df_tournament_simulated['Week'].max()
    min_week = df_tournament_simulated['Week'].min()

    #On va calculer le nombre de points au fur et à mesure des semaines 
    points = [0]*52

    df_week_ranking_simulated = pd.DataFrame(columns = ['Week','Tournament','Result','Points Earned','Total Ranking Points','Estimated Ranking','Points to Top'])


    #On a le même nombre de points que sans les tournois ajoutés jusqu'à la semaine du premier tournoi ajouté
    for week in range(1,min_week+1):
        points[week-1] = df_week_ranking['Total Ranking Points'].iloc[week-1]
        estimate_rank, distance_to_rank = estimate_ranking(points[week-1],type_ranking,df_world_ranking_at_week)
        df_week_ranking_simulated.loc[len(df_week_ranking_simulated)]=[week,"No Tournament","",0,points[week-1],estimate_rank,distance_to_rank]

    #On simule chaque semaine et on récupère le nombre de points après chaque semaine
    for week in range(min_week+1,53):
        df_player_tournaments_results_simulated = pd.concat([df_player_tournaments_results[df_player_tournaments_results['Week']>=week],df_tournament_simulated[df_tournament_simulated['Week']<week]])
        df_player_tournaments_results_simulated = get_world_ranking(df_player_tournaments_results_simulated)
        total_points = df_player_tournaments_results_simulated.loc[df_player_tournaments_results_simulated['Calculation']==True,'Points'].sum()
        points[week-1] = total_points
        estimate_rank, distance_to_rank = estimate_ranking(points[week-1],type_ranking,df_world_ranking_at_week)
        df_week_ranking_simulated.loc[len(df_week_ranking_simulated)]=[week,"No Tournament","",0,points[week-1],estimate_rank,distance_to_rank]
        
        df_week = df_player_tournaments_results_simulated[df_player_tournaments_results_simulated["Week"]==week-1]
        #On récupère le nom du tournois ainsi que les points remportés et le résultat
        if len(df_week)>0:
            df_week_ranking_simulated.loc[week-2,'Tournament']=df_week['Tournament'].values[0]
            df_week_ranking_simulated.loc[week-2,'Result']=df_week['Result'].values[0]
            df_week_ranking_simulated.loc[week-2,'Points Earned']=df_week['Points'].values[0]
    
    # #On ajoute le nom des tournois le résultat et les points pour les tournois de l'année précédente
    # for week in range(max_week+1,53):
    #     df_week_ranking_simulated.loc[week-1,'Tournament']=df_week_ranking['Tournament'].iloc[week-1]
    #     df_week_ranking_simulated.loc[week-1,'Result']=df_week_ranking['Result'].iloc[week-1]
    #     df_week_ranking_simulated.loc[week-1,'Points Earned']=df_week_ranking['Points Earned'].iloc[week-1]

    return df_week_ranking_simulated


#Fonction qui va ajouter une trace à la figure plotly pour la visualisation de l'évolution du ranking avec la simulation
def get_viz_ranking_simulated(df_week_ranking_simulated,fig,year,name):
    markers_colors, markers_sizes, markers_shapes = get_viz_settings(df_week_ranking_simulated,year)

    custom_data_simulated = np.stack((df_week_ranking_simulated['Tournament'],df_week_ranking_simulated['Result'],df_week_ranking_simulated['Points Earned'],df_week_ranking_simulated['Estimated Ranking'],df_week_ranking_simulated['Points to Top']), axis=-1)

    fig.add_trace(go.Scatter(x=df_week_ranking_simulated['Week'],
                                    y=df_week_ranking_simulated['Total Ranking Points'],
                                    customdata=custom_data_simulated,
                                    name=name,
                                    marker_color=markers_colors,
                                    marker_size=markers_sizes,
                                    marker_symbol = markers_shapes,
                                    marker_opacity = 1,
                                    #line_color="rgba(155,48,255, 0.4)",
                                    fill="tozeroy",
                                    fillcolor="rgba(182, 208, 226,0.1)"))

    fig.update_traces(mode="markers+lines",
                        hovertemplate = '<b>Week %{x}:</b>'+
                        '<br><b>Total Ranking Points</b>: %{y}'+
                        '<br><b>Estimated Ranking: %{customdata[3]}</b>'+
                        '<br><b>%{customdata[4]}</b>'+
                        '<br>'+
                        '<br>Tournament: %{customdata[0]}'+
                        '<br>Result: %{customdata[1]}'+
                        '<br>Points Earned: %{customdata[2]}'
                        )

    return fig