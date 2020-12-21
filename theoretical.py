import numpy as np
import os
from itertools import permutations
import random

def get_blank_modifiers():
    return np.zeros(len(Artifact.name_to_idx))

def get_modifier_value(modifier_arr:np.array, modifier_name: str):
    return modifier_arr[Artifact.name_to_idx[modifier_name]]

#returns the modifiers array from the given stat dictionary
def get_modifiers_from_stat_dict(stats:dict):
    modifiers = get_blank_modifiers()
    
    for k,v in stats.items():
        modifiers[Artifact.name_to_idx[k]] = v
    return modifiers

#Finished
class Weapon:
    def __init__(self, name: str, baseatk, stats:dict):
        elementaldamage = 0
        globalpercent = 0
        self.name = name
        self.baseattack = baseatk
        self.modifiers = get_modifiers_from_stat_dict(stats)
        # self.modifiers = np.array([atkpercent, critrate, critdamage, globalpercent, physdmg, elementaldamage, 0, 0, 0, 0, 0, 0, 0, 0])
        # Atk% , cr, crdmg, globaldmg, physdmg, elementaldmg, fire, water, wind, geo, ice, electro, dendro, normal

class Character:
    def __init__(self, name: str, lvl:int, baseatk, stats:dict):
        self.name = name
        self.baseattack = baseatk
        self.lvl = lvl
        self.modifiers = get_modifiers_from_stat_dict(stats)

class Artifact():
    '''
    Class for managing a single artifact and its substat values. Global fields are included in the class as these can be randomized.
    '''
    stats = {"Atk%":46.6, "Def%":58.3, "HP%":46.6, "EM":187, "CR":31.1, "CDMG":62.2, "ER":51.8, "PhysDmg":58.3, "ElementalDmg":46.6, "Healing":35.9, "Atk+":311, "HP+":4780}
    valid_main_stats = {1: ["HP+"], 2: ["Atk+"], 3:["Atk%"], 4:["Atk%", "PhysDmg", "ElementalDmg"], 5:["Atk%", "CR", "CDMG"]}
    name_to_idx = {"Atk%": 0, "CR": 1, "CDMG": 2, "Global":3, "PhysDmg":4, "ElementalDmg": 5, "Pyro":6, "Aqua": 7, "Anemo":8,"Geo":9,"Cryo":10,"Electro":11, "Dendro":12, "Normal":13, "Atk+": 14}
    sub_stat_rolls = {"Atk%":[4.1,4.7,5.3,5.8],"CR":[2.7,3.1,3.5,3.9], "CDMG":[5.4,6.2,7,7.8], "ATK+":[14,16,18,19]}
    valid_sub_stats = ["Atk%", "CR", "CDMG", "Atk+",]

    def __init__(self, artifact_number, current_stats=[]):
        self.artifact_number = artifact_number
        
        if len(current_stats) == 0:
            self.randomize_stats()
        else:
            self.current_substats = current_stats   

    def get_modifiers(self) -> np.array:
        modifiers = get_blank_modifiers()
        
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
        total_substats = len(Artifact.valid_sub_stats)
        current_substats = np.random.choice(total_substats,4, replace=False)
        current_substats = list(current_substats)
        self.current_substats = [(Artifact.valid_sub_stats[x], []) for x in current_substats]

        for (substat, l) in self.current_substats:
            roll = np.random.randint(len(Artifact.sub_stat_rolls[substat]))
            l.append(roll)

class ArtifactSet():
    '''
    Class for managing sets of artifacts, which is the modifiers of 5 artifacts together as well as a set bonus.
    '''
    set_bonuses = {"Brave Heart": [("Atk%", 18), ("Global", 15)], "Beserker": [("CR", 12), ("CR", 24)], 
                    "Gladiators": [("Atk%", 18), ("Normal", 30)], "Thundersoother":[("Atk%",0), ("Global", 35)],
                    "Crimson Witch of Flames": [("Pyro", 15), ("Pyro", 22.5)]}

    def __init__(self , randomize_substats=True):
        self.artifacts = []
        
        if randomize_substats:
            for i in range(1,6):
                self.artifacts.append(Artifact(i))
        else:
            pass

    def get_collective_modifiers(self):
        modifiers = get_blank_modifiers()
        
        for artifact in self.artifacts:
            modifiers += artifact.get_modifiers()

        return modifiers

#finished
def getDamage(wep:Weapon, ch: Character, artset: ArtifactSet, dmg_percents):
    # inputs a weapon, character, artifact set, and a list of dmg percents, and returns the overall percent damage
    # after all multiplers are apllied
    #
    # dmg_percents is a list of tuples (total%, ["type1", "type2", etc])
    cum_mods = wep.modifiers + ch.modifiers + artset.get_collective_modifiers()
    base_attack = wep.baseattack + ch.baseattack
    atk_mod = (base_attack) * get_modifier_value(cum_mods, "Atk%") + get_modifier_value(cum_mods, "Atk+")
    crit_rate = min(get_modifier_value(cum_mods, "CR"), 85)
    crit_mod = crit_rate / 100 * (1 + get_modifier_value(cum_mods,"CDMG") / 100) + (1-crit_rate/100)
    total_percent_dmg = 0

    for percent, types in dmg_percents:
        damage_specific_mods = 1
        
        for ty in types: 
            damage_specific_mods += get_modifier_value(cum_mods, ty) / 100

        damage_specific_mods += get_modifier_value(cum_mods, "Global") / 100
        total_percent_dmg += percent * damage_specific_mods * base_attack * crit_mod

    return total_percent_dmg

#Todo: Establish the correct iterator or pose as a linear optimization problem. 
def generate_optimal_damage_output(damager_dealer:Character, slap_stick: Weapon, time, percentage_counts, output_file_path):
    bonuses_list = ArtifactSet.set_bonuses.items()

    for i in range(len(bonuses_list)):
        active_set_bonuses = [(i, 1)]
        active_set_bonuses.append((i, 2))
        set_modifiers = get_blank_modifiers()

        # Replace nested for loops with iterator for the active classes
        for active_set_idx, lvl in active_set_bonuses:
            set_modifier_1 = get_modifiers_from_stat_dict(dict(ArtifactSet.set_bonuses[active_set_idx][lvl]))

        for j in range(i, len(bonuses_list)):
            # For every combination of active artifact set bonuses
                # For every possible cominbation of main stats
                    # For every possible combination of sub stats
                        # for each weapon

            pass


if __name__ == "__main__":
    time = 30
    damage_percents = [(1921, ["Normal", "PhysDmg"]), (810, ["Electro", "Elemental"])]
    output_file = os.path.join(os.getcwd(), "data")
    generate_optimal_damage_output(time, damage_percents, output_file)