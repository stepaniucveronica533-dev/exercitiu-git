import argparse
import json
from dataclasses import asdict, dataclass


CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        for fragment in CAI_SUSPECTE:
            if fragment in self.cale:
                return True
        return False


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"


def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        date = json.load(f)
        return [Proces(**d) for d in date]


def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        date = json.load(f)
        return [Eveniment(**d) for d in date]


@dataclass
class Inventar:
    procese: list

    @classmethod
    def din_json(cls, cale):
        procese = procese_din_json(cale)
        return cls(procese)

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self):
        grupuri = {}
        for p in self.procese:
            grupuri.setdefault(p.user, []).append(p.nume)
        return grupuri


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("capturi")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    inv = Inventar.din_json(args.capturi + "/procese.json")
    evenimente = evenimente_din_json(args.capturi + "/evenimente.json")
    suspecte = inv.suspecte()
    alarme = [e for e in evenimente if e.e_suspect()]

    if args.json:
        raport = {
            "procese_suspecte": [asdict(p) for p in suspecte],
            "alarme": [asdict(e) for e in alarme],
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    print(f"Procese: {len(inv)} | suspecte: {len(suspecte)}")
    for p in suspecte:
        print(f"  [{p.pid}] {p.nume} ({p.user}) {p.cale}")

    print(f"Evenimente: {len(evenimente)} | alarme: {len(alarme)}")
    for e in alarme:
        print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")


if __name__ == "__main__":
    main()