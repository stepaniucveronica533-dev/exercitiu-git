
def test_doar_ce_e_nou():
    # Lista cu elementele actuale
    acum = {"a", "b", "c"}

    # Lista cu elementele vechi
    baza = {"a", "b"}

    # Verificam ca doar "c" este nou
    assert acum - baza == {"c"}
