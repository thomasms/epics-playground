#!/usr/bin/env python

import time
from functools import reduce
import operator
from collections import defaultdict
from datetime import datetime
import numpy as np
import pvapy as pv
import logging


PV_NAME = "pvapy:alarm"

EPOCH = datetime.utcfromtimestamp(0)

logging.basicConfig(
    filename="servePvWithAlarm.log",
    # encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y/%m/%d %I:%M:%S %p",
)
logger = logging.getLogger("serve alarm pv")


def timestampnow():
    dt = datetime.now() - EPOCH
    seconds_since_epoch = int(dt.total_seconds())
    nanoseconds = int(dt.microseconds * 1e3)
    return pv.PvTimeStamp(seconds_since_epoch, nanoseconds)


def makealarm(x, HIHI=50, HI=40, LO=20, LOLO=10):

    alarms = [
        (lambda x: abs(x) > HIHI, pv.PvAlarm(2, 2, "MAJOR problem")),
        (lambda x: abs(x) > HI, pv.PvAlarm(1, 1, "MINOR problem")),
        (lambda x: abs(x) < LOLO, pv.PvAlarm(2, 2, "MAJOR problem")),
        (lambda x: abs(x) < LO, pv.PvAlarm(1, 1, "MINOR problem")),
        (lambda x: True, pv.PvAlarm(0, 0, "No problem")),
    ]

    alarm = [a for f, a in alarms if f(x)][0]

    if alarm.getStatus() > 0:
        logger.warning(
            f"Alarm raised status={alarm.getStatus()} message={alarm.getMessage()}"
        )

    return alarm


def makePV(x, m=10, s=2, HIHI=50, HI=40, LO=20, LOLO=10, timestamp=None):
    if timestamp is None:
        timestamp = timestampnow()

    alarm = makealarm(x, HIHI=HIHI, HI=HI, LO=LO, LOLO=LOLO)

    logger.debug(f"Created PV with value: {x:.4f}")
    mean = pv.PvObject({"value": pv.FLOAT}, {"value": m})
    sigma = pv.PvObject({"value": pv.FLOAT}, {"value": s})
    limits = {
        "HIHI": pv.PvObject({"value": pv.FLOAT}, {"value": HIHI}),
        "HI": pv.PvObject({"value": pv.FLOAT}, {"value": HI}),
        "LO": pv.PvObject({"value": pv.FLOAT}, {"value": LO}),
        "LOLO": pv.PvObject({"value": pv.FLOAT}, {"value": LOLO}),
    }
    name = pv.PvObject({"value": pv.STRING}, {"value": "my:alias:name"})

    return pv.PvObject(
        {
            "value": pv.FLOAT,
            "mean": mean,
            "sigma": sigma,
            "name": name,
            "limits": limits,
            "alarm": alarm,
            "timeStamp": timestamp,
        },
        {
            "value": x,
            "mean": mean.toDict(),
            "sigma": sigma.toDict(),
            "name": name.toDict(),
            "limits": limits,
            "alarm": alarm.toDict(),
            "timeStamp": timestamp.toDict(),
        },
    )


class Cache:
    def __init__(self):
        alarm = makealarm(30)
        self._cache = {
            "mean": 30,
            "sigma": 0,
            "name": "",
            "limits": {
                "hihi": 50,
                "hi": 40,
                "lo": 20,
                "lolo": 10,
            },
            "alarm": alarm,
        }
        self.separator = "/"

    @property
    def maplist(self):
        def getkeys(obj, pstr=""):
            keys = []
            for key in list(obj.keys()):
                keys.append(f"{pstr}{key}")
                if isinstance(obj[key], dict):
                    keys.extend(getkeys(obj[key], pstr=f"{pstr}{key}{self.separator}"))
            return keys

        return getkeys(self._cache)

    def get(self, keystr):
        return reduce(operator.getitem, keystr.split(self.separator), self._cache)

    def _updateDict(self, keystr, value):
        mapList = keystr.split(self.separator)
        reduce(operator.getitem, mapList[:-1], self._cache)[mapList[-1]] = value

    def update(self, keystr, value):
        logger.info(f"Cached {keystr}: {value}")
        self._updateDict(keystr, value)


cache = Cache()


def changed_params_cb(x):
    global cache

    # key is cache, value is from EPICS
    vmap = {
        "mean": "mean/value",
        "sigma": "sigma/value",
        "name": "name/value",
        "limits/hihi": "limits/HIHI/value",
        "limits/hi": "limits/HI/value",
        "limits/lo": "limits/LO/value",
        "limits/lolo": "limits/LOLO/value",
        "alarm": "alarm",
    }

    def log_and_cache(ckey, ekey):
        v = cache.get(ckey)
        e = reduce(operator.getitem, ekey.split("/"), x)
        if e != v:
            cache.update(ckey, e)

    [log_and_cache(c, e) for c, e in vmap.items()]


def runServer():
    pv1 = makePV(0)
    server = pv.PvaServer(PV_NAME, pv1, changed_params_cb)

    while True:
        m = pv1["mean"]["value"]
        s = pv1["sigma"]["value"]
        x = np.random.normal(m, s)
        if x != pv1["value"]:
            pv1["value"] = x
            pv1["timeStamp"] = timestampnow().toDict()
            limits = cache.get("limits")
            pv1["limits"]["HIHI"] = limits["hihi"]
            pv1["limits"]["HI"] = limits["hi"]
            pv1["limits"]["LO"] = limits["lo"]
            pv1["limits"]["LOLO"] = limits["lolo"]
            pv1["alarm"] = makealarm(
                x,
                HIHI=limits["hihi"],
                HI=limits["hi"],
                LO=limits["lo"],
                LOLO=limits["lolo"],
            )
            logger.debug(f"New x value: {x:.4f}")

        time.sleep(abs(np.random.normal(0.3, 0.1)))


runServer()
