from pyowm.owm import OWM
from pyowm.utils import formatting,timestamps
from geopy.geocoders import Nominatim
import requests
import matplotlib.pyplot as plt
import datetime
import mpld3
import json


owm = OWM("9297169f55274dfbf3f79162c9678b13")
mgr = owm.weather_manager()
accu_api="L1jY2SjkhBlsbhZG7c3uAJo3iVtIlZBe"
solcast_api="pZipflSatVeWc30GUTP2TxgXL-R4iVIa"
API_KEY="89acdee0-d06d-11ed-b59d-0242ac130002-89acdf58-d06d-11ed-b59d-0242ac130002"

# city=input("city : ")

def find_current_weather_status(lat, long):
    observation = mgr.weather_at_coords(lat, long)
    weather = observation.weather
    return (weather.detailed_status)

def find_current_and_today_min_max_temperature(lat,long):
    weather = mgr.weather_at_coords(lat,long).weather
    temp_dict_fahrenheit = weather.temperature('fahrenheit')
    return(temp_dict_fahrenheit['temp_min'],temp_dict_fahrenheit['temp_max'])
def current_wind_info(lat=10,long=10):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=windspeed_10m&timezone=Asia/Tokyo&limit=7"
    response = requests.get(url)
    data = response.json()
    wind_speed = data["hourly"]["windspeed_10m"]
    return wind_speed[0]
def is_it_going_to_rain_tomorrow(lat,long):
    mgr = owm.weather_manager()
    three_h_forecaster = mgr.forecast_at_coords(lat,long,interval='3h')
    tomorrow = timestamps.tomorrow()  # datetime object for tomorrow
    return three_h_forecaster.will_be_rainy_at(tomorrow)
def sunrise_sunset(lat,long):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_coords(lat,long)
    weather = observation.weather
    sunrise_unix = weather.sunrise_time()  # default unit: 'unix'
    sunrise_iso = weather.sunrise_time(timeformat='iso')
    sunrise_date = weather.sunrise_time(timeformat='date')
    sunrset_unix = weather.sunset_time()  # default unit: 'unix'
    sunrset_iso = weather.sunset_time(timeformat='iso')
    sunrset_date = weather.sunset_time(timeformat='date')
    return(sunrise_iso[11:19],sunrset_iso[11:19])
def lat_long_find(city):
    try:
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(city)
        print("The latitude of the location is: ", location.latitude)
        print("The longitude of the location is: ", location.longitude)
        latitude=location.latitude
        longitude=location.longitude

    except TypeError:
        print("Coordinates of " + city + "is not found")
