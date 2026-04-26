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
