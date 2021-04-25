#!/usr/bin/env python

import time
from collections import defaultdict
from datetime import datetime
from random import randint
import numpy as np
import pvapy as pv
import logging


PV_NAME = "pvapy:logging"

EPOCH = datetime.utcfromtimestamp(0)

logging.basicConfig(
    filename="servePvWithLogging.log",
    # encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y/%m/%d %I:%M:%S %p",
)
logger = logging.getLogger("serve alarm pv")

cache = {
    "mean": 0,
    "sigma": 0,
    "name": "",
}

def timestampnow():
    dt = datetime.now() - EPOCH
    seconds_since_epoch = int(dt.total_seconds())
    nanoseconds = int(dt.microseconds * 1e3)
    return pv.PvTimeStamp(seconds_since_epoch, nanoseconds)

def makePV(x, m=10, s=2, timestamp=None):
    if not timestamp:
        timestamp = timestampnow()

    logger.debug(f"Created PV with value: {x:.4f}")
    mean = pv.PvObject({"value": pv.FLOAT}, {"value": m})
    sigma = pv.PvObject({"value": pv.FLOAT}, {"value": s})
    name = pv.PvObject({"value": pv.STRING}, {"value": "my:alias:name"})

    return pv.PvObject(
        {
            "value": pv.FLOAT,
            "mean": mean,
            "sigma": sigma,
            "name": name,
            "timeStamp": timestamp,
        },
        {
            "value": x,
            "mean": mean.toDict(),
            "sigma": sigma.toDict(),
            "name": name.toDict(),
            "timeStamp": timestamp.toDict(),
        },
    )

def changed_params_cb(x):
    global cache
    def log_and_cache(prop):
        if x[prop]["value"] != cache[prop]:
            logger.info(f"Changed {prop} from {cache[prop]} to {x[prop]['value']}")
            cache[prop] = x[prop]["value"]

    props = list(cache.keys())
    [log_and_cache(prop) for prop in props]

def runServer():
    pv1 = makePV(0)
    server = pv.PvaServer(PV_NAME, pv1, changed_params_cb)

    while True:
        m = pv1['mean']['value']
        s = pv1['sigma']['value']
        x = np.random.normal(m, s)
        if x != pv1['value']:
            pv1['value'] = x
            pv1['timeStamp'] = timestampnow().toDict()
            logger.debug(f"New x value: {x:.4f}")

        time.sleep(abs(np.random.normal(0.3, 0.1)))


runServer()
