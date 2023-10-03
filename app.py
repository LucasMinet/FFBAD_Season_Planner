import streamlit as st
import pandas as pd
import numpy as np

from bwf_scrapping import *
from simulation import *


#Initialisation des joueurs / On garde ceux avec plus de 1000pts au WR
#Simple Hommes
df_french_players_ms = pd.read_excel('./FRANCE_PLAYERS/MEN_SINGLES_FRANCE_PLAYERS.xlsx')
df_french_players_ms = df_french_players_ms[df_french_players_ms['Points']>=1000]
#Simple Femmes
df_french_players_ws = pd.read_excel('./FRANCE_PLAYERS/WOMEN_SINGLES_FRANCE_PLAYERS.xlsx')
df_french_players_ws = df_french_players_ws[df_french_players_ws['Points']>=1000]
#Double Hommes
df_french_players_md = pd.read_excel('./FRANCE_PLAYERS/MEN_DOUBLES_FRANCE_PLAYERS.xlsx')
df_french_players_md = df_french_players_md[df_french_players_md['Points']>=1000]
#Double Femmes
df_french_players_wd = pd.read_excel('./FRANCE_PLAYERS/WOMEN_DOUBLES_FRANCE_PLAYERS.xlsx')
df_french_players_wd = df_french_players_wd[df_french_players_wd['Points']>=1000]
#Double Mixte
df_french_players_xd = pd.read_excel('./FRANCE_PLAYERS/MIXED_DOUBLES_FRANCE_PLAYERS.xlsx')
df_french_players_xd = df_french_players_xd[df_french_players_xd['Points']>=1000]

if 'launch_simulation' not in st.session_state or 'selected_players' not in st.session_state or 'selected_week_simulation' not in st.session_state:
    st.session_state['launch_simulation'] = False
    #Sauvegarde le joueur qui a été choisi
    st.session_state['selected_players'] = ""
    #Sauvegarde la semaine qui est choisie
    st.session_state['selected_week_simulation'] = ""

#Sidebar
with st.sidebar:
    #Titre de l'application
    st.title("Season Planner")

    #Filtres pour la liste déroulante des joueurs
    category_filter = st.radio(label="Filters",options=["Men's Singles","Women's Singles","Men's Doubles","Women's Doubles","Mixed Doubles"],horizontal=True)

    #On affiche la liste déroulante des joueurs en fonction du choix précédent
    if category_filter=="Men's Singles":
        #Liste déroulante pour la sélection des joueurs/paires
        selected_players = st.selectbox(label="Choose a Player",options=df_french_players_ms['Player'])
    elif category_filter=="Women's Singles":
        #Liste déroulante pour la sélection des joueurs/paires
        selected_players = st.selectbox(label="Choose a Player",options=df_french_players_ws['Player'])
    elif category_filter=="Men's Doubles":
        #Liste déroulante pour la sélection des joueurs/paires
        options_md = df_french_players_md['Player1'].values + " / " + df_french_players_md["Player2"]
        selected_players = st.selectbox(label="Choose a Pair",options=options_md)
    elif category_filter=="Women's Doubles":
        #Liste déroulante pour la sélection des joueurs/paires
        options_wd = df_french_players_wd['Player1'].values + " / " + df_french_players_wd["Player2"]
        selected_players = st.selectbox(label="Choose a Pair",options=options_wd)
    elif category_filter=="Mixed Doubles":
        #Liste déroulante pour la sélection des joueurs/paires
        options_xd = df_french_players_xd['Player1'].values + " / " + df_french_players_xd["Player2"]
        selected_players = st.selectbox(label="Choose a Pair",options=options_xd)

    #On choisi la semaine de début de simulation
    if 'df_options_weeks' not in st.session_state:
        df_options_weeks = get_world_ranking_weeks()
        st.session_state['df_options_weeks'] = df_options_weeks
        
    else:
        df_options_weeks = st.session_state['df_options_weeks']
    
    options_weeks = ["Week "+str(i+1)+" -> "+df_options_weeks['options_weeks'].values[i] for i in range(len(df_options_weeks['options_weeks'])-1,-1,-1)]
    week_selected = st.selectbox("Choose Starting Week for Simulation",options=options_weeks)
    number_week_simulation = week_selected.split(' -> ')[0].split(' ')[1]
    selected_week_simulation = week_selected.split(' -> ')[1]


    #On crée un boutton qui va permettre de débuter la simulation
    button_simulation = st.button("Start the simulation")

    st.image('./assets/logo_FFBaD.png',width=120)

    if st.session_state['selected_players'] != selected_players or st.session_state['selected_week_simulation'] != selected_week_simulation:
        #Reset l'état de l'apllication lorsqu'on change de simulation
        st.session_state['launch_simulation'] = False
        st.session_state['df_player_tournament_results']=None
        st.session_state['df_ranking_over_weeks']=None
        st.session_state['df_ranking_over_weeks_simulated']=None
        st.session_state['figure_ranking_chart']=None
        st.session_state['figure_ranking_chart_simulated']=None
        st.session_state['df_tournament_simulated'] = pd.DataFrame(columns=["Year","Week","Tournament","Result","Points","Calculation","Matches","Team","Matching Id","Continental Games","Continental Championships","World Championships"])
        st.session_state['previous_df_tournament_simulated'] = pd.DataFrame(columns=["Year","Week","Tournament","Result","Points","Calculation","Matches","Team","Matching Id","Continental Games","Continental Championships","World Championships"])


