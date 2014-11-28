"""
Module test_main

Tests for the command line interface in the main module
"""
import sys
import argparse
import shlex

from mock import patch
# Pylint does not work well with nose.tools
# pylint: disable=no-name-in-module
from nose.tools import assert_true
# pylint: enable=no-name-in-module

import main


@patch('main.handle_maps')
def test_draw_maps(mock_maps_handler):
    sys.argv = shlex.split(
        'program maps 1111 --popularity 2 --excluded=JavaScript')
    main.main()
    assert_true(mock_maps_handler.called)
    mock_maps_handler.assert_called_once_with(
        argparse.Namespace(
            excluded=['JavaScript'],
            func=main.handle_maps,
            log_level=21,
            popularity=2,
            project_number='1111'))


@patch('main.handle_maps')
def test_draw_maps_no_excludes(mock_maps_handler):
    sys.argv = shlex.split('program maps 1111 --popularity 1')
    main.main()
    assert_true(mock_maps_handler.called)
    mock_maps_handler.assert_called_once_with(
        argparse.Namespace(
            excluded=None,
            func=main.handle_maps,
            log_level=21,
            popularity=1,
            project_number='1111'))


@patch('main.handle_maps')
def test_draw_maps_multiple_excludes(mock_maps_handler):
    sys.argv = shlex.split(
        'program maps 1111 --popularity 2 --excluded JavaScript PHP')
    main.main()
    assert_true(mock_maps_handler.called)
    mock_maps_handler.assert_called_once_with(
        argparse.Namespace(
            excluded=['JavaScript', 'PHP'],
            func=main.handle_maps,
            log_level=21,
            popularity=2,
            project_number='1111'))


@patch('main.handle_correlate')
def test_correlate(mock_correlate_handler):
    sys.argv = shlex.split('program correlate 1111')
    main.main()
    assert_true(mock_correlate_handler.called)
    mock_correlate_handler.assert_called_once_with(
        argparse.Namespace(
            func=main.handle_correlate,
            log_level=21,
            project_number='1111'))
