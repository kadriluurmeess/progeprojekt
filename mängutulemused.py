import json
import os
from datetime import datetime

TULEMUSED = [
    {
        "kuupäev": "2025-12-13 09:51:29",
        "tase": 1,
        "punktid": 2,
        "max_punktid": 6,
        "protsent": 33.3
    },
    {
        "kuupäev": "2025-12-13 09:52:02",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 4,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-13 09:52:12",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 4,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-13 09:52:14",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 4,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-13 09:53:21",
        "tase": 1,
        "punktid": 2,
        "max_punktid": 4,
        "protsent": 50.0
    },
    {
        "kuupäev": "2025-12-13 09:53:38",
        "tase": 1,
        "punktid": 2,
        "max_punktid": 2,
        "protsent": 100.0
    },
    {
        "kuupäev": "2025-12-13 09:57:28",
        "tase": 2,
        "punktid": 20,
        "max_punktid": 30,
        "protsent": 66.7
    },
    {
        "kuupäev": "2025-12-13 09:58:45",
        "tase": 2,
        "punktid": 10,
        "max_punktid": 10,
        "protsent": 100.0
    },
    {
        "kuupäev": "2025-12-13 10:09:44",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 6,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-13 10:09:46",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 6,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-13 10:09:46",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 6,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-13 10:09:47",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 6,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-13 10:10:03",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 6,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-13 10:10:07",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 6,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-16 19:44:39",
        "tase": 99,
        "punktid": 1,
        "max_punktid": 2,
        "protsent": 50.0
    }
]


def _save_results_to_module():
    """Kirjuta TULEMUSED tagasi sellesse moodulifaili."""
    path = os.path.abspath(__file__)
    content = "TULEMUSED = " + json.dumps(TULEMUSED, indent=4, ensure_ascii=False) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def get_results():
    """Tagasta tulemuste koopia."""
    return list(TULEMUSED)


def add_result(tase: int, punktid: int, max_punktid: int, kuupäev: str | None = None):
    """Lisa uus tulemus ja salvesta failina."""
    if kuupäev is None:
        kuupäev = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    protsent = round((punktid / max_punktid * 100) if max_punktid > 0 else 0.0, 1)

    TULEMUSED.append({
        "kuupäev": kuupäev,
        "tase": tase,
        "punktid": punktid,
        "max_punktid": max_punktid,
        "protsent": protsent
    })

    _save_results_to_module()
