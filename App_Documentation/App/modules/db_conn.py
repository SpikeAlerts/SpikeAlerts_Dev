import os # For working with Operating System
from urllib.parse import urlparse
from dotenv import load_dotenv # Loading .env info
load_dotenv()

# heroku psql automatically populates app config var with a DATABASE_URL. 
# if is running remotely, parses config var into connection dict and gets DB_OPTIONS
if os.getenv('DATABASE_URL'): 
  parsed_url = urlparse(os.getenv('DATABASE_URL'))
  creds = [parsed_url.path[1:],
        parsed_url.username,
        parsed_url.password,
        parsed_url.port,
        parsed_url.hostname,
        os.getenv('DB_OPTIONS')
        ]
  # print(creds)
  pg_connection_dict = dict(zip(['dbname', 'user', 'password', 'port', 'host', 'options'], creds))
# else if running locally, gets vars from .env
else:
  creds = [os.getenv('DB_NAME'),
          os.getenv('DB_USER'),
          os.getenv('DB_PASS'),
          os.getenv('DB_PORT'),
          os.getenv('DB_HOST'),
          os.getenv('DB_OPTIONS')
          ]
# print(creds)
  pg_connection_dict = dict(zip(['dbname', 'user', 'password', 'port', 'host', 'options'], creds))
