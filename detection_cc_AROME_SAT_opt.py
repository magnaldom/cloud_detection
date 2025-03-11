#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:52:43 2021

@author: magnaldom

Algorithme de détection ciel clair en se basant sur la nébulosité en sortie d'AROME et non sur le flux au sol'
"""

import numpy as np
import netCDF4 as nc
from netCDF4 import Dataset
from datetime import datetime, timedelta
import sys; sys.path.insert(0,'/cnrm/phynh/data1/magnaldom/Outils')
from plot_AROME import plot_AROME, plot_AROME_var, plot_AROME_var_cumul
from zenith_angle import zenith_angle_ephem
import math
import time



def dcc_AROME_SAT_cumul_zone(arome, date, lon, lat, M, N, K, fn_lim):
	annee = date.year
	mois = date.month
	jour = date.day
	h = date.hour

	debut_boucle = time.time()


	nebul_h	= np.sum(arome.variables["ATMONEBUL_TOTALE"][h,M-K:M+K+1,N-K:N+K+1])
	nebul_h_1 = np.sum(arome.variables["ATMONEBUL_TOTALE"][h-1,M-K:M+K+1,N-K:N+K+1])


	#print("Temps de boucle csd_a zone", time.time()-debut_boucle)


	csd = 0
	nebul_tot = (nebul_h - nebul_h_1)/(2*K+1)**2/3600
	#print(nebul_tot)
	if nebul_tot>fn_lim:
		csd = 1

	return  csd, nebul_tot

def dcc_AROME_SAT_cumul_zone_assim(arome, date, lon, lat, M, N, K, fn_lim):
	annee = date.year
	mois = date.month
	jour = date.day
	h = date.hour

	debut_boucle = time.time()


	nebul_h	= np.sum(arome.variables["ATMONEBUL_TOTALE"][h,M-K:M+K+1,N-K:N+K+1])


	#print("Temps de boucle csd_a zone", time.time()-debut_boucle)


	csd = 0
	nebul_tot = (nebul_h)/(2*K+1)**2/3600
	#print(nebul_tot)
	if nebul_tot>fn_lim:
		csd = 1

	return  csd, nebul_tot

def dcc_AROME_SAT_cumul_zone_ins(arome, date, lon, lat, M, N, K, fn_lim):
	annee = date.year
	mois = date.month
	jour = date.day
	h = date.hour

	debut_boucle = time.time()


	nebul_h	= np.sum(arome.variables["ATMONEBUL_TOTALE"][h,M-K:M+K+1,N-K:N+K+1])
	nebul_h_1 = np.sum(arome.variables["ATMONEBUL_TOTALE"][h-1,M-K:M+K+1,N-K:N+K+1])
	nebul_h_ins	= np.sum(arome.variables["SURFNEBUL_TOTALE"][h,M-K:M+K+1,N-K:N+K+1])


	#print("Temps de boucle csd_a zone", time.time()-debut_boucle)


	csd = 0
	nebul_tot = (nebul_h - nebul_h_1)/(2*K+1)**2/3600
	nebul_tot_ins = (nebul_h_ins)/(2*K+1)**2
	#print("nebul ins", nebul_tot_ins)
	#print(nebul_tot)
	if nebul_tot>fn_lim:
		csd = 1

	return  csd, nebul_tot, nebul_tot_ins

def fournearestpoints_AROME(lon,lat, M,N):

	fichier = "/cnrm/phynh/data1/magnaldom/STOCKAGE_AROME_UP/DATA/202008/AROME_20200801.nc"

	arome1250m = Dataset(fichier, "r", format="NETCDF4")

	latt = arome1250m.variables["Latitude"][:]
	lont = arome1250m.variables["Longitude"][:]


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


#	print("lecture hp5", end-start)
#	print(latt[M,N], lont[M,N],latt[M1,N1], lont[M1,N1], latt[M2,N2], lont[M2,N2], latt[M3,N3], lont[M3,N3],lat, lon)

	return M1, N1, M2, N2, M3, N3

#for d in  range(1,2):
#	date = datetime(2020,8,d)
#	print(date)
#	lon = 1.37883
#	lat = 43.621
#	M =675
#	N = 499
#	#date_a, csd, zen, ghi, nebul = dcc_AROME_SAT_cumul(date, lon, lat, M, N)
#	#print(csd)
#	date_a, csd, zen, ghi, nebul = dcc_AROME_SAT_inst(date, lon, lat, M, N)
#	print(csd)


