BOSS_MAX_HP = 300
BOSS_ATTACK_BASE = 5
BOSS_ATTACKS_PER_TURN = 1


def calcul_degats_boss(niveau):
    degat_par_coup = BOSS_ATTACK_BASE * (2 ** (niveau - 1))
    return degat_par_coup, BOSS_ATTACKS_PER_TURN
