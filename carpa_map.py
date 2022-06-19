#impoprting necessary libraries
# This script plots the mp of Carpathian Basin
import wradlib as wrl
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
try:
    get_ipython().magic("matplotlib inline")
except:
    plt.ion()
import numpy as np
# Some more matplotlib tools we will need...
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm, Normalize,NoNorm,PowerNorm,TwoSlopeNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
from matplotlib.transforms import offset_copy
import matplotlib.lines as mlines
import matplotlib as mpl
import matplotlib.colors as colors
#set the Wradlib Environment
os.environ["WRADLIB_DATA"] = "/Volumes/WINDOWS/" 
# specifying the file path and file name
path = '/Volumes/WINDOWS/'
file = 'output_SRTMGL3.tif'
## function for drawing scale
##function for scale

def drow_the_scale(y,x,text,length = 1.5,lw = 5,alpha = 0.5):
    #Draw scale function
    # y represents the latitude of the scale bar
    # x represents the longitude at the beginning of the scale
    # text represents the last scale value of the scale bar
    # Length represents the length of the scale bar in longitude
    # lw represents the width of the scale bar
    step = length/5     #Calculate the step size and draw five grids
    #Draw five black and white lines
    ax.hlines(y=y,xmin=x,         xmax=x + step,  colors="black", ls="-", lw=lw,transform=ccrs.PlateCarree())
    ax.hlines(y=y,xmin=x + step,  xmax=x + step*2,colors="white", ls="-", lw=lw,transform=ccrs.PlateCarree())
    ax.hlines(y=y,xmin=x + step*2,xmax=x + step*3,colors="black", ls="-", lw=lw,transform=ccrs.PlateCarree())
    ax.hlines(y=y,xmin=x + step*3,xmax=x + step*4,colors="white", ls="-", lw=lw,transform=ccrs.PlateCarree())
    ax.hlines(y=y,xmin=x + step*4,xmax=x + step*5,colors="black", ls="-", lw=lw,transform=ccrs.PlateCarree())
    #Draw two long scales
    ax.vlines(x = x,          ymin = y - (lw/100) *3, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.PlateCarree())
    ax.vlines(x = x + length, ymin = y - (lw/100) *3, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.PlateCarree())
    #Draw four segments
    ax.vlines(x = x + step,   ymin = y - (lw/100) *2, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.PlateCarree())
    ax.vlines(x = x + step*2, ymin = y - (lw/100) *2, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.PlateCarree())
    ax.vlines(x = x + step*3, ymin = y - (lw/100) *2, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.PlateCarree())
    ax.vlines(x = x + step*4, ymin = y - (lw/100) *2, ymax = y + lw/100, colors="black", ls="-", lw=1,transform=ccrs.PlateCarree())
    #Writing, 0500 km
    ax.text(x +alpha,           y - (lw/100) *7,'0', horizontalalignment = 'center',transform =  ccrs.PlateCarree(),fontsize = 15)
    ax.text(x +length+alpha,  y - (lw/100) *7,text,horizontalalignment = 'center',transform =    ccrs.PlateCarree(),fontsize = 15)
    ax.text(x +alpha + length/2,y + (lw/100)*2 ,'km',horizontalalignment = 'center', transform = ccrs.PlateCarree(),fontsize = 15)


## function for making borders, Optional
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
            plt.hlines(y=y,xmin=xmin,xmax=xmin+step,colors="white", ls="-", lw=lw,transform = ccrs.PlateCaree())
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

