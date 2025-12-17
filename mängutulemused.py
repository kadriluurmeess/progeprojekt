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
    },
    {
        "kuupäev": "2025-12-16 20:08:17",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 22,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-16 20:08:18",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 22,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-17 09:50:31",
        "tase": 1,
        "punktid": 2,
        "max_punktid": 11,
        "protsent": 18.2
    },
    {
        "kuupäev": "2025-12-17 09:50:32",
        "tase": 1,
        "punktid": 2,
        "max_punktid": 11,
        "protsent": 18.2
    },
    {
        "kuupäev": "2025-12-17 09:50:49",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 11,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-17 09:50:49",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 11,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-17 09:50:49",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 11,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-17 09:50:50",
        "tase": 1,
        "punktid": 0,
        "max_punktid": 11,
        "protsent": 0.0
    },
    {
        "kuupäev": "2025-12-17 09:52:04",
        "tase": 1,
        "punktid": 5,
        "max_punktid": 11,
        "protsent": 45.5
    },
    {
        "kuupäev": "2025-12-17 09:53:33",
        "tase": 1,
        "punktid": 11,
        "max_punktid": 11,
        "protsent": 100.0
    },
    {
        "kuupäev": "2025-12-17 20:18:46",
        "tase": 1,
        "punktid": 11,
        "max_punktid": 11,
        "protsent": 100.0,
        "kestus_sek": None
    },
    {
        "kuupäev": "2025-12-17 20:58:18",
        "tase": 1,
        "punktid": 2,
        "max_punktid": 2,
        "protsent": 100.0,
        "kestus_sek": 9.20016
    },
    {
        "kuupäev": "2025-12-17 20:58:34",
        "tase": 2,
        "punktid": 2,
        "max_punktid": 2,
        "protsent": 100.0,
        "kestus_sek": 9.50532
    },
    {
        "kuupäev": "2025-12-17 22:35:29",
        "tase": 1,
        "punktid": 2,
        "max_punktid": 2,
        "protsent": 100.0,
        "kestus_sek": 10.562617
    },
    {
        "kuupäev": "2025-12-17 22:35:43",
        "tase": 2,
        "punktid": 2,
        "max_punktid": 2,
        "protsent": 100.0,
        "kestus_sek": 9.942037
    },
    {
        "kuupäev": "2025-12-17 22:36:06",
        "tase": 3,
        "punktid": 1,
        "max_punktid": 1,
        "protsent": 100.0,
        "kestus_sek": 18.984966
    }
]

def add_result(tase: int, punktid: int, max_punktid: int, kestus_sek=None):
    """
    Lisab uue tulemuse TULEMUSED listi.
    
    Args:
        tase: Mängu tase
        punktid: Saadud punktid
        max_punktid: Maksimaalne võimalik punktide arv
        kestus_sek: Mängu kestus sekundites (valikuline)
    """
    protsent = round((punktid / max_punktid * 100), 1) if max_punktid > 0 else 0.0
    
    uus_tulemus = {
        "kuupäev": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tase": tase,
        "punktid": punktid,
        "max_punktid": max_punktid,
        "protsent": protsent,
        "kestus_sek": kestus_sek
    }
    
    TULEMUSED.append(uus_tulemus)
    
    # Salvesta faili
    try:
        _salvesta_faili()
    except Exception as e:
        print(f"Hoiatus: Ei saanud tulemust faili salvestada: {e}")


def get_results():
    """
    Tagastab kõik tulemused.
    
    Returns:
        list: TULEMUSED list
    """
    return TULEMUSED


def _salvesta_faili():
    """
    Salvestab TULEMUSED listi tagasi.
    Kirjutab üle ainult TULEMUSED listi, funktsioonid jäävad puutumata.
    """
    faili_nimi = __file__
    
    # Loe praegune fail
    with open(faili_nimi, 'r', encoding='utf-8') as f:
        read_lines = f.readlines()
    
    # Leia TULEMUSED = [ ja vastav ]
    algus_rida = None
    lopp_rida = None
    sulgude_tase = 0
    
    for i, rida in enumerate(read_lines):
        if 'TULEMUSED = [' in rida and algus_rida is None:
            algus_rida = i
            sulgude_tase = 1
        elif algus_rida is not None:
            sulgude_tase += rida.count('[') - rida.count(']')
            if sulgude_tase == 0:
                lopp_rida = i
                break
    
    if algus_rida is None or lopp_rida is None:
        raise ValueError("Ei suutnud leida TULEMUSED listi")
    
    # Genereeri uus TULEMUSED list
    uued_read = []
    uued_read.append("TULEMUSED = [\n")
    
    for i, tulemus in enumerate(TULEMUSED):
        uued_read.append("    {\n")
        uued_read.append(f'        "kuupäev": "{tulemus["kuupäev"]}",\n')
        uued_read.append(f'        "tase": {tulemus["tase"]},\n')
        uued_read.append(f'        "punktid": {tulemus["punktid"]},\n')
        uued_read.append(f'        "max_punktid": {tulemus["max_punktid"]},\n')
        uued_read.append(f'        "protsent": {tulemus["protsent"]}')
        
        if "kestus_sek" in tulemus:
            uued_read.append(f',\n        "kestus_sek": {tulemus["kestus_sek"]}')
        
        uued_read.append("\n    }")
        if i < len(TULEMUSED) - 1:
            uued_read.append(",")
        uued_read.append("\n")
    
    uued_read.append("]\n")
    
    # Kombineeri: algus + uus TULEMUSED + lõpp (funktsioonid)
    valjund = read_lines[:algus_rida] + uued_read + read_lines[lopp_rida + 1:]
    
    # Kirjuta tagasi
    with open(faili_nimi, 'w', encoding='utf-8') as f:
        f.writelines(valjund)
