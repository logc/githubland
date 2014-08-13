import fiona
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

boundaries = fiona.open(
    'borders/world_country_admin_boundary_shapefile_with_fips_codes.shp')
european = [
    'Austria',
    'Belgium',
    'Bulgaria',
    'Cyprus',
    'Czech Republic',
    'Denmark',
    'Estonia',
    'Finland',
    'France',
    'Germany',
    'Greece',
    'Hungary',
    'Italy',
    'Latvia',
    'Lithuania',
    'Luxembourg',
    'Malta',
    'Netherlands',
    'Poland',
    'Portugal',
    'Republic of Ireland',
    'Romania',
    'Slovakia',
    'Slovenia',
    'Spain',
    'Sweden',
    'United Kingdom']


def is_european(rec):
    return rec['properties']['CNTRY_NAME'] in european

european_boundaries = filter(is_european, boundaries)


x1 = -20.
x2 = 40.
y1 = 32.
y2 = 64.

m = Basemap(
    resolution='i', projection='merc', llcrnrlat=y1, urcrnrlat=y2,
    llcrnrlon=x1, urcrnrlon=x2, lat_ts=(x1+x2)/2)
m.drawcountries(linewidth=0.5)
m.drawcoastlines(linewidth=0.5)
# m.drawparallels(
#     np.arange(y1, y2, 2.), labels=[1, 0, 0, 0], color='black',
#     dashes=[1, 0], labelstyle='+/-', linewidth=0.2)
# m.drawmeridians(
#     np.arange(x1, x2, 2.), labels=[0, 0, 0, 1], color='black',
#     dashes=[1, 0], labelstyle='+/-', linewidth=0.2)

plt.savefig('sample.png')
