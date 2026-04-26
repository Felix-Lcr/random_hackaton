import csv
import os

SCOREBOARD_FILE = "scoreboard.csv"


def charger_scores():
    scores = []
    if os.path.exists(SCOREBOARD_FILE):
        with open(SCOREBOARD_FILE, "r", encoding="utf-8") as f:
            for ligne in csv.reader(f, delimiter=";"):
                if ligne:
                    scores.append(ligne)
    return scores[:3]


def sauvegarder_score(nom, lancers):
    scores = charger_scores()
    scores.append(["?", nom, str(lancers)])
    scores.sort(key=lambda x: int(x[2]))
    final = [[str(i + 1), s[1], s[2]] for i, s in enumerate(scores[:3])]
    with open(SCOREBOARD_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, delimiter=";").writerows(final)
