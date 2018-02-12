from full_season_forecaster.pitcher_calaculator import calculate_game
from os import sys

def input_last_outing_stats():
		outing_innings = float(raw_input('How many Innings?\n                                  '))
		outing_homeruns_allowed = float(raw_input('How Many Home Runs?\n                           '))
		outing_strikeouts = float(raw_input('How Many Strikeouts?\n                               '))
		outing_hits_allowed = float(raw_input('How Many Hits?\n                          '))
		outing_total_walks = float(raw_input('How Many Walks?\n                             '))
		outing_earned_runs = float(raw_input('How Many Earned Runs?\n                             '))
		if outing_innings >= 6 and outing_earned_runs <= 3:
			outing_quality_starts = 1
		else:
			outing_quality_starts = 0
		outing_win = 0
		outing_loss = 0
		outing_blown_saves = 0
		outing_saves = 0
		decision = raw_input('Did the pitcher get a win, loss, save, or blown save?\n                             ')
		if decision.lower() == "win":
			outing_win = 1
		elif decision.lower() == "loss" or  decision.lower() == "lost":
			outing_losses = 1
		elif decision.lower().replace(' ', '') == "blownsave":
			outing_blown_saves = 1
		elif decision.lower().replace(' ', '') == "save":
			outing_saves = 1
		else:
			print("error")
			sys.exit()
		# projected_fip = float(raw_input('What was the FIP\n                           '))
		projected_fip = 0
		return outing_innings, outing_earned_runs, outing_win, outing_loss, outing_blown_saves, \
			outing_saves, outing_quality_starts, outing_hits_allowed, outing_homeruns_allowed, \
			outing_total_walks, outing_strikeouts, projected_fip

outing_innings, outing_earned_runs, outing_win, outing_loss, outing_blown_saves, \
			outing_saves, outing_quality_starts, outing_hits_allowed, outing_homeruns_allowed, \
			outing_total_walks, outing_strikeouts, projected_fip = input_last_outing_stats()


result = calculate_game(outing_innings, outing_earned_runs, \
	outing_total_walks,outing_hits_allowed, outing_homeruns_allowed, outing_strikeouts, \
	outing_saves, outing_win, outing_loss, outing_quality_starts)

print(result)
