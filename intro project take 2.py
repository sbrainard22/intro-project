#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:39:29 2024

@author: seychellebrainard
"""

import netCDF4 as nc
import numpy as np
import xarray as xr
import cmocean
import cartopy.crs as ccrs
from matplotlib import pyplot as plt

fn = '/Users/seychellebrainard/desktop/met/intro_project.nc'
ds = xr.open_mfdataset(fn)




ds_period = ds.sel(time=slice('2015', '2020'))
ds_surface = ds_period['thetao'].isel(depth = 0)
s_amp = ds_surface.max(dim='time') - ds_surface.min(dim='time')
temp_mean = ds_surface.mean(dim='time')


fig, axes = plt.subplots(1, 2, figsize=(12, 5), subplot_kw={'projection': ccrs.LambertConformal()})
#, subplot_kw={'projection': ccrs.AlbersEqualArea()}
# transform=ccrs.PlateCarree()


temp_plot = temp_mean.plot(ax=axes[0], transform=ccrs.PlateCarree())
#plt.title('Mean Temperature at Surface')
axes[0].set_title('Surface Temperature')
#plt.xlabel('Longitude')
axes[0].set_xlabel('Longitude')
#plt.ylabel('latitude')
axes[0].set_ylabel('Latitude')
#colorbar_tempt = plt.colorbar(temp_plot, label = 'Average Temp')
colorbar_temp = plt.colorbar(temp_plot, ax=axes[0], label = "Temperature (°C)")



contour_plot = s_amp.plot.contourf(ax=axes[1], levels=12, transform=ccrs.PlateCarree())
axes[1].set_title('Seasonal Amplitude')
axes[1].set_xlabel('Longitude')
axes[1].set_ylabel('latitude')
#plt.xlabel('Longitude')
#plt.ylabel('Latitude')
#colorbar = plt.colorbar(contour_plot, label='Temperature Amplitude (°C)')
colorbar_amp = plt.colorbar(contour_plot, ax=axes[1], label='Temperature Amplitude (°C)')

plt.tight_layout()
plt.show()