tab1, tab2, tab3 = st.tabs(["Ranking Simulation", "Players Comparisons", "Tournaments Calendar"])

with tab1:
    #On Crée la page principale
    title_main = st.title("Please Start a Simulation")

    #On démarre la simulation jusqu'à obtenir le graphique
    if button_simulation and st.session_state['launch_simulation']==False:
        df_options_weeks = st.session_state['df_options_weeks']
        #On récupère les infos sur les resultats en tournois du joueur/paire
        if category_filter=="Men's Singles":
            df_players_selected = df_french_players_ms[df_french_players_ms["Player"]==selected_players]
            playerId = df_players_selected['PlayerId'].iloc[0]
            df_player_tournament_results = get_tournament_list_men_singles(playerId,selected_players,df_options_weeks['weeks_ids'].iloc[0])
            type_ranking = 'men_singles'

        elif category_filter=="Women's Singles":
            df_players_selected = df_french_players_ws[df_french_players_ws["Player"]==selected_players]
            playerId = df_players_selected['PlayerId'].iloc[0]
            df_player_tournament_results = get_tournament_list_women_singles(playerId,selected_players,df_options_weeks['weeks_ids'].iloc[0])
            type_ranking = 'women_singles'

        elif category_filter=="Men's Doubles":
            df_players_selected = df_french_players_md[(df_french_players_md["Player1"]==selected_players.split(" / ")[0]) & (df_french_players_md["Player2"]==selected_players.split(" / ")[1])]
            playerId = df_players_selected['PlayerId1'].iloc[0]
            df_player_tournament_results = get_tournament_list_men_doubles(playerId,selected_players.split(" / ")[0],selected_players.split(" / ")[1],df_options_weeks['weeks_ids'].iloc[0])
            type_ranking = 'men_doubles'

        elif category_filter=="Women's Doubles":
            df_players_selected = df_french_players_wd[(df_french_players_wd["Player1"]==selected_players.split(" / ")[0]) & (df_french_players_wd["Player2"]==selected_players.split(" / ")[1])]
            playerId = df_players_selected['PlayerId1'].iloc[0]
            df_player_tournament_results = get_tournament_list_women_doubles(playerId,selected_players.split(" / ")[0],selected_players.split(" / ")[1],df_options_weeks['weeks_ids'].iloc[0])
            type_ranking = 'women_doubles'

        elif category_filter=="Mixed Doubles":
            df_players_selected = df_french_players_xd[(df_french_players_xd["Player1"]==selected_players.split(" / ")[0]) & (df_french_players_xd["Player2"]==selected_players.split(" / ")[1])]
            playerId = df_players_selected['PlayerId1'].iloc[0]
            df_player_tournament_results = get_tournament_list_mixed_doubles(playerId,selected_players.split(" / ")[0],selected_players.split(" / ")[1],df_options_weeks['weeks_ids'].iloc[0])
            type_ranking = 'mixed_doubles'

        #On sauvegarde tout en cache
        st.session_state['df_player_tournament_results']=df_player_tournament_results
        st.session_state['launch_simulation']=True
        st.session_state['selected_players']=selected_players
        st.session_state['type_ranking']=type_ranking
        st.session_state['selected_week_simulation'] = selected_week_simulation
        #On récupère l'évolution du classement sur chaque semaine...
        first_week_2023 = df_options_weeks['weeks_ids'].iloc[0]
        #On récupère le classement mondial
        df_world_ranking_at_week = get_world_ranking_at_week(first_week_2023,type_ranking)
        st.session_state['df_ranking_over_weeks']=get_ranking_over_weeks(df_player_tournament_results,type_ranking,df_world_ranking_at_week)

        #Si la semaine de départ est différente de la semaine 1:
        if selected_week_simulation != df_options_weeks['options_weeks'].iloc[0]:
            details_week = df_options_weeks[df_options_weeks['options_weeks']==selected_week_simulation]
            week_id = details_week['weeks_ids'].iloc[0]
            if type_ranking == "men_singles":
                df_player_tournament_results_from_starting_week=get_tournament_list_men_singles(playerId,selected_players,week_id)
            elif type_ranking == "women_singles":
                df_player_tournament_results_from_starting_week=get_tournament_list_women_singles(playerId,selected_players,week_id)
            elif type_ranking == "men_doubles":
                df_player_tournament_results_from_starting_week = get_tournament_list_men_doubles(playerId,selected_players.split(" / ")[0],selected_players.split(" / ")[1],week_id)
            elif type_ranking == "women_doubles":
                df_player_tournament_results_from_starting_week = get_tournament_list_women_doubles(playerId,selected_players.split(" / ")[0],selected_players.split(" / ")[1],week_id)
            elif type_ranking == "mixed_doubles":
                df_player_tournament_results_from_starting_week = get_tournament_list_mixed_doubles(playerId,selected_players.split(" / ")[0],selected_players.split(" / ")[1],week_id)
            #On sauvegarde tout en cache
            df_player_tournament_results_from_starting_week = df_player_tournament_results_from_starting_week[df_player_tournament_results_from_starting_week['Year']=='2023']
            
            if len(df_player_tournament_results_from_starting_week)>0:
                df_player_tournament_results_from_starting_week["Matching Id"]=0
                df_player_tournament_results_from_starting_week["Team"]=0
                df_player_tournament_results_from_starting_week["Continental Games"]=0
                df_player_tournament_results_from_starting_week["Continental Championships"]=0
                df_player_tournament_results_from_starting_week["World Championships"]=0
            
                st.session_state['df_tournament_simulated'] = df_player_tournament_results_from_starting_week
                st.session_state['week_id'] = week_id
                #On récupère l'évolution du classement sur chaque semaine
                df_ranking_over_weeks = st.session_state['df_ranking_over_weeks']
                #On récupère le classement mondial
                df_world_ranking_at_week = get_world_ranking_at_week(week_id,type_ranking)
                st.session_state['get_world_ranking_at_week']=df_world_ranking_at_week
                df_ranking_over_weeks_simulated = get_ranking_over_weeks_simulated(df_player_tournament_results,df_player_tournament_results_from_starting_week,df_ranking_over_weeks,type_ranking,df_world_ranking_at_week)
                #On sauvegarde l'état
                st.session_state['df_ranking_over_weeks_simulated'] = df_ranking_over_weeks_simulated
            #On crée la figure initiale pour 2022
            df_ranking_over_weeks = st.session_state['df_ranking_over_weeks']
            figure_ranking_chart = get_viz_ranking(df_ranking_over_weeks,'2022',name="2022 Ranking")
            st.session_state['figure_ranking_chart'] = figure_ranking_chart


    # #On ajoute le tournois et on fait la simulation jusqu'à obtenir le graphique
    def add_simulated_tournament():
        df_tournament_simulated = st.session_state['df_tournament_simulated']
        #On ajoute le tournois dans un dataframe pour la simulation
        details_tournament = df_2023_tournaments_list[df_2023_tournaments_list['Tournament']==tournament_name]
        #Si on a un tournoi par équipe:
        if details_tournament['Team'].iloc[0]==1:
            result = "1"
            points_earned = points_earned_tournament
            tournament_week = details_tournament['Week'].values[0]
            matching_id = details_tournament['Matching Id'].values[0]
            df_tournament_simulated.loc[len(df_tournament_simulated)]= [2023,int(tournament_week),tournament_name,result,points_earned,False,"",0,matching_id,0,0,0]

        else:
            points_earned = details_tournament[result_tournament].values[0]
            tournament_week = details_tournament['Week'].values[0]
            matching_id = details_tournament['Matching Id'].values[0]
            df_tournament_simulated.loc[len(df_tournament_simulated)]= [2023,int(tournament_week),tournament_name,result_tournament,points_earned,False,"",0,matching_id,0,0,0]

        #On récupère l'évolution du classement sur chaque semaine
        df_player_tournament_results = st.session_state['df_player_tournament_results']
        df_ranking_over_weeks = st.session_state['df_ranking_over_weeks']
        type_ranking = st.session_state['type_ranking']
        #On récupère le classement mondial
        df_world_ranking_at_week = st.session_state['get_world_ranking_at_week']
        df_ranking_over_weeks_simulated = get_ranking_over_weeks_simulated(df_player_tournament_results,df_tournament_simulated,df_ranking_over_weeks,type_ranking,df_world_ranking_at_week)
        #On sauvegarde l'état
        st.session_state['df_tournament_simulated'] = df_tournament_simulated
        st.session_state['df_ranking_over_weeks_simulated'] = df_ranking_over_weeks_simulated

    #Si la simulation est lancée
    if st.session_state['launch_simulation']==True:
        title_main.title("Ranking Simulation of "+selected_players)

        df_tournament_simulated = st.session_state['df_tournament_simulated']
        #On ne veut pas avoir la possibilité de choisir deux tournois sur la même semaine
        list_week_to_exclude = [df_tournament_simulated['Week'].iloc[i] for i in range(len(df_tournament_simulated))]
        df_2023_tournaments_list_filtered = df_2023_tournaments_list[~df_2023_tournaments_list['Week'].isin(list_week_to_exclude)]
        df_2023_tournaments_list_filtered = df_2023_tournaments_list_filtered.sort_values(by=['Week'], ascending=True)
        #Multi choix pour filtrer les tournois
        filter_tournaments = st.multiselect("Filter Tournaments",options=df_2023_tournaments_list.sort_values(by=[1], ascending=False)['Category'].unique())
        #Liste déroulante avec tous les tournois de 2023
        if len(filter_tournaments)>0:
            df_2023_tournaments_list_filtered = df_2023_tournaments_list_filtered[df_2023_tournaments_list_filtered['Category'].isin(filter_tournaments)]
            short_name_categories = get_short_name_categories(df_2023_tournaments_list_filtered)
            options = ["Week "+str(df_2023_tournaments_list_filtered['Week'].iloc[i]) +" -> "+str(df_2023_tournaments_list_filtered['Tournament'].iloc[i])+" -> "+short_name_categories[i] for i in range(len(df_2023_tournaments_list_filtered))]
            selected_tournament = st.selectbox("Add a tournament",options=options)
            if len(options)>0:
                tournament_name = selected_tournament.split(' -> ')[1]
        else:
            short_name_categories = get_short_name_categories(df_2023_tournaments_list_filtered)
            options = ["Week "+str(df_2023_tournaments_list_filtered['Week'].iloc[i]) +" -> "+str(df_2023_tournaments_list_filtered['Tournament'].iloc[i])+" -> "+short_name_categories[i] for i in range(len(df_2023_tournaments_list_filtered))]
            selected_tournament = st.selectbox("Add a tournament",options=options)
            if len(options)>0:
                tournament_name = selected_tournament.split(' -> ')[1]

        if len(options)>0:
            #Liste déroulante avec les résultats possibles
            details_tournament = df_2023_tournaments_list[df_2023_tournaments_list['Tournament']==tournament_name]
            #Si le tournoi est par équipe:
            if details_tournament['Team'].iloc[0]==1:
                points_earned_tournament = st.number_input("Estimated Points Earned",min_value=0,max_value=13000,step=1)
            #Sinon:
            else:
                result_tournament = st.selectbox("Estimated Results",options=[1,2,3,4,"5-6","7-8","9-16","17-32","33-64","65-128","129-256","257-512","513-1024"])

            #Bouton pour ajouter le tournoi à la simulation
            button_add_tournament = st.button("Add Tournament",on_click=add_simulated_tournament)

        with st.expander("Graph Details"):
            st.image("./assets/legend_ranking_plot_dark.png")

        #On affiche le graphique

        if len(st.session_state['df_tournament_simulated'])==0:
            df_ranking_over_weeks = st.session_state['df_ranking_over_weeks']
            figure_ranking_chart = get_viz_ranking(df_ranking_over_weeks,'2022','2022 Ranking')
            st.session_state['figure_ranking_chart'] = figure_ranking_chart
            ranking_chart = st.plotly_chart(figure_ranking_chart,use_container_width=True)
        elif st.session_state['previous_df_tournament_simulated'].equals(st.session_state['df_tournament_simulated']):
            figure_ranking_chart_simulated = st.session_state['figure_ranking_chart_simulated']
            ranking_chart = st.plotly_chart(figure_ranking_chart_simulated,use_container_width=True)
        else:
            df_ranking_over_weeks_simulated = st.session_state['df_ranking_over_weeks_simulated']
            figure_ranking_chart = st.session_state['figure_ranking_chart']
            figure_ranking_chart_simulated = go.Figure(figure_ranking_chart)
            figure_ranking_chart_simulated = get_viz_ranking_simulated(df_ranking_over_weeks_simulated,figure_ranking_chart_simulated,'2023',"2023 Simulation")
            st.session_state['figure_ranking_chart_simulated']=figure_ranking_chart_simulated
            ranking_chart = st.plotly_chart(figure_ranking_chart_simulated,use_container_width=True)
            st.session_state['previous_df_tournament_simulated']= st.session_state['df_tournament_simulated'].copy()


    #Si on veut supprimer le tournoi selectionné de la simulation
    def delete_simulated_tournament(tournament_to_update):
        df_tournament_simulated = st.session_state['df_tournament_simulated']
        #On trouve l'index de la ligne a supprimer
        index_to_drop = df_tournament_simulated[df_tournament_simulated["Tournament"]==tournament_to_update].index.values[0]
        #On retire la ligne
        df_tournament_simulated.drop(index_to_drop,inplace=True)
        #On reset les indices
        df_tournament_simulated.reset_index(drop=True,inplace=True)

        if len(df_tournament_simulated)>0:
            #On met à jour la simulation
            #On récupère l'évolution du classement sur chaque semaine
            df_player_tournament_results = st.session_state['df_player_tournament_results']
            df_ranking_over_weeks = st.session_state['df_ranking_over_weeks']
            type_ranking = st.session_state['type_ranking']
            #On récupère le classement mondial
            df_world_ranking_at_week = st.session_state['get_world_ranking_at_week']
            df_ranking_over_weeks_simulated = get_ranking_over_weeks_simulated(df_player_tournament_results,df_tournament_simulated,df_ranking_over_weeks,type_ranking,df_world_ranking_at_week)
            #On sauvegarde l'état
            st.session_state['df_tournament_simulated'] = df_tournament_simulated
            st.session_state['df_ranking_over_weeks_simulated'] = df_ranking_over_weeks_simulated
        else:
            #On sauvegarde l'état
            st.session_state['df_tournament_simulated'] = df_tournament_simulated

    #Si on veut modifier le résultat du tournoi selectionné
    def update_simulated_tournament(tournament_to_update):
        df_tournament_simulated = st.session_state['df_tournament_simulated']
        #On trouve l'index de la ligne a supprimer
        index_to_modify = df_tournament_simulated[df_tournament_simulated["Tournament"]==tournament_to_update].index.values[0]
        details_tournament = df_2023_tournaments_list[df_2023_tournaments_list['Tournament']==tournament_to_update]
        #On modifie le dataframe
        #Si on a un tournoi par équipe:
        if details_tournament['Team'].iloc[0]==1:
            new_points_earned = new_points_earned_tournament
            df_tournament_simulated.loc[index_to_modify,"Points"]=new_points_earned

        else:
            new_points_earned = details_tournament[new_estimated_results].values[0]
            df_tournament_simulated.loc[index_to_modify,"Points"]=new_points_earned
            df_tournament_simulated.loc[index_to_modify,"Result"]=new_estimated_results

        #On met à jour la simulation
        #On récupère l'évolution du classement sur chaque semaine
        df_player_tournament_results = st.session_state['df_player_tournament_results']
        df_ranking_over_weeks = st.session_state['df_ranking_over_weeks']
        type_ranking = st.session_state['type_ranking']
        #On récupère le classement mondial
        df_world_ranking_at_week = st.session_state['get_world_ranking_at_week']
        df_ranking_over_weeks_simulated = get_ranking_over_weeks_simulated(df_player_tournament_results,df_tournament_simulated,df_ranking_over_weeks,type_ranking,df_world_ranking_at_week)
        #On sauvegarde l'état
        st.session_state['df_tournament_simulated'] = df_tournament_simulated
        st.session_state['df_ranking_over_weeks_simulated'] = df_ranking_over_weeks_simulated
        

    if len(st.session_state['df_tournament_simulated'])>0:
        with st.expander("Update Simulation"):
            df_tournament_simulated = st.session_state['df_tournament_simulated']
            df_ranking_over_weeks_simulated = st.session_state["df_ranking_over_weeks_simulated"]
            #Bouton de téléchargement de la simulation
            button_download_simulation = st.download_button(label="Download Current Simulation",data=df_ranking_over_weeks_simulated.to_csv(index=False),file_name='Simulation '+selected_players+'.csv',mime='text/csv')
            st.dataframe(df_tournament_simulated.iloc[:,1:5],use_container_width=True)
            #Choix du tournoi à modifier
            tournament_to_update = st.selectbox(label="Update Tournament",options=df_tournament_simulated['Tournament'])
            
            cols1, cols2 = st.columns(2)
            with cols1:
                st.button("Delete Tournament",on_click=delete_simulated_tournament,args=[tournament_to_update])
            with cols2:
                details_tournament = df_2023_tournaments_list[df_2023_tournaments_list['Tournament']==tournament_to_update]
                #Si le tournoi est par équipe:
                if details_tournament['Team'].iloc[0]==1:
                    new_points_earned_tournament = st.number_input("New Estimated Points",min_value=0,max_value=13000,step=1)
                #Sinon:
                else:
                    new_estimated_results = st.selectbox("New Estimated Results",options=[1,2,3,4,"5-6","7-8","9-16","17-32","33-64","65-128","129-256","257-512","513-1024"])
                
                st.button("Modify Results",on_click=update_simulated_tournament,args=[tournament_to_update])

