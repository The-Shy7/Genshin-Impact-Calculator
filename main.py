import numpy as np
import os
from itertools import permutations
import random
import artifact

class Weapon:
    def __init__(self, name: str, baseatk, stats):
        elementaldamage = 0
        globalpercent = 0
        self.name = name
        self.baseattack = baseatk
        self.modifiers = np.array([atkpercent, critrate, critdamage, globalpercent, physdmg, elementaldamage, 0, 0, 0, 0, 0, 0, 0, 0])
        # Atk% , cr, crdmg, globaldmg, physdmg, elementaldmg, fire, water, wind, geo, ice, electro, dendro, normal

class Character:
    def __init__(self, name: str, lvl:int, baseatk, modifiers):
        self.modifiers = modifiers
        self.name = name
        self.baseattack = baseatk
        self.lvl = lvl


class Artifact():
    stats = {"Atk%":46.6, "Def%":58.3, "HP%":46.6, "EM":187, "CR":31.1, "CDMG":62.2, "ER":51.8, "PhysDmg":58.3, "ElementalDmg":46.6, "Healing":35.9, "Atk+":311, "HP+":4780}
    valid_main_stats = {1: ["HP+"], 2: ["Atk+"], 3:["Atk%"], 4:["Atk%", "PhysDmg", "ElementalDmg"], 5:["Atk%", "CR", "CDMG"]}
    name_to_idx = {"Atk%": 0, "CR": 1, "CDMG": 2, "Global":3, "PhysDmg":4, "ElementalDmg": 5, "Pyro":6, "Aqua": 7, "Anemo":8,"Geo":9,"Cryo":10,"Electro":11, "Dendro":12, "Normal":13}

    sub_stat_rolls = {"Atk%":[4.1,4.7,5.3,5.8],"CR":[2.7,3.1,3.5,3.9], "CDMG":[5.4,6.2,7,7.8], "ATK+":[14,16,18,19]}
    sub_stats = ["Atk%", "CR", "CDMG", "Atk+",]

    def __init__(self, artifact_number, current_stats=[]):
        self.artifact_number = artifact_number
        if len(current_stats) == 0:
            self.randomize_stats()
        else:
            self.current_substats = current_stats   
    

    def get_modifiers(self) -> np.array:
        modifiers = np.zeros(14)
        for substat, rolls in self.current_substats:
            idx = Artifact.name_to_idx[substat]
            for roll in rolls:
                modifiers[idx] += Artifact.sub_stat_rolls[substat][roll]
        return modifiers
        # current_substats [("substat", [roll1intosubstat, roll2, etc])]

    def randomize_artifact(self):
        possible_main_stats = Artifact.valid_main_stats[self.artifact_number]
        self.main_stat = random.choice[possible_main_stats]
        self.rolls = self._randomize_initial_substats()
        self._randomize_upgrade()

    def _randomize_upgrade(self, numrolls=5):
        for i in range(numrolls):
            roll_num = np.random.randint(4)
            substat, rolls = self.current_substats[roll_num]
            roll_val = np.random.randint(len(Artifact.sub_stat_rolls[substat]))
            rolls.append(roll_val)

    def _randomize_initial_substats(self):
        total_substats = len(Artifact.sub_stats)
        current_substats = np.random.choice(total_substats,4, replace=False)
        current_substats = list(current_substats)
        self.current_substats = [(Artifact.sub_stats[x], []) for x in current_substats]

        for (substat, l) in self.current_substats:
            roll = np.random.randint(len(Artifact.sub_stat_rolls[substat]))
            l.append(roll)


class ArtifactSet():
    set_bonuses = {"Brave Heart": [("Atk%", 18), ("Global", 15)], "Beserker": [("CR", 12), ("CR", 24)], "Gladiators": [("Atk%", 18), ("Normal", 30)], "Thundersoother":[("Atk%",0), ("Global", 35)]}

    def __init__(self , randomize_substats=True):
        self.artifacts = []
        if randomize_substats:
            for i in range(1,6):
                self.artifacts.append(Artifact(i))
        else:
            pass

    def get_collective_modifiers(self):
        modifiers = np.zeros(14)
        for artifact in self.artifacts:
            modifiers += artifact.get_modifiers()

        return modifiers



def getGetDamage(wep:Weapon, ch: Character, artset: ArtifactSet) -> float:
    cumulative_stats = wep.modifiers + ch.modifiers + artset.modifiers
    base_attack = wep.baseattack + ch.baseattack
    base_attack = (base_attack)

def main():
    pass


if __name__ == "__main__":
    main()