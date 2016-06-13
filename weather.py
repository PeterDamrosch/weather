import os
import datetime
import requests
import collections

# Cities dictionary
cities = { "New York": '40.663619,-73.938589',
            "Boston": '42.331960,-71.020173'
        }

# Build query
def get_forecast_data(city, request_time):
	# Build query - https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE,TIME
	base = "https://api.forecast.io/forecast/"
	api_key = os.environ["FORECAST_KEY"] + "/"
	query = cities[city] + "," + str(request_time)
	return base + api_key + query

# Get time for 30 days ago
thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)

# Do it all in lists, because I can't figure out the key errors I'm getting for dictionaries
max_temp_results = {
	"time_list": [],
	"New York": [],
	"Boston": []
}

# Repeat for 30 days (2 requests per day, one for each city)
for i in range(30):
	# Set request time based on i (incrementing 1 day each time)
		request_time = thirty_days_ago + datetime.timedelta(days=i)

		# Convert to unix time
		request_time = request_time.strftime("%s")

		# Add to time_list dictionary
		max_temp_results['time_list'].append(request_time)

		for city in cities.keys():
			# Get city temperature data
			r = requests.get(get_forecast_data(city, request_time))

			# Append Boston temp
			max_temp = r.json()['daily']['data'][0]['temperatureMax']
			max_temp_results[city].append(max_temp)
