import argparse
import logging
import time

import maps


def parse_command_line():
    """Parse the command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument('project_number')
    parser.add_argument('-p', '--popularity', type=int, default=1)
    parser.add_argument('-e', '--excluded', nargs='+')
    parser.add_argument(
        '-l', '--log-level', metavar='LEVEL',
        action='store', dest='log_level', default=21,
        type=int, choices=xrange(51),
        help='1 DEBUG; 11 INFO; 21 WARNING; 31 ERROR; 41 CRITICAL')
    return parser.parse_args()


def main():
    """Main function"""
    args = parse_command_line()
    logging.basicConfig(
        format='%(asctime)s %(module)s.%(funcName)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S', level=args.log_level)
    try:
        start = time.time()
        if not args.excluded:
            maps.draw_map_for_popularity(args.project_number, args.popularity)
        else:
            maps.draw_map_for_popularity(
                args.project_number, args.popularity, args.excluded)
    finally:
        logging.warning(
            '--- {} seconds ellapsed ---'.format(time.time() - start))


if __name__ == '__main__':
    main()
