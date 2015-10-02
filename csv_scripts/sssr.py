import requests
import csv
import datetime
import pandas as pd
import time

#Thanks to http://sunrise-sunset.org/ for the data.

start = datetime.datetime(2003,01,01)
end = datetime.datetime(2015,05,14)
dates = pd.date_range(start,end)

url = "http://api.sunrise-sunset.org/json?lat=37.7749295&lng=-122.4194155&date={date}"
dic_time = {"PM":{"12":"05","1":"06","2":"07","3":"08","4":"09"},"AM":{"12":"17","1":"18","2":"19","3":"20","4":"21"}}

arch = open("csv/sssr.csv", "w")
arch_csv = csv.writer(arch)
arch_csv.writerow(("Date","Sunrise","Sunset"))

contador = 0

for date in dates:
	r = requests.get(url.format(date=str(date).split()[0]))
	day = r.json()

	a = day["results"]["sunrise"]
	b = day["results"]["sunset"]

	sr= a.split()
	ss= b.split()

	sr_t = sr[0].split(":")
	ss_t = ss[0].split(":")

	sr_t[0] = dic_time[sr[1]][sr_t[0]]
	ss_t[0] = dic_time[ss[1]][ss_t[0]]

	sunrise = ":".join(sr_t)
	sunset = ":".join(ss_t)

	arch_csv.writerow((str(date).split()[0],sunrise,sunset))

	contador += 1
	if contador%100 == 0:
		print contador
	time.sleep(2)

arch.close()
