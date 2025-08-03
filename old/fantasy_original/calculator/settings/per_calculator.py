'''
To calculate the average expected score of a team verse leftys we need to calculate.
ab_per_game
hits_per_ab = total_hits/total_ab
hr_per_ab = total_hr/total_ab
er_per_ab = total_ER/total_ab
runs_per_ab = total_runs/total_ab
rbis_per_ab = total_rbis/total_ab
so_per_ab = total_so/total_ab
bb_per_ab = total_bb/total_ab
wins_per_ab = 
'''



def get_average_per_ab(this_stat,this_ab_total):
    return float(this_stat)/float(this_ab_total)
