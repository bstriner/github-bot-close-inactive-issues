import os
import yaml
from github import Github
from datetime import datetime, timedelta
import logging
import logging.config
import time

CONFIG_FILE = 'github_bot.yml'


def start_logging(config):
    logging_config = None
    if "logging-config" in config:
        logging_config = config["logging-config"]
    if not logging_config:
        logging_config = os.path.join(os.path.dirname(__file__), "logging.conf")
    if not os.path.exists(logging_config):
        raise ValueError("Logging configuration file does not exist: {}".format(logging_config))
    logging.config.fileConfig(logging_config)


def get_config_file():
    return os.path.join(os.path.expanduser('~'), CONFIG_FILE)


def get_config(config_file=None):
    if not config_file:
        config_file = get_config_file()
    if not os.path.exists(config_file):
        raise ValueError("Configuration file does not exist: {}".format(config_file))
    with open(config_file) as f:
        return yaml.load(f)


def connect(config):
    # return Github(config["user"], config["token"])
    # return PyGithub.Blocking.Builder().OAuth(token).Build()
    return Github(config["user"], config["token"])


def get_deadline(lm, config):
    first_closing_date = None
    if "first_closing_date" in config:
        first_closing_date = config["first_closing_date"]
    closing = int(config["schedule"]["closing"])
    deadline = lm + timedelta(days=closing)
    if first_closing_date:
        return max(deadline, first_closing_date)
    else:
        return deadline


def rate_limit(config):
    logging.info("Checking rate limit for user {}".format(config["user"]))
    conn = connect(config)
    rate = conn.get_rate_limit().rate
    reset = datetime.fromtimestamp(conn.rate_limiting_resettime)
    logging.info("Limit: {}, Remaining: {}, Reset: {}".format(rate.limit, rate.remaining, reset))

def wait_for_rate_limit(conn, min=100, sleep_time=60*5):
    remaining = conn.get_rate_limit().rate.remaining
    while remaining < min:
        logging.info("Current limit: {}. Sleeping for {} seconds.".format(remaining, sleep_time))
        time.sleep(sleep_time)
        remaining = conn.get_rate_limit().rate.remaining
