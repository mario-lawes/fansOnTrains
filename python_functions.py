import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta

# -----------------------------
# Haversine Funktionen
# -----------------------------
def haversine_vectorized(lat, lon, lats, lons):
    """
    Vektorisiertes Haversine für Arrays.
    lat, lon: einzelne Position (float)
    lats, lons: Arrays mit Stop-Koordinaten
    Returns: Array mit Entfernungen in km
    """
    R = 6371  # Erdradius in km
    phi1 = np.radians(lat)
    phi2 = np.radians(lats)
    delta_phi = np.radians(lats - lat)
    delta_lambda = np.radians(lons - lon)
    a = np.sin(delta_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def find_closest_stop(lat, lon, all_stops_df):
    """
    Findet den nächsten Stop zum Punkt (lat, lon) mithilfe von vektorisierten Haversine-Berechnungen.
    """
    lats = all_stops_df['stop_lat'].to_numpy()
    lons = all_stops_df['stop_lon'].to_numpy()
    dists = haversine_vectorized(lat, lon, lats, lons)
    idx = np.argmin(dists)
    closest_stop = all_stops_df.iloc[idx].to_dict()
    closest_stop['distance_km'] = dists[idx]
    return closest_stop

# -----------------------------
# Hauptfunktion
# -----------------------------
def get_train_connections_for_game(game_info_df, 
                                   all_stops_df,
                                   trips_df,
                                   stop_times_df,
                                   routes_df,
                                   calendar_df, 
                                   window_hours=3, 
                                   trip_type='departure'):
    """
    Liefert Zugverbindungen für ein Spiel basierend auf Start/Ziel-Koordinaten, 
    GTFS-Daten (stops, trips, stop_times, routes, calendar) und Zeitfenster.
    """
    # -----------------------------
    # Start/Ziel bestimmen
    # -----------------------------
    if trip_type.lower() == "departure":
        lat_start, lon_start = game_info_df["home_lat"], game_info_df["home_lon"]
        lat_end, lon_end = game_info_df["away_lat"], game_info_df["away_lon"]
    else:  # 'arrival'
        lat_start, lon_start = game_info_df["away_lat"], game_info_df["away_lon"]
        lat_end, lon_end = game_info_df["home_lat"], game_info_df["home_lon"]

    # Datum
    date = pd.to_datetime(game_info_df["date"])
    date_only = date.date()

    # -----------------------------
    # Nächste Bahnhöfe
    # -----------------------------
    station_start = find_closest_stop(lat_start, lon_start, all_stops_df)
    station_end   = find_closest_stop(lat_end, lon_end, all_stops_df)
    start_ids = [station_start['stop_id']]
    end_ids   = [station_end['stop_id']]
    print(station_start, station_end)
    # -----------------------------
    # Aktive Trips
    # -----------------------------
    weekday = date.strftime("%A").lower()
    active_service_ids = calendar_df[calendar_df[weekday] == 1]['service_id'].tolist()
    active_trips = trips_df[trips_df['service_id'].isin(active_service_ids)]
    stop_times_active = stop_times_df[stop_times_df['trip_id'].isin(active_trips['trip_id'])]

    # -----------------------------
    # Trips zwischen Start und Ziel
    # -----------------------------
    stop_times_start = stop_times_active[stop_times_active['stop_id'].isin(start_ids)]
    stop_times_end   = stop_times_active[stop_times_active['stop_id'].isin(end_ids)]
    common_trips = set(stop_times_start['trip_id']).intersection(set(stop_times_end['trip_id']))

    # -----------------------------
    # Zeitfenster
    # -----------------------------
    input_time = datetime.combine(date_only, datetime.min.time())  # Mit 00:00 als Basis
    if trip_type.lower() == 'arrival':
        window_start = input_time - timedelta(hours=(2 + window_hours))
        window_end   = input_time + timedelta(hours=2)
    else:  # departure
        window_start = input_time + timedelta(hours=2)
        window_end   = input_time + timedelta(hours=(2 + window_hours))

    # -----------------------------
    # Stopps sammeln
    # -----------------------------
    rows = []
    for trip_id in common_trips:
        trip_times = stop_times_active[stop_times_active['trip_id'] == trip_id].sort_values('stop_sequence')
        try:
            start_idx = trip_times[trip_times['stop_id'].isin(start_ids)].index[0]
            end_idx   = trip_times[trip_times['stop_id'].isin(end_ids)].index[0]
        except IndexError:
            continue
        if start_idx >= end_idx:
            continue
        stops_between = trip_times.loc[start_idx:end_idx]

        # Start/End Zeit
        start_time_str = stops_between.iloc[0]['departure_time']
        end_time_str   = stops_between.iloc[-1]['arrival_time']
        start_dt = datetime.strptime(start_time_str, "%H:%M:%S").replace(year=date_only.year, month=date_only.month, day=date_only.day)
        end_dt   = datetime.strptime(end_time_str, "%H:%M:%S").replace(year=date_only.year, month=date_only.month, day=date_only.day)

        if trip_type.lower() == 'departure' and not (window_start <= start_dt <= window_end):
            continue
        if trip_type.lower() == 'arrival' and not (window_start <= end_dt <= window_end):
            continue

        # Route Name
        route_id = trips_df.loc[trips_df['trip_id'] == trip_id, 'route_id'].values[0]
        route_info = routes_df[routes_df['route_id'] == route_id]
        if 'route_long_name' in routes_df.columns and not route_info['route_long_name'].isna().all():
            route_name = route_info['route_long_name'].values[0]
        elif 'route_short_name' in routes_df.columns and not route_info['route_short_name'].isna().all():
            route_name = route_info['route_short_name'].values[0]
        else:
            route_name = str(route_id)

        # Stopps sammeln
        for _, stop_row in stops_between.iterrows():
            stop_info = all_stops_df[all_stops_df['stop_id'] == stop_row['stop_id']].iloc[0]
            rows.append({
                'match_id': game_info_df.get('match_id', None),
                'trip_id': trip_id,
                'route': route_name,
                'stop_sequence': stop_row['stop_sequence'],
                'stop_name': stop_info['stop_name'],
                'stop_lon': stop_info['stop_lon'],
                'stop_lat': stop_info['stop_lat'],
                'arrival': stop_row.get('arrival_time', ''),
                'departure': stop_row.get('departure_time', ''),
                'date': date
            })

    return pd.DataFrame(rows)
