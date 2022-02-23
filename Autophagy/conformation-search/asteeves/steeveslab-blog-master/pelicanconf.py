#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'asteeves'
SITENAME = u'steeveslab-blog'
SITEURL = 'asteeves.github.io'

TIMEZONE = 'US/Eastern'

DEFAULT_LANG = u'en'

DEFAULT_DATE_FORMAT = '%b %d, %Y'

# Set the article URL
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

#added for ipython notebook with liquid-tags plugin by jakevdp
THEME = "pelican-octopress-theme"
PLUGIN_PATH = 'pelican-plugins'
PLUGINS = ['summary', 'liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.include_code', 'liquid_tags.notebook',
           'liquid_tags.youtube', 'liquid_tags.literal']

STATIC_PATHS = ['images', 'figures', 'downloads', 'favicon.png']

CODE_DIR = 'downloads/code'
NOTEBOOK_DIR = 'downloads/notebooks'

MD_EXTENSIONS = ['smarty']

# The theme file should be updated so that the base header contains the line:
#
#  {% if EXTRA_HEADER %}
#    {{ EXTRA_HEADER }}
#  {% endif %}
# 
# This header file is automatically generated by the notebook plugin
if not os.path.exists('_nb_header.html'):
    import warnings
    warnings.warn("""_nb_header.html not found. 
                    Rerun make html to finalize build.""")
else:
    EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8').replace(
    "highlight ","highlight-ipynb ")

#
TWITTER_USER = 'SteevesLab'
# not sure why the twitter widget is blank
#TWITTER_WIDGET_ID = 553033582500122624


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  ()

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/SteevesLab'),)

DEFAULT_PAGINATION = 10
#SUMMARY_MAX_LENGTH = 100

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
