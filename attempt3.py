# IMPORT RELEVANT PACKAGES

import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import Polygon
import random
from PIL import Image
import time

# CREATE FUNCTIONS FOR DRAWING HEXAGONS IN THE CORRECT PLACES

def create_hexagon (x, y, size):
    """Create a hexagon given a center (x, y) and size."""
    angle = np.linspace(np.pi/6, 2 * np.pi + np.pi/6, 7)
    hex_x = x + size * np.cos(angle)
    hex_y = y + size * np.sin(angle)
    return Polygon(zip(hex_x, hex_y))

def hexr (state, hex_size = 0.3):
    distance_between_centers_horizontal = 2 * hex_size * np.cos(np.pi / 6)
    x2 = state[0] + distance_between_centers_horizontal
    y2 = state[1]
    return (x2, y2)

def hexar (state, hex_size = 0.3):
    distance_between_centers_horizontal = 2 * hex_size * np.cos(np.pi / 6)
    distance_between_centers_vertical = 2 * hex_size * np.sin(np.pi / 6)
    x3 = state[0] + distance_between_centers_horizontal / 2
    y3 = state[1] + distance_between_centers_vertical + hex_size /2
    return (x3, y3)

def hexal (state, hex_size = 0.3):
    distance_between_centers_horizontal = 2 * hex_size * np.cos(np.pi / 6)
    distance_between_centers_vertical = 2 * hex_size * np.sin(np.pi / 6)
    x3 = state[0] - distance_between_centers_horizontal / 2
    y3 = state[1] + distance_between_centers_vertical + hex_size /2
    return (x3, y3)

def hexbr (state, hex_size = 0.3):
    distance_between_centers_horizontal = 2 * hex_size * np.cos(np.pi / 6)
    distance_between_centers_vertical = 2 * hex_size * np.sin(np.pi / 6)
    x3 = state[0] + distance_between_centers_horizontal / 2
    y3 = state[1] + distance_between_centers_vertical - 2.5*hex_size
    return (x3, y3)

# CREATE CARDINAL LOCATIONS, NAMES AND ABBREVIATIONS FOR THE STATES

California = (1.5, 2); Arizona = hexr(California); Nevada = hexar(California); Oregon = hexal(California); Idaho = hexar(Oregon); Washington = hexal (Idaho); Montana = hexr(Washington); North_Dakota = hexr(Montana); Minnesota = hexr(North_Dakota); Wisconsin = hexr(Minnesota); Wyoming = hexr(Idaho); South_Dakota = hexr(Wyoming); Iowa = hexr(South_Dakota); Illinois = hexr(Iowa); Indiana = hexr(Illinois); Ohio = hexr(Indiana); Michigan = hexar(Indiana); Pennsylvania = hexr(Ohio); New_Jersey = hexr(Pennsylvania)
Connecticut = hexr(New_Jersey); New_York = hexar(Pennsylvania); Massachusetts = hexr(New_York); Rhode_Island = hexr(Massachusetts); New_Hampshire = hexal(Rhode_Island)
Vermont = hexar(New_York); Maine = hexar(New_Hampshire); Utah = hexr(Nevada); Nebraska = hexr(Utah); Missouri = hexr(Nebraska); Kentucky = hexr(Missouri); West_Virginia = hexr(Kentucky); Maryland = hexr(West_Virginia); Delaware = hexr(Maryland); Colorado = hexr(Arizona); Kansas = hexr(Colorado); Arkansas = hexr(Kansas); Tennessee = hexr(Arkansas); Virginia = hexr(Tennessee); North_Carolina = hexr(Virginia); New_Mexico = hexbr(Arizona); Oklahoma = hexr(New_Mexico); Louisiana = hexr(Oklahoma); Mississippi = hexr(Louisiana); Alabama = hexr(Mississippi); South_Carolina = hexr(Alabama); Texas = hexbr(New_Mexico); Georgia = hexbr(Alabama); Florida = hexr(Georgia); temp_Hawaii = hexbr(Florida); Hawaii = hexr(hexr(temp_Hawaii)); temp_Alaska = hexal(Washington); Alaska = hexal(temp_Alaska)

state_list = [California, Arizona, Nevada, Oregon, Idaho, Washington, Montana, North_Dakota, Minnesota, Wisconsin, Wyoming, South_Dakota, Iowa, Illinois, Indiana, Ohio, Michigan, Pennsylvania, New_Jersey, Connecticut, New_York, Massachusetts, Rhode_Island, New_Hampshire, Vermont, Maine, Utah, Nebraska, Missouri, Kentucky, West_Virginia, Maryland, Delaware, Colorado, Kansas, Arkansas, Tennessee, Virginia, North_Carolina, New_Mexico, Oklahoma, Louisiana, Mississippi, Alabama, South_Carolina, Texas, Georgia, Florida, Hawaii, Alaska]

