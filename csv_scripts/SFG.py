import csv
#Thanks to http://www.pro-football-reference.com/ for all the data

def date_converter(date,year):
	month = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05",
		"Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10",
		"Nov":"11","Dec":"12"}
	
	date_split = date.split()
	date_converted = str(year)+"-"+month[date_split[1]]+"-"+date_split[2]
	

	return date_converted


def streak(streak,year):
	strk = len(streak)
	if strk == 0:
		return
	if streak[0] == "+":
		return str(strk)

	return str(strk*-1)


def main():
	name = "teams_SFG_{year}-schedule-scores_team_schedule.csv"
	start_year = 2003
	end_year = 2015
	headers = ("Game","Date","W/L","Rank","Time","D/N","Attendance","Streak")

	f=open("SFG.txt","w")
	f_csv=csv.writer(f)

	f_csv.writerow(headers)
	cont = 1

	for year in range(start_year,end_year + 1):
		arch = open(name.format(year=year),"r")
		arch_csv = csv.reader(arch)
		for line in arch_csv:
			if len(line) == 0:
				continue
			#if header or away game: next!
			if line[5] == "@" or line[0] == "Rk" or line[0] == "":
				continue

			game = cont
			date = date_converter(line[2],year)
			wl = line[7]
			rank = line[12]
			time = line[17]
			dn = line[18]
			att = line[19]
			strk = streak(line[20],year)

			f_csv.writerow((game,date,wl[0],rank,time,dn,att,strk))
			cont += 1

		arch.close()	
	f.close()
main()
