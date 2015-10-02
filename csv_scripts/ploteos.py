from math import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import time
import Image

#import prettyplotlib as ppl

#Esto va con matplotlib 1.4
matplotlib.style.use('ggplot')
#%matplotlib inline

#SUNSETSUNRISE
def plotSunsetSunrise_01():
	"""Horario de Amanecer y Atardecer a lo largo de un periodo anual"""
	#Convertimos Dates a formato de fechas para ploteo
	df = dfSunsetSunrise
	df['Date'] = pd.to_datetime(df['Date'])

	df = df.set_index(df['Date'])
	df = df.drop('Date',1)
	
	print df

	ax = df['2003-01-01':'2003-12-31'].plot(kind='line',linewidth=4.0, figsize=(8, 6), ylim=(0,24), title='Horario de Amanecer y Atardecer a lo largo de un periodo anual')
	ax.set_xlabel("")
	ax.set_ylabel("Hora")
	plt.savefig("Ploteos/Matplotlib/Sunset Sunrise/Horario de Amanecer y Atardecer a lo largo de un periodo anual.png")
	plt.cla()
	plt.clf()
	plt.close()
	
def plotSunsetSunrise_02():
	"""Relacion entre el horario de Amanecer y Atardecer"""
	#Convertimos Dates a formato de fechas para ploteo
	df = dfSunsetSunrise
	df['Date'] = pd.to_datetime(df['Date'])

	df = df.set_index(df['Date'])
	df = df.drop('Date',1)
	
	print df
	
	#Con las correcciones de fran deberia completarse la linea faltante
	ax = df['2003-01-01':'2003-12-31'].plot(kind='line', x='SunriseNormalized', y='SunsetNormalized',linewidth=4.0 , xlim=(5.5,8.5), figsize=(8, 6), title='Relacion entre el horario de Amanecer y Atardecer')
	ax.set_xlabel("Horario Amanecer (hs)")
	ax.set_ylabel("Horario Atardecer (hs)")
	#plt.axis('equal')
	plt.savefig("Ploteos/Matplotlib/Sunset Sunrise/Relacion entre el horario de Amanecer y Atardecer.png")
	plt.cla()
	plt.clf()
	plt.close()


#COORDENADAS
def plotCoordenadas_01():
	"""Coordenadas de todos los crimenes"""
	#Respetar los xlim ylim y figsize para mantener la escala
	ax = dfTrain.plot(kind='scatter', x='X', y='Y', xlim=(-122.52,-122.36), ylim=(37.705,37.825), figsize=(10, 9), s=3, c='k', title='Coordenadas de todos los crimenes')
	#ax.grid(True)
	#plt.axis('equal')
	plt.savefig("Ploteos/Matplotlib/Coordenadas de todos los crimenes.png")
	plt.cla()
	plt.clf()
	plt.close()
	
def plotCoordenadas_02():
	"""Histograma de coordenadas de crimenes"""
	#Respetar los xlim ylim y figsize para mantener la escala
	#dfTrain.plot(kind='hexbin', x='X', y='Y', gridsize=50, colormap='RdYlGn_r', figsize=(10, 6), title='Histograma en coordenadas de todos los crimenes')
	ax = dfTrain.plot(kind='hexbin', x='X', y='Y', gridsize=200, colormap='gist_stern', figsize=(12, 9), xlim=(-122.52,-122.36), ylim=(37.705,37.825), title='Histograma de coordenadas de crimenes')
	#plt.axis('equal')
	ax.set_axis_bgcolor('k')
	ax.grid(color='k')
	
	
	#im = Image.open('Ploteos/SF grid corte Gmaps.png')
	#height = im.size[1]
	#width = im.size[0]
	#box = ax.get_position()
	#fig = plt.figure()
	#fig.figimage(im, box.x0, box.y0)
	#fig.savefig('Ploteos/temp.png', dpi=80)
	#box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	
	plt.savefig("Ploteos/Matplotlib/Histograma de coordenadas de crimenes.png")
	plt.cla()
	plt.clf()
	plt.close()

def plotCoordenadas_03():
	"""Histograma de coordenadas de crimenes para cada categoria"""
		#Respetar los xlim ylim y figsize para mantener la escala
	for categoria in lsCategory:
		ax = dfTrain[dfTrain['Category']==categoria].plot(kind='hexbin', x='X', y='Y', gridsize=200, colormap='gist_stern', figsize=(12, 9), xlim=(-122.52,-122.36), ylim=(37.705,37.825), title='Histograma de coordenadas de crimenes para la categoria '+str(categoria).replace('/','-'))
		#plt.axis('equal')
		ax.set_axis_bgcolor('k')
		ax.grid(color='k')
		
		box = ax.get_position()
		#ax.set_position([box.x0, box.y0, box.width, box.height])
		#ax.set_position([box.x0, box.y0, box.width, box.width])
		
		plt.savefig("Ploteos/Matplotlib/Histograma de coordenadas de crimenes para cada categoria/"+str(categoria).replace('/','-')+".png")
		plt.cla()
		plt.clf()
		plt.close()

def plotCoordenadas_04(): #BUG, tengo que usar el sistema de colores por grupo para arreglarlo
	"""Coordenadas de todos los crimenes por distrito"""
	df = pd.DataFrame.from_csv("csv/train-filtered.csv", header=0, sep=',', index_col=False, encoding='UTF-8')
	df.plot(kind='scatter', x='X', y='Y', c='PdDistrict', figsize=(10, 8), title='Coordenadas de todos los crimenes')
	plt.axis('equal')
	plt.savefig("Ploteos/Matplotlib/Coordenadas de todos los crimenes por distrito.png")
	plt.cla()
	plt.clf()
	plt.close()

