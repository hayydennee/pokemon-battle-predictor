# Damage calculation for a Pokemon battle simulator
def calculate_damage(attacker, defender, type_chart):
    # determine whether to use attack or special attack
    if attacker.attack >= attacker.special_attack:
        offensive_stat = attacker.attack
        defensive_stat = defender.defense
    else:
        offensive_stat = attacker.special_attack
        defensive_stat = defender.special_defense

    # look up type multiplier
    multiplier = type_chart[attacker.type1][defender.type1]

    # check for second type
    if defender.type2:
        multiplier *= type_chart[attacker.type1][defender.type2]

    # return damage
    return (offensive_stat / defensive_stat) * multiplier


# Simulate a battle between two Pokemon
def simulate(attacking, defending, type_chart):

    # Simulate the battle until one Pokemon faints
    while attacking.hp > 0 and defending.hp > 0:
        if attacking.speed >= defending.speed:
            # Attacking Pokemon goes first
            damage = calculate_damage(attacking, defending, type_chart)
            defending.hp -= damage

            # Check if defending Pokemon has fainted
            if defending.hp <= 0:
                break

            # Defending Pokemon goes second
            damage = calculate_damage(defending, attacking, type_chart)
            attacking.hp -= damage

        else:            
            # Defending Pokemon goes first
            damage = calculate_damage(defending, attacking, type_chart)
            attacking.hp -= damage

            # Check if attacking Pokemon has fainted
            if attacking.hp <= 0:
                break

            # Attacking Pokemon goes second
            damage = calculate_damage(attacking, defending, type_chart)
            defending.hp -= damage

    # Return the winner    
    return attacking if attacking.hp > 0 else defending