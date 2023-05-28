import redis
from pyhive import presto

def handle_query(query):
    r = redis.Redis(host='localhost', port=6379, db=0)
    presto_cursor = presto.connect(host='localhost', port=8080).cursor()
    result = r.get(query)
    
    if result is not None:
        # Redis stores data as bytes, so we decode it back to string
        result = result.decode('utf-8') 
    else:
        presto_cursor.execute(query)
        rows = presto_cursor.fetchall()
        result_str = str(rows)
        r.set(query, result_str)
        result = result_str
    return result