def plotCoordenadas_05():
	"""Histograma de coordenadas de crimenes sin los crimenes del Hall of Justice"""
	#Respetar los xlim ylim y figsize para mantener la escala
	#dfTrain.plot(kind='hexbin', x='X', y='Y', gridsize=50, colormap='RdYlGn_r', figsize=(10, 6), title='Histograma en coordenadas de todos los crimenes')
	df = dfTrain[dfTrain['(X,Y)']!='(-122.403404791,37.7754207067)']
	ax = df.plot(kind='hexbin', x='X', y='Y', gridsize=200, colormap='gist_stern', figsize=(12, 9), xlim=(-122.52,-122.36), ylim=(37.705,37.825), title='Histograma de crimenes sin los crimenes del Hall of Justice')
	#plt.axis('equal')
	ax.set_axis_bgcolor('k')
	ax.grid(color='k')
	
	
	#im = Image.open('Ploteos/SF grid corte Gmaps.png')
	#height = im.size[1]
	#width = im.size[0]
	#box = ax.get_position()
	#fig = plt.figure()
	#fig.figimage(im, box.x0, box.y0)
	#fig.savefig('Ploteos/temp.png', dpi=80)
	#box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	
	plt.savefig("Ploteos/Matplotlib/Histograma de crimenes sin los crimenes del Hall of Justice.png")
	plt.cla()
	plt.clf()
	plt.close()

def plotCoordenadas_06():
	"""Histograma de coordenadas de crimenes para cada categoria sin los crimenes del Hall of Justice"""
		#Respetar los xlim ylim y figsize para mantener la escala
	
	df = dfTrain[dfTrain['(X,Y)']!='(-122.403404791,37.7754207067)']
	for categoria in lsCategory:
		ax = df[df['Category']==categoria].plot(kind='hexbin', x='X', y='Y', gridsize=200, colormap='gist_stern', figsize=(12, 9), xlim=(-122.52,-122.36), ylim=(37.705,37.825), title='Histograma de coordenadas de crimenes para la categoria '+str(categoria).replace('/','-')+' sin los crimenes del Hall of Justice')
		#plt.axis('equal')
		ax.set_axis_bgcolor('k')
		ax.grid(color='k')
		
		box = ax.get_position()
		#ax.set_position([box.x0, box.y0, box.width, box.height])
		#ax.set_position([box.x0, box.y0, box.width, box.width])
		
		plt.savefig("Ploteos/Matplotlib/Histograma de coordenadas de crimenes para cada categoria sin los crimenes del Hall of Justice/"+str(categoria).replace('/','-')+".png")
		plt.cla()
		plt.clf()
		plt.close()

#CANTIDAD DE CRIMENES DE CADA ATRIBUTO
def plotCantidadDeCrimenesDeCadaAtributo_01():
	"""Cantidad de crimenes en cada hora"""
	df2 = pd.DataFrame({'Cantidad de Crimenes':np.zeros(shape=(len(lsHora)))}, index=lsHora)

	#Le hacemos floor a todas las horas
	dfTmp = dfTrain
	dfTmp['TimeNormalized'] = dfTrain['TimeNormalized'].apply(lambda hora: int(floor(hora)))
	
	for hora in lsHora:
		cantCrimenesEnEsaHora = len(dfTmp[dfTmp['TimeNormalized']==hora].index)
		df2.ix[hora,'Cantidad de Crimenes'] = cantCrimenesEnEsaHora

	print df2

	ax = df2.plot(kind='bar', figsize=(10, 6), width=0.8, title='Cantidad de crimenes en cada hora')
	#ax.set_ylabel("Cantidad de Crimenes")
	ax.set_xlabel("Hora")
	plt.setp(ax.get_xticklabels(), rotation="horizontal")
	plt.savefig("Ploteos/Matplotlib/Cantidad de crimenes en cada hora.png")
	plt.cla()
	plt.clf()
	plt.close()

def plotCantidadDeCrimenesDeCadaAtributo_02():
	"""Cantidad de crimenes en cada dia de la semana"""
	df2 = pd.DataFrame({'Cantidad de Crimenes':np.zeros(shape=(len(lsDayOfWeek)))}, index=lsDayOfWeek)
	
	for diaDeLaSemana in lsDayOfWeek:
		cantCrimenesEnElDiaDeLaSemana = len(dfTrain[dfTrain['DayOfWeek']==diaDeLaSemana].index)
		df2.ix[diaDeLaSemana,'Cantidad de Crimenes'] = cantCrimenesEnElDiaDeLaSemana

	print df2
	
	ax = df2.plot(kind='bar', figsize=(10, 6), width=0.8, title='Cantidad de crimenes en cada dia de la semana')
	
	#Colocar label, investigar..
	#ppl.bar(ax, annotate=True)

	plt.setp(ax.get_xticklabels(), rotation="horizontal")
	plt.savefig("Ploteos/Matplotlib/Cantidad de crimenes en cada dia de la semana-.png")

	plt.cla()
	plt.clf()
	plt.close()
	
def plotCantidadDeCrimenesDeCadaAtributo_03():
	"""Cantidad de crimenes de cada categoria"""
	df2 = pd.DataFrame({'Cantidad de Crimenes':np.zeros(shape=(len(lsCategory)))}, index=lsCategory)

	for categoria in lsCategory:
		cantCrimenesEnEsaCategoria = len(dfTrain[dfTrain['Category']==categoria].index)
		df2.ix[categoria,'Cantidad de Crimenes'] = cantCrimenesEnEsaCategoria

	#df2 = df2.sort(columns='Cantidad de Crimenes', ascending=False)	
	print df2
	
	ax = df2.plot(kind='barh', figsize=(10, 6), width=0.8, title='Cantidad de crimenes de cada categoria')
	#ax.set_ylabel("Crimenes", fontsize=40)
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Cantidad de crimenes de cada categoria.png")
	plt.cla()
	plt.clf()
	plt.close()

