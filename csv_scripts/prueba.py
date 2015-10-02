from datetime import datetime, timedelta, tzinfo
import pytz
import pandas as pd

# TODO: sacar globals
pacific = pytz.timezone('US/Pacific')

def localizeDatesYmdHMS(dateString):
	'''Retorna la fecha Dates con informacion de la timezone de SF'''
	dt = datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S")
	dt = pacific.localize(dt)
	return dt

def localizeDatesYdm(dateString):
	'''Retorna la fecha Dates con informacion de la timezone de SF'''
	dt = datetime.strptime(dateString, "%Y-%d-%m")
	dt = pacific.localize(dt)
	return dt

def dateNormalized(dt):
	'''Retorna la fecha en formato TimeStamp
	que es la cantidad de segundos que pasaron desde el 1/1/1970'''
	dt = dt.replace(hour=0, minute=0, second=0)
	#Usar esta linea con python2.7
	return int(dt.strftime("%s"))
	#Usar esta linea con python3
	#return dt.replace(hour=0, minute=0, second=0).timestamp()
	
def timeNormalized(dt):
	'''Retorna la hora normalizada de 0 a 23 de una fecha en formato"'''
	return (dt.hour*60*60 + dt.minute*60 + dt.second) / float(60 * 60)
	
def main():
	dfTrain = pd.read_table("csv/sssr-normalized.csv", sep=',')
	
	raw_input()
	
	dfTrain = pd.read_table("prueba.csv", sep=',')
	#Hacemos una copia del Dates
	dfTrain['DatesOriginal'] =  dfTrain['Dates']

	#Agregamos la timezone de SF
	dfTrain['Dates'] = dfTrain['Dates'].apply(localizeDatesYmdHMS)
	
	#Creamos la columna TimeNormalized (debe ir antes de modificar las fechas)
	dfTrain['Time'] = dfTrain['Dates'].apply(timeNormalized)
	
	#Creamos la columna DatesTimeStamp sin la hora
	dfTrain['Dates'] = dfTrain['Dates'].apply(dateNormalized)
	
	print dfTrain
		
if __name__ == "__main__":
	main()
	print("Done.")
