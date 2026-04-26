def resolve_player_turn(hero, enemy, slots):
    events = []
    for s in slots:
        if not s.dice:
            continue
        total = s.total
        if s.kind == 'attack':
            enemy.hp = max(0, enemy.hp - total)
            events.append(('dmg_enemy', total))
        elif s.kind == 'heal':
            hero.hp = min(hero.max_hp, hero.hp + total)
            events.append(('heal_hero', total))
        elif s.kind == 'defense':
            hero.block = total
            events.append(('block', total))
    return events

def resolve_enemy_turn(hero, enemy):
    raw = enemy.roll_attack()
    absorbed = min(hero.block, raw)
    dmg = raw - absorbed
    hero.block = max(0, hero.block - raw)
    hero.hp = max(0, hero.hp - dmg)
    return {'raw': raw, 'absorbed': absorbed, 'dmg': dmg}
