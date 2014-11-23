"""
Module test_maps

Tests for the `maps` module
"""
from collections import OrderedDict

from mock import patch, ANY
# Pylint does not work well with nose.tools
# pylint: disable=no-name-in-module
from nose.tools import assert_equal, ok_
# pylint: enable=no-name-in-module

import maps


def test_choosing_coordinates():
    """Test that coordinates are well chosen"""
    boundary = {'geometry': {'coordinates': [[[
        (0, 0),
        (0, 0)]],
        [[(1, 0),
          (1, 0),
          (1, 0)]]],
        'type': 'MultiPolygon'},
        'id': '230',
        'properties': OrderedDict(
            [(u'FIPS_CNTRY', u'UK'), (u'CNTRY_NAME', u'United Kingdom')]),
        'type': 'Feature'}
    coords = boundary['geometry']['coordinates']
    ok_(len(coords[0][0]) < len(coords[1][0]))
    assert_equal(maps.unnest(coords), coords[1][0])


@patch('maps.draw_map_with_labels')
@patch('bigquery.get_most_popular_language')
def test_draw_map_excluding(mock_bigquery, mock_do_draw):
    """Test how to draw a map excluding some languages from possible results"""
    fake_project_number = 22
    mock_bigquery.side_effect = lambda x, y, z: 'Python'
    maps.draw_map_for_popularity(fake_project_number)
    mock_do_draw.assert_called_once_with([('Python', ANY, ANY)] * 39, 0)
