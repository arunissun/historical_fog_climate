# importing necessary libraries

import warnings

import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.mpl.ticker as cticker
from cartopy.util import add_cyclic_point
import cartopy.feature as cfeature
from matplotlib.colors import LogNorm, Normalize,NoNorm,PowerNorm,TwoSlopeNorm
from matplotlib.transforms import offset_copy

# setting the path and file name
path ='/Volumes/WINDOWS/GIS_FILES/'
fname='elev_ens_0.1deg_reg_v25.0e.nc'

# open the dataset and setting the lons and lats of Europe
ds=xr.open_dataset(path+fname)
lat_min = 44
lat_max = 50
lon_min = 12.5
lon_max = 27
europe = [-25, 45, 34, 70]

# function for creating the map scale
def drow_the_scale(y,x,text,length = 1.5,lw = 5,alpha = 0.5):
    #Draw scale function
    # y represents the latitude of the scale bar
    # x represents the longitude at the beginning of the scale
    # text represents the last scale value of the scale bar
    # Length represents the length of the scale bar in longitude
    # lw represents the width of the scale bar
    step = length/5     #Calculate the step size and draw five grids
    #Draw five black and white lines
    ax.hlines(y=y,xmin=x,         xmax=x + step,  colors="black", ls="-", lw=lw,transform=ccrs.Geodetic())
    ax.hlines(y=y,xmin=x + step,  xmax=x + step*2,colors="white", ls="-", lw=lw,transform=ccrs.Geodetic())
    ax.hlines(y=y,xmin=x + step*2,xmax=x + step*3,colors="black", ls="-", lw=lw,transform=ccrs.Geodetic())
    ax.hlines(y=y,xmin=x + step*3,xmax=x + step*4,colors="white", ls="-", lw=lw,transform=ccrs.Geodetic())
    ax.hlines(y=y,xmin=x + step*4,xmax=x + step*5,colors="black", ls="-", lw=lw,transform=ccrs.Geodetic())
    #Draw two long scales
    ax.vlines(x = x,          ymin = y - (lw/100) *3, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.Geodetic())
    ax.vlines(x = x + length, ymin = y - (lw/100) *3, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.Geodetic())
    #Draw four segments
    ax.vlines(x = x + step,   ymin = y - (lw/100) *2, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.Geodetic())
    ax.vlines(x = x + step*2, ymin = y - (lw/100) *2, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.Geodetic())
    ax.vlines(x = x + step*3, ymin = y - (lw/100) *2, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.Geodetic())
    ax.vlines(x = x + step*4, ymin = y - (lw/100) *2, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.Geodetic())
    #Writing, 0500 km
    ax.text(x +alpha +1,           y -(lw/100)*7-1,'0', horizontalalignment = 'center',transform =  text_transform,fontsize = 15)
    ax.text(x +length+alpha+2,    y -(lw/100)*7-1,'500',horizontalalignment = 'center',transform =  text_transform,fontsize = 15)
    ax.text(x +alpha + length/2+1,y +(lw/100)*2+1,'km',horizontalalignment = 'center', transform = text_transform,fontsize = 15)

## function for borders
def drowscale(extent,scale_y,scale_x,scale_text,step = 5,lw = 10,scale_length = 1.5,scale_lw = 5,scale_alpha = 0.5):
        
    # Draw a map with black and white borders and scale bars
    # Ext: indicates the latitude and longitude around [west, east, south, north]
    # scale_y,scale_x,scale_text: represents the position, latitude, longitude and scale value of the scale bar
    # Step: represents the step length, and a grid represents several longitudes and latitudes
    # lw: represents the width of the border
    # scale_length: represents the length of the scale bar (in longitude, for example, 1.5 longitudes)
    # scale_lw: represents the width of the scale bar
    for y in [extent[2],extent[3]] :#Draw the upper and lower borders
        xmin = extent[0]
        while (xmin < extent[1]):
            plt.hlines(y=y,xmin=xmin,xmax=xmin+step,colors="white", ls="-", lw=lw,transform = ccrs.Geodetic())
            xmin = xmin+step*2
        xmin = extent[0]+step
        while (xmin < extent[1]):
            plt.hlines(y=y,xmin=xmin,xmax=xmin+step,colors="black", ls="-", lw=lw,transform = ccrs.Geodetic())
            xmin = xmin+step*2
    for x in [extent[0],extent[1]] :#Draw left and right
        ymin = extent[2]
        while (ymin < extent[3]):
            plt.vlines(x = x, ymin = ymin, ymax = ymin+step, colors="black", ls="-", lw=lw,transform = ccrs.Geodetic())
            ymin = ymin+step*2
        ymin = extent[2]+step
        while (ymin < extent[3]):
            plt.vlines(x = x, ymin = ymin, ymax = ymin+step, colors="white", ls="-", lw=lw,transform = ccrs.Geodetic())
            ymin = ymin+step*2
    drow_the_scale(scale_y,scale_x,scale_text,scale_length,scale_lw,scale_alpha)

# Make the figure larger
fig = plt.figure(figsize=(20,20))

# Set the axes using the specified map projection
ax=plt.axes(projection=ccrs.Mercator())

# Make a filled contour plot
dem = ax.pcolormesh(ds['longitude'], ds['latitude'], ds['elevation'],
            transform = ccrs.PlateCarree(),cmap = plt.cm.terrain, norm = LogNorm(vmin = 1,vmax = 4000))
#ax.set_extent([lon_min, lon_max, lat_min, lat_max])
ax.set_extent([europe[0],europe[1],europe[2],europe[3]])
# Add coastlines

ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAKES,linewidth = 2)
ax.add_feature(cfeature.RIVERS,linewidth = 2)
ax.add_feature(cfeature.OCEAN)


#add colorbar
cb = plt.gcf().colorbar(dem, pad=0.075,extend = 'both',shrink = 0.5)
cb.ax.tick_params(labelsize=20)
cb.set_label('terrain height [m]',fontsize = 20)


gl = ax.gridlines(crs = ccrs.PlateCarree(),draw_labels=True, color='black', alpha=0.2, linestyle='--')
gl.xlabel_style = {'size': 20, 'color': 'black'}
gl.ylabel_style = {'size': 20, 'color': 'black'}
ax.text(40,69.5,u'\u25B2 \nN ', ha='center', fontsize=20, 
            family='Arial', rotation = 0,transform = ccrs.PlateCarree())

geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
text_transform = offset_copy(geodetic_transform, units='dots', x=-25)
drow_the_scale(40,-20,'200',length = 5.9,lw = 5,alpha = 0.5)
lon0,lon1,lat0,lat1 = [14, 27, 44, 50]
box_x = [lon0, lon1, lon1, lon0, lon0]
box_y = [lat0, lat0, lat1, lat1, lat0]
ax.plot(box_x, box_y, color='red',  transform= ccrs.PlateCarree())

plt.show()