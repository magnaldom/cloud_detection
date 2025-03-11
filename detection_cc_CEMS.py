#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:52:43 2021

@author: magnaldom

Algorithme de detection de ciel clair avec le sdonnées SAT de fraction nuageuse CEMS (ctth_effective)
"""
import cProfile
import pstats
import numpy as np
import netCDF4 as nc
from netCDF4 import Dataset
from datetime import datetime, timedelta
import sys; sys.path.insert(0,'/cnrm/phynh/data1/magnaldom/Outils')
from plot_CEMS import plot_CEMS, plot_CEMS_moy, plot_CEMS_moy4points
from zenith_angle import zenith_angle_ephem
from moyenne import moyenne
import math
import h5py
import time
import numpy.ma as ma




def dcc_CEMS_cumul(date, lon, lat, M, N):
#	annee = date.year
#	mois = date.month
#	jour = date.day
#	fichier = "/cnrm/phynh/data1/magnaldom/STOCKAGE_AROME_UP/DATA/%s%s/AROME_%s%s%s.nc" %(str(date.year).zfill(4),str(date.month).zfill(2), str(date.year).zfill(4),str(date.month).zfill(2),str(date.day).zfill(2))

	#date_a, ghi = plot_AROME(M,N,date)
	#date_a, nebul = plot_AROME_var_cumul(M,N, date, 'ATMONEBUL_TOTALE')
	start = time.time()
	date_a, nebul = plot_CEMS_moy(M,N,date,'cma')
	end = time.time()
	#print("temps plot", end-start)

	zen = []
	for i in range(len(date_a)):
		cos_zen = zenith_angle_ephem(lat, lon, date_a[i]+timedelta(minutes = -30))
		zen.append(math.degrees(np.arccos(cos_zen)))

	csd = np.zeros(len(date_a))
	for i in range(len(csd)):
		#print(nebul[i])
		if zen[i]>75:
			csd[i] = np.inf
		else :
			if nebul[i]>0:
				#print("Ya nuage", nebul[i])
				csd[i] = 1
	end2 = time.time()
	#print("temps dcc", end2-start)


	return date_a, csd, zen, nebul

def dcc_CEMS_inst(date, lon, lat, M, N):
#	annee = date.year
#	mois = date.month
#	jour = date.day
#	fichier = "/cnrm/phynh/data1/magnaldom/STOCKAGE_AROME_UP/DATA/%s%s/AROME_%s%s%s.nc" %(str(date.year).zfill(4),str(date.month).zfill(2), str(date.year).zfill(4),str(date.month).zfill(2),str(date.day).zfill(2))

	#date_a, ghi = plot_AROME(M,N,date)
	#date_a, nebul = plot_AROME_var_cumul(M,N, date, 'ATMONEBUL_TOTALE')
	start = time.time()
	date_a, nebul = plot_CEMS(M,N,date,'cma')
	#print(len(nebul))
	end = time.time()
	#print(end-start)

	zen = []
	for i in range(len(date_a)):
		cos_zen = zenith_angle_ephem(lat, lon, date_a[i])#+timedelta(minutes = -30))
		zen.append(math.degrees(np.arccos(cos_zen)))

	csd = np.zeros(len(date_a))
	for i in range(len(csd)):
		#print(nebul[i])
		if zen[i]>75:
			csd[i] = np.inf
		else :
			if nebul[i]>0:
				#print("Ya nuage", nebul[i])
				csd[i] = 1
	csd_h = []
	date_ah = []
	for i in range(len(date_a)):
		if date_a[i].minute == 0:
			date_ah.append(date_a[i])
			csd_h.append(csd[i])
	return date_ah, csd_h, zen, nebul

def dcc_CEMS_cumul_10(date, lon, lat, M, N):
#	annee = date.year
#	mois = date.month
#	jour = date.day
#	fichier = "/cnrm/phynh/data1/magnaldom/STOCKAGE_AROME_UP/DATA/%s%s/AROME_%s%s%s.nc" %(str(date.year).zfill(4),str(date.month).zfill(2), str(date.year).zfill(4),str(date.month).zfill(2),str(date.day).zfill(2))

	#date_a, ghi = plot_AROME(M,N,date)
	#date_a, nebul = plot_AROME_var_cumul(M,N, date, 'ATMONEBUL_TOTALE')
	date_a, nebul = plot_CEMS_moy(M,N,date,'ctth_effectiv')

	zen = []
	for i in range(len(date_a)):
		cos_zen = zenith_angle_ephem(lat, lon, date_a[i]+timedelta(minutes = -30))
		zen.append(math.degrees(np.arccos(cos_zen)))

	csd = np.zeros(len(date_a))
	for i in range(len(csd)):
		#print(nebul[i])
		if zen[i]>75:
			csd[i] = np.inf
		else :
			if nebul[i]>0.1:
				#print("Ya nuage", nebul[i])
				csd[i] = 1
	return date_a, csd, zen, nebul

def fournearestpoints(lon,lat, M,N):
	start = time.time()
	fi_latlon= h5py.File("/cnrm/phynh/data1/magnaldom/CEMS/latlon_+000.0.h5",'r')
	latt = fi_latlon['latitudes']
	lont = fi_latlon['longitudes']
	nlat = len(latt)
	nlon = len(lont[0,:])
	#print(nlon,nlat)
#	LAT_c = np.zeros((nlat,nlon))
#	LON_c = np.zeros((nlat,nlon))
#	for i in range(nlat):
#		for j in range(nlon):
#			LAT_c[i,j] = latt[i,j]
#			LON_c[i,j] = lont[i,j]


#def des quatres points
	M = int(M)
	N = int(N)
	if lon >= lont[M,N]:
		if lat >= latt[M,N]:
			M1 = M
			N1 = N + 1
			M2 = M + 1
			N2 = N + 1
			M3 = M + 1
			N3 = N

		if lat < latt[M,N]:
			M1 = M + 1
			N1 = N
			M2 = M + 1
			N2 = N - 1
			M3 = M
			N3 = N - 1

	if lon < lont[M,N]:
		if lat >= latt[M,N]:
			M1 = M - 1
			N1 = N
			M2 = M - 1
			N2 = N + 1
			M3 = M
			N3 = N + 1

		if lat < latt[M,N]:
			M1 = M
			N1 = N - 1
			M2 = M - 1
			N2 = N - 1
			M3 = M - 1
			N3 = N

	end = time.time()
#	print("lecture hp5", end-start)
#	print(latt[M,N], lont[M,N],latt[M1,N1], lont[M1,N1], latt[M2,N2], lont[M2,N2], latt[M3,N3], lont[M3,N3],lat, lon)

	return M1, N1, M2, N2, M3, N3

def dcc_CEMS_cumul_moypoints(date, lon, lat, M, N, M1, N1, M2,N2, M3, N3):



	date_a, nebul, nebul1, nebul2, nebul3 = plot_CEMS_moy4points(date,"cma", M, N, M1, N1, M2, N2, M3, N3)

	zen = []
	nebul_moy = []
	for i in range(len(date_a)):
		cos_zen = zenith_angle_ephem(lat, lon, date_a[i]+timedelta(minutes = -30))
		zen.append(math.degrees(np.arccos(cos_zen)))

	csd = np.zeros(len(date_a))
	for i in range(len(csd)):
		m = [nebul[i], nebul1[i], nebul2[i], nebul3[i]]
		nebul_moy.append(moyenne(m))
		#print(nebul[i])
		if zen[i]>90:
			csd[i] = np.inf
		else :
			if moyenne(m)>0:
				#print("Ya nuage", nebul[i])
				csd[i] = 1
	return date_a, csd, zen, nebul_moy




#lon =1.37883
#lat = 43.621
#M = 471
#N = 1891
##M = 225 +226
##N = 1610 +305
#M1, N1, M2, N2, M3, N3 = fournearestpoints(lon,lat,M,N)
#
#start = time.time()
#for d in range(1,32):
#	date = datetime(2020,8,d)
#	print(date)
#
##	date_a, csd, zen, ghi, nebul = dcc_AROME_SAT_cumul(date, lon, lat, M, N)
##	print(csd)
#	#date_a, csd, zen, nebul = dcc_CEMS_cumul(date, lon, lat, M, N)
#	date_a, csd, zen, nebul = dcc_CEMS_cumul_moypoints(date, lon, lat, M, N, M1, N1, M2, N2, M3, N3)
#	#date_a, csd2, zen, nebul2 = dcc_CEMS_cumul_moypoints_var(date, lon, lat, M, N, M1, N1, M2, N2, M3, N3, "ctth_effectiv")
#	#print(len(csd))
#	print(csd)
#	#print(csd2)
#end = time.time()
#print(end-start)
#



