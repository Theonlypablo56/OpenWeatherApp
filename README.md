# Console Weather App Assignment (OpenWeatherMap API)

## Overview
This **console-based** Python application retrieves and displays **current weather information**, using either the inputted city, inputted coordinates, or if nothing is entered, automatically gets your location using your IP address.

It connects and utilizes **OpenWeatherMap API** to fetch live weather data while also using Geopy and Nominatim to handle all location geocoding.

---
## Features
- Fetches **live weather data** (temperature, humidity, visibility, wind speed/gusts, pressure, sunrise/sunset, and more)
- Supports **Metric (°C | km/h)** and **Imperial (°F | mph)** units  
- Accepts **city names**, **latitude/longitude**, **popular location names**, or automatically detects your **current IP-based location**
- Displays **sunrise/sunset times** and **total daylight hours**
- Includes a **random weather generator** and **test mode** that reads from a saved data file for offline usage
- Handles bad inputs, missing data, and API errors gracefully by defaulting missing values to '0' or 'N/A'.

---
## Usage
1. The user is prompted to choose a unit system (Metric or Imperial).
2. The program asks for a location input — city, coordinates, or blank (for IP lookup).
3. It sends a request to OpenWeatherMap’s `/data/2.5/weather` API.
4. JSON data is received, parsed, and displayed in a readable format.
5. Weather information such as temperature, wind speed, sunrise/sunset, and conditions is printed to the console.

---
## Examples
- City Name Example
```
Welcome to the Weather App!, Enter 'I' for Imperial units (°F|mph) or nothing to default to Metric units (°C|km/h). Exit the app by typing 'exit'!:
> I
Enter city name, address, or coordinates (latitude, longitude) separated by comma or enter nothing to get your location's weather:
> Chicago
Weather in Chicago
Temperature: 28.94°F ❄️ with Highs of 30.0°F and Lows of 28.0°F
Feels Like: 20.37°F
Conditions: clear sky 🌙
Wind blowing at 9.22 mph with 0.0 mph gusts, Direction: ← W (280°)
Sunrise at: 06:34:20 | Sunset at: 16:34:40 | Total Daylight Hours: 10 hrs
Pressure: 1023 hPa | Visibility: 10000 meters
Humidity: 72%
```
- Location Name Example
```
Welcome to the Weather App!, Enter 'I' for Imperial units (°F|mph) or nothing to default to Metric units (°C|km/h). Exit the app by typing 'exit'!:
> I
Enter city name, address, or coordinates (latitude, longitude) separated by comma or enter nothing to get your location's weather:
> The Bean
Weather in Chicago
Temperature: 28.94°F ❄️ with Highs of 30.0°F and Lows of 28.0°F
Feels Like: 20.37°F
Conditions: clear sky 🌙
Wind blowing at 9.22 mph with 0.0 mph gusts, Direction: ← W (280°)
Sunrise at: 06:34:20 | Sunset at: 16:34:40 | Total Daylight Hours: 10 hrs
Pressure: 1023 hPa | Visibility: 10000 meters
Humidity: 72%
```
- Coordinate and Metric Unit Example
```
Welcome to the Weather App!, Enter 'I' for Imperial units (°F|mph) or nothing to default to Metric units (°C|km/h). Exit the app by typing 'exit'!:
> 
Enter city name, address, or coordinates (latitude, longitude) separated by comma or enter nothing to get your location's weather:
> 41.8827, -87.6233
Weather in Chicago
Temperature: 28.94°F ❄️ with Highs of 30.0°F and Lows of 28.0°F
Feels Like: 20.37°F
Conditions: clear sky 🌙
Wind blowing at 9.22 mph with 0.0 mph gusts, Direction: ← W (280°)
Sunrise at: 06:34:20 | Sunset at: 16:34:40 | Total Daylight Hours: 10 hrs
Pressure: 1023 hPa | Visibility: 10000 meters
Humidity: 72%
```
- Random Mode Example
```
Welcome to the Weather App!, Enter 'I' for Imperial units (°F|mph) or nothing to default to Metric units (°C|km/h). Exit the app by typing 'exit'!: 
>
Enter city name, address, or coordinates (latitude, longitude) separated by comma or enter nothing to get your location's weather:
> random
Random weather mode selected.
Weather in Chicago
Temperature: 43.92°C 💀🌋 with Highs of 45.92°C and Lows of 39.92°C
Feels Like: 42.42°C
Conditions: scattered clouds ❄️
Wind blowing at 17.51 km/h with 10.85 km/h gusts, Direction: → E (84°)
Sunrise at: 06:12:56 | Sunset at: 19:56:12 | Total Daylight Hours: 13 hrs
Pressure: 1010 hPa | Visibility: 10000 meters
Humidity: 89%
```
- Test Mode Example
```
Welcome to the Weather App!, Enter 'I' for Imperial units (°F|mph) or nothing to default to Metric units (°C|km/h). Exit the app by typing 'exit'!:
>  
Enter city name, address, or coordinates (latitude, longitude) separated by comma or enter nothing to get your location's weather:
> test
Test mode selected, using data from local file.
Weather in Chicago
Temperature: -0.31°C ❄️ with Highs of 0.61°C and Lows of -1.12°C
Feels Like: -5.93°C
Conditions: snow ❄️
Wind blowing at 6.17 km/h with 0 km/h gusts, Direction: ↖ NW (320°)
Sunrise at: 06:34:20 | Sunset at: 16:34:40 | Total Daylight Hours: 10 hrs
Pressure: 1024 hPa | Visibility: 10000 meters
Humidity: 69%
```
---
## Requirements
- An OpenWeatherMap API Key is required and must be put in a .env file within the project folder under the variable name "OWM_API_KEY". You can get the required API Key on https://openweathermap.org
```
OWM_API_KEY=ExampleAPIKey
```
Python **3.8+** is required, along with these libraries
```
pip install requests python-dotenv geopy
```
