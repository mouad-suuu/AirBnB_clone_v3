#!/usr/bin/python3
""" Initialize the views """

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from .index import * 
from .cities import *
from .users import *
from .places_reviews import *
from .places_amenities import *
from .places import *
