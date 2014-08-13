import fiona
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Polygon

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
    'Norway',
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


def unnest(L):
    # As found on:
    # http://stackoverflow.com/questions/6039103/counting-deepness-or-the-deepest-level-a-nested-list-goes-to
    depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
    current_depth = depth(L)
    while current_depth > 1:
        L = L[0]
        current_depth -= 1
    return L

labels = []
for european_boundary in european_boundaries:
    name = european_boundary['properties']['CNTRY_NAME']
    crds = european_boundary['geometry']['coordinates']
    crds = unnest(crds)
    polygon = Polygon(crds)
    labels.append((name, polygon.centroid.x, polygon.centroid.y))


x1 = -20.
x2 = 40.
y1 = 32.
y2 = 64.

m = Basemap(
    resolution='l', projection='aea',
    lon_0=0, lat_0=40, llcrnrlat=y1, urcrnrlat=y2,
    llcrnrlon=x1, urcrnrlon=x2, lat_ts=(x1+x2)/2)
m.drawcountries(linewidth=0.5)
m.fillcontinents(color='0.8')
m.drawcoastlines(linewidth=0.5)
for label in labels:
    x, y = m(label[1], label[2])
    plt.text(x, y, label[0], ha='center')
# m.drawparallels(
#     np.arange(y1, y2, 2.), labels=[1, 0, 0, 0], color='black',
#     dashes=[1, 0], labelstyle='+/-', linewidth=0.2)
# m.drawmeridians(
#     np.arange(x1, x2, 2.), labels=[0, 0, 0, 1], color='black',
#     dashes=[1, 0], labelstyle='+/-', linewidth=0.2)

plt.savefig('sample.png')
