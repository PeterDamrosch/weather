import pandas as pd
import matplotlib.pyplot as plt
import sqlite3 as lite

con = lite.connect('weather.db')

# Create df from database
df = pd.read_sql_query('SELECT * FROM max_temperature ORDER BY request_time', con, index_col='request_time')

# Plot cities
df.plot()
plt.show()

# Check out range across the 30 days for each city
cities = df.columns
for city in cities:
	range = df[city].max() - df[city].min()
	mean = round(df[city].mean(),2)
	std = round(df[city].std(),2)
	print "{} - range: {}, mean: {}, standard deviation: {}".format(city, range, mean, std)