def plotCantidadDeCrimenesDeCadaAtributo_07():
	"""Cantidad de crimenes de cada categoria en escala logaritmica"""
	df2 = pd.DataFrame({'Cantidad de Crimenes':np.zeros(shape=(len(lsCategory)))}, index=lsCategory)

	for categoria in lsCategory:
		cantCrimenesEnEsaCategoria = len(dfTrain[dfTrain['Category']==categoria].index)
		df2.ix[categoria,'Cantidad de Crimenes'] = cantCrimenesEnEsaCategoria

	df2 = df2.sort(columns='Cantidad de Crimenes', ascending=False)	
	print df2
	
	ax = df2.plot(kind='barh', logx=True, figsize=(10, 6), width=0.8, title='Cantidad de crimenes de cada categoria (Ordenado) en escala logaritmica')
	#ax.set_ylabel("Crimenes", fontsize=40)
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Cantidad de crimenes de cada categoria (Ordenado) en escala logaritmica.png")
	plt.cla()
	plt.clf()
	plt.close()
	
def plotCantidadDeCrimenesDeCadaAtributo_04():
	"""Cantidad de crimenes de cada distrito"""
	df2 = pd.DataFrame({'Cantidad de Crimenes':np.zeros(shape=(len(lsPdDistrict)))}, index=lsPdDistrict)

	for distrito in lsPdDistrict:
		cantCrimenesEnElDistrito = len(dfTrain[dfTrain['PdDistrict']==distrito].index)
		df2.ix[distrito,'Cantidad de Crimenes'] = cantCrimenesEnElDistrito

	df2 = df2.sort(columns='Cantidad de Crimenes', ascending=False)
	print df2
	
	ax = df2.plot(kind='barh', figsize=(10, 6), width=0.8, title='Cantidad de crimenes de cada distrito')
	#ax.set_ylabel("Crimenes", fontsize=40)
	plt.setp(ax.get_yticklabels(), fontsize=12)
	plt.savefig("Ploteos/Matplotlib/Cantidad de crimenes de cada distrito.png")
	plt.cla()
	plt.clf()
	plt.close()

def plotCantidadDeCrimenesDeCadaAtributo_05():
	"""Cantidad de crimenes de cada categoria de la coordenada (-122.403404791,37.7754207067)"""
	df2 = pd.DataFrame({'Cantidad de Crimenes':np.zeros(shape=(len(lsCategory)))}, index=lsCategory)
	dfTrainFiltered = dfTrain[dfTrain['(X,Y)'] == '(-122.403404791,37.7754207067)']
	for categoria in lsCategory:
		cantCrimenesEnEsaCategoria = len(dfTrainFiltered[dfTrainFiltered['Category']==categoria].index)
		df2.ix[categoria,'Cantidad de Crimenes'] = cantCrimenesEnEsaCategoria

	#df2 = df2.sort(columns='Cantidad de Crimenes', ascending=False)	
	print df2
	
	ax = df2.plot(kind='barh', figsize=(10, 6), width=0.8, title='Cantidad de crimenes de cada categoria de la coordenada (-122.403404791,37.7754207067)')
	#ax.set_ylabel("Crimenes", fontsize=40)
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Cantidad de crimenes de cada categoria de la coordenada (-122.403404791,37.7754207067).png")
	plt.cla()
	plt.clf()
	plt.close()	

def plotCantidadDeCrimenesDeCadaAtributo_06():
	"""Cantidad de crimenes de cada categoria (Ordenado)"""
	df2 = pd.DataFrame({'Cantidad de Crimenes':np.zeros(shape=(len(lsCategory)))}, index=lsCategory)

	for categoria in lsCategory:
		cantCrimenesEnEsaCategoria = len(dfTrain[dfTrain['Category']==categoria].index)
		df2.ix[categoria,'Cantidad de Crimenes'] = cantCrimenesEnEsaCategoria

	df2 = df2.sort(columns='Cantidad de Crimenes', ascending=False)	
	print df2
	
	ax = df2.plot(kind='barh', figsize=(10, 6), width=0.8, title='Cantidad de crimenes de cada categoria (Ordenado)')
	#ax.set_ylabel("Crimenes", fontsize=40)
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Cantidad de crimenes de cada categoria (Ordenado).png")
	plt.cla()
	plt.clf()
	plt.close()

#Crimenes de un atributo en funcion de otro atributo
def plot8():
	"""Crimenes de cada categoria en funcion del dia de la semana"""
	zero_data = np.zeros(shape=(len(lsDayOfWeek),len(lsCategory))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=lsDayOfWeek, columns=lsCategory)	

	for categoria in lsCategory:
		dftmp1 = dfTrain[dfTrain['Category']==categoria]
		for dia in lsDayOfWeek:
			df2.ix[dia,categoria] = len(dftmp1[dftmp1['DayOfWeek']==dia].index)
		
		print df2[categoria]	
		
		ax = df2[categoria].plot(kind='bar', figsize=(10, 6), title="Crimenes de la categoria "+str(categoria).replace('/','-') +" en funcion del dia de la semana")
		plt.setp(ax.get_xticklabels(), rotation="horizontal")
		plt.savefig("Ploteos/Matplotlib/Categoria en funcion del dia de la semana/"+str(categoria).replace('/','-') +".png")
		plt.cla()
		plt.clf()
		plt.close()

