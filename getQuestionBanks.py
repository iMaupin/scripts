from psycopg2 import connect
from queries import questionBanksIDandName
db = connect()

cur = db.cursor()
# fetch questionBank names and IDs and store them in a dictionary
cur.execute(questionBanksIDandName)
res = cur.fetchall()
banks = []
for item in res:
    bank = {'name': item[0], 'id': item[1]}
    banks.append(bank)
