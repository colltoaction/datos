# -*- coding: utf-8 -*-

from datetime import datetime
import pandas as pd
import numpy as np
import time
import pytz
from matplotlib.mlab import PCA

# TODO: sacar globals
#pacific = pytz.timezone('US/Pacific')

def setMedianByDistrict(dfTrain, coordCol, pdDistrict):
	#Filtro por el distrito (metodo en desuso pero se guarda para tenerlo)
	dfTrainTmp = dfTrain[dfTrain['PdDistrict'] == pdDistrict]
	return dfTrainTmp[coordCol].median()

def obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dataframe, columna):
	'''Obtenemos todos los casos de PdDistrict (por ejemplo) que se encuentran en el dataframe.'''
	#Filtramos las filas y nos quedamos solo las que tienen elementos de la columna 'columna' distintos.
	dfSinDuplicadosDeDistritos = dataframe.drop_duplicates(subset=columna, take_last=True)
	#Convertimos esa columna (serie) en una lista
	lsValues = dfSinDuplicadosDeDistritos[columna].tolist()
	return lsValues

def correccionDeCoordenadasAnomalas(dfTrain):
	#Filtramos las filas y nos quedamos solo con las filas con coordenadas Anomalas
	dfTmp = dfTrain[(dfTrain['X'] == -120.5)]
	dfTrainFilterAnomalCoords = dfTmp[(dfTmp['Y'] == 90)]

	lsDistritos = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrain, 'PdDistrict')

	#Generamos un diccionario con las medianas X Y de cada distrito
	dicMedianasPorDistrito = {}
	for distrito in lsDistritos:
		dfTrainTmp = dfTrain[dfTrain['PdDistrict'] == distrito]
		medianaXdelDistrito =  dfTrainTmp['X'].median()
		medianaYdelDistrito =  dfTrainTmp['Y'].median()
		dicMedianasPorDistrito[distrito] = (medianaXdelDistrito,medianaYdelDistrito)

	#Recorremos solo las filas con coordenadas anomalas
	for id in dfTrainFilterAnomalCoords.index.values:
		#Asigno la mediana a la coordenada anomala usando el diccionario de coordenads por distrito
		#dfTrain['X'][id] y dfTrain.ix[id,'X'] son equivalentes pero el 2do no genera copia del dataframe
		dfTrain.ix[id,'X'] = dicMedianasPorDistrito.get(dfTrain['PdDistrict'][id])[0]
		dfTrain.ix[id,'Y'] = dicMedianasPorDistrito.get(dfTrain['PdDistrict'][id])[1]
		#print id, dfTrain['PdDistrict'][id], dfTrain['X'][id], dfTrain['Y'][id]

	#Corregimos cada una de esas filas usando otro metodo
	#Modifico la columna PdDistrict con las coordenadas promedio de esos distritos pero las guardo luego en la col de la coordenada
	#dfTrainFilterAnomalCoords['X'] = dfTrainFilterAnomalCoords['PdDistrict'].apply((lambda pdDistrict: setMedianByDistrict(dfTrain,'X',pdDistrict)))
	#dfTrainFilterAnomalCoords['Y'] = dfTrainFilterAnomalCoords['PdDistrict'].apply((lambda pdDistrict: setMedianByDistrict(dfTrain,'Y',pdDistrict)))
	return dfTrain

def localizeDatesYmdHMS(dateString):
	'''Retorna la fecha Dates con informacion de la timezone de SF'''
	dt = datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S")
	#dt = pacific.localize(dt)
	return dt

def localizeDatesYdm(dateString):
	'''Retorna la fecha Dates con informacion de la timezone de SF'''
	dt = datetime.strptime(dateString, "%Y-%d-%m")
	#dt = pacific.localize(dt)
	return dt

def dateNormalized(dt):
	'''Retorna la fecha en formato TimeStamp
	que es la cantidad de segundos que pasaron desde el 1/1/1970'''
	#dt = dt.replace(hour=0, minute=0, second=0)
	#Usar esta linea con python2.7
	return int(dt.strftime("%s"))
	#Usar esta linea con python3
	#return dt.replace(hour=0, minute=0, second=0).timestamp()

