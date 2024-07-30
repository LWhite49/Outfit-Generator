# Hello patrick ;) 

# First three inputs are arrays of 4 colors as extracted from productColors
# three obect ids
# Seventh input is a 0 or 1, where 0 is dislike and 1 is like

# This doesn't actually have to return anything, maybe send a simple string if there was a failure for debugging purposes

import sys
# import os

# relative_path = os.path.join(os.path.dirname(__file__), '../../python/recommendation_system')
# sys.path.append(os.path.abspath(relative_path))

import json
import ast
import pandas as pd

from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

# read inputs from site
# top = ast.literal_eval(sys.argv[1])
# bottom = ast.literal_eval(sys.argv[2])
# shoe = ast.literal_eval(sys.argv[3])
# outfit = [top, bottom, shoe]
# top_id = ast.literal_eval(sys.argv[4])
# bottom_id = ast.literal_eval(sys.argv[5])
# shoe_id = ast.literal_eval(sys.argv[6])
# reaction = ast.literal_eval(sys.argv[7])

# Initialize ENV
load_dotenv()

# Source ENV
connectionString = getenv('DB_CONNECTION_PY')
# Connect to Mongo
client = MongoClient(connectionString)
# Connect to DBs
db = client['test']
print('Connected to clothes database')
arcv = client['archive']
print('Connected to archive database')

# source outfit ids
top_id = sys.argv[4]
bottom_id = sys.argv[5]
shoe_id = sys.argv[6]
reaction = sys.argv[7]

# pull associated document from clothes database
#* right now there isn't a way to see what sex collection an item came from so we have to check the id against both
# top
sex = 'M' # we will also attach a sex indicator to outfit sets
collection = db['topmens']
top = collection.find_one({'_id': top_id}, projection={'_id': False})
 # _id will be excluded from the returned document, as we will rely on new _id when inserting it into the archive
if not top:
    collection = db['topwomens']
    top = collection.find_one({'_id': top_id}, projection={'_id': False})
    sex = 'F' # reassign sex
    # TODO this reassignment ^ is assuming that outfits will be of a consistent sex throughout

# insert top into archive
collection = arcv['tops']
if collection.find_one(top): # check that this item hasn't already been archived
    print('Top already in archive.')
else:
    result = collection.insert_one(top)
    top_arcv_id = result.inserted_id # save new, unique archival _id

# bottom
collection = db['bottommens']
bottom = collection.find_one({'_id': bottom_id}, projection={'_id': False})
if not bottom:
    collection = db['bottomwomens']
    bottom = collection.find_one({'_id': bottom_id}, projection={'_id': False})

# insert bottom into archive
collection = arcv['bottoms']
if collection.find_one(bottom):
    print('Bottom already in archive.')
else:
    result = collection.insert_one(bottom)
    bottom_arcv_id = result.inserted_id

# shoe
collection = db['shoemens']
shoe = collection.find_one({'_id': shoe_id}, projection={'_id': False})
if not shoe:
    collection = db['shoewomens']
    shoe = collection.find_one({'_id': shoe_id}, projection={'_id': False})

# insert shoe into archive
collection = arcv['shoes']
if collection.find_one(shoe):
    print('Shoe already in archive.')
else:
    result = collection.insert_one(shoe)
    shoe_arcv_id = result.inserted_id

# todo: if an item wasn't found we can get by just on the colors passed and make an object from that

# create a new document to represent outfit set
outfit = {'sex': sex, 'top_id': top_arcv_id, 'bottom_id': bottom_arcv_id, 'shoe_id': shoe_arcv_id, 'reaction': reaction}
collection = arcv['reacted_sets']
collection.insert_one(outfit)

client.close()
# new_data = pd.DataFrame(columns=[[f'{x}ID', f'{x}_Color1', f'{x}_Color1_Area', f'{x}_Color2', f'{x}_Color2_Area', \
#     f'{x}_Color3', f'{x}_Color3_Area', f'{x}_Color4', f'{x}_Color4_Area'] for x in ['Top', 'Bottom', 'Shoe']])

# data_row = []
# for item in zip(outfit, [top_id, bottom_id, shoe_id]):
#     data_row.append(item[1])
#     for i in range(4):
#         data_row.append(item[0][i])

# print(top_id, bottom_id, shoe_id)

# tops = pd.read_csv('tops.csv')

# # "[[39, 0.7626759825691902], [74, 0.9842073665159553], [94, 0.9927596179385189], [1, 0.826938610669784]]" "[[81, 0.04446910845485719], [80, 0.31393216907364074], [61, 0.1948204741327889], [21, 0.02505551032096842]]" "[[32, 0.18874528147337621], [10, 0.8188436866791314], [15, 0.032815546289438946], [73, 0.8232446951901217]]" "e54240" "f21bc7" "97214c" "1"
# sys.stdout.flush()