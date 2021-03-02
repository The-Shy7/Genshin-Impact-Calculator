import numpy as np

class Weapon(object):
    def __init__(self, base_attack, attack_mod, special_mod, mv_mod, crit, cdmg):
        self.base_attack = base_attack
        self.attack_mod = attack_mod
        self.special_mod = special_mod
        self.mv_mod = mv_mod
        self.crit = crit 
        self.cdmg = cdmg

class Character(object):
    def __init__(self, base_attack, attack_mod, special_mod, crit, cdmg):
        self.base_attack = base_attack
        self.attack_mod = attack_mod
        self.special_mod = special_mod
        self.crit = crit 
        self.cdmg = cdmg

class ArtifactSet(object):
    def __init__(self, attack_mod, special_mod, crit):
        self.attack_mod = attack_mod
        self.special_mod = special_mod
        self.crit = crit 

def get_eval(wep: Weapon, char: Character, art: ArtifactSet):
        
    def evaluate(a, c, d):
        cr_rate = min(.05 + .039*(c+5) + wep.crit + art.crit + char.crit, 1)
        return ((wep.base_attack + char.base_attack) * (0.058* (a+4)+1 + art.attack_mod + char.attack_mod + wep.attack_mod) + 311) * ( # Attack Mod
                cr_rate * (1.5 + 0.078*(d + 4)) + 1 - cr_rate) * ( # Crit 
                    1 + .583 + char.special_mod + wep.special_mod + art.special_mod) # Special Mod

    return evaluate

def get_highest(wep: Weapon, char: Character, art: ArtifactSet):
    multiplier_calc = get_eval(wep, char, art)
    res = []
    for a in range(21):
        for c in range(26):
            if a + c <= 25:
                d = 25 - a - c
                temp = ((a,c,d), multiplier_calc(a,c,d))
                res.append(temp)
                # print(temp)
    res.sort(key=lambda x: x[1], reverse=True)
    return res[0], res[1], res[2]

if __name__ == "__main__":
    razor = Character(234, 0, .30, 0, 0)
    Skyward_pride = Weapon(674, 0, .08, .80, 0,0)
    wolfs_grave = Weapon(608, .796, 0,0,0,0)
    gladiators = ArtifactSet(.15, .35,0)


    print(get_highest(razor,Skyward_pride,gladiators))
    print(get_highest(razor,wolfs_grave,gladiators))