def timeNormalized(dt):
	'''Retorna la hora normalizada de 0 a 23 de una fecha en formato"'''
	return (dt.hour*60*60 + dt.minute*60 + dt.second) / float(60 * 60)

def dateString(dt):
	return dt.strftime("%Y-%m-%d 00:00:00")

def datesToTimestamp(dateString):
	'''Retorna la fecha Dates en formato "%Y-%m-%d %H:%M:%S" a TimeStamp
	que es la cantidad de segundos que pasaron desde el 1/1/1970'''
	dt = datetime.strptime(str(dateString),"%Y-%m-%d %H:%M:%S")
	dt = pacific.localize(dt)
	return int(dt.strftime("%s"))

def reemplazarComillasSimplesPorEspacios(descriptString):
	return descriptString.replace("'", " ")

def esDiaNoche(row):
	if row['SunriseNormalized'] < row['TimeNormalized'] <= row['SunsetNormalized']:
		return 'Day'
	else:
		return 'Night'

def coordinate(row):
	return '('+str(row['X'])+','+str(row['Y'])+')'

def dateTimeToDate(dateTime):
	date = dateTime[0:10]
	return date

def dateTimeToYear(dateTime):
	year = dateTime[0:4]
	return year
	
def dateTimeToMonth(dateTime):
	month = dateTime[5:7]
	return month
	
def dateTimeToDay(dateTime):
	day = dateTime[8:10]
	return day

def timeToTimeNormalized(time):
	hora = int(time[0:2])
	minuto = int(time[3:5])
	segundo = int(time[6:8])
	timeNormalized = (hora * 60 * 60 + minuto * 60 + segundo) / float(60 * 60)
	return timeNormalized

def dateTimeToTimeNormalized(dateTime):
	timeNormalized = timeToTimeNormalized(dateTime[11:19])
	return timeNormalized

def testDateTimeVsDateTimeTimestampBool(row):
	#print row['DateTimeTimestamp']
	dt = datetime.fromtimestamp(row['DateTimeTimestamp'])
	dateTimeStampStr = dt.strftime("%Y-%m-%d %H:%M:%S")
	date = row['DateTime']
	#print  date, dateTimeStampStr
	if date == dateTimeStampStr:
		return True
	else:
		print ('No coinciden:', date, dateTimeStampStr)
		return False

def testDateTimeVsDateTimeTimestamp(path):
	df = pd.DataFrame.from_csv(path, header=0, sep=',', index_col=False)
	#Creamos una col que dice si paso el test
	df['testDateTimeVsDateTimestamp'] = df.apply(testDateTimeVsDateTimeTimestampBool, axis=1)
	if len(df[df['testDateTimeVsDateTimestamp']==False].index) > 0:
		print('Fallo el testDateTimeVsDateTimeTimestamp')
	else:
		print('Paso el testDateTimeVsDateTimeTimestamp')

def dateTimeToDateTimeTimestamp(dateTime):
	#dt = datetime.totimestamp(dateTime)
	dt = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
	dateTimeTimestamp = int(dt.strftime("%s"))
	return dateTimeTimestamp

def genSSSR_normalized(pathInput, pathOutput):
	dfSunsetSunrise = pd.DataFrame.from_csv(pathInput, header=0, sep=',', index_col=False)
	dfSunsetSunrise['SunriseNormalized'] = dfSunsetSunrise['Sunrise'].apply(timeToTimeNormalized)
	dfSunsetSunrise['SunsetNormalized'] = dfSunsetSunrise['Sunset'].apply(timeToTimeNormalized)
	dfSunsetSunrise.to_csv(pathOutput, sep=',', index=False, header=True)