def plot9():
	"""Crimenes de cada categoria en funcion de la hora del dia"""
	zero_data = np.zeros(shape=(len(lsHora),len(lsCategory))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=lsHora, columns=lsCategory)	

	for categoria in lsCategory:
		dftmp1 = dfTrain[dfTrain['Category']==categoria]
		#'Equivalente' a hacer int(floor(Hora)))
		dftmp1['TimeNormalized'] = dftmp1['TimeNormalized']-dftmp1['TimeNormalized']%1
		for hora in lsHora:
			df2.ix[hora,categoria] = len(dftmp1[dftmp1['TimeNormalized']==hora].index)
		print df2[categoria]	
		
		ax = df2[categoria].plot(kind='bar', figsize=(10, 6), title="Crimenes de la categoria "+str(categoria).replace('/','-') +" en funcion de la hora del dia")
		plt.setp(ax.get_xticklabels(), rotation="horizontal")
		plt.savefig("Ploteos/Matplotlib/Categoria en funcion de la hora del dia/"+str(categoria).replace('/','-') +".png")
		plt.cla()
		plt.clf()
		plt.close()

def plot10():
	"""Crimenes de cada categoria en funcion de daylight"""
	zero_data = np.zeros(shape=(len(lsDaylight),len(lsCategory))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=lsDaylight, columns=lsCategory)
	
	for categoria in lsCategory:
		dftmp1 = dfTrain[dfTrain['Category']==categoria]
		for daylight in lsDaylight:
			df2.ix[daylight,categoria] = len(dftmp1[dftmp1['Daylight']==daylight].index)
		print df2[categoria]	
		
		ax = df2[categoria].plot(kind='bar', figsize=(10, 6), title="Crimenes de la categoria "+str(categoria).replace('/','-') +" en funcion de daylight")
		plt.setp(ax.get_xticklabels(), rotation="horizontal")
		plt.savefig("Ploteos/Matplotlib/Categoria en funcion de daylight/"+str(categoria).replace('/','-') +".png")
		plt.cla()
		plt.clf()
		plt.close()

def plot11():
	"""Crimenes de cada categoria en funcion de resolution"""
	zero_data = np.zeros(shape=(len(lsResolution),len(lsCategory))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=lsResolution ,columns=lsCategory)
		
	for categoria in lsCategory:
		dftmp1 = dfTrain[dfTrain['Category']==categoria]
		for resolucion in lsResolution:
			df2.ix[resolucion,categoria] = len(dftmp1[dftmp1['Resolution']==resolucion].index)
		print df2[categoria]	
		
		ax = df2[categoria].plot(kind='barh', figsize=(10, 6), title="Crimenes de la categoria "+str(categoria).replace('/','-') +" en funcion de resolution")
		plt.setp(ax.get_xticklabels(), rotation="horizontal")
		plt.setp(ax.get_yticklabels(), fontsize=5)
		plt.savefig("Ploteos/Matplotlib/Categoria en funcion de resolution/"+str(categoria).replace('/','-') +".png")
		plt.cla()
		plt.clf()
		plt.close()

def plot12():
	"""Crimenes de cada resolution en funcion de la categoria"""
	zero_data = np.zeros(shape=(len(lsCategory),len(lsResolution))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=lsCategory ,columns=lsResolution)
		
	for resolucion in lsResolution:
		dftmp1 = dfTrain[dfTrain['Resolution']==resolucion]
		for categoria in lsCategory:
			df2.ix[categoria,resolucion] = len(dftmp1[dftmp1['Category']==categoria].index)
		print df2[resolucion]	
		
		ax = df2[resolucion].plot(kind='barh', figsize=(10, 6), title="Crimenes de cada resolution "+str(resolucion).replace('/','-') +" en funcion de categoria")
		plt.setp(ax.get_xticklabels(), rotation="horizontal")
		plt.setp(ax.get_yticklabels(), fontsize=5)
		plt.savefig("Ploteos/Matplotlib/Resolution en funcion de categoria/"+str(resolucion).replace('/','-') +".png")
		plt.cla()
		plt.clf()
		plt.close()


#PORCENTAJES
def plot13():
	"""Porcentaje de crimenes a la luz del dia en funcion de la categoria"""
	cols = ['Ratio Crimenes Diurnos', 'Ratio Crimenes Nocturnos']
	fils = lsCategory
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=fils ,columns=cols)

	for fil in fils:	
		dftmp1 = dfTrain[dfTrain['Category'] == fil]
		dftmp2 = dftmp1[dftmp1['Daylight'] == 'Day']
		nCrimenesTot = len(dftmp1.index)
		nCrimenesDia = len(dftmp2.index)
		print fil, nCrimenesTot, nCrimenesDia
		if nCrimenesTot!=0:
			porcentajeDia = nCrimenesDia/float(nCrimenesTot)*100		
		else: #Solucion poco satisfactoria
			porcentaje = 0.5*100
		df2.ix[fil,'Ratio Crimenes Diurnos'] = porcentajeDia
		df2.ix[fil,'Ratio Crimenes Nocturnos'] = 100-porcentajeDia
	df3 = df2.sort(columns='Ratio Crimenes Diurnos', ascending=False)
	ax = df3.plot(kind='barh', xlim=(0,100), figsize=(10, 6), width=0.999, color=('#79ccff','#223038'), stacked=True, title="Porcentaje de crimenes a la luz del dia en funcion de la categoria")
	plt.setp(ax.get_xticklabels(), rotation="horizontal")
	plt.axvline(50, color='k') #Dibujamos el divisor de dia noche
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Porcentaje de crimenes a la luz del dia en funcion de la categoria.png")
	plt.cla()
	plt.clf()
	plt.close()
	
