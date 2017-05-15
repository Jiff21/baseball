
class ScoringSettings(object):
	BB = -1.0
	BBI = -1.0
	ER = -1.0
	HA = -1.0
	HB = -1.0
	HRA = -3.0
	INN = 3.0
	K = 1.0
	W = 5.0
	L = -3.0
	S = 5.0
	QS = 0.0

class ExampleOuting(object):
	total_walks = 3.0
	earned_runs = 3.0
	innings = 7.0
	wins = 0.0
	losses = 0.0
	strikeouts = 7.0
	saves = 0.0
	hits_allowed = 10.0
	homeruns_allowed = 1.0
	quality_starts = 0.0


def calculate_game(innings, earned_runs, total_walks, hits_allowed, \
	homeruns_allowed, strikeouts, saves, wins, losses, quality_starts):
	print 'In Calculate game \nWins ' + str(wins) + '\nlosses: ' + str(losses)
	total = (innings * ScoringSettings.INN) + (earned_runs \
		* ScoringSettings.ER) + (total_walks * ScoringSettings.BBI) \
		+ (hits_allowed * ScoringSettings.HA) \
		+ (homeruns_allowed * ScoringSettings.HRA) \
		+ (strikeouts * ScoringSettings.K) \
		+ (saves * ScoringSettings.S) \
		+ (wins * ScoringSettings.W) \
		+ (losses * ScoringSettings.L) \
		+ (quality_starts * ScoringSettings.QS)
	return total

def inning_extrapolator():
	# Default Values Or Comment Out Inputs to run.
	season_innings = 72.1
	season_starts = 11.0
	season_era = 2.89
	season_win_total = 5.0
	season_loss_total = 3.0
	season_hits_allowed = 78.0  
	season_home_runs = 11.0
	season_walk_total = 23.0
	season_strikeouts = 66.0
	projected_starts = 31.0
	projected_fip =  4.37

	# season_innings = float(raw_input('How many Innings Pitched Last Season?\n                                  '))
	# season_starts = float(raw_input('How many Game Starts Last Season?\n                                    '))
	# season_era = float(raw_input('What was the ERA Last Season?\n                           '))
	# season_home_runs = float(raw_input('How Many Home Runs Last Season?\n                           '))
	# season_strikeouts = float(raw_input('How Many Strikeouts Last Season?\n                               '))
	# season_win_total = float(raw_input('How Many Wins Last Season?\n                        '))
	# season_loss_total = float(raw_input('How many Losses Last Season?\n                           '))
	# season_hits_allowed = float(raw_input('How Many Hits Last Season?\n                          '))
	# season_walk_total = float(raw_input('How Many Walks last season?\n                             '))
	# projected_starts = float(raw_input('How many starts next season?\n                           '))
	# projected_fip = float(raw_input('What was the FIP\n                           '))


	innings_projection = round(projected_starts * (season_innings / season_starts), 1)
	points_from_innings = round(innings_projection * ScoringSettings.INN, 1)
	# print 'Innings Projection is: ' + str(innings_projection)
	# print 'points_from_innings Projection is:\n ' + str(points_from_innings)
	# print '\n\n'

	projected_win_percentage = season_win_total / season_starts
	points_from_wins = round((projected_starts * projected_win_percentage) * ScoringSettings.W, 0)

	projected_loss_percentage = season_loss_total / season_starts
	points_from_losses = round((projected_starts * projected_loss_percentage) * ScoringSettings.L, 0)
	# print 'projected_win_percentage Projection is:\n ' + str(projected_win_percentage)
	# print 'points_from_wins Projection is:\n ' + str(points_from_wins)
	# print '\n\n'
	# print 'projected_loss_percentage Projection is:\n ' + str(projected_loss_percentage)
	# print 'points_from_losses Projection is:\n ' + str(points_from_losses)
	# print '\n\n'

	points_from_earned_runs = round((innings_projection * (season_era/9)), 2) * ScoringSettings.ER
	# print 'points_from_earned_runs Projection is:\n ' + str(points_from_earned_runs)
	# print '\n\n'

	homerun_rate = season_home_runs/season_innings
	projected_hra = round(homerun_rate * innings_projection, 0)
	points_from_home_runs = int(projected_hra * ScoringSettings.HRA)
	# print 'homerun_rate Projection is:\n ' + str(homerun_rate)
	# print 'projected_hra Projection is:\n ' + str(projected_hra)
	# print 'points_from_home_runs Projection is:\n ' + str(points_from_home_runs)
	# print '\n\n'

	strikeout_rate = season_strikeouts/season_innings
	projected_stikeouts = round(strikeout_rate * innings_projection, 0)
	points_from_strikeouts = int(projected_stikeouts * ScoringSettings.K)
	# print 'strikeout_rate Projection is:\n ' + str(strikeout_rate)
	# print 'projected_stikeouts Projection is:\n ' + str(projected_stikeouts)
	# print 'points_from_strikeouts Projection is:\n ' + str(points_from_strikeouts)
	# print '\n\n'


	hit_rate = season_hits_allowed/season_innings
	projected_hits = round(hit_rate * innings_projection, 0)
	points_from_hits = int(projected_hits * ScoringSettings.HA)
	# print 'hit_rate Projection is:\n ' + str(hit_rate)
	# print 'projected_hits Projection is:\n ' + str(projected_hits)
	# print 'points_from_hits Projection is:\n ' + str(points_from_hits)
	# print '\n\n'


	walk_rate = season_walk_total/season_innings
	projected_walks = round(walk_rate * innings_projection, 0)
	points_from_walks = int(projected_walks * ScoringSettings.BB)
	# print 'walk_rate Projection is:\n ' + str(walk_rate)
	# print 'projected_walks Projection is:\n ' + str(projected_walks)
	# print 'points_from_walks Projection is:\n ' + str(points_from_walks)
	# print '\n\n'



	next_season_total = points_from_innings + points_from_strikeouts + points_from_wins \
		+ points_from_losses + points_from_hits + points_from_walks + points_from_home_runs \
		+ points_from_earned_runs
	print 'Next Seasons Total based on ERA would be: ' + str(next_season_total)

	points_from_fip_runs = round((innings_projection * (projected_fip/9)), 2) * ScoringSettings.ER
	next_season_total = points_from_innings + points_from_strikeouts + points_from_wins \
		+ points_from_losses + points_from_hits + points_from_walks + points_from_home_runs \
		+ points_from_fip_runs
	print 'Next Seasons Total based on ERA would be: ' + str(next_season_total)


test_example = calculate_game(ExampleOuting.innings, ExampleOuting.earned_runs, \
	ExampleOuting.total_walks, ExampleOuting.hits_allowed, \
	ExampleOuting.homeruns_allowed, ExampleOuting.strikeouts, \
	ExampleOuting.saves, ExampleOuting.wins, ExampleOuting.losses, \
	ExampleOuting.quality_starts)

# print test_example

# new_season_total = inning_extrapolator()