#Onglet comparaisons de joueurs
with tab2:
    st.title("Players Comparisons")

    #File uploader:
    uploaded_files = st.file_uploader("Choose Simulation CSV Files you want to compare",type='csv',accept_multiple_files=True)
    st.caption('Names of files will appear in the legend')
    if len(uploaded_files)>0:
        try:
            nb_file = 0
            for uploaded_file in uploaded_files:
                dataframe_simulation = pd.read_csv(uploaded_file)
                dataframe_simulation.fillna('', inplace=True)
                if nb_file == 0:
                    figure_comparisons = go.Figure()
                    figure_comparisons = get_viz_ranking_simulated(dataframe_simulation,figure_comparisons,'2023',uploaded_file.name[:-4])
                    nb_file+=1
                else:
                    figure_comparisons = get_viz_ranking_simulated(dataframe_simulation,figure_comparisons,'2023',uploaded_file.name[:-4])

            st.plotly_chart(figure_comparisons,use_container_width=True)
        except:
            st.text('Error ! Uploaded files are not Simulations files with the extension .csv')

#Onglet Calendrier
with tab3:
    cal_cols1, cal_cols2 = st.columns(2)
    with cal_cols1:
        #Multi choix pour filtrer les tournois par catégorie
        filter_tournaments_category = st.multiselect("Filter by Category",options=df_2023_tournaments_list.sort_values(by=[1], ascending=False)['Category'].unique())
    with cal_cols2:
        #Multi choix pour filtrer les tournois par continent
        filter_tournaments_continent = st.multiselect("Filter by Continent",options=['Europe','Asia','North America','South America','Oceania','Africa'])

    #Liste déroulante avec tous les tournois de 2023
    if len(filter_tournaments_category)>0 and len(filter_tournaments_continent)==0:
        df_2023_tournaments_list_filtered_calendar = df_2023_tournaments_list[df_2023_tournaments_list['Category'].isin(filter_tournaments_category)]
    elif len(filter_tournaments_continent)>0 and len(filter_tournaments_category)==0:
        df_2023_tournaments_list_filtered_calendar = df_2023_tournaments_list[df_2023_tournaments_list['Continent'].isin(filter_tournaments_continent+[np.nan])]
    elif len(filter_tournaments_continent)>0 and len(filter_tournaments_category)>0:
        df_2023_tournaments_list_filtered_calendar = df_2023_tournaments_list[(df_2023_tournaments_list['Category'].isin(filter_tournaments_category)) & (df_2023_tournaments_list['Continent'].isin(filter_tournaments_continent+[np.nan]))]
    else:
        df_2023_tournaments_list_filtered_calendar = df_2023_tournaments_list

    short_name_categories_calendar = get_short_name_categories(df_2023_tournaments_list_filtered_calendar)
    options_calendar = ["Week "+str(df_2023_tournaments_list_filtered_calendar['Week'].iloc[i]) +" -> "+str(df_2023_tournaments_list_filtered_calendar['Tournament'].iloc[i])+" -> "+short_name_categories_calendar[i] for i in range(len(df_2023_tournaments_list_filtered_calendar))]
    selected_tournament_calendar = st.selectbox("Get Details about a Tournament",options=options_calendar)
    if len(options_calendar)>0:
        tournament_name_calendar = selected_tournament_calendar.split(' -> ')[1]
        details_tournament_calendar = df_2023_tournaments_list[df_2023_tournaments_list['Tournament']==tournament_name_calendar].replace(np.nan,'-')

        metric_cols1, metric_cols2, metric_cols3 = st.columns(3)
        metric_cols1.metric("Entry Deadline",details_tournament_calendar['Entry Deadline'].iloc[0])
        metric_cols2.metric("World Ranking Date",details_tournament_calendar['World Ranking Date'].iloc[0])
        metric_cols3.metric("M & Q Report",details_tournament_calendar['M & Q Report'].iloc[0])
        metric_cols1.metric("Seeding Date",details_tournament_calendar['Seeding Date'].iloc[0])
        metric_cols2.metric("Withdrawal Deadline",details_tournament_calendar['Withdrawal Deadline'].iloc[0])
        metric_cols3.metric("Draw Date",details_tournament_calendar['Draw Date'].iloc[0])

        if details_tournament_calendar['Tournament Link'].iloc[0]!="-":
            with metric_cols1:
                st.write("[Tournament Link](%s)" % details_tournament_calendar['Tournament Link'].iloc[0])
        if details_tournament_calendar['Website'].iloc[0]!="-":
            with metric_cols2:
                st.write("[Tournament Website](%s)" % details_tournament_calendar['Website'].iloc[0])
        
    # st.header("List of Tournaments matching filters")
    # st.dataframe(df_2023_tournaments_list_filtered_calendar,use_container_width=True)