def plot14():
	"""Porcentaje de crimenes a la luz del dia en funcion del distrito"""
	cols = ['Ratio Crimenes Diurnos', 'Ratio Crimenes Nocturnos']
	fils = lsPdDistrict
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=fils ,columns=cols)
		
	for fil in fils:	
		dftmp1 = dfTrain[dfTrain['PdDistrict'] == fil]
		dftmp2 = dftmp1[dftmp1['Daylight'] == 'Day']
		nCrimenesTot = len(dftmp1.index)
		nCrimenesDia = len(dftmp2.index)
		print fil, nCrimenesTot, nCrimenesDia
		if nCrimenesTot!=0:
			porcentajeDia = nCrimenesDia/float(nCrimenesTot)*100		
		else:
			porcentaje = 0.5*100
		df2.ix[fil,'Ratio Crimenes Diurnos'] = porcentajeDia
		df2.ix[fil,'Ratio Crimenes Nocturnos'] = 100-porcentajeDia
	df3 = df2.sort(columns='Ratio Crimenes Diurnos', ascending=False)
	ax = df3.plot(kind='barh', xlim=(0,100), figsize=(10, 6), width=0.999, color=('#79ccff','#223038'), stacked=True, title="Porcentaje de crimenes a la luz del dia en funcion del distrito")
	plt.setp(ax.get_xticklabels(), rotation="horizontal")
	plt.axvline(50, color='k') #Dibujamos el divisor de dia noche
	plt.savefig("Ploteos/Matplotlib/Porcentaje de crimenes a la luz del dia en funcion del distrito.png")
	plt.cla()
	plt.clf()
	plt.close()

def plot15():
	"""Porcentaje de crimenes a la luz del dia en funcion de la resolucion"""
	df = pd.DataFrame.from_csv("csv/train-filtered.csv", header=0, sep=',', index_col=False, encoding='UTF-8')
	
	cols = ['Ratio Crimenes Diurnos', 'Ratio Crimenes Nocturnos']
	#Obtenemos todos los casos de PdDistrict que se encuentran en el csv.
	dffils = df['Resolution'].drop_duplicates()
	fils = []
	for i, row in enumerate(dffils.values):
		print i, row
		fils.append(row)
	
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=fils ,columns=cols)
		
	for i in range(len(fils)):	
		dftmp1 = df[df['Resolution'] == fils[i]]
		dftmp2 = dftmp1[dftmp1['Daylight'] == 'Day']
		nCrimenesTot = len(dftmp1.index)
		nCrimenesDia = len(dftmp2.index)
		print fils[i], nCrimenesTot, nCrimenesDia
		if nCrimenesTot!=0:
			porcentajeDia = nCrimenesDia/float(nCrimenesTot)*100		
		else:
			porcentaje = 0.5*100
		df2['Ratio Crimenes Diurnos'][i] = porcentajeDia
		df2['Ratio Crimenes Nocturnos'][i] = 100-porcentajeDia
	df3 = df2.sort(columns='Ratio Crimenes Diurnos', ascending=False)
	ax = df3.plot(kind='barh', xlim=(0,100), figsize=(10, 6), width=0.999, color=('#79ccff','#223038'), stacked=True, title="Porcentaje de crimenes a la luz del dia en funcion de la resolucion")
	plt.setp(ax.get_xticklabels(), rotation="horizontal")
	plt.setp(ax.get_yticklabels(), fontsize=4)
	plt.axvline(50, color='k') #Dibujamos el divisor de dia noche
	plt.savefig("Ploteos/Matplotlib/Porcentaje de crimenes a la luz del dia en funcion de la resolucion.png")
	plt.cla()
	plt.clf()
	plt.close()

def plot17():
	"""Porcentaje de crimenes segun la hora en funcion de la categoria"""	
	cols = lsHora #Aca va el ratio
	fils = lsCategory
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=fils ,columns=cols)

	for i in range(len(fils)):	
		dftmp1 = df[df['Category'] == fils[i]]
		dftmp1['Time'] = dftmp1['Time']-dftmp1['Time']%1
		nCrimenesTot = len(dftmp1.index)
		for j in cols:
			dftmp2 = dftmp1[dftmp1['Time'] == j]
			nCrimenesDeLaHoraJ = len(dftmp2.index)
			print fils[i], nCrimenesTot, nCrimenesDeLaHoraJ
			if nCrimenesTot!=0:
				porcentajeHoraJ = nCrimenesDeLaHoraJ/float(nCrimenesTot)*100		
			else:
				print 'Estas al horno'
			df2[j][i] = porcentajeHoraJ
	#df3 = df2.sort(columns='Ratio Crimenes Diurnos', ascending=False)
	#color=('#79ccff','#223038'),
	ax = df2.plot(kind='barh', xlim=(0,100), figsize=(10, 6), colormap='Set2', width=0.999, stacked=True, title="Porcentaje de crimenes segun la hora en funcion de la categoria")
	plt.setp(ax.get_xticklabels(), rotation="horizontal")

	# Shrink current axis by 20%
	#box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	# Put a legend to the right of the current axis
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)

	
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Porcentaje de crimenes segun la hora en funcion de la categoria.png")
	plt.cla()
	plt.clf()
	plt.close()