def plot_dem(ax):
    cmap = plt.cm.gist_earth
    norm = LogNorm(vmin = 1,vmax = 2500)
    
    
    filename = wrl.util.get_wradlib_data_file('/Volumes/WINDOWS/output_SRTMGL3.tif')
    ds = wrl.io.open_raster(filename)
    # pixel_spacing is in output units (lonlat)
    ds = wrl.georef.reproject_raster_dataset(ds, spacing=0.005)
    rastervalues, rastercoords, proj = wrl.georef.extract_raster_dataset(ds)
    # specify kwargs for plotting, using terrain colormap and LogNorm
    dem = ax.pcolormesh(rastercoords[..., 0], rastercoords[..., 1],
                        rastervalues, cmap= cmap, norm=norm,
                        transform=ccrs.PlateCarree())
    # add colorbar and title
    # we use LogLocator for colorbar
    cb = plt.gcf().colorbar(dem, pad=0.075,shrink = 0.5,spacing = 'proportional',extend = 'both')
    cb.set_label('terrain height [m]',fontsize = 20)
    cb.ax.tick_params(labelsize=20)
    #plotting the North direction and arrow
    ax.text(26,49,u'\u25B2 \nN ', ha='center', fontsize=20, 
            family='Arial', rotation = 0,transform = ccrs.PlateCarree())

## plotting the cities and their names 

