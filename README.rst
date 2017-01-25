github-bot-close-inactive-issues
================================

Bot for automatically closing inactive GitHub issues. Based on
configuration, bot will close inactive issues and/or post comments
warning that issues will be closed.

For each issue, bot will calculate a last modified time based on
comments, events, and issue creation.

-  If issue was last modified more than ``warning_start`` days ago, a
   warning comment is posted to the issue.
-  Warning messages will not be posted more than every
   ``warning_frequency`` days.
-  If issue was last modified more than ``closing`` days ago, a comment
   is posted and the issue is closed.

Both warning comment and closing comment are configurable.

Intallation
-----------

Stable Release
~~~~~~~~~~~~~~

.. code:: shell

    pip install github-bot-close-inactive-issues

Development Release
~~~~~~~~~~~~~~~~~~~

.. code:: shell

    git clone https://github.com/bstriner/github-bot-close-inactive-issues.git
    cd github-bot-close-inactive-issues
    python setup.py install

Configuration
-------------

Bot expects the configuration file ``github_bot.yml`` in the user's home
directory. A different file path can be provided by using the
``--config`` command line option. Most configuration can also be
overridden by the command line.

.. code:: yaml

    user: user
    token: token
    repo: user/repo
    messages:
      warning: >
        Warning: this issue has been inactive for {days_inactive} days and
        will be automatically closed on {deadline:%Y-%m-%d} if there is no further activity.
      closing: >
        Notice: this issue has been closed because it has been inactive for {days_inactive} days.
        You may reopen this issue if it has been closed in error.
    schedule:
      warning_start: 14 # days before starting warnings
      warning_frequency: 7 # minimum time between warnings
      closing: 56 # days before closing

    # label to add to issues when closing automatically (optional)
    # label: inactive

    # issue warnings instead of closing until this date (optional)
    # first_closing_date: 2017-03-01 12:00:00

    # path to custom logging configuration (optional)
    # logging-config: /home/user/logging.conf

    # Do not warn or close issues opened by these users
    #ignore-users:
    #  - username1
    #  - username2

Scripts
-------

github-rate-limit.py
~~~~~~~~~~~~~~~~~~~~

Use ``github-rate-limit.py`` to check connection and rate limit.

.. code:: shell

    usage: github-rate-limit.py [-h] [--config CONFIG]
                                [--logging-config LOGGING_CONFIG] [--user USER]
                                [--token TOKEN]

    Check rate limit.

    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
      --logging-config LOGGING_CONFIG
                            Logging configuration file
      --user USER           Github user
      --token TOKEN         Github token

github-close-inactive-issues.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``github-close-inactive-issues.py`` to close inactive issues and
post warnings.

.. code:: shell

    usage: github-close-inactive-issues.py [-h] [--config CONFIG]
                                          [--logging-config LOGGING_CONFIG]
                                           [--user USER] [--token TOKEN]
                                           [--repo REPO] [--test]

    Run bot to maintain issues.

    optional arguments:
      -h, --help            show this help message and exit
      --config CONFIG       Configuration file
      --logging-config LOGGING_CONFIG
                            Logging configuration file
      --user USER           Github user
      --token TOKEN         Github token
      --repo REPO           Repository
      --test                Print actions that would be taken but do not modify repository

Notes
-----

Tokens and Rate Limits
~~~~~~~~~~~~~~~~~~~~~~

You can use a password for your token but you will be rate limited to 60
requests per hour. Create an access token to raise the rate limit to
5000 per hour.

`Creating an Access Token for Command Line
Use <https://help.github.com/articles/creating-an-access-token-for-command-line-use/>`__

You may provide the access token to the bot either on the command line
or in the configuration file.

You should set permissions to the configuration file such that only the
bot can view it.

Use a Dedicated Account
~~~~~~~~~~~~~~~~~~~~~~~

Use a dedicated user account for the bot. The bot calculates last
modified time by checking for comments for users other than the bot.
Otherwise, each time the bot posted a warning the last modified date
would reset. If you use your own account for the bot, it may close an
issue if that account is the only one commenting on that issue.

-  Make sure to verify your account's email address
-  Add that account as a collaborator to your repository
-  **Keep your bot account password and token secret!**

first\_closing\_date
~~~~~~~~~~~~~~~~~~~~

If you include ``first_closing_date`` in your configuration, the bot
will not begin closing issues until that date. The bot will issue
warnings as usual.

If the calculated closing date of an issue is before the
``first_closing_date``, the closing date will be pushed back until that
date.

Logging
~~~~~~~

Bot uses python ``logging`` module. A default ``logging.conf`` is
provided but can be overridden by including ``logging-config`` in
``github_bot.yml`` or passing ``--logging-config`` on the command line.

Labels
~~~~~~

Bot can add a label to issues when they are closed. Make sure to create
that label on GitHub and confirm that the name exactly matches the name
in the configuration file.

Ignoring users
~~~~~~~~~~~~~~

Bot can ignore issues created by selected users, such as the repository
owner.

Questions?
----------

Please feel free to submit issues or pull requests if you have any
questions or concerns. Cheers!