def plot18():
	"""Porcentaje de crimenes segun la categoria en funcion de resolution"""
	zero_data = np.zeros(shape=(len(lsResolution),len(lsCategory))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=lsResolution ,columns=lsCategory)

	for resolucion in lsResolution:
		dftmp1 = dfTrain[dfTrain['Resolution'] == resolucion]
		nCrimenesTot = len(dftmp1.index)
		for categoria in lsCategory:
			dftmp2 = dftmp1[dftmp1['Category'] == categoria]
			nCrimenesDeLaCategoria = len(dftmp2.index)
			porcentajeCategoria = nCrimenesDeLaCategoria/float(nCrimenesTot)*100
			print categoria, nCrimenesTot, nCrimenesDeLaCategoria
			df2.ix[resolucion,categoria] = porcentajeCategoria

	ax = df2.plot(kind='barh', xlim=(0,100), figsize=(10, 6), colormap='Set2', width=0.999, stacked=True, title="Porcentaje de crimenes segun la categoria en funcion de resolution")
	plt.setp(ax.get_xticklabels(), rotation="horizontal")

	# Shrink current axis by 20%
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
	# Put a legend to the right of the current axis
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=6)

	
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Porcentaje de crimenes segun la categoria en funcion de resolution.png")
	plt.cla()
	plt.clf()
	plt.close()

def plot18bis():
	"""Porcentaje de crimenes segun la categoria en funcion de ClimateDisaster"""
	zero_data = np.zeros(shape=(len(lsClimateDisaster),len(lsCategory))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=lsClimateDisaster, columns=lsCategory)

	for desastreClimatico in lsClimateDisaster:
		dftmp1 = dfTrain[dfTrain['ClimateDisaster'] == desastreClimatico]
		nCrimenesTot = len(dftmp1.index)
		for categoria in lsCategory:
			dftmp2 = dftmp1[dftmp1['Category'] == categoria]
			nCrimenesDeLaCategoria = len(dftmp2.index)
			porcentajeCategoria = nCrimenesDeLaCategoria/float(nCrimenesTot)*100
			print categoria, nCrimenesTot, nCrimenesDeLaCategoria
			df2.ix[desastreClimatico,categoria] = porcentajeCategoria

	print df2
	ax = df2.plot(kind='barh', xlim=(0,100), figsize=(10, 6), colormap='Set2', width=0.999, stacked=True, title="Porcentaje de crimenes segun la categoria en funcion de ClimateDisaster")
	plt.setp(ax.get_xticklabels(), rotation="horizontal")

	# Shrink current axis by 20%
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
	# Put a legend to the right of the current axis
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=6)

	
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Porcentaje de crimenes segun la categoria en funcion de ClimateDisaster.png")
	plt.cla()
	plt.clf()
	plt.close()

def plot19():
	"""Porcentaje de crimenes segun la categoria en funcion de Hora"""
	zero_data = np.zeros(shape=(len(lsHora),len(lsCategory))) #Inicializo en 0
	df2 = pd.DataFrame(zero_data, index=lsHora ,columns=lsCategory)

	for hora in lsHora:
		dftmp1 = dfTrain
		dftmp1['Time'] = dftmp1['Time']-dftmp1['Time']%1
		dftmp2 = dftmp1[dftmp1['Time'] == hora]
		print dftmp2

		nCrimenesTot = len(dftmp2.index)
		print nCrimenesTot
		
		for categoria in lsCategory:
			dftmp3 = dftmp2[dftmp2['Category'] == categoria]
			nCrimenesDeLaCategoria = len(dftmp3.index)
			try:
				porcentajeCategoria = nCrimenesDeLaCategoria/float(nCrimenesTot)*100
				print categoria, nCrimenesTot, nCrimenesDeLaCategoria
				df2.ix[hora,categoria] = porcentajeCategoria
			except:
				'Error'

	ax = df2.plot(kind='barh', xlim=(0,100), figsize=(10, 6), colormap='Set2', width=0.999, stacked=True, title="Porcentaje de crimenes segun la categoria en funcion de Hora")
	plt.setp(ax.get_xticklabels(), rotation="horizontal")

	# Shrink current axis by 20%
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
	# Put a legend to the right of the current axis
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=6)

	
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Porcentaje de crimenes segun la categoria en funcion de Hora.png")
	plt.cla()
	plt.clf()
	plt.close()

def plot20():
	#Cantidad de crimenes por dia en un periodo anual (2003)
	df = pd.DataFrame.from_csv("csv/Cantidad de crimenes por dia.csv", header=0, sep=',', index_col=False, encoding='UTF-8')

	df['Date'] = pd.to_datetime(df['Date'])
	df = df.set_index(df['Date'])
	df = df.drop('Date',1)
	
	print df
	lsAnios = [2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015]
	for anio in lsAnios:	
		ax = df[str(anio)+'-01-01':str(anio)+'-12-31'].plot(kind='area', ylim=(0,600), figsize=(10, 6), title='Cantidad de crimenes por dia en un periodo anual ('+str(anio)+')')
		#ax.set_ylabel("Cantidad de Crimenes")
		ax.set_xlabel("")
		plt.setp(ax.get_xticklabels(), rotation="horizontal")
		plt.savefig('Ploteos/Matplotlib/Cantidad de crimenes de por dia en un periodo anual/'+str(anio)+'.png')
		plt.cla()
		plt.clf()
		plt.close()
		
def plot22():
	#Cantidad de crimenes por dia en diciembre (2003)
	df = pd.DataFrame.from_csv("csv/Cantidad de crimenes por dia.csv", header=0, sep=',', index_col=False, encoding='UTF-8')

	df['Date'] = pd.to_datetime(df['Date'])
	df = df.set_index(df['Date'])
	df = df.drop('Date',1)
	
	print df
	lsAnios = [2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015]
	for anio in lsAnios:	
		ax = df[str(anio)+'-12-01':str(anio)+'-12-31'].plot(kind='area', ylim=(0,600), figsize=(10, 6), title='Cantidad de crimenes por dia en diciembre ('+str(anio)+')')
		#ax.set_ylabel("Cantidad de Crimenes")
		ax.set_xlabel("")
		plt.setp(ax.get_xticklabels(), rotation="horizontal")
		plt.savefig('Ploteos/Matplotlib/Cantidad de crimenes por dia en diciembre/'+str(anio)+'.png')
		plt.cla()
		plt.clf()
		plt.close()

