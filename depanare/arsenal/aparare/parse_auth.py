import re
from collections import Counter


# Tiparul pentru găsirea autentificărilor eșuate
TIPAR = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\S+) port"
)


# A1: Verifică un rând și întoarce utilizatorul și IP-ul
def esec(linie):
    m = TIPAR.search(linie)

    if m is None:
        return None

    return (m.group(1), m.group(2))


# A2: Citește fișierul și formează lista eșecurilor
def citeste_esecuri(cale):
    esecuri = []

    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri

    with f:
        for linie in f:
            r = esec(linie)

            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})

    return esecuri


# A3: Numără eșecurile pentru fiecare adresă IP
def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)


# A4: Citește, numără și afișează rezumatul
def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("log")
    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)

    print("Esecuri de autentificare:", len(esecuri))

    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")


# Pornește funcția principală când rulăm acest program
if __name__ == "__main__":
    main()