def genCantidadDeCrimenesPorCoordenada(pathTrainFiltered, pathTestFiltered, pathCantidadCrimenesPorCoordenada):
	t0 = time.clock()

	dfTrainFiltered = pd.DataFrame.from_csv(pathTrainFiltered, header=0, sep=',', index_col=False)
	dfTestFiltered = pd.DataFrame.from_csv(pathTestFiltered, header=0, sep=',', index_col=False)

	lsCoordenadaTrain = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrainFiltered, 'Coordinate');
	lsCoordenadaTest = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTestFiltered, 'Coordinate');
	lsCoordenada = lsCoordenadaTrain+lsCoordenadaTest

	t1 = time.clock()

	cols = ['Train', 'Test']
	fils = lsCoordenada
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	df = pd.DataFrame(zero_data, index=fils ,columns=cols)

	print ('Cantidad de fechas Train:',len(lsCoordenadaTrain))
	print ('Cantidad de fechas Test:',len(lsCoordenadaTest))
	print ('Cantidad de fechas en Total:',len(lsCoordenada))

	df['Train'] = dfTrainFiltered.groupby('Coordinate').size()
	df['Test'] = dfTestFiltered.groupby('Coordinate').size()
	#Completamos los NANS con 0
	df.fillna(0, inplace=True)
	df = df.sort(['Train', 'Test'], ascending=False)
	df.drop_duplicates(inplace=True)
	#Seteamos el nombre del index
	df.index.names = ['Coordenada']
	print df
	df.to_csv(pathCantidadCrimenesPorCoordenada, sep=',', index=True, header=True)#, encoding='UTF-8')
	print pathCantidadCrimenesPorCoordenada, 'generado.'

	t2 = time.clock()

	print('Tiempo de lectura del test.csv, train.csv y juntarlos:', str(t1-t0))
	print('Tiempo de generar el cant crimenes por coordenada.csv:', str(t2-t1))
	print('Tiempo Total:', str(t2-t0))

def genCantidadDeCrimenesPorDia(pathTrainFiltered, pathTestFiltered, pathCantidadCrimenesPorDia):
	t0 = time.clock()

	dfTrainFiltered = pd.DataFrame.from_csv(pathTrainFiltered, header=0, sep=',', index_col=False)
	dfTestFiltered = pd.DataFrame.from_csv(pathTestFiltered, header=0, sep=',', index_col=False)

	lsDateTrain = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrainFiltered, 'Date');
	lsDateTest = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTestFiltered, 'Date');
	lsDate = lsDateTrain+lsDateTest
	lsDate.sort()

	t1 = time.clock()

	cols = ['Train', 'Test']
	fils = lsDate
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	df = pd.DataFrame(zero_data, index=fils ,columns=cols)

	print ('Cantidad de fechas Train:',len(lsDateTrain))
	print ('Cantidad de fechas Test:',len(lsDateTest))
	print ('Cantidad de fechas en Total:',len(lsDate))

	df['Train'] = dfTrainFiltered.groupby('Date').size()
	df['Test'] = dfTestFiltered.groupby('Date').size()
	#Completamos los NANS con 0
	df.fillna(0, inplace=True)

	#Seteamos el nombre del index
	df.index.names = ['Date']
	print df
	df.to_csv(pathCantidadCrimenesPorDia, sep=',', index=True, header=True)#, encoding='UTF-8')
	print pathCantidadCrimenesPorDia, 'generado.'

	t2 = time.clock()

	print('Tiempo de lectura del test.csv, train.csv y juntarlos:', str(t1-t0))
	print('Tiempo de generar el cant crimenes.csv:', str(t2-t1))
	print('Tiempo Total:', str(t2-t0))

