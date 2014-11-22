"""
Module maps

Produces the maps of Europe where country names have been subsituted by a
programming language.  This language can be the Xth most preferred language as
counted on Github commits originating from that country, or it can be the Xth
most preferred language excluding some languages.
"""
import sys
import logging
from itertools import imap, ifilter

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
# This line is required by the matplotlib API in order to change the default
# Tex font
# pylint: disable=star-args
plt.rc('font', **{'family': 'serif', 'serif': ['New Century Schoolbook']})
# pylint: enable=star-args


def unnest(nested_list):
    """
    Returns a flat list out of a nested list
    """
    depth = lambda nested_list: isinstance(nested_list, list) and max(
        imap(depth, nested_list)) + 1
    current_depth = depth(nested_list)
    while current_depth > 1:
        lengths = imap(len, nested_list)
        if all([length == 1 for length in lengths]):
            nested_list = [item for sublist
                           in nested_list for item in sublist]
            current_depth -= 1
            continue
        nested_list = nested_list[lengths.index(max(lengths))]
        current_depth -= 1
    return nested_list


def draw_map_with_labels(labels, map_number):
    """
    Draws a map once the labels substituting country names are given
    """
    min_lon = -20.
    max_lon = 49.
    min_lat = 32.
    max_lat = 60.
    europe = Basemap(
        resolution='l',
        projection='aea',
        lon_0=0,
        lat_0=40,
        llcrnrlat=min_lat,
        urcrnrlat=max_lat,
        llcrnrlon=min_lon,
        urcrnrlon=max_lon,
        lat_ts=(min_lon+max_lon)/2)
    europe.drawcountries(linewidth=0.2, color=COUNTRY_COLOR)
    europe.drawmapboundary(linewidth=0.5, fill_color=SEA_COLOR)
    europe.fillcontinents(color=LAND_COLOR, lake_color=SEA_COLOR)
    europe.drawcoastlines(linewidth=0.2)
    for label in labels:
        lon, lat = europe(label[1], label[2])
        plt.text(lon, lat, label[0],
                 color=TEXT_COLOR, fontweight='heavy', fontstyle='oblique',
                 ha='center', clip_on=True)
    plt.tight_layout()
    logging.info('Saving into file: languages_{}.png'.format(map_number + 1))
    plt.savefig('languages_{}.png'.format(map_number + 1))


def draw_map_for_popularity(project_number, popularity=0, excluded=None):
    """
    Draw map showing languanges at a certain position in the popularity list.
    Default position is 0, i.e. the most popular language
    """
    boundaries = fiona.open(
        'borders/world_country_admin_boundary_shapefile_with_fips_codes.shp')
    european = get_european_country_names()

    def is_european(rec):
        """ Returns True if boundary is an european country """
        return rec['properties']['CNTRY_NAME'] in european

    european_boundaries = ifilter(is_european, boundaries)

    labels = []
    for european_boundary in european_boundaries:
        ignored = ['Luxembourg', 'Andorra', 'Liechtenstein', 'Macedonia',
                   'Malta', 'Monaco', 'San Marino', 'Vatican City',
                   'Northern Cyprus']
        try:
            name = european_boundary['properties']['CNTRY_NAME']
            if name in ignored:
                continue
            logging.debug("Querying BigQuery about {0}".format(name))
            language = bigquery.get_most_popular_language(
                project_number, name, popularity)
            if excluded:
                while language in excluded:
                    popularity = popularity + 1
                    language = bigquery.get_most_popular_language(
                        project_number, name, popularity)
            if language == 'JavaScript':
                language = 'JS'
            logging.debug(
                "#{0} most popular language in {1} is {2}".format(
                    popularity + 1, name, language))
            crds = european_boundary['geometry']['coordinates']
            crds = unnest(crds)
            polygon = Polygon(crds)
            if name == 'Russia':
                label = (language, 37, 55)  # Moscow lon, lat
                labels.append(label)
                continue
            # The Polygon x and y members seem to be constructed at runtime
            # pylint: disable=no-member
            label = (language, polygon.centroid.x, polygon.centroid.y)
            # pylint: enable=no-member
            logging.debug(label)
            labels.append(label)
        except (KeyboardInterrupt, RuntimeError):
            logging.exception("An exception happened:")
            logging.warning(
                "Writing output to sample_{}.png".format(popularity))
            draw_map_with_labels(labels, popularity)
            sys.exit(1)
    draw_map_with_labels(labels, popularity)
