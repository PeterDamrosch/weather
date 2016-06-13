import os
import datetime
import requests
import sqlite3 as lite

# Connect to database
con = lite.connect('weather.db')
cur = con.cursor()

# Cities dictionary - key names here are the same as the city column names in the database
cities = { "new_york": '40.663619,-73.938589',
            "boston": '42.331960,-71.020173'
        }

# Build query - https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE,TIME
def get_forecast_data(city, request_time):
	base = "https://api.forecast.io/forecast/"
	api_key = os.environ["FORECAST_KEY"] + "/"
	query = cities[city] + "," + str(request_time)
	return base + api_key + query

# Get time for 30 days ago
thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)

# Repeat for 30 days (2 requests per day, one for each city)
for i in range(30):
	# Set request time based on i (incrementing 1 day each time)
		request_time = thirty_days_ago + datetime.timedelta(days=i)

		# Convert to unix time
		request_time = request_time.strftime("%s")

		# Add request time to table
		with con:
			cur.execute('INSERT INTO max_temperature (request_time) VALUES (?)', (request_time,))

		# Get max temperature for each city in the cities dictionary
		for city in cities.keys():
			# Send request using URL built in get_forecast_data
			r = requests.get(get_forecast_data(city, request_time))

			# Pull out the maximum temperature for that day
			max_temp = r.json()['daily']['data'][0]['temperatureMax']

			# Add max_temp to database
			with con:
				cur.execute('UPDATE max_temperature SET ' + city + ' = ' + str(max_temp) + ' WHERE request_time = ' + request_time + ';')