def genTrainFiltered(pathTrain, pathTrainFiltered, pathSSSRNormalized):
	t0 = time.clock()

	print('Comienza lectura de los dataframes contenidos en '+ pathTrain, pathSSSRNormalized)

	#Genero el dataframe a partir del csv train
	dfTrain = pd.DataFrame.from_csv(pathTrain, header=0, sep=',', index_col=False)
	dfSunsetSunrise = pd.DataFrame.from_csv(pathSSSRNormalized, header=0, sep=',', index_col=False)
	#Otra forma de leer un csv
	#dfSunsetSunrise = pd.read_table("csv/sssr-normalized.csv", sep=",")

	t1 = time.clock()

	print('Comienza la edicion del dataframe')
	#Renombramos Dates por Date
	dfTrain.rename(columns={'Dates':'DateTime'}, inplace=True)

	#Creamos la columna Date
	dfTrain['Date'] = dfTrain['DateTime'].apply(dateTimeToDate)

	#Creamos la columna TimeNormalized
	dfTrain['TimeNormalized'] = dfTrain['DateTime'].apply(dateTimeToTimeNormalized)

	#Creamos la columna DateTimeTimestamp
	dfTrain['DateTimeTimestamp'] = dfTrain['DateTime'].apply(dateTimeToDateTimeTimestamp)

	#Agregamos la timezone de SF
	#dfTrain['DatesTimestamp'] = dfTrain['Dates'].apply(localizeDatesYmdHMS)

	#Creamos la columna TimeNormalized (debe ir antes de modificar las fechas)
	#dfTrain['TimeNormalized'] = dfTrain['DatesTimestamp'].apply(timeNormalized)

	#Creamos la columna DatesTimeStamp sin la hora
	#dfTrain['DatesTimestamp'] = dfTrain['DatesTimestamp'].apply(dateNormalized)

	#Creamos la columna DatesTimeStamp sin la hora
	#dfTrain['Date'] = dfTrain['DatesTimestamp'].apply(dateString)



	#Creamos la columna DayLight
	dfTrain = pd.merge(dfTrain, dfSunsetSunrise, on='Date', how='left')
	dfTrain['Daylight'] = dfTrain.apply(esDiaNoche, axis=1)
	dfTrain.drop(['Sunset','Sunrise','SunsetNormalized','SunriseNormalized'], axis=1, inplace=True)

	##Creamos la columna ClimateDisaster
	##dfClimateDisaster['Dates'] = dfClimateDisaster['Dates'].apply(localizeDatesYdm)
	##dfClimateDisaster['Dates'] = dfClimateDisaster['Dates'].apply(dateNormalized)
	##dfMerged = pd.merge(dfMerged, dfClimateDisaster, on='Dates', how='left')

	#Correccion de Coordenadas Anomalas
	dfTrain = correccionDeCoordenadasAnomalas(dfTrain)

	#Creamos la columna XY
	dfTrain['Coordinate'] = dfTrain.apply(coordinate, axis=1)

	#Reemplazamos los caracteres en las descripciones de los crimenes "'" y los reemplazamos por " " para no generar conflictos con el Weka
	dfTrain['Descript'] = dfTrain['Descript'].apply(reemplazarComillasSimplesPorEspacios)

	t2 = time.clock()

	print('Comienza la escritura del '+pathTrainFiltered)
	dfTrain.to_csv(pathTrainFiltered, sep=',', index=False, header=True)#, encoding='UTF-8')
	t3 = time.clock()

	print('Tiempo de lectura del train.csv:', str(t1-t0))
	print('Tiempo de edicion del dataframe:', str(t2-t1))
	print('Tiempo de escritura del train-filtered.csv:', str(t3-t2))
	print('Tiempo Total:', str(t3-t0))


