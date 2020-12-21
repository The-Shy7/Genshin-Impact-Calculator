import numpy as np
import random
import time

'''
Script for finding the effective crit rate and crit-rate gain of royal weapons
See https://genshin-impact.fandom.com/wiki/Royal_Greatsword 
'''

def find_EV(base_crit, crit_gain, gain_max_level, num_steps = 10000, batch_size = 100):
    crit_count = 0
    trial_count = 0
    crit_thresh = base_crit * np.ones(batch_size)
    max_crit_rate = base_crit + gain_max_level * crit_gain
    
    while trial_count < num_steps:
        samples = np.random.rand(batch_size)
        
        # print(samples)
        # print(crit_thresh)
        # print(crit_count)
        
        crit_hit = np.less(samples, crit_thresh)
        
        #count number of crits
        crit_count += np.count_nonzero(crit_hit)
        trial_count += batch_size
        
        #increment crit rate on all misses and reset all hits to initial crit rate
        crit_thresh = (1 - crit_hit) * (crit_gain + crit_thresh) + crit_hit * base_crit
        
        # cap crit rate gain at whatever the max crit rate can be.
        if max_crit_rate < 1:
            overcap = np.greater(crit_thresh, max_crit_rate)
            crit_thresh = overcap * max_crit_rate + (1-overcap) * crit_thresh
    
    return crit_count / trial_count
    
def find_EV_baseline(base_crit, crit_gain, max_increment, num_steps):
    crit_count = 0
    attempt_count = 0
    crit_rate = base_crit
    increment = 0

    while attempt_count < num_steps:
        n = random.random()

        if n <= crit_rate:
            #crit
            crit_count += 1
            crit_rate = base_crit
            increment = 0
        else :
            # missed crit
            if increment < max_increment:
                crit_rate += crit_gain
                increment += 1
        
        attempt_count += 1

    return crit_count / attempt_count



if __name__ == "__main__":
    batch_size = 1000
    num_steps = 100000
    base_crit = .05
    crit_gain = .16
    gain_max_level = 5

    tic = time.perf_counter()
    print("Started Calculating effective crit rate...")
    effective_cr = find_EV(base_crit, crit_gain, gain_max_level, num_steps * batch_size, batch_size)
    print("Approximate CritRate: {}".format( effective_cr))
    print("Approximate crit gain: {}".format(effective_cr - base_crit))
    print(f"Executed {num_steps} using batch size {batch_size} in {time.perf_counter() - tic:0.4f}")

    # Base Line Timer (not vectorized)
    # print()
    # tic = time.perf_counter()
    # print("Started Calculating effective crit rate...")
    # crit_list = []
    # for i in range(batch_size):
    #     crit_list.append(find_EV_baseline(base_crit,crit_gain,5, num_steps ))
    # effective_cr = np.mean(np.array(crit_list))
    # print("Approximate CritRate: {}".format( effective_cr))
    # print("Approximate crit gain: {}".format(effective_cr - base_crit))
    # print(f"Executed {num_steps} using batch size {batch_size} in {time.perf_counter() - tic:0.4f}")