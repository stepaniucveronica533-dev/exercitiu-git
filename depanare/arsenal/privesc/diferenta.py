from arsenal.privesc.enum import nume, GTFO
def citeste_linii(fisier):
    with open(fisier, "r", encoding="utf-8") as f:
        return f.read().splitlines()

def cai(fisier):
    return set(citeste_linii(fisier))

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("vechi")
    p.add_argument("nou")
    args = p.parse_args()
    vechi = cai(args.vechi)
    nou = cai (args.nou)
    adaugate = nou - vechi
    sterse = vechi - nou
    print(len(adaugate), "SUID noi fata de sistemul curat")
    for c in sorted(adaugate):
        print(" ", c)
    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in adaugate}
    periculoase = [c for c in sorted(adaugate) if nume(c) in GTFO]
    print("periculoase NOI:", periculoase)
if __name__ == "__main__":
    main()






