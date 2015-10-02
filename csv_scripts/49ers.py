import csv
#Thanks to http://www.baseball-reference.com/ for all the data

def date_converter(date,year):
	month = {"January":"01","February":"02","March":"03","Apr":"04","May":"05",
		"Jun":"06","Jul":"07","Aug":"08","September":"09","October":"10",
		"November":"11","December":"12"}
	
	date_split = date.split()
	day = date_split[1]
	if len(day) == 1:
		day = "0" + day
	date_converted = str(year)+"-"+month[date_split[0]]+"-"+day
	
	return date_converted

def main():
	name = "teams_sfo_{year}_team_gamelogs.csv"
	start_year = 2003
	end_year = 2014
	headers = ("Game","Date","W/L","Record","Scored","Allowed")

	f=open("49ers.txt","w")
	f_csv=csv.writer(f)

	f_csv.writerow(headers)
	cont = 1

	for year in range(start_year,end_year+1):
		arch = open(name.format(year=year),"r")
		arch_csv = csv.reader(arch)
		for line in arch_csv:
			if len(line) == 0:
				continue
			#if header or away game: next!
			if line[7] == "@" or line[0] == "Week" or line[1] == "" or line[0] == "Preseason Games":
				continue

			game = cont
			date = date_converter(line[2],year)
			wl = line[4]
			record = line[6]
			scored = line[9]
			allowed = line[10]
			f_csv.writerow((game,date,wl,record,scored,allowed))
			cont += 1

		arch.close()	
	f.close()
main()
