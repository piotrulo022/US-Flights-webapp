import pandas as pd
from nycflights13 import flights

codes = pd.read_csv('airports_codes.csv', sep = ';', on_bad_lines='skip')

def summarize_routes_from_origin(origin):
    """
    Summarizes the routes from a given origin by calculating mean delays, distance, and air time.
    
    Parameters:
    flights_df (DataFrame): The DataFrame containing flight data.
    origin (str): The origin airport code (e.g., "EWR").
    
    Returns:
    DataFrame: A summary DataFrame with columns: origin, dest, mean_arr_delay, mean_dep_delay,
               mean_distance, mean_air_time.
    """
    # Filter flights by the specified origin
    filtered_flights = flights[flights['origin'] == origin]
    
    # Group by destination and calculate summary statistics
    summary = filtered_flights.groupby('dest').agg(
        mean_arr_delay=('arr_delay', 'mean'),
        mean_dep_delay=('dep_delay', 'mean'),
        mean_distance=('distance', 'mean'),
        mean_air_time=('air_time', 'mean')
    ).reset_index()
    
    # Add the origin column
    summary['origin'] = origin
    
    # Rearrange columns to place 'origin' first
    summary = summary[['origin', 'dest', 'mean_arr_delay', 'mean_dep_delay', 'mean_distance', 'mean_air_time']]
    
    return summary


def get_origins():
    return flights['origin'].unique().tolist()


def get_dests():
    return flights['dest'].unique().tolist()

def get_coords(airport):
    coords = codes.loc[codes['Airport Code'] == airport][['Latitude', 'Longitude']].iloc[0].to_dict()

    return coords