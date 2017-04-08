from setuptools import setup, find_packages
import os

long_description = open('README.rst').read()

VERSION = '0.0.4'

package_data = {"github_bot_close_inactive_issues": ["logging.conf"]}

setup(name='github-bot-close-inactive-issues',
      version=VERSION,
      description='Bot for automatically closing inactive issues in GitHub repositories',
      url='https://github.com/bstriner/github-bot',
      download_url='https://github.com/bstriner/github-bot-close-inactive-issues/tarball/v{}'.format(VERSION),
      author='Ben Striner',
      author_email='btriner@gmail.com',
      packages=find_packages(),
      package_data=package_data,
      long_description=long_description,
      keywords=['github', 'issues', 'inactive', 'abandoned'],
      license='MIT',
      classifiers=[
          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3'
      ],
      entry_points={
          'console_scripts': [
              'github-rate-limit=github_bot_close_inactive_issues.rate_limit:main',
              'github-close-inactive-issues=github_bot_close_inactive_issues.close_inactive_issues:main'
          ]
      },
      install_requires=[
          'PyGithub','pyyaml'
      ]
      )
