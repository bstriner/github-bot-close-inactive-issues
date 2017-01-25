import argparse
from .utils import get_config, rate_limit, start_logging
import logging
import logging.config


def main(argv):
    parser = argparse.ArgumentParser(description='Check rate limit.')
    parser.add_argument('--config', action="store", help='Configuration file')
    parser.add_argument('--logging-config', action="store", help='Logging configuration file')
    parser.add_argument('--user', action="store", help='Github user')
    parser.add_argument('--token', action="store", help='Github token')
    args = parser.parse_args(argv)
    config = get_config(args.config)
    if args.user:
        config["user"] = args.user
    if args.token:
        config["token"] = args.token
    if args.logging_config:
        config["logging-config"] = args.logging_config
    start_logging(config)
    rate_limit(config)