def plot_cities(ax):
    # plot city dots with annotation, finalize plot
    # lat/lon coordinates of five cities in Bangladesh
    lats_h = [47.47,47.7194,47.2566,47.1043,46.0727]
    lons_h = [19.06,18.8956,16.5993,20.7417,18.2323]
    lats_h1= [47.2279]
    lons_h1= [21.1408]
    lats_r = [45.7994,46.1866,46.7712]#,
    lons_r = [20.7120,21.3123,23.6236]#,
    lats_r1 = [45.7936,46.7212,45.8609,45.7489]
    lons_r1 = [24.1213,25.5855,25.7886,21.2087]
    lats_c = [45.8150,45.3271,45.7019]
    lons_c = [15.9819,14.4422,17.7011]
    lats_u=[48.6208]
    lons_u=[22.2879]
    c_h = ['Budapest (1886-1919)','Dobogókõ (1899-1914)', 
           'Herény (1890-1919)', 'Túrkeve (1897-1918)','Pécs (1890-1916)']
    c_h1 = ['Szerep (1919)']
    c_r = ['Zsombolya\n(1889-1906)', 'Arad (1886-1890)','Kolozsvar\n(1901-1916)'] 
    c_r1 = ['Nagyszeben\n(1886-1919)','Gyergyószentmiklós\n(1897-1900)',
            'Szepsiszentgyórgy\n(1901-1915)',
            'Temesvár\n(1907-1916)']
    c_s = ['Arvavarjája (1886-1892)','Liptóúvár\n(1912-1915)',
           'Pozsony (1886-1888)','Ógyalla (1890-1915)','Poprád\n(1910-1911)',
           'Eperjes (1886-1888)','Felka (1902-1906)']
    c_c = ['Zágráb\n(1886-1914)','Fiume (1901-1915)','Szlatina\n(1886-1888)']
    c_u = ['Ungvár (1889-1916)']
    lons_s = [19.3568,19.6173,17.1077,18.1958,20.2954,21.2393,21.6786]
    lats_s = [49.2620,49.0810,48.1486,47.8795,49.0511,49.0018,48.4677]
    for lon, lat, city in zip(lons_h, lats_h, c_h):
        ax.plot(lon, lat, marker='o', color='red', markersize=7,
             alpha=0.7, transform=ccrs.PlateCarree())
        ax.text(lon -0.1, lat, city,verticalalignment='center', horizontalalignment='right',
                transform=ccrs.PlateCarree(),fontsize=15)
    for lon, lat, city in zip(lons_r, lats_r, c_r):
        ax.plot(lon, lat, marker='o', color='blue', markersize=7,
             alpha=0.7, transform=ccrs.PlateCarree())
        ax.text(lon -0.1, lat, city,verticalalignment='center', horizontalalignment='right',
                transform=ccrs.PlateCarree(),fontsize=15)
    #####Romania    
    ax.plot(lons_r1[0]-0.1,lats_r1[0], marker='o', color='blue', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_r1[1]-0.1,lats_r1[1], marker='o', color='blue', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_r1[2]-0.1,lats_r1[2], marker='o', color='blue', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_r1[3]-0.1,lats_r1[3], marker='o', color='blue', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    
    ## N,G,S,T
    ax.text(lons_r1[0]-0.2,lats_r1[0], c_r1[0],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_r1[1]+0.5,lats_r1[1]+0.3, c_r1[1],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_r1[2]+0.5,lats_r1[2]+0.3, c_r1[2],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_r1[3]+0.8,lats_r1[3]-0.3, c_r1[3],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ###slovakia
    ax.plot(lons_s[0],lats_s[0], marker='o', color='purple', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_s[1],lats_s[1], marker='o', color='purple', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_s[2],lats_s[2], marker='o', color='purple', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_s[3],lats_s[3], marker='o', color='purple', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_s[4],lats_s[4], marker='o', color='purple', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_s[5],lats_s[5], marker='o', color='purple', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_s[6],lats_s[6], marker='o', color='purple', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    #A,L,Poz,Ogy,Pop,Ep,Fel
    ax.text(lons_s[0]-0.1,lats_s[0], c_s[0],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_s[1]-0.1,lats_s[1]-0.2, c_s[1],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_s[2]-0.1,lats_s[2], c_s[2],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_s[3]+2.5,lats_s[3]+0.2, c_s[3],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_s[4]+1,lats_s[4]+0.3, c_s[4],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_s[5]+2.7,lats_s[5], c_s[5],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_s[6]-0.1,lats_s[6], c_s[6],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    
    ##croatia
    ax.plot(lons_c[0],lats_c[0], marker='o', color='black', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_c[1],lats_c[1], marker='o', color='black', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.plot(lons_c[2],lats_c[2], marker='o', color='black', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    #Z,F,S
    ax.text(lons_c[0]-0.1,lats_c[0], c_c[0],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_c[1]+2.5,lats_c[1], c_c[1],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ax.text(lons_c[2]+1,  lats_c[2]-0.25, c_c[2],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ##Ukraine
    ax.plot(lons_u[0],lats_u[0], marker='o', color='orange', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.text(lons_u[0]+2.7,lats_u[0], c_u[0],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)
    ##hungary szerep
    ax.plot(lons_h1[0],lats_h1[0], marker='o', color='red', markersize=7,alpha=0.7, transform=ccrs.PlateCarree())
    ax.text(lons_h1[0]+1.9,lats_h1[0], c_h1[0],verticalalignment='center', horizontalalignment='right',transform=ccrs.PlateCarree(),fontsize=15)


## final_plotting the Carpathian basin map
map_proj = ccrs.Mercator()
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection=map_proj)
plot_dem(ax)
#plot_water(ax)
#plot_lakes(ax)
plot_cities(ax)
drow_the_scale(y = 44.5,x = 22,text = '200',length = 2.55,lw = 5,alpha = 0.0)
ax.set_extent([12.5, 27, 44, 50], crs=ccrs.PlateCarree())



#t = ax.set_title('Carpathian Basin',fontsize = 20)
ax.minorticks_on()

ax.add_feature(cfeature.OCEAN)

ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAKES,linewidth = 2)
ax.add_feature(cfeature.RIVERS,linewidth = 2)

#ax.add_feature(cfeature.BORDERS, linestyle='--', linewidth = 2)
gl = ax.gridlines(crs = ccrs.PlateCarree(),draw_labels=True, color='black', alpha=0.2, linestyle='--')

gl.xlabel_style = {'size': 20, 'color': 'black'}
gl.ylabel_style = {'size': 20, 'color': 'black'}


left = 0.1
bottom = 0.2
width = 0.5
height = 0.1
rect = [left,bottom,width,height]

ax5 = plt.axes(rect)
Romania = mlines.Line2D([], [], color='blue', marker='o', linestyle='None',
                          markersize=10, label='Romania')
Hungary = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=10, label='Hungary')
Croatia = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
                          markersize=10, label='Croatia')
Slovakia = mlines.Line2D([], [], color='purple', marker='o', linestyle='None',
                          markersize=10, label='Slovakia')
Ukraine = mlines.Line2D([], [], color='orange', marker='o', linestyle='None',
                          markersize=10, label='Ukraine')




ax5.legend(title = 'Location of meteorological stations',title_fontsize=15,
           handles=[Hungary,Romania,Slovakia, Croatia,Ukraine],loc = [0.3,0.5],ncol = 5,prop = {'size':15})


ax5.axis('off')
plt.show()