def genTrainFilteredV2(pathTrain, pathTrainFilteredV2, pathSSSRNormalized):
	t0 = time.clock()

	print('Comienza lectura de los dataframes contenidos en '+ pathTrain, pathSSSRNormalized)

	#Genero el dataframe a partir del csv train
	dfTrain = pd.DataFrame.from_csv(pathTrain, header=0, sep=',', index_col=False)
	dfSunsetSunrise = pd.DataFrame.from_csv(pathSSSRNormalized, header=0, sep=',', index_col=False)
	#Otra forma de leer un csv
	#dfSunsetSunrise = pd.read_table("csv/sssr-normalized.csv", sep=",")

	t1 = time.clock()

	print('Comienza la edicion del dataframe')
	#Renombramos Dates por Date
	dfTrain.rename(columns={'Dates':'DateTime'}, inplace=True)

	#Creamos la columna Date
	dfTrain['Date'] = dfTrain['DateTime'].apply(dateTimeToDate)

	#Creamos la columna Year
	dfTrain['Year'] = dfTrain['DateTime'].apply(dateTimeToYear)
	
	#Creamos la columna Month
	dfTrain['Month'] = dfTrain['DateTime'].apply(dateTimeToMonth)
	
	#Creamos la columna Day
	dfTrain['Day'] = dfTrain['DateTime'].apply(dateTimeToDay)

	#Creamos la columna TimeNormalized
	dfTrain['TimeNormalized'] = dfTrain['DateTime'].apply(dateTimeToTimeNormalized)

	#Creamos la columna DateTimeTimestamp
	dfTrain['DateTimeTimestamp'] = dfTrain['DateTime'].apply(dateTimeToDateTimeTimestamp)

	#Creamos la columna DayLight
	dfTrain = pd.merge(dfTrain, dfSunsetSunrise, on='Date', how='left')
	dfTrain['Daylight'] = dfTrain.apply(esDiaNoche, axis=1)
	dfTrain.drop(['Sunset','Sunrise','SunsetNormalized','SunriseNormalized'], axis=1, inplace=True)

	##Creamos la columna ClimateDisaster
	##dfClimateDisaster['Dates'] = dfClimateDisaster['Dates'].apply(localizeDatesYdm)
	##dfClimateDisaster['Dates'] = dfClimateDisaster['Dates'].apply(dateNormalized)
	##dfMerged = pd.merge(dfMerged, dfClimateDisaster, on='Dates', how='left')

	#Correccion de Coordenadas Anomalas
	dfTrain = correccionDeCoordenadasAnomalas(dfTrain)

	#Creamos la columna XY
	dfTrain['Coordinate'] = dfTrain.apply(coordinate, axis=1)

	#Reemplazamos los caracteres en las descripciones de los crimenes "'" y los reemplazamos por " " para no generar conflictos con el Weka
	dfTrain['Descript'] = dfTrain['Descript'].apply(reemplazarComillasSimplesPorEspacios)

	#Dropeamos Descript, PdDistrict, Address y Resolution
	dfTrain.drop(['Descript','PdDistrict','Address','Resolution','DateTime','Date','Category','DayOfWeek','Daylight','Coordinate'], axis=1, inplace=True)
	#dfTrain.drop(['Descript','Address','Resolution','DateTime','Date','Category','Daylight',], axis=1, inplace=True)

	t2 = time.clock()
	print dfTrain
	
	print('Comienza la escritura del '+pathTrainFilteredV2)
	dfTrain.to_csv(pathTrainFilteredV2, sep=',', index=False, header=True)#, encoding='UTF-8')
	t3 = time.clock()

	print('Tiempo de lectura del train.csv:', str(t1-t0))
	print('Tiempo de edicion del dataframe:', str(t2-t1))
	print('Tiempo de escritura del train-filtered.csv:', str(t3-t2))
	print('Tiempo Total:', str(t3-t0))