def current_temperature(lat,long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m&timezone=Asia/Tokyo&limit=7"
    response = requests.get(url)
    data = response.json()
    temperature = data["hourly"]["temperature_2m"]
    return temperature[0]

#graph forecasting weather
def temperature_forecasting(lat,long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m&timezone=Asia/Tokyo&limit=7"
    response = requests.get(url)
    data = response.json()
    temp_data = data["hourly"]["temperature_2m"]
    temp_hour=data["hourly"]["time"]
    plt.plot(temp_hour,temp_data)
    plt.xlabel('Time (hours)')
    plt.ylabel('Temperature (°C)')
    plt.title('7-Day-s Temperature Forecast')
    plt.show()
    return temp_data
def relative_humidity(lat,long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=relativehumidity_2m&timezone=Asia/Tokyo&limit=7"
    response = requests.get(url)
    data = response.json()
    humidity_data_yaxis=data["hourly"]["relativehumidity_2m"]
    humidity_data_xaxix=data["hourly"]["time"]
    plt.plot(humidity_data_xaxix,humidity_data_yaxis)
    plt.xlabel('Time (hours)')
    plt.ylabel('Relative Humidity (%)')
    plt.title('7-Day Relative-Humidity Forecast')
    plt.show()
    return humidity_data_yaxis
def dewpoint_forecasting(lat,long):
    url= f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=dewpoint_2m&timezone=Asia/Tokyo&limit=7"
    response = requests.get(url)
    data = response.json()
    dew_point_yaxis= data["hourly"]["dewpoint_2m"]
    dew_point_xaxis=data["hourly"]["time"]
    plt.plot(dew_point_xaxis,dew_point_yaxis)
    plt.xlabel('Time (hours)')
    plt.ylabel('dewpoint (°C)')
    plt.title('7-Day Dewpoint Forecast')
    plt.show()
    return dew_point_yaxis
def precipitation_forecasting(lat,long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=precipitation&timezone=Asia/Tokyo&limit=7"
    response = requests.get(url)
    data = response.json()
    humidity_data_yaxis = data["hourly"]["precipitation"]
    humidity_data_xaxis=data["hourly"]["time"]
    plt.plot(humidity_data_xaxis,humidity_data_yaxis)
    plt.xlabel('Time (hours)')
    plt.ylabel('Precipitation Over a Hour (mm)')
    plt.title('7-Day Precipitaion Forecast')
    plt.show()
    return humidity_data_yaxis
def rain_forecasting(lat,long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=rain&timezone=Asia/Tokyo&limit=7"
    response = requests.get(url)
    data = response.json()
    rain_data_yaxis = data["hourly"]["rain"]
    rain_data_xaxis=data["hourly"]["time"]
    plt.plot(rain_data_xaxis,rain_data_yaxis)
    plt.xlabel('Time (hours)')
    plt.ylabel('Rain (mm)')
    plt.title('7-Day Rain Forecast')
    plt.show()
def cloudcover_forecasting(lat,long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=cloudcover&timezone=Asia/Tokyo&limit=7"
    response = requests.get(url)
    data = response.json()
    cloud_cover_yaxis = data["hourly"]["cloudcover"]
    cloud_cover_xaxis=data["hourly"]["time"]
    plt.plot(cloud_cover_xaxis,cloud_cover_yaxis)
    plt.xlabel('Time (hours)')
    plt.ylabel('CLoud Cover (%)')
    plt.title('7-Day CloudCover Forecast')
    plt.show()
def windspeed_forecasting(lat,long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=windspeed_10m&timezone=Asia/Tokyo&limit=7"
    response = requests.get(url)
    data = response.json()
    wind_speed_xaxis = data["hourly"]["windspeed_10m"]
    wind_speed_yaxis=data["hourly"]["time"]
    print(wind_speed_xaxis)
    plt.plot(wind_speed_xaxis,wind_speed_yaxis)
    plt.xlabel('Time (hours)')
    plt.ylabel('Windspeed (km/h)')
    plt.title('7-Day WindSpeed Forecast')
    plt.show()
def irradiance_forecasting(lat,long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=direct_normal_irradiance&timezone=Asia/Tokyo&limit=7"
    response = requests.get(url)
    data = response.json()
    irradnce_yaxis = data["hourly"]["direct_normal_irradiance"]
    irradnce_xaxis=data["hourly"]["time"]
    plt.plot(irradnce_xaxis,irradnce_yaxis)
    plt.xlabel('Time (hours)')
    plt.ylabel('Irradiance (W/m^2)')
    plt.title('7-Day Irradiance Forecast')
    plt.show()
def find_altitude(lat,long):
    url=f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={long}"
    response = requests.get(url)
    data = response.json()
    print(data["elevation"])
def forecast_wind_power(lat,long):
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=7)

    params = {
        'lat': lat,
        'lng': long,
        'start': start,
        'end': end,
        'params': 'windSpeed',
        'source': 'sg',
    }

    headers = {
        'Authorization': API_KEY
        # Replace YOUR_API_KEY with your actual API key
    }

    response = requests.get('https://api.stormglass.io/v2/weather/point', params=params, headers=headers)

    data = response.json()['hours']
    wind_speeds = [d['windSpeed']['sg'] for d in data]
    time_stamps = [d['time'] for d in data]

    rho = 1.225  # air density
    rotor_area = 100  # rotor swept area in m^2
    wind_powers = [0.5 * rho * rotor_area * (wind_speed ** 3) for wind_speed in wind_speeds]

    plt.plot(time_stamps, wind_powers)
    plt.xlabel('Time')
    plt.ylabel('Wind Power (Watts)')
    plt.title('Wind Power Forecast In Your Area')
    timestamps = []
    for element in time_stamps:
        sliced_part = element[5:]
        timestamps.append(sliced_part)

    x_ticks = range(0, len(timestamps), int(len(timestamps) / 6))  # divide x-axis into 6 parts
    x_labels = [timestamps[i] for i in x_ticks]
    plt.xticks(x_ticks, x_labels)
    plt.show()
def forecast_solar_power(lat,lon):
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=7)

    # Get solar irradiance data from Stormglass API
    response = requests.get(
        f"https://api.stormglass.io/v2/solar/point?lat={lat}&lng={lon}&start={start}&end={end}&params=downwardShortWaveRadiationFlux",
        headers={"Authorization": API_KEY}
    )

    data = response.json()['hours']
    irradiances = [d['downwardShortWaveRadiationFlux'] for d in data]

    # Assume a fixed photovoltaic efficiency of 15%
    pv_efficiency = 0.15

    # Calculate PV power in Watts
    pv_powers = [irradiance['sg'] * pv_efficiency for irradiance in irradiances]

    # Plot PV power data
    time_stamps = [datetime.datetime.fromisoformat(d['time']).strftime('%m-%d %H:%M') for d in data]
    plt.plot(time_stamps, pv_powers)
    plt.xlabel('Time')
    plt.ylabel('PV Power (Watts)')
    plt.title('PV Power Forecast for Your Area')
    timestamps=[]
    for element in time_stamps:
        sliced_part = element[5:]
        timestamps.append(sliced_part)

    x_ticks = range(0, len(timestamps), int(len(timestamps) / 6))  # divide x-axis into 6 parts
    x_labels = [timestamps[i] for i in x_ticks]
    plt.xticks(x_ticks, x_labels)
    plt.show()
def forecast_tidal_energy(lat,long):
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=7)

    # Get tidal data from Stormglass API
    response = requests.get(
        f"https://api.stormglass.io/v2/tide/sea-level/point?lat={lat}&lng={long}&start={start}&end={end}&step=1",
        headers={"Authorization": API_KEY}
    )

    data = response.json()
    print(data)
    sea_levels = [d['sg'] for d in data['data']]
    print(sea_levels)

    # Assume a fixed conversion efficiency of 50%
    conversion_efficiency = 0.5

    # Calculate tidal energy in kWh/m^2
    tidal_energy = [sea_level * conversion_efficiency for sea_level in sea_levels]
    time_stamps = [d['time']for d in data['data']]
    # Plot tidal energy data
    # timestamps = [datetime.datetime.fromtimestamp(d['time']).strftime('%m-%d %H:%M') for d in data]
    plt.plot(time_stamps, tidal_energy)
    timestamps = []
    for element in time_stamps:
        sliced_part = element[5:]
        timestamps.append(sliced_part)
    plt.xlabel('Time')
    plt.ylabel('Tidal Energy (kWh/m^2)')
    plt.title('Tidal Energy Forecast for Your Area')
    x_ticks = range(0, len(timestamps), int(len(timestamps) / 3))  # divide x-axis into 6 parts
    x_labels = [timestamps[i] for i in x_ticks]
    plt.xticks(x_ticks, x_labels)
    plt.show()
    html_fig = mpld3.fig_to_html(plt.gcf())
    return html_fig
def find_city_name(lat=12,lon=10):
    geolocator = Nominatim(user_agent="geoapiExercises")
    Latitude = str(lat)
    Longitude = str(lon)

    location = geolocator.reverse(Latitude + "," + Longitude)

    # Display
    print(location)
def predict_solar_power(lat,long):
    timeperiod=float(input("tell time_period to calculate solar_energy"))
    # Prompt the user to enter a date and time
    date_string = input("Enter a date and time (YYYY-MM-DD HH:MM): ")

    # Parse the date and time string into a datetime object
    target_date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')

    # Calculate the start and end datetimes for the API request
    start = target_date
    end = start + datetime.timedelta(hours=timeperiod)

    # Get solar irradiance data from Stormglass API
    response = requests.get(
        f"https://api.stormglass.io/v2/solar/point?lat={lat}&lng={long}&start={start}&end={end}&params=downwardShortWaveRadiationFlux",
        headers={"Authorization": API_KEY}
    )

    data = response.json()['hours']
    irradiances = [d['downwardShortWaveRadiationFlux'] for d in data]

    # Assume a fixed photovoltaic efficiency of 15%
    pv_efficiency = 0.15

    # Calculate PV power in Watts
    pv_powers = [irradiance['sg'] * pv_efficiency for irradiance in irradiances]

    # Plot PV power data
    time_stamps = [datetime.datetime.fromisoformat(d['time']).strftime('%m-%d %H:%M') for d in data]
    plt.plot(time_stamps, pv_powers)
    plt.xlabel('Time')
    plt.ylabel('PV Power (Watts)')
    plt.title('PV Power Forecast for Your Area')
    timestamps = []
    for element in time_stamps:
        sliced_part = element[5:]
        timestamps.append(sliced_part)
    x_ticks = range(0, len(timestamps), int(len(timestamps) / 6))  # divide x-axis into 6 parts
    x_labels = [timestamps[i] for i in x_ticks]
    plt.xticks(x_ticks, x_labels)
    plt.show()
    print(pv_powers)
def predict_wind_power(lat,long):
    timeperiod = float(input("tell time_period to calculate solar_energy"))

    # Prompt the user to enter a date and time
    date_string = input("Enter a date and time (YYYY-MM-DD HH:MM): ")

    # Parse the date and time string into a datetime object
    target_date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')

    # Calculate the start and end datetimes for the API request
    start = target_date
    end = start + datetime.timedelta(hours=timeperiod)
    params = {
        'lat': lat,
        'lng': long,
        'start': start,
        'end': end,
        'params': 'windSpeed',
        'source': 'sg',
    }

    headers = {
        'Authorization': API_KEY
        # Replace YOUR_API_KEY with your actual API key
    }
    response = requests.get('https://api.stormglass.io/v2/weather/point', params=params, headers=headers)

    data = response.json()['hours']
    wind_speeds = [d['windSpeed']['sg'] for d in data]
    time_stamps = [d['time'] for d in data]
    rho = 1.225  # air density
    rotor_area = 100  # rotor swept area in m^2
    wind_powers = [0.5 * rho * rotor_area * (wind_speed ** 3) for wind_speed in wind_speeds]

    plt.plot(time_stamps, wind_powers)
    plt.xlabel('Time')
    plt.ylabel('Wind Power (Watts)')
    plt.title('Wind Power Forecast In Your Area')
    timestamps = []
    for element in time_stamps:
        sliced_part = element[5:]
        timestamps.append(sliced_part)
    x_ticks = range(0, len(timestamps), int(len(timestamps) / 6))  # divide x-axis into 6 parts
    x_labels = [timestamps[i] for i in x_ticks]
    plt.xticks(x_ticks, x_labels)
    plt.show()
    print(wind_powers)
def predict_tidal_energy(lat,long):
    import datetime
    import requests
    import matplotlib.pyplot as plt

    day = float(input("Enter number of days to forecast: "))
    date_string = input("Enter a date and time (YYYY-MM-DD HH:MM): ")

    # Parse the date and time string into a datetime object
    target_date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')
    start = target_date
    end = start + datetime.timedelta(hours=day)

    # Get tidal data from Stormglass API
    response = requests.get(
        f"https://api.stormglass.io/v2/tide/sea-level/point?lat={lat}&lng={long}&start={start}&end={end}&step=1",
        headers={"Authorization": API_KEY}
    )

    data = response.json()
    print(data)
    sea_levels = [d['sg'] for d in data['data']]
    print(sea_levels)

    # Assume a fixed conversion efficiency of 50%
    conversion_efficiency = 0.5

    # Calculate tidal energy in kWh/m^2
    tidal_energy = [sea_level * conversion_efficiency for sea_level in sea_levels]
    time_stamps = [d['time'] for d in data['data']]
    # Plot tidal energy data
    # timestamps = [datetime.datetime.fromtimestamp(d['time']).strftime('%m-%d %H:%M') for d in data]
    plt.plot(time_stamps, tidal_energy)
    timestamps = []
    for element in time_stamps:
        sliced_part = element[5:]
        timestamps.append(sliced_part)
    plt.xlabel('Time')
    plt.ylabel('Tidal Energy (kWh/m^2)')
    plt.title('Tidal Energy Forecast for Your Area')
    timestamps = []
    for element in time_stamps:
        sliced_part = element[5:]
        timestamps.append(sliced_part)
    x_ticks = range(0, len(timestamps), int(len(timestamps) / 3))  # divide x-axis into 6 parts
    x_labels = [timestamps[i] for i in x_ticks]
    plt.xticks(x_ticks, x_labels)
    plt.show()
c=input("Enter The city ")
lat_long_find(c)
predict_solar_power(10,15)