def plot21(): #BUG
	#Cantidad de crimenes por dia en un periodo anual (2003)	
	df = dfTrain[dfTrain['Category'] == 'SUICIDE']
	cols = ['Cantidad de crimenes'] #Aca va el ratio	
	fils = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(df, 'Date')
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	dfPlot = pd.DataFrame(zero_data, index=fils ,columns=cols)
	
	df['Date'] = pd.to_datetime(df['Date'])
	df = df.set_index(df['Date'])
	df = df.drop('Date',1)
	
	print df
	lsAnios = [2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015]
	for anio in lsAnios:	
		categoria = 'SUICIDE'
		ax = df[str(anio)+'-01-01':str(anio)+'-12-31'].plot(kind='area', ylim=(0,50), figsize=(10, 6), title='Cantidad de crimenes de la categoria '+str(categoria).replace('/','-')+' por dia en un periodo anual ('+str(anio)+')')
		#ax.set_ylabel("Cantidad de Crimenes")
		ax.set_xlabel("")
		plt.setp(ax.get_xticklabels(), rotation="horizontal")
		plt.savefig('Ploteos/Matplotlib/Cantidad de crimenes de la categoria ' + str(categoria).replace('/','-') +' por dia en un periodo anual/'+str(anio)+'.png')
		plt.cla()
		plt.clf()
		plt.close()


#MEDIAS
def plotMediasPorDiaDeCrimenes_01():
	"""Media de Cantidad de crimenes de cada categoria por dia en el Train"""
	cols = ['Average'] #Aca va el ratio
	fils = lsCategory
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	dfPlot = pd.DataFrame(zero_data, index=fils ,columns=cols)
	
	df = dfTrain
	cantDiasConCrimen = getCantDias(df)
	print 'cantDiasConCrimen:', cantDiasConCrimen

	for categoria in lsCategory:
		dfCategory = df[df['Category']==categoria]
		cantCrimenesEnEsaCategoria = len(df[df['Category']==categoria].index)
		average = cantCrimenesEnEsaCategoria/float(cantDiasConCrimen)
		dfPlot.ix[categoria,'Average'] = average

	print dfPlot
	
	ax = dfPlot.plot(kind='barh', figsize=(10, 6), width=0.8, title='Media de Cantidad de crimenes de cada categoria por dia en el Train')
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Media de Cantidad de crimenes de cada categoria por dia en el Train.png")
	plt.cla()
	plt.clf()
	plt.close()

def plotMediasPorDiaDeCrimenes_02():
	"""Media de Cantidad de crimenes de cada categoria por dia en la coordenada (-122.403404791,37.7754207067)"""
	cols = ['Average'] #Aca va el ratio
	fils = lsCategory
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	dfPlot = pd.DataFrame(zero_data, index=fils ,columns=cols)
	
	df = dfTrain[dfTrain['(X,Y)'] == '(-122.403404791,37.7754207067)']
	
	cantDiasConCrimen = getCantDias(df)
	print 'cantDiasConCrimen:', cantDiasConCrimen

	for categoria in lsCategory:
		dfCategory = df[df['Category']==categoria]
		cantCrimenesEnEsaCategoria = len(df[df['Category']==categoria].index)
		average = cantCrimenesEnEsaCategoria/float(cantDiasConCrimen)
		dfPlot.ix[categoria,'Average'] = average

	print dfPlot
	
	ax = dfPlot.plot(kind='barh', figsize=(10, 6), width=0.8, title='Media de Cantidad de crimenes de cada categoria por dia en la coordenada (-122.403404791,37.7754207067)')
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Media de Cantidad de crimenes de cada categoria por dia en la coordenada (-122.403404791,37.7754207067).png")
	plt.cla()
	plt.clf()
	plt.close()
	
def plotMediasPorDiaDeCrimenes_03():
	"""Media de Cantidad de crimenes de cada categoria por dia el dia 2014-10-30"""
	cols = ['Average'] #Aca va el ratio
	fils = lsCategory
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	dfPlot = pd.DataFrame(zero_data, index=fils ,columns=cols)
	
	df = dfTrain[dfTrain['Date'] == '2014-10-30']
	
	cantDiasConCrimen = getCantDias(df)
	print 'cantDiasConCrimen:', cantDiasConCrimen

	for categoria in lsCategory:
		dfCategory = df[df['Category']==categoria]
		cantCrimenesEnEsaCategoria = len(df[df['Category']==categoria].index)
		average = cantCrimenesEnEsaCategoria/float(cantDiasConCrimen)
		dfPlot.ix[categoria,'Average'] = average

	print dfPlot
	
	ax = dfPlot.plot(kind='barh', figsize=(10, 6), width=0.8, title='Media de Cantidad de crimenes de cada categoria por dia el dia 2014-10-30')
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Media de Cantidad de crimenes de cada categoria por dia el dia 2014-10-30.png")
	plt.cla()
	plt.clf()
	plt.close()

