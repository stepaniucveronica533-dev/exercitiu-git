import argparse
import json  # Ne ajuta sa salvam raportul in format JSON
import sys  # Citim argumentele programului
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        return [linie.strip() for linie in f
                if linie.strip() and not linie.strip().startswith("#")]

from pathlib import Path
cai = citeste_linii(Path(__file__).parent / "start" / "suid.txt")
# Afisam mesajul doar cand nu cerem JSON
if "--json" not in sys.argv:
    print("linii SUID:", len(cai))
def nume(cale):
    return str(cale).rsplit("/", 1)[-1]

nume_unice = {nume(c) for c in cai}
# Afisam rezultatul doar daca nu cerem JSON
if "--json" not in sys.argv:
    print("SUID distincte:", len(nume_unice))



# A3 - Verificam fisierele SUID

GTFO = {"find", "vim.basic", "vim", "nmap", "cp",
        "bash", "less", "awk", "python3", "perl"}

def suid_constatari(cai):
    rezultat = []
    for c in sorted(set(cai)):
        fisier = {
            "cale": str(c),
            "nume": nume(c),
            "risc": "mare" if nume(c) in GTFO else "normal"
        }
        rezultat.append(fisier)
    return rezultat

suid = suid_constatari(cai)
mari = [c for c in suid if c["risc"] == "mare"]


# Afisam rezultatele doar daca nu cerem JSON
if "--json" not in sys.argv:
    print(len(suid), "SUID,", len(mari), "cu risc mare")
    print(sorted(c["nume"] for c in mari))



# A4 - Citim informatiile sudo

def sudo_constatari(cale):
    rezultat = []
    for linie in citeste_linii(cale):
        user, drept = linie.split(" : ", 1)
        rezultat.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal"
        })
    return rezultat

sudo = sudo_constatari(
    Path(__file__).parent / "start" / "sudo.txt"
)


# Afisam rezultatul sudo doar daca nu cerem JSON
if "--json" not in sys.argv:
    print("sudo:", len(sudo), "gasite")



# A4 - Citim sarcinile programate (cron)

def cron_constatari(cale):
    rezultat = []

    for linie in citeste_linii(cale):
        campuri = linie.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])

        rezultat.append({
            "user": user,
            "comanda": comanda,
            "risc": "normal"
        })

    return rezultat


cron = cron_constatari(
    Path(__file__).parent / "start" / "crontab.txt"
)


# Afisam rezultatul cron doar daca nu cerem JSON
if "--json" not in sys.argv:
    print("cron:", len(cron), "gasite")


# A4 - Grupam toate rezultatele intr-un dicționar

raport = {
    "suid": suid,   # Lista fisierelor SUID
    "sudo": sudo,   # Lista drepturilor utilizatorilor
    "cron": cron    # Lista sarcinilor programate
}


# Afisam rezultatele doar daca nu cerem JSON
if "--json" not in sys.argv:
    print("SUID:", len(raport["suid"]))
    print("sudo:", len(raport["sudo"]))
    print("cron:", len(raport["cron"]))


# A5 - Pregatim raportul final

def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    # Grupam rezultatele pentru raport
    raport_final = {
        "suid": suid,
        "sudo": sudo,
        "cron": cron
    }

    # Verificam daca utilizatorul a cerut formatul JSON
    if a.json:
        # Afisam raportul in format JSON
        print(json.dumps(raport_final, indent=2, ensure_ascii=False))
        return


    # Verificam fiecare categorie din raport
    for categorie, lista in raport_final.items():

        # Alegem elementele cu risc mare
        mari = [c for c in lista if c.get("risc") == "mare"]

        # Afisam numarul total si riscurile mari
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    # Adunam utilizatorii din sudo si cron
    utilizatori = {c["user"] for c in raport_final["sudo"]}

    utilizatori.update(c["user"] for c in raport_final["cron"])



    # Afisam numele fara repetari
    print("utilizatori implicati:", ", ".join(sorted(utilizatori)))

    # Salvam raportul intr-un fisier JSON
    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport_final, f, indent=2, ensure_ascii=False)

    # Anuntam ca raportul a fost salvat
    print("Raport salvat in enum.json")
    # Pornim programul principal


if __name__ == "__main__":
    main()





