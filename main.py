"""
Module main

Entry point for this project
"""
import argparse
import logging
import time

import maps
import correlations


def handle_maps(args):
    maps.draw_map_for_popularity(
        args.project_number, args.popularity, args.excluded)


def handle_correlate(args):
    correlations.produce_all_figures(args.project_number)


def parse_command_line():
    """Parse the command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l', '--log-level', metavar='LEVEL',
        action='store', dest='log_level', default=21,
        type=int, choices=xrange(51),
        help='1 DEBUG; 11 INFO; 21 WARNING; 31 ERROR; 41 CRITICAL')
    subparsers = parser.add_subparsers()
    parser_maps = subparsers.add_parser('maps')
    parser_maps.add_argument('project_number')
    parser_maps.add_argument('-p', '--popularity', type=int, default=1)
    parser_maps.add_argument('-e', '--excluded', nargs='+')
    parser_maps.set_defaults(func=handle_maps)
    parser_corr = subparsers.add_parser('correlate')
    parser_corr.add_argument('project_number')
    parser_corr.set_defaults(func=handle_correlate)
    return parser.parse_args()


def main():
    """Main function"""
    args = parse_command_line()
    logging.basicConfig(
        format='%(asctime)s %(module)s.%(funcName)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', level=args.log_level)
    start = time.time()
    try:
        args.func(args)
    finally:
        logging.info(
            'Done in {} seconds'.format(time.time() - start))


if __name__ == '__main__':
    main()
