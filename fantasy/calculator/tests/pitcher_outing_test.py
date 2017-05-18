from full_season_forecaster.pitcher_calaculator import calculate_game

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

test_example = calculate_game(ExampleOuting.innings, ExampleOuting.earned_runs, \
	ExampleOuting.total_walks, ExampleOuting.hits_allowed, \
	ExampleOuting.homeruns_allowed, ExampleOuting.strikeouts, \
	ExampleOuting.saves, ExampleOuting.wins, ExampleOuting.losses, \
	ExampleOuting.quality_starts)

print test_example
