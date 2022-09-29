import os

import dotenv
import requests
from sqlalchemy import MetaData, create_engine
from sqlalchemy.exc import ProgrammingError


dotenv.load_dotenv('.env')
cred = {
    'user': os.getenv('DB_USER'),
    'pwd': os.getenv('DB_PWD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'db_name': os.getenv('DB_NAME')
}
db_url = f"mysql+mysqlconnector://{cred['user']}:{cred['pwd']}@{cred['host']}:{cred['port']}/{cred['db_name']}"
engine = create_engine(db_url)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def check_db_tables():
    con = engine.connect()
    stmt = 'select count(1) where exists (select * from {})'
    res = {}
    for t in ['scans', 'identities']:
        try:
            is_data_in_table = list(con.execute(stmt.format(t)))[0][0]
        except ProgrammingError:
            print(f'Table {t} does not exist!')
        except:
            is_data_in_table = 0
        finally:
            res[t] = is_data_in_table
    
    con.close()
    return res


def get_token():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'username': os.getenv('VYYER_USERNAME'),
        'password': os.getenv('VYYER_PASSWORD'),
        'client_id': os.getenv('VYYER_CLIENT_ID'),
        'client_secret': os.getenv('VYYER_CLIENT_SECRET'),
        'audience': 'https://test-unified.client-api.vyyer.id', 
        'scope': '*',
        'grant_type': 'password'
        }
    auth0_url = "https://vyyer.us.auth0.com/oauth/token"

    print('Obtaining new token')
    token = requests.post(auth0_url, data=payload, headers=headers)
    token = token.json()
    return token['access_token']


def load_scans(headers, table_obj, pages=40):
    rename_map = {'ID': 'id', 'IdentityID': 'identity_id', 'CreatedAt': 'created_at', 'VerdictValue': 'verdict_value'}
    url = "https://test-unified.client-api.vyyer.id/api/v2/scans/get"

    with engine.connect() as con:
        for page in range(1, pages+1):
            print(f'Processing scans (page: {page}/{pages})')

            payload = {'Page': page, "PerPage": 25}
            res = requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                res = res.json()
            else:
                print(f'Failed to get data (page: {page}, status: {res.status_code}')
                continue

            data = [{rename_map[k]: v for k, v in d.items() if k in rename_map.keys()} for d in res['Data']]
            try:
                con.execute(table_obj.insert(data))
            except Exception as e:
                print(f'Failed to save chunk {page}, reason: {e}')

    print('Loaded scans')


def load_ids(headers, table_obj, per_page=250):
    url = "https://test-unified.client-api.vyyer.id/api/v2/identities/get"
    rename_map = {'ID': 'id', 'LicenseNumber': 'license_number', 'FullName': 'full_name', 
                  'Address': 'address', 'ExpiresAt': 'expires_at'}

    with engine.connect() as con:
        #load unique identity_ids from scans
        ids = con.execute('select distinct identity_id from scans')
        ids = sorted(list({r[0] for r in ids.all()}))
        for n, page in enumerate(chunks(ids, per_page)):
            print(f'Processing ids (page: {n}/{len(ids)//per_page})')

            payload = {'IDs': page}
            res = requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                res = res.json()
            else:
                print(f'Failed to get data (page: {page}, status: {res.status_code}')
                continue

            data = [{rename_map[k]: v for k, v in d.items() if k in rename_map.keys()} for d in res['Data']]

            try:
                con.execute(table_obj.insert(data))
            except Exception as e:
                pass
                # print(f'Failed to save chunk {page}, reason: {e}')
    
    print('Loaded identities')


def main():
    #check for data
    res = check_db_tables()

    #if scans and/or ids table empty - get token to load data
    if sum(res.values()) <= 1:
        token = os.getenv('ACCESS_TOKEN')
        if not token:
            token = get_token()
        headers = {'Content-Type':'application/json',
          'Authorization':f'Bearer {token}',
          'X-User-Id':'Auth0User',
          'X-Org-Id':'Auth0Org'}

        insp = MetaData(bind=engine)
        insp.reflect()

    if not res['scans']:
        table_obj = insp.tables['scans']
        load_scans(headers, table_obj)
    else:
        print('Not loading scans')
    
    if not res['identities']:
        table_obj = insp.tables['identities']
        load_ids(headers, table_obj)
    else:
        print('Not loading ids')


if __name__ == "__main__":
    main()
    print('Finished data loading')