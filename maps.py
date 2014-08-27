import sys
import logging

import fiona
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Polygon

import bigquery
from countries import get_european_country_names


def unnest(L):
    # As found on:
    # http://stackoverflow.com/questions/6039103/counting-deepness-or-the-deepest-level-a-nested-list-goes-to
    depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
    current_depth = depth(L)
    while current_depth > 1:
        L = L[0]
        current_depth -= 1
    return L


def draw_map_with_labels(labels, map_number):
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
    plt.savefig('sample_{}.png'.format(map_number))


def draw_map_for_popularity(popularity=0):
    boundaries = fiona.open(
        'borders/world_country_admin_boundary_shapefile_with_fips_codes.shp')
    european = get_european_country_names()

    def is_european(rec):
        return rec['properties']['CNTRY_NAME'] in european

    european_boundaries = filter(is_european, boundaries)

    labels = []
    for european_boundary in european_boundaries:
        try:
            name = european_boundary['properties']['CNTRY_NAME']
            logging.warning("Querying BigQuery about {0}".format(name))
            language = bigquery.get_most_popular_language(name, popularity)
            logging.warning(
                "#{0} most popular language there is {1}".format(
                    popularity + 1, language))
            crds = european_boundary['geometry']['coordinates']
            crds = unnest(crds)
            polygon = Polygon(crds)
            labels.append((language, polygon.centroid.x, polygon.centroid.y))
        except KeyboardInterrupt:
            draw_map_with_labels(labels, popularity)
            logging.warning(
                "You exited the application; output written to "
                "sample_{}.png".format(popularity))
            sys.exit(1)
    draw_map_with_labels(labels, popularity)
