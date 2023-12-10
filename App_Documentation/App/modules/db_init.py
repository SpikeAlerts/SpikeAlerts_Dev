### Import Packages

# File manipulation

import os # For working with Operating System
import shutil # For deleting folders
import urllib # For accessing websites
import zipfile # For extracting from Zipfiles
from io import BytesIO # For reading bytes objects

import requests # Accessing the Web
import datetime as dt # Working with dates/times

# Analysis

import numpy as np
import pandas as pd # Data Management
import geopandas as gpd # Spatial Data Manipulation

# Database 

import psycopg2 # For working with postgresql database
from psycopg2 import sql
from App.modules.db_conn import pg_connection_dict

# Environmental variables

from dotenv import load_dotenv # Loading .env info
load_dotenv() # Load .env file
purpleAir_api = os.getenv('PURPLEAIR_API_TOKEN')

# Load our Functions

script_path = os.path.join('App','modules')

### Definitions

def extract_zip_from_url(url=None, savepath=None):
  # '''Extract a zipfile from the internet
  # then unpack it in to it's own folder 
  # within the working directory.
  # Takes a single url (string).'''

    if not os.path.exists(savepath):
        os.makedirs(savepath)
    # Unload zip into the new folder
    response = urllib.request.urlopen(url) # Get a response
    zip_folder = zipfile.ZipFile(BytesIO(response.read())) # Read Response
    zip_folder.extractall(path=savepath) # Extract files
    zip_folder.close() # Close zip object

def get_boundary_from_url():
  # Download Data
  ## Twin Cities Metro Boundaries - Downloaded from MN GeospatialCommons gisdata.mn.gov  (~ 5mb)
  url = "https://resources.gisdata.mn.gov/pub/gdrs/data/pub/us_mn_state_metc/bdry_census2020counties_ctus/shp_bdry_census2020counties_ctus.zip"
  # Create folder name for file
  folder_name = 'shp_bdry_census2020counties_ctus' # url.split('/')[-1][:-4] <- programatic way to get foldernam
  # Define path for downloaded files
  savepath = os.path.join('Data', folder_name)
  extract_zip_from_url(url, savepath)

  # Read & Select
  # Get path
  filename = 'Census2020CTUs.shp'
  path = os.path.join(savepath, filename)
  ctus_boundaries = gpd.read_file(path)
  # Select Minneapolis
  mpls_boundary = ctus_boundaries[ctus_boundaries['CTU_NAME'] == 'Minneapolis']
  return mpls_boundary
  # # Write the selected features to a new featureclass
  # arcpy.management.CopyFeatures(mpls_boundary, "mpls_boundary")

def pg_post_boundaries(mpls_boundary):
  # connect to db
  conn = psycopg2.connect(**pg_connection_dict)
  cur = conn.cursor()   # Create Cursor for commands
  ## Redo everything below here
  # Insert into table
  cols = ['CTU_ID', 'CTU_NAME', 'CTU_CODE', 'geometry'] # Relative columns
  for i, row in mpls_boundary[cols].iterrows():
    cur.execute(
      'INSERT INTO "Minneapolis Boundary"("CTU_ID", "CTU_NAME", "CTU_CODE", geometry)'
      'VALUES (%(ctu_id)s, %(ctu_name)s, %(ctu_code)s, ST_Transform(ST_SetSRID(ST_GeomFromText(%(geom)s), 26915),4326)::geometry);',
      {'ctu_id': row.iloc[0],
        'ctu_name' : row.iloc[1],
        'ctu_code': row.iloc[2],
        'geom': row.iloc[3].wkt})
    conn.commit() # Commit command
  cur.close() # Close cursor
  conn.close() # Close connection
  print('initted!')

def db_need_init():
  conn = psycopg2.connect(**pg_connection_dict)
  cur = conn.cursor()
  cur.execute('SELECT * FROM "Minneapolis Boundary"')
  response = cur.fetchall()
  cur.close()
  conn.close()
  
  if len(response) > 0:
    return False
  else:
    return True

def db_init():
  # execute get boundary --> post values to database
  pg_post_boundaries(get_boundary_from_url())

def db_notinit():
   print("you're not init!")
