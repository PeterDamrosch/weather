import sqlite3 as lite

# Create max_temperature database with unix time as key and columns for New York and Boson
con = lite.connect('weather.db')
cur = con.cursor()
with con:
	cur.execute('CREATE TABLE max_temperature (request_time INT, new_york NUMERIC, boston NUMERIC, philadelphia NUMERIC, nashville NUMERIC, washington_dc NUMERIC);')

