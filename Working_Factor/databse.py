import requests
import csv
import json

def get_database_for_forecasting(lat,lon,starttime,endtime):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date={starttime}&end_date={endtime}&hourly=temperature_2m")
    data = response.json()
    print(data)
    rows=data['hourly']['time']
    cols=data['hourly']['temperature_2m']
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'temperature_2m'])
        for i in range(len(rows)):
            writer.writerow([rows[i], cols[i]])