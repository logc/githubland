import sys
import logging

import fiona
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Polygon

import bigquery
from countries import get_european_country_names


SEA_COLOR = 'silver'
LAND_COLOR = 'white'
TEXT_COLOR = 'black'
COUNTRY_COLOR = 'darkviolet'

plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'serif', 'serif': ['New Century Schoolbook']})


def unnest(L):
    depth = lambda L: isinstance(L, list) and max(map(depth, L)) + 1
    current_depth = depth(L)
    while current_depth > 1:
        lengths = map(len, L)
        if all([length == 1 for length in lengths]):
            L = [item for sublist in L for item in sublist]
            current_depth -= 1
            continue
        L = L[lengths.index(max(lengths))]
        current_depth -= 1
    return L


def draw_map_with_labels(labels, map_number):
    x1 = -20.
    x2 = 49.
    y1 = 32.
    y2 = 60.
    m = Basemap(
        resolution='l', projection='aea',
        lon_0=0, lat_0=40, llcrnrlat=y1, urcrnrlat=y2,
        llcrnrlon=x1, urcrnrlon=x2, lat_ts=(x1+x2)/2)
    m.drawcountries(linewidth=0.2, color=COUNTRY_COLOR)
    m.drawmapboundary(linewidth=0.5, fill_color=SEA_COLOR)
    m.fillcontinents(color=LAND_COLOR, lake_color=SEA_COLOR)
    m.drawcoastlines(linewidth=0.2)
    for label in labels:
        x, y = m(label[1], label[2])
        plt.text(x, y, label[0],
                 color=TEXT_COLOR, fontweight='heavy', fontstyle='oblique',
                 ha='center', clip_on=True)
    plt.tight_layout()
    logging.info('Saving into file: languages_{}.png'.format(map_number + 1))
    plt.savefig('languages_{}.png'.format(map_number + 1))


def draw_map_excluding(project_number, excluded):
    boundaries = fiona.open(
        'borders/world_country_admin_boundary_shapefile_with_fips_codes.shp')
    european = get_european_country_names()

    def is_european(rec):
        return rec['properties']['CNTRY_NAME'] in european

    european_boundaries = filter(is_european, boundaries)

    labels = []
    correspondences = {}
    for european_boundary in european_boundaries:
        popularity = 1
        ignored = ['Luxembourg', 'Andorra', 'Liechtenstein', 'Macedonia',
                   'Malta', 'Monaco', 'San Marino', 'Vatican City',
                   'Northern Cyprus']
        try:
            name = european_boundary['properties']['CNTRY_NAME']
            if name in ignored:
                continue
            logging.info("Querying BigQuery about {0}".format(name))
            language = bigquery.get_most_popular_language(
                project_number, name, popularity)
            while language in excluded:
                popularity = popularity + 1
                language = bigquery.get_most_popular_language(
                    project_number, name, popularity)
            logging.warning(
                "#{0} most popular language in {1} is {2}".format(
                    popularity + 1, name, language))
            crds = european_boundary['geometry']['coordinates']
            crds = unnest(crds)
            polygon = Polygon(crds)
            if name == 'Russia':
                label = (language, 37, 55)  # Moscow lon, lat
                labels.append(label)
                continue
            label = (language, polygon.centroid.x, polygon.centroid.y)
            logging.debug(label)
            labels.append(label)
            correspondences[name] = language
        except (KeyboardInterrupt, RuntimeError):
            logging.exception("An exception happened:")
            logging.warning(
                "Writing output to sample_{}.png".format(popularity))
            draw_map_with_labels(labels, popularity)
            sys.exit(1)
    draw_map_with_labels(labels, popularity)


def draw_map_for_popularity(project_number, popularity=0):
    boundaries = fiona.open(
        'borders/world_country_admin_boundary_shapefile_with_fips_codes.shp')
    european = get_european_country_names()

    def is_european(rec):
        return rec['properties']['CNTRY_NAME'] in european

    european_boundaries = filter(is_european, boundaries)

    labels = []
    correspondences = {}
    for european_boundary in european_boundaries:
        ignored = ['Luxembourg', 'Andorra', 'Liechtenstein', 'Macedonia',
                   'Malta', 'Monaco', 'San Marino', 'Vatican City',
                   'Northern Cyprus']
        try:
            name = european_boundary['properties']['CNTRY_NAME']
            if name in ignored:
                continue
            #logging.info("Querying BigQuery about {0}".format(name))
            language = bigquery.get_most_popular_language(
                project_number, name, popularity)
            if language == 'JavaScript':
                language = 'JS'
            #logging.warning(
            #    "#{0} most popular language in {1} is {2}".format(
            #        popularity + 1, name, language))
            crds = european_boundary['geometry']['coordinates']
            crds = unnest(crds)
            polygon = Polygon(crds)
            if name == 'Russia':
                label = (language, 37, 55)  # Moscow lon, lat
                labels.append(label)
                continue
            label = (language, polygon.centroid.x, polygon.centroid.y)
            #logging.debug(label)
            labels.append(label)
            correspondences[name] = language
        except (KeyboardInterrupt, RuntimeError):
            logging.exception("An exception happened:")
            logging.warning(
                "Writing output to sample_{}.png".format(popularity))
            draw_map_with_labels(labels, popularity)
            sys.exit(1)
    draw_map_with_labels(labels, popularity)