def plotMediasPorDiaDeCrimenes_04():
	"""Media de Cantidad de crimenes de cada categoria por dia el dia 2014-12-25"""
	cols = ['Average'] #Aca va el ratio
	fils = lsCategory
	zero_data = np.zeros(shape=(len(fils),len(cols))) #Inicializo en 0
	dfPlot = pd.DataFrame(zero_data, index=fils ,columns=cols)
	
	df = dfTrain[dfTrain['Date'] == '2014-12-25']
	
	cantDiasConCrimen = getCantDias(df)
	print 'cantDiasConCrimen:', cantDiasConCrimen

	for categoria in lsCategory:
		dfCategory = df[df['Category']==categoria]
		cantCrimenesEnEsaCategoria = len(df[df['Category']==categoria].index)
		average = cantCrimenesEnEsaCategoria/float(cantDiasConCrimen)
		dfPlot.ix[categoria,'Average'] = average

	print dfPlot
	
	ax = dfPlot.plot(kind='barh', figsize=(10, 6), width=0.8, title='Media de Cantidad de crimenes de cada categoria por dia el dia 2014-12-25')
	plt.setp(ax.get_yticklabels(), fontsize=5)
	plt.savefig("Ploteos/Matplotlib/Media de Cantidad de crimenes de cada categoria por dia el dia 2014-12-25.png")
	plt.cla()
	plt.clf()
	plt.close()

def obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dataframe, columna):
	'''Obtenemos todos los casos de PdDistrict (por ejemplo) que se encuentran en el dataframe.'''	
	#Filtramos las filas y nos quedamos solo las que tienen elementos de la columna 'columna' distintos.
	dfSinDuplicadosDeDistritos = dataframe.drop_duplicates(subset=columna, take_last=True)
	#Convertimos esa columna (serie) en una lista
	lsValues = dfSinDuplicadosDeDistritos[columna].tolist()
	return lsValues

def getCantDias(df):
	ls = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(df, 'Date')
	return len(ls)

def main():
	global dfTrain
	global dfSunsetSunrise
	global dfCantCrimenesPorDia
	global lsHora
	global lsDaylight
	global lsDayOfWeek
	global lsCategory
	global lsResolution
	global lsAddress
	global lsDescript
	global lsPdDistrict
	global lsTuplaXY
	global lsDatesTimeStamp
	
	dfTrain = pd.DataFrame.from_csv("csv/train-filtered-pandas.csv", header=0, sep=',', index_col=False, encoding='UTF-8')
	dfSunsetSunrise = pd.DataFrame.from_csv("csv/sssr-normalized.csv", header=0, sep=',', index_col=False, encoding='UTF-8')
	dfCantCrimenesPorDia = pd.DataFrame.from_csv("csv/Cantidad de crimenes por dia.csv", header=0, sep=',', index_col=False, encoding='UTF-8')

	
	lsHora = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	lsDaylight = ['Day', 'Night']
	lsDayOfWeek = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
	lsCategory = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrain, 'Category')
	lsResolution = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrain, 'Resolution')
	lsAddress = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrain, 'Address')
	lsDescript = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrain, 'Descript')
	lsPdDistrict = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrain, 'PdDistrict')
	lsTuplaXY = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrain, 'Coordinate')
	lsDate = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfTrain, 'Date')
	#lsDatesTimeStampTotales = obtenerTodosLosValoresPosiblesDeUnaColumnaDelDataFrame(dfSunsetSunrise, 'Dates')
			
	#Plots de SunsetSunrise
	#plotSunsetSunrise_01()								#Horario de Amanecer y Atardecer a lo largo de un periodo anual
	#plotSunsetSunrise_02()								#Relacion entre el horario de Amanecer y Atardecer
	
	#Plots de Coordenadas (Los plots de coordenadas tienen el problema que ploteamos Latitud y Longitud y no coordenadas cartesianas)
	#plotCoordenadas_01()								#Coordenadas de todos los crimenes
	#plotCoordenadas_02()								#Histograma de coordenadas de crimenes
	#plotCoordenadas_03()								#Histograma de coordenadas de crimenes para cada categoria
	#plotCoordenadas_04() #BUG							#Coordenadas de todos los crimenes por distrito
	#plotCoordenadas_05()								#Histograma de coordenadas de crimenes sin los crimenes del Hall of Justice
	#plotCoordenadas_06()								#Histograma de coordenadas de crimenes para cada categoria sin los crimenes del Hall of Justice
	
	#Cantidad de crimenes de cada atributo
	#plotCantidadDeCrimenesDeCadaAtributo_01()			#Cantidad de crimenes en cada hora	
	#plotCantidadDeCrimenesDeCadaAtributo_02()			#Cantidad de crimenes en cada dia de la semana
	#plotCantidadDeCrimenesDeCadaAtributo_03()			#Cantidad de crimenes de cada categoria
	#plotCantidadDeCrimenesDeCadaAtributo_04()			#Cantidad de crimenes de cada distrito
	#plotCantidadDeCrimenesDeCadaAtributo_05()			#Cantidad de crimenes de cada categoria de la coordenada (-122.403404791,37.7754207067)
	#plotCantidadDeCrimenesDeCadaAtributo_06()			#Cantidad de crimenes de cada categoria (Ordenado)
	#plotCantidadDeCrimenesDeCadaAtributo_07()			#Cantidad de crimenes de cada categoria (Ordenado) en escala logaritmica

	
	#Crimenes de un atributo en funcion de otro
	#plot8() #L
	#plot9() #L
	#plot10() #L
	#plot11() #L
	#plot12() #L
	
	#Porcentajes
	#plot13()
	#plot14()
	#plot15()
	#plot17()
	#plot18()
	#plot18bis()
	#plot19()
	#plot20()
	#plot21()
	#plot22()

	#Medias
	#plotMediasPorDiaDeCrimenes_01()
	#plotMediasPorDiaDeCrimenes_02()
	#plotMediasPorDiaDeCrimenes_03()
	#plotMediasPorDiaDeCrimenes_04()
	
	
	#a = time.clock()
	#plot8()
	#a = time.clock() - a
	#b = time.clock()
	#plot8_2()
	#b = time.clock() - b
	#print 'Tiempo A:', a
	#print 'Tiempo B:', b
		
if __name__ == "__main__":
	main()
	print "Done."
