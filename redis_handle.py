import sys
import traceback
import redis


class RedisClien:
    def __init__(self, _db=0):
        host = '192.168.3.229'
        passwd = 'Gi3d85028501'
        port = 6379
        self.host = host
        self.port = port
        self.passwd = passwd
        self.db = _db
        self.client = redis.Redis(host=host, port=port, password=passwd, db=db, decode_responses=True)

    def get(self, key):
        return self.client.get(key)

    def get_time(self, key):
        return self.client.ttl(key)

    def set(self, key, value):
        return self.client.set(key, value)

    def set_time(self, key, time=None):
        if not time:
            time = self.get_time(key='quarter_invoice_price_10666')
        return self.client.expire(key, time)

    def dele(self, key):
        return self.client.delete(key)

    def close(self):
        return self.client.close()


if __name__ == '__main__':
    """
    python redis_handle.py get quarter_invoice_price_38742
    python redis_handle.py dele quarter_invoice_price_38742
    python redis_handle.py set quarter_invoice_price_38742 300000.00
    """
    db = 0
    r = RedisClien(db)
    mode = getattr(r, sys.argv[1])
    try:
        if len(sys.argv) > 3:
            print(mode(sys.argv[2], sys.argv[3]))
        else:
            print(mode(sys.argv[2]))
    except:
        print(traceback.format_exc())