abbrv_list = ['CA', 'AZ', 'NV', 'OR', 'ID', 'WA', 'MT', 'ND', 'MN', 'WI', 'WY', 'SD', 'IA', 'IL', 'IN', 'OH', 'MI', 'PA', 'NJ', 'CT', 'NY', 'MA', 'RI', 'NH', 'VT', 'ME', 'UT', 'NE', 'MO', 'KY', 'WV', 'MD', 'DE', 'CO', 'KS', 'AR', 'TN', 'VA', 'NC', 'NM', 'OK', 'LA', 'MS', 'AL', 'SC', 'TX', 'GA', 'FL', 'HI', 'AK']

name_list = ['California', 'Arizona', 'Nevada', 'Oregon', 'Idaho', 'Washington', 'Montana', 'North Dakota', 'Minnesota', 'Wisconsin', 'Wyoming', 'South Dakota', 'Iowa', 'Illinois', 'Indiana', 'Ohio', 'Michigan', 'Pennsylvania', 'New Jersey', 'Connecticut', 'New York', 'Massachusetts', 'Rhode Island', 'New Hampshire', 'Vermont', 'Maine', 'Utah', 'Nebraska', 'Missouri', 'Kentucky', 'West Virginia', 'Maryland', 'Delaware', 'Colorado', 'Kansas', 'Arkansas', 'Tennessee', 'Virginia', 'North Carolina', 'New Mexico', 'Oklahoma', 'Louisiana', 'Mississippi', 'Alabama', 'South Carolina', 'Texas', 'Georgia', 'Florida', 'Hawaii', 'Alaska']

pres_list = ['Washington', 'Adams Sr', 'Jefferson', 'Madison', 'Monroe', 'Adams Jr', 'Jackson', 'W.Harrison', 'Van Buren', 'Tyler', 'Polk', 'Taylor', 'Fillmore', 'Pierce', 'Buchanan', 'Lincoln', 'A.Johnson', 'Grant', 'Hayes', 'Garfield', 'Arthur', 'Cleveland', 'B.Harrison', 'McKinley', 'T.Roosevelt', 'Taft', 'Wilson', 'Harding', 'Coolidge', 'Hoover', 'F.Roosevelt', 'Truman', 'Eisenhower', 'Kennedy', 'L.Johnson', 'Nixon', 'Ford', 'Carter', 'Reagan', 'Bush Sr', 'Clinton', 'Bush Jr', 'Obama', 'Trump', 'Biden', 'X1', 'X2', 'X3', 'X4', 'X5']

# CREATE GEOLOCATIONS FOR THE STATES BASED ON CARDINAL LOCATIONS AND ADD NAMES, ABBREVIATIONS TO THE GEODATAFRAME

hexagons = [create_hexagon(x, y, 0.3) for x, y in state_list]
states_geodf = gpd.GeoDataFrame(geometry = gpd.GeoSeries(hexagons))
states_geodf["state_names"] = name_list
states_geodf["abbreviations"] = abbrv_list
states_geodf["cardinals"] = state_list
states_geodf["presidents"] = pres_list

# CREATE FUNCTION FOR LATER USE, LABELLING CHARTS BASED ON A GEODATAFRAME WITH A ROW CALLED 'abbreviations' WHICH WILL BE USED FOR LABELS

def init_labels(ax, geodf):
    for idx, row in geodf.iterrows():
        centroid_x, centroid_y = row['geometry'].centroid.xy
        label = row['abbreviations']
        ax.annotate(label, (centroid_x[0], centroid_y[0]), ha='center', fontsize=8, color='blue', xytext=(centroid_x[0], centroid_y[0] - 0.2))

def add_labels(ax, geodf):
    for idx, row in geodf.iterrows():
        centroid_x, centroid_y = row['geometry'].centroid.xy
        label = row['presidents']

        # Check if 'X' is in the label
        if 'X' in label:
            label = ''  # Set label to blank if 'X' is present
        
        ax.annotate(label, (centroid_x[0], centroid_y[0]), ha='center', va='center', fontsize=8)


# CREATE A FUNCTION FOR SELECTING TWO STATES AT RANDOM. THE FIRST WILL BE THE LOSER AND THE SECOND THE WINNER (REMEMBER THIS!)

def choose_win_lose(my_df):
    
    rand_choices_index_list = []
    rand_choices_abbrv_list = []
    rand_choices_names_list = []
    rand_choices_pres_list = []
    
    random_index_2 = random.randint(0, len(my_df) - 1)
    
    # Ensure unclaimed states cannot win!  
    rows_with_X = my_df[my_df['presidents'].str.contains('X', case=True, na=False)].index.tolist()
    
    while True:
        random_index_1 = random.randint(0, len(my_df) - 1)
        if random_index_1 not in rows_with_X:
            break

    random_index_2 = random.randint(0, len(my_df) - 1) 
    
    # Ensure the two indices are distinct
    while random_index_1 == random_index_2:
        random_index_2 = random.randint(0, len(my_df) - 1)

    while my_df['presidents'][random_index_1] == my_df['presidents'][random_index_2]:
        random_index_2 = random.randint(0, len(my_df) - 1)

      
    rand_choices_index_list.append(random_index_1)
    rand_choices_index_list.append(random_index_2)
    
    rand_choices_names_list.append(my_df["state_names"][random_index_1])
    rand_choices_names_list.append(my_df["state_names"][random_index_2])
    
    rand_choices_abbrv_list.append(my_df["abbreviations"][random_index_1])
    rand_choices_abbrv_list.append(my_df["abbreviations"][random_index_2])

    rand_choices_pres_list.append(my_df["presidents"][random_index_1])
    rand_choices_pres_list.append(my_df["presidents"][random_index_2])

    smalldf = pd.DataFrame(list(zip(rand_choices_index_list, rand_choices_names_list, rand_choices_abbrv_list, rand_choices_pres_list)))
    smalldf.columns = ['indices', 'state_names', 'abbreviations', 'presidents']

    return smalldf