def genTestFiltered(pathTest, pathTestFiltered, pathSSSRNormalized):
	t0 = time.clock()

	print('Comienza lectura de los dataframes contenidos en '+ pathTest, pathSSSRNormalized)

	#Genero el dataframe a partir del csv train
	dfTest = pd.DataFrame.from_csv(pathTest, header=0, sep=',', index_col=False)
	dfSunsetSunrise = pd.DataFrame.from_csv(pathSSSRNormalized, header=0, sep=',', index_col=False)
	#Otra forma de leer un csv
	#dfSunsetSunrise = pd.read_table("csv/sssr-normalized.csv", sep=",")

	t1 = time.clock()

	print('Comienza la edicion del dataframe')
	#Renombramos Dates por Date
	dfTest.rename(columns={'Dates':'DateTime'}, inplace=True)

	#Creamos la columna Date
	dfTest['Date'] = dfTest['DateTime'].apply(dateTimeToDate)

	#Creamos la columna TimeNormalized
	dfTest['TimeNormalized'] = dfTest['DateTime'].apply(dateTimeToTimeNormalized)

	#Creamos la columna DateTimeTimestamp
	dfTest['DateTimeTimestamp'] = dfTest['DateTime'].apply(dateTimeToDateTimeTimestamp)

	#Creamos la columna DayLight
	dfTest = pd.merge(dfTest, dfSunsetSunrise, on='Date', how='left')
	dfTest['Daylight'] = dfTest.apply(esDiaNoche, axis=1)
	dfTest.drop(['Sunset','Sunrise','SunsetNormalized','SunriseNormalized'], axis=1, inplace=True)

	##Creamos la columna ClimateDisaster
	##dfClimateDisaster['Dates'] = dfClimateDisaster['Dates'].apply(localizeDatesYdm)
	##dfClimateDisaster['Dates'] = dfClimateDisaster['Dates'].apply(dateNormalized)
	##dfMerged = pd.merge(dfMerged, dfClimateDisaster, on='Dates', how='left')

	#Correccion de Coordenadas Anomalas
	dfTest = correccionDeCoordenadasAnomalas(dfTest)

	#Creamos la columna XY
	dfTest['Coordinate'] = dfTest.apply(coordinate, axis=1)

	#Reemplazamos los caracteres en las descripciones de los crimenes "'" y los reemplazamos por " " para no generar conflictos con el Weka
	#dfTest['Descript'] = dfTest['Descript'].apply(reemplazarComillasSimplesPorEspacios)

	t2 = time.clock()

	print('Comienza la escritura del '+pathTestFiltered)
	dfTest.to_csv(pathTestFiltered, sep=',', index=False, header=True)#, encoding='UTF-8')
	t3 = time.clock()

	print('Tiempo de lectura del test.csv:', str(t1-t0))
	print('Tiempo de edicion del dataframe:', str(t2-t1))
	print('Tiempo de escritura del test-filtered.csv:', str(t3-t2))

	print('Tiempo Total:', str(t3-t0))

def genVDM_AtributoCategorico(pathTrainFiltered, atributoCategorico):
	dfTrainFiltered = pd.DataFrame.from_csv(pathTrainFiltered, header=0, sep=',', index_col=False)
	lsAtributoCategorico = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrainFiltered, atributoCategorico)
	lsCategory = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrainFiltered, 'Category')

	#df tiene P(atributoCategorico|Category)
	zero_data = np.zeros(shape=(len(lsAtributoCategorico),len(lsCategory))) #Inicializo en 0
	df = pd.DataFrame(zero_data, index=lsAtributoCategorico ,columns=lsCategory)

	zero_data = np.zeros(shape=(len(lsAtributoCategorico),len(['Cantidad']))) #Inicializo en 0
	dftmp2 = pd.DataFrame(zero_data, index=lsAtributoCategorico ,columns=['Cantidad'])

	for categoria in lsCategory:
		print categoria
		dftmp1 = dfTrainFiltered[dfTrainFiltered['Category'] == categoria]
		nCrimenesCategory = float(len(dftmp1.index))
		dftmp2['Cantidad'] = dftmp1.groupby(atributoCategorico).size()
		dftmp2['Cantidad'].fillna(0, inplace=True)
		dftmp2 = dftmp2 / nCrimenesCategory
		df[categoria] = dftmp2['Cantidad']
	print df
	df.to_csv('csv/VDM/prob'+atributoCategorico+'TalqueCategory.csv', sep=',', index=True, header=True)

def genVDM_AtributoCategorico2(pathTrainFiltered, atributoCategorico):
	dfTrainFiltered = pd.DataFrame.from_csv(pathTrainFiltered, header=0, sep=',', index_col=False)
	lsAtributoCategorico = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrainFiltered, atributoCategorico)
	lsCategory = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrainFiltered, 'Category')

	#df tiene P(Category|atributoCategorico)
	zero_data = np.zeros(shape=(len(lsCategory),len(lsAtributoCategorico))) #Inicializo en 0
	df = pd.DataFrame(zero_data, index=lsCategory ,columns=lsAtributoCategorico)

	zero_data = np.zeros(shape=(len(lsCategory),len(['Cantidad']))) #Inicializo en 0
	dftmp2 = pd.DataFrame(zero_data, index=lsCategory ,columns=['Cantidad'])

	for valor in lsAtributoCategorico:
		print valor
		dftmp1 = dfTrainFiltered[dfTrainFiltered[atributoCategorico] == valor]
		nCrimenesAtributoCategorico = float(len(dftmp1.index))
		dftmp2['Cantidad'] = dftmp1.groupby('Category').size()
		dftmp2['Cantidad'].fillna(0, inplace=True)
		dftmp2 = dftmp2 / nCrimenesAtributoCategorico
		df[valor] = dftmp2['Cantidad']
	print df
	df.to_csv('csv/VDM/probCategoryTalque'+atributoCategorico+'.csv', sep=',', index=True, header=True)

