import requests
import dotenv
import os
import json
import random
from datetime import datetime as dt
from geopy.geocoders import Nominatim

API_URL = "https://api.openweathermap.org/data/2.5/weather"
test_data_path = 'weatherExample.txt'
geolocator = Nominatim(user_agent="weather_app")
API_KEY = ''
is_imperial = False
tempUnit = '°C'
speedUnit = 'km/h'

# region ---------------- Getter Functions ---------------
def get_public_IP():
  try:
    response = requests.get("https://api.ipify.org?format=json", timeout=5)
    if response.status_code == 200:
      ip_data = response.json()
      return ip_data.get("ip", "8.8.8.8")
    else:
      print("Failed to retrieve public IP")
      return "8.8.8.8"
  except Exception as e:
    print(f"Error occurred: {e}")
    return "8.8.8.8"

def get_IP_location(ip_address):
  ipProvider_URL = "http://ip-api.com/json/"
  default = {'lat': 0, 'lon': 0, 'city': 'Chicago'}
  try:
    response = requests.get(f"{ipProvider_URL}{ip_address}", timeout=5)
    if response.status_code == 200:
      data = response.json()
      lat = data.get('lat', 0)
      lon = data.get('lon', 0)
      city = data.get('city', 'Unknown')
      timezone = data.get('timezone', 'UTC')
      if lat != 0 and lon != 0:
        location = {
          "lat": lat, 
          "lon": lon,
          "city": city,
          "timezone": timezone
          }
        return location
      else:
        return "Location data not available"
    else:
      return default
  except Exception as e:
    print('Error with getting IP location, possible network issue.')
    return default

def get_weather(location, appid, is_test=False, is_city=False, is_random=False):
  params = {
    "appid": appid,
    "units": "metric"
  }
  if is_random:
    return create_random_weather()
  if is_city:
    params["q"] = location
  elif isinstance(location, dict):
    params["lat"] = location.get("lat")
    params["lon"] = location.get("lon")
  else:
    print("Invalid location format")
    return {"error": "Invalid location format"}
  if is_test:
    with open(test_data_path, 'r') as f:
      return json.load(f)
  try:
    res = requests.get(API_URL, params=params, timeout=5)
    if res.status_code == 200:
      return res.json()
    elif res.status_code == 401:
      print("Error: Unauthorized. Check your API key.")
      return False
    else:
      print(f"Error: Received status code {res.status_code} from Weather API")
      return False
  except Exception as e:
    print(f"Error fetching weather data: {e}")
    return False

