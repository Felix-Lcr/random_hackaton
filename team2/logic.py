from collections import Counter


def evaluer_main(des):
    compte = Counter(des)
    valeurs = sorted(compte.values(), reverse=True)
    uniques = sorted(set(des))
    est_suite = len(uniques) == 5 and (uniques[-1] - uniques[0] == 4)

    if valeurs == [5]:
        return "FIVE OF A KIND", 120, 12
    if valeurs[0] == 4:
        return "FOUR OF A KIND", 60, 7
    if est_suite:
        return "STRAIGHT", 50, 5
    if valeurs == [3, 2]:
        return "FULL HOUSE", 40, 4
    if valeurs[0] == 3:
        return "THREE OF A KIND", 30, 3
    if valeurs[:2] == [2, 2]:
        return "TWO PAIR", 20, 2
    if valeurs[0] == 2:
        return "PAIR", 10, 2
    return "HIGH CARD", 5, 1


def calculer_score(des):
    nom, chips_base, multi = evaluer_main(des)
    somme_des = sum(des)
    score = (chips_base + somme_des) * multi
    return nom, chips_base, somme_des, multi, score
