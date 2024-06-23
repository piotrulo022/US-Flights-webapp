import pandas as pd


FLIGHTS = pd.read_csv('./dataset/flights_tiny.csv', on_bad_lines='skip')
CODES = pd.read_csv('./dataset/airports_codes.csv', sep = ';', on_bad_lines='skip')

def summarize_routes_from_origin(flights:pd.DataFrame, origin: str) -> pd.DataFrame:
    filtered_flights = flights[flights['ORIGIN'] == origin]

    summary = filtered_flights.groupby('DEST').agg(
                                        ORIGIN = ('ORIGIN', 'first'),
                                        ORIGIN_CITY=('ORIGIN_CITY', 'first'),
                                        DEST_CITY=('DEST_CITY', 'first'),
                                        AIRLINE = ('AIRLINE', 'first'),
                                        mean_crs_dep_time=('CRS_DEP_TIME', 'mean'),
                                        mean_dep_time=('DEP_TIME', 'mean'),
                                        mean_dep_delay=('DEP_DELAY', 'mean'),
                                        mean_taxi_out=('TAXI_OUT', 'mean'),
                                        mean_wheels_off=('WHEELS_OFF', 'mean'),
                                        mean_wheels_on=('WHEELS_ON', 'mean'),
                                        mean_taxi_in=('TAXI_IN', 'mean'),
                                        mean_crs_arr_time=('CRS_ARR_TIME', 'mean'),
                                        mean_arr_time=('ARR_TIME', 'mean'),
                                        mean_arr_delay=('ARR_DELAY', 'mean'),
                                        mean_cancelled=('CANCELLED', 'mean'),
                                        mean_diverted=('DIVERTED', 'mean'),
                                        mean_crs_elapsed_time=('CRS_ELAPSED_TIME', 'mean'),
                                        mean_elapsed_time=('ELAPSED_TIME', 'mean'),
                                        mean_air_time=('AIR_TIME', 'mean'),
                                        mean_distance=('DISTANCE', 'mean'),
                                        mean_delay_due_carrier=('DELAY_DUE_CARRIER', 'mean'),
                                        mean_delay_due_weather=('DELAY_DUE_WEATHER', 'mean'),
                                        mean_delay_due_nas=('DELAY_DUE_NAS', 'mean'),
                                        mean_delay_due_security=('DELAY_DUE_SECURITY', 'mean'),
                                        mean_delay_due_late_aircraft=('DELAY_DUE_LATE_AIRCRAFT', 'mean')
                                        ).reset_index()
    

    return summary



def get_origins(flights):
    originandcity = flights['ORIGIN'] + ', ' + flights['ORIGIN_CITY']
    return originandcity.unique().tolist()
    # return flights['ORIGIN'].unique().tolist()

def get_dests(flights):
    return flights['DEST'].unique().tolist()


def get_coords(codes, airport):
    coords = codes.loc[codes['Airport Code'] == airport][['Latitude', 'Longitude']].iloc[0].to_dict()

    return coords


AIRLINE_COLORS = {
    'Alaska Airlines Inc.': '#0033A0',
    'Allegiant Air': '#7A0048',
    'American Airlines Inc.': '#DF0024',
    'Delta Air Lines Inc.': '#8B1024',
    'Endeavor Air Inc.': '#8A8D8F',
    'Envoy Air': '#949CA0',
    'ExpressJet Airlines LLC d/b/a aha!': '#FF6600',
    'Frontier Airlines Inc.': '#1E4FA3',
    'Hawaiian Airlines Inc.': '#FF0000',
    'Horizon Air': '#74ACD1',
    'JetBlue Airways': '#0071BC',
    'Mesa Airlines Inc.': '#5276A7',
    'PSA Airlines Inc.': '#004A85',
    'Republic Airline': '#3B75B3',
    'SkyWest Airlines Inc.': '#0033A0',
    'Southwest Airlines Co.': '#EE352E',
    'Spirit Air Lines': '#FF7F00',
    'United Air Lines Inc.': '#002244'
}