def main():
	pathTrain = 'csv/train.csv'
	pathTest = 'csv/test.csv'
	pathTrainFiltered = 'csv/train-filtered-pandas.csv'
	pathTrainFilteredV2 = 'csv/train-filtered-pandasV2.csv'
	pathTestFiltered = 'csv/test-filtered-pandas.csv'
	pathSSSR = 'csv/sssr.csv'
	pathSSSRNormalized = 'csv/sssr-normalized.csv'
	pathCantidadCrimenesPorDia = 'csv/Cantidad de crimenes por dia.csv'
	pathCantidadCrimenesPorCoordenada = 'csv/Cantidad de crimenes por coordenada.csv'

	#Genero sssr-normalized.csv
	#genSSSR_normalized(pathSSSR, pathSSSRNormalized)

	#Genero el train-filtered.csv
	#genTrainFiltered(pathTrain, pathTrainFiltered, pathSSSRNormalized)

	#Genero el train-filteredV2.csv
	#genTrainFilteredV2(pathTrain, pathTrainFilteredV2, pathSSSRNormalized)
	df = pd.DataFrame.from_csv(pathTrainFilteredV2, header=0, sep=',', index_col=False)
	#df.drop(['Year','Month','Day','TimeNormalized','DateTimeTimestamp'], axis=1, inplace=True)
	
	print df
	#print 'PCA..'
	#results = PCA(df)
	#print 'results..'
	#print results.fracs
	#print 'resultsfracs..'
	
	#Normalizar columnas
	#df[['X','Y','Year','Month','Day','TimeNormalized','DateTimeTimestamp']] = df[['X','Y','Year','Month','Day','TimeNormalized','DateTimeTimestamp']].apply(lambda x: (x - x.mean()) / (x.max() - x.min()))
	
	#print df
	#print 'PCA..'
	#results = PCA(df)
	#print 'results..'
	#print results.fracs
	#print 'resultsfracs..'

	#Genero el test-filtered.csv
	#genTestFiltered(pathTest, pathTestFiltered, pathSSSRNormalized)

	#Testeo si se puede recuperar correctamente el timestamp
	#testDateTimeVsDateTimeTimestamp(pathTrainFiltered)

	#Genero 'Cantidad de crimenes por dia.csv'
	#genCantidadDeCrimenesPorDia(pathTrainFiltered, pathTestFiltered, pathCantidadCrimenesPorDia)
	#genCantidadDeCrimenesPorCoordenada(pathTrainFiltered, pathTestFiltered, pathCantidadCrimenesPorCoordenada)

	#Genero los VDM
	#genVDM_AtributoCategorico(pathTrainFiltered, 'Daylight')
	#genVDM_AtributoCategorico(pathTrainFiltered, 'Resolution')
	#genVDM_AtributoCategorico(pathTrainFiltered, 'Descript')
	#genVDM_AtributoCategorico(pathTrainFiltered, 'Coordinate')
	#genVDM_AtributoCategorico(pathTrainFiltered, 'DayOfWeek')

	#genVDM_AtributoCategorico2(pathTrainFiltered, 'Daylight')
	#genVDM_AtributoCategorico2(pathTrainFiltered, 'Resolution')
	#genVDM_AtributoCategorico2(pathTrainFiltered, 'Descript')
	#genVDM_AtributoCategorico2(pathTrainFiltered, 'Coordinate')
	#genVDM_AtributoCategorico2(pathTrainFiltered, 'DayOfWeek')

if __name__ == "__main__":
	main()
	print("Done.")