# CREATE A FUNCTION FOR UPDATING A DATAFRAME BASED ON A GAME (GAME IS AN OUTPUT OF CHOOSE_WIN_LOSE) 
# SUCH THAT THE LOSER OF A BATTLE IS FULLY REPLACED BY THE WINNER!

def update_df(my_df, game):
    old_state_name = game.iloc[1,1]
    new_state_name = game.iloc[0,1]
    old_state_abbrv = game.iloc[1,2]
    new_state_abbrv = game.iloc[0,2]
    old_state_pres = game.iloc[1,3]
    new_state_pres = game.iloc[0,3]

    my_df['state_names'].replace({old_state_name: new_state_name}, inplace=True)
    my_df['abbreviations'].replace({old_state_abbrv: new_state_abbrv}, inplace=True)
    my_df['presidents'].replace({old_state_pres: new_state_pres}, inplace=True)
    
    return my_df

# NOW START THE STREAMLIT APP

def main():

    # Add a title and bring in the original image
    st.title("Otis's US State Battle game")
    st.image("usflag.jpg")
    
    if st.button("Click here to commence the battle!"):
        
        fig, ax = plt.subplots(figsize=(12,10))
        states_geodf['presidents'] = np.random.permutation(states_geodf['presidents'].values)
        states_geodf.plot(ax=ax, edgecolor='black', color='lightgray')
        init_labels(ax, states_geodf)
        add_labels(ax, states_geodf)
        plt.axis('off')
        plt.annotate("Presidents have taken their starting positions!", xy=(3.5, 4.5), ha="center", fontsize=14)
        plt.savefig("current_df.png")
        plt.close()
        st.image(Image.open("current_df.png"))
        time.sleep(0.5)

        num_states_held = 0
        winning_president = None
        
        while num_states_held < 50:
            game = choose_win_lose(states_geodf)
            win_index = game.indices[0]
            lose_index = game.indices[1]
            num_states_prev = len(states_geodf[states_geodf.iloc[:,4]==states_geodf.iloc[game.indices[1],4]])
            prev_df = states_geodf.copy()
            current_df = update_df(states_geodf, game)
            num_states_held = len(current_df[current_df.iloc[:,4]==current_df.iloc[game.indices[0],4]])
            fig, ax = plt.subplots(figsize=(12,10))
            current_df.plot(ax=ax, edgecolor='black', color='lightgray')
        
            win_hexagons = current_df[current_df.presidents==game.iloc[0,3]]
            win_hexagons.plot(ax=ax, color='cornflowerblue', edgecolor='black')

            lose_hexagons = prev_df[prev_df.presidents==game.iloc[1,3]]
            lose_hexagons.plot(ax=ax, color="lightseagreen", edgecolor="black")
            add_labels(ax, current_df)      

            plt.axis('off')
            if num_states_prev==1:
                if game.iloc[1,3] in ['X1', 'X2', 'X3', 'X4', 'X5']:
                    plt.annotate(f"{game.iloc[0,3]} has taken one of the unclaimed states.", xy=(3.5, 4.5), ha="center", fontsize=14)
                else:
                    plt.annotate(f"{game.iloc[0,3]} has defeated {game.iloc[1,3]}, who held one state.", xy=(3.5, 4.5), ha="center", fontsize=14)
            else:         
                plt.annotate(f"{game.iloc[0,3]} has defeated {game.iloc[1,3]}, who held {num_states_prev} states.", xy=(3.5, 4.5), ha="center", fontsize=14)
                       
            if num_states_held==50:
                plt.annotate(f"{game.iloc[0,3].upper()} IS THE WINNER!!", xy=(3.5, 4.1), ha="center", fontsize=14)
            else:
                plt.annotate(f"{game.iloc[0,3]} now owns {num_states_held} states!!", xy=(3.5, 4.1), ha="center", fontsize=14)
            plt.savefig("current_df.png")
            plt.close()
            st.image(Image.open("current_df.png"))
            time.sleep(2)
            winning_president = game.iloc[0,3]

        #image_filename = f"{winning_president}.png"
        
        #col1, col2 = st.columns(2)
        #col1.image(Image.open(image_filename), use_column_width=True)
        #col2.image("winners_crown.jpg", use_column_width=True)
        # Display images in each column
        #col1.image("usflag.jpg", use_column_width=True)
        #col2.image("state_image.png", use_column_width=True)
               

if __name__ == "__main__":
    main()
