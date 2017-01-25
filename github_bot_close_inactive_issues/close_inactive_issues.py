import argparse
from .utils import get_config, connect, get_deadline, rate_limit, start_logging
from .issues import issue_last_modified, issue_last_warning
from .issues import issue_close, issue_warning
import logging
import logging.config
from datetime import datetime


def process_issues(config):
    conn = connect(config)
    rate_limit(config)
    repo = conn.get_repo(config["repo"])
    issues = repo.get_issues(state="open")
    schedule = config["schedule"]
    warning_start = schedule["warning_start"]
    warning_frequency = schedule["warning_frequency"]
    closing = schedule["closing"]
    logging.info("Starting close_inactive_issues")
    logging.info("Repo: {}, User: {}".format(config["repo"], config["user"]))
    logging.info("warning_start: {}, warning_frequency: {}, closing: {}".format(
        warning_start, warning_frequency, closing))
    count = 0
    for issue in issues:
        count += 1
        lm = issue_last_modified(issue, config["user"])
        lw = issue_last_warning(issue, config["user"])
        now = datetime.utcnow()
        days_inactive = (now - lm).days
        deadline = get_deadline(lm, config)
        # if after deadline
        if now > deadline:
            # close the issue
            logging.info("Issue {}: closed after inactive for {} days".format(issue.number, days_inactive))
            if "test" not in config:
                issue_close(issue, config, days_inactive, config["label"])
        # if after warning_start
        elif days_inactive >= warning_start:
            # if no previous warning or more than warning_frequency since last warning
            if (lw is None) or ((now - lw).days >= warning_frequency):
                # post a warning
                logging.info(
                    "Issue {}: warning posted, inactive for {} days, will be closed after {}".format(
                        issue.number, days_inactive, deadline))
                if "test" not in config:
                    issue_warning(issue, config, days_inactive, deadline)
            else:
                # no warning, just log
                logging.info("Issue {}: inactive for {} days, will be closed after {}".format(
                    issue.number, days_inactive, deadline))
    logging.info("Processed {} open issues".format(count))


def main(argv):
    parser = argparse.ArgumentParser(description='Run bot to maintain issues.')
    parser.add_argument('--config', action="store", help='Configuration file')
    parser.add_argument('--logging-config', action="store", help='Logging configuration file')
    parser.add_argument('--user', action="store", help='Github user')
    parser.add_argument('--token', action="store", help='Github token')
    parser.add_argument('--repo', action="store", help='Repository')
    parser.add_argument('--label', action="store", help='Add this label to issues when closing')
    parser.add_argument('--test', action="store_true",
                        help='Print actions that would be taken but do not modify repository')
    args = parser.parse_args(argv)
    config = get_config(args.config)
    if args.user:
        config["user"] = args.user
    if args.token:
        config["token"] = args.token
    if args.repo:
        config["repo"] = args.repo
    if args.logging_config:
        config["logging-config"] = args.logging_config
    if args.test:
        config["test"] = True
    if args.label:
        config["label"] = args.label
    if "label" not in config:
        config["label"] = None
    start_logging(config)
    process_issues(config)