# endregion
# region --------------- Parsing/Decoding Functions ------------
def parse_weather_response(weatherData, is_24hr_format=False):
  if "error" in weatherData:
    return weatherData["error"]
  main = weatherData.get("main", {})
  city = weatherData.get("name", "Unknown location")
  temp = main.get("temp", "N/A")
  description = weatherData.get("weather", [{}])[0].get("description", "N/A")
  time = dt.fromtimestamp(weatherData.get('dt', 0)).strftime('%Y-%m-%d %H:%M:%S') if weatherData.get('dt', 0) != 0 else 'N/A'
  sys = weatherData.get('sys', {})
  sunrise = dt.fromtimestamp(sys.get('sunrise', 0)).strftime('%H:%M:%S') if sys.get('sunrise', 0) != 0 else 'N/A'
  sunset = dt.fromtimestamp(sys.get('sunset', 0)).strftime('%H:%M:%S') if sys.get('sunset', 0) != 0 else 'N/A'
  total_daylight = sys.get('sunset', 0) - sys.get('sunrise', 0) if sys.get('sunset', 0) != 0 and sys.get('sunrise', 0) != 0 else 'N/A'
  total_daylight = (total_daylight // 60) // 60 if isinstance(total_daylight, int) else 'N/A'  # in hours
  if not is_24hr_format:
    time = dt.fromtimestamp(weatherData.get('dt', 0)).strftime('%Y-%m-%d %I:%M:%S %p') if weatherData.get('dt', 0) != 0 else 'N/A'
  pressure = main.get("pressure", "N/A")
  humidity = main.get("humidity", "N/A")
  visibility = weatherData.get("visibility", "N/A")
  feels_like = main.get("feels_like", "N/A")
  min_temp = main.get("temp_min", "N/A")
  max_temp = main.get("temp_max", "N/A")

  weather_icon = weatherData.get('weather', [{}])[0].get('icon', '')
  wind = weatherData.get("wind", {})
  wind_direction = wind.get("deg", 0)
  wind_speed = wind.get("speed", 0)
  wind_gust = wind.get("gust", 0)

  temp_icon = temp_to_emoji(temp)
  weather_icon = weather_to_emoji(weather_icon)

  if is_imperial:
    wind_speed = round(wind_speed * 2.23694, 2)  # Convert m/s to mph
    wind_gust = round(wind_gust * 2.23694, 2)
    temp = c_to_f(temp)
    feels_like = c_to_f(feels_like)
    min_temp = c_to_f(min_temp)
    max_temp = c_to_f(max_temp)

  parsed = {
    "city": city,
    "temperature": temp,
    "description": description,
    "time": time,
    "pressure": pressure,
    "humidity": humidity,
    "visibility": visibility,
    "feels_like": feels_like,
    "min_temp": min_temp,
    "max_temp": max_temp,
    "sunrise": sunrise,
    "sunset": sunset,
    "total_daylight_hours": total_daylight,
    "wind_direction": wind_direction,
    "wind_speed": wind_speed,
    "wind_gust": wind_gust,
    'temp_icon': temp_icon,
    'weather_icon': weather_icon
  }
  return parsed

def location_decode(location_arr):
  location = {"lat": 0, "lon": 0}
  if len(location_arr) == 2:
    lat = float(location_arr[0]) if isinstance(location_arr[0], (int, float, str)) else 0.0
    lon = float(location_arr[1]) if isinstance(location_arr[1], (int, float, str)) else 0.0
    return {"lat": lat, "lon": lon}
  elif len(location_arr) > 2:
    print('Error: Improper location format')
    return {'lat': 0, 'lon': 0}
  city = location_arr[0]
  try:
    location = geolocator.geocode(city, timeout=6)
  except Exception as e:
    print("Error geocoding location")
    return {'lat': 0, 'lon': 0}
  if location:
    return {"lat": location.latitude, "lon": location.longitude}
  else:
    print("Error: Location not found, Probably just a bad input.\nReformatting your inputted location might help.")
    return {'lat': 0, 'lon': 0}

def c_to_f(celsius):
  return round(celsius * 9/5 + 32, 2)

def temp_to_emoji(temp):
  if temp < -28:
    return "💀🧊"
  if temp < 0:
    return "❄️"
  elif temp < 10:
    return "🥶"
  elif temp < 20:
    return "😊"
  elif temp < 30:
    return "🔥"
  elif temp > 40:
    return "💀🌋"
  else:
    return "☹️"

def weather_to_emoji(icon_code):
  icon_map = {
    "01d": "☀️",
    "01n": "🌙",
    "02d": "🌤️",
    "02n": "☁️🌙",
    "03d": "☁️",
    "03n": "☁️",
    "04d": "☁️☁️",
    "04n": "☁️☁️",
    "09d": "🌧️",
    "09n": "🌧️",
    "10d": "🌦️",
    "10n": "🌦️",
    "11d": "⛈️",
    "11n": "⛈️",
    "13d": "❄️",
    "13n": "❄️",
    "50d": "🌫️",
    "50n": "🌫️"
  }
  return icon_map.get(icon_code, "")

def angle_to_direction(angle, is_arrow=False):
  directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
  arrows = ['↑', '↗', '→', '↘', '↓', '↙', '←', '↖']
  idx = round(angle / 45) % 8
  if is_arrow:
    return arrows[idx]
  return directions[idx]
# endregion
# region ----------- prompting/printing functions -------------

def user_prompt():
  locationRes = ''
  locationArr = []
  print("\n\nWelcome to the Weather App!, Enter 'I' for Imperial units (°F|mph) or nothing to default to Metric units (°C|km/h). Exit the app by typing 'exit'!: ")
  try:
    unitRes = input().strip().upper()
    global is_imperial
    if unitRes == 'I':
      global tempUnit
      global speedUnit
      tempUnit = '°F'
      speedUnit = 'mph'
      is_imperial = True
    if unitRes == 'EXIT':
      return {"break": True}
  except Exception as e:
    print(f"Input error: {e}")
  print("Enter city name, address, or coordinates (latitude, longitude) separated by comma or enter nothing to get your location's weather: ")
  try:
    locationRes = input().strip()
  except Exception as e:
    print(f"Input error: {e}")
    return {"lat": 0, "lon": 0}
  if locationRes.lower() == 'test':
    print("Test mode selected, using data from local file.")
    return {"lat": 0, "lon": 0, 'is_test': True}
  elif locationRes.lower() == 'random':
    print("Random weather mode selected.")
    return {"lat": 0, "lon": 0, 'is_random': True}
  if locationRes == '':
    user_IP = get_public_IP()
    if user_IP == '8.8.8.8':
      print('Error: Invalid IP, possible connection issue.')
    user_location = get_IP_location(user_IP)
    user_lat, user_lon = user_location.get("lat"), user_location.get("lon")
    locationArr = [user_lat, user_lon]
  elif ',' in locationRes:
    coords = [item.strip() for item in locationRes.split(',')]
    if len(coords) == 2:
      for i in range(2):
        try:
          coords[i] = float(coords[i])
        except ValueError:
          print("Invalid coordinate value, defaulting to 0")
          coords[i] = 0.0
      locationArr = coords
    else:
      print("Invalid coordinates format")
      locationArr = [0, 0]
  else:
    locationArr = [locationRes]
  return location_decode(locationArr)

def prompt_loop():
  while True:
    user_location = user_prompt()
    if user_location.get('break', False):
      print("Exiting Weather App. Goodbye!")
      break
    elif user_location.get('is_test', False):
      user_weather = get_weather(user_location, API_KEY, is_test=True)
    elif user_location.get('is_random', False):
      user_weather = get_weather(user_location, API_KEY, is_random=True)
    else:
      if not check_connectivity():
        print('Error: No Internet Connection found, Exiting...')
        exit()
      user_weather = get_weather(user_location, API_KEY)
    if not isinstance(user_weather, dict):
      print('Error: Failed to retrieve weather data.')
      return;
      
    user_parsed = parse_weather_response(user_weather)
    print_weather_log(user_parsed)

def print_weather_log(data):
  print(f"Weather in {data['city']}")
  print(f"Temperature: {data['temperature']}{tempUnit} {data['temp_icon']} with Highs of {data['max_temp']}{tempUnit} and Lows of {data['min_temp']}{tempUnit}")
  print(f"Feels Like: {data['feels_like']}{tempUnit}")
  print(f"Conditions: {data['description']} {data['weather_icon']}")
  print(f"Wind blowing at {data['wind_speed']} {speedUnit} with {data['wind_gust']} {speedUnit} gusts, Direction: {angle_to_direction(data['wind_direction'], is_arrow=True)} {angle_to_direction(data['wind_direction'])} ({data['wind_direction']}°)")
  print(f"Sunrise at: {data['sunrise']} | Sunset at: {data['sunset']} | Total Daylight Hours: {data['total_daylight_hours']} hrs")
  print(f"Pressure: {data['pressure']} hPa | Visibility: {data['visibility']} meters")
  print(f"Humidity: {data['humidity']}%")
# endregion
# region --------------- Checking/Testing Functions ----------------
def check_connectivity(url='https://www.google.com?', timeout=5):
  try:
    requests.get(url, timeout=timeout)
    return True
  except requests.ConnectionError:
    return False
  except requests.ConnectTimeout:
    return False
  except Exception as e:
    print(f'Error: {e}')
    return False

def create_random_weather():
  weather_list = ["clear sky", "few clouds", "scattered clouds", "broken clouds", "shower rain", "rain", "thunderstorm", "snow", "mist"]
  icon_list = ['01d', '01n', '02d', '02n', '03d', '03n', '04d', '04n', '09d', '09n', '10d', '10n', '11d', '11n', '13d', '13n', '50d', '50n']
  temp_range = [-30, 50]
  pressure_range = [980, 1050]
  date_range = [dt(2006, 8, 24, 15, 46), dt(2025, 6, 25)]
  speed_range = [0, 40]
  gust_range = [0, 60]
  random_weather = random.choice(weather_list)
  random_icon = random.choice(icon_list)
  random_temp = round(random.uniform(temp_range[0], temp_range[1]), 2)
  random_pressure = random.randint(pressure_range[0], pressure_range[1])
  random_date = random.randint(int(date_range[0].timestamp()), int(date_range[1].timestamp()))
  random_speed = round(random.uniform(speed_range[0], speed_range[1]), 2)
  random_gust = round(random.uniform(gust_range[0], gust_range[1]), 2)
  random_humidity = random.randint(10, 100)
  data = {
    "name": "Chicago",
    "main": {
      "temp": random_temp,
      "feels_like": round(random_temp - 1.5, 2),
      "temp_min": round(random_temp - 4.0, 2),
      "temp_max": round(random_temp + 2.0, 2),
      "pressure": random_pressure,
      "humidity": random_humidity
    },
    "weather": [
      {
        "description": random_weather,
        "icon": random_icon
      }
    ],
    "dt": random_date,
    "sys": {
      "sunrise": int(dt.fromtimestamp(random_date).replace(hour=6, minute=12, second=56).timestamp()),
      "sunset": int(dt.fromtimestamp(random_date).replace(hour=19, minute=56, second=12).timestamp())
    },
    "visibility": 10000,
    "wind": {
      "speed": random_speed,
      "deg": random.randint(0, 360),
      "gust": random_gust
    }

  }
  return data
# endregion
# region ---------------- Utility Functions ----------------
def fileLog(message, is_json=False, file="weatherExample.txt", is_printed=True):
  if is_json:
    message = json.dumps(message, indent=2)
  else:
    message = str(message)
  try:
    with open(file, "a") as f:
      print(message) if is_printed else None
      f.write(message + "\n")
  except Exception as e:
    print(f"Failed to write to log file: {e}")
# endregion

if __name__ == "__main__":
  dotenv.load_dotenv()
  API_KEY = os.getenv("OWM_API_KEY")
  prompt_loop()