from flask import Flask

import redis
from prometheus_redis_client import REGISTRY

from aaprom.collectors import load_all

try:
    load_all()
except:
    pass

## Needs to match the local.py setting this is not django so we dont expose metrics
r = redis.from_url("redis://redis:6379/1") 
r.flushdb() # Cleanup at startup

REGISTRY.set_redis(r)

app = Flask(__name__)

@app.route("/metrics") # Prometh uses this
@app.route("/") # i am lazy and ue this for debug
def prom_export():
    return REGISTRY.output()

if __name__ == "__main__":
    app.run()
