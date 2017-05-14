from scoring_settings import ScoringSettings
bs = ScoringSettings.Batting

def pa_extrapolator():
	# Default Values Or Comment Out Inputs to run.
	season_plate_appearances = 432.0
	season_walks = 38.0
	season_IBB = 0
	season_HBP = 5
	season_hits = 119.0
	season_doubles = 27.0
	season_triples = 2.0
	season_home_runs = 8.0
	season_singles = season_hits - season_doubles - season_triples - season_home_runs
	season_runs = 59.0
	season_rbis = 37.0
	season_strikeouts = 42.0
	season_stolen_bases = 3.0
	season_caught_stealing = 2.0
	projected_plate_appearences = 600.0


	# season_plate_appearances = float(raw_input('How many Plate Appearences Last Season?\n                                  '))
	# season_walks = float(raw_input('How many Walks Last Season?\n                    '))
	# season_IBB = float(raw_input('How many Intentional Walks  Last Season?\n                    '))
	# season_HBP =float(raw_input('How many Hit By Pitches Last Season?\n                    '))
	# season_hits = float(raw_input('How many Hits Last Season?\n                    '))
	# season_doubles = float(raw_input('How many Doubles Last Season?\n                    '))
	# season_triples = float(raw_input('How many Triples Last Season?\n                    '))
	# season_home_runs = float(raw_input('How many Home Runs Last Season?\n                    '))
	# season_singles = season_hits - season_doubles - season_triples - season_home_runs
	# season_runs = float(raw_input('How many Runs Last Season?\n                    '))
	# season_rbis = float(raw_input('How many RBI\'s Last Season?\n                    '))
	# season_strikeouts = float(raw_input('How many Strikeouts Last Season?\n                    '))
	# season_stolen_bases = float(raw_input('How many Stolen Bases Last Season?\n                    '))
	# season_caught_stealing = float(raw_input('How many Caught Stealings Last Season?\n                    '))
	# projected_plate_appearences = float(raw_input(('How many Plate Appearances next Season?\n                    '))


	walk_rate = season_walks/season_plate_appearances
	projected_walks = walk_rate * projected_plate_appearences
	project_walk_points = projected_walks * bs.BB
	# calc = ScoringSettings.calculate_off_rate(self)

	# total = calc(self, season_plate_appearances, season_walks, projected_plate_appearences, \
	# 		bs.BB)
	# print self.total
	# print projected_walks

	double_rate = season_doubles / season_plate_appearances
	project_doubles = double_rate * projected_plate_appearences
	project_double_points = project_doubles * bs.D

	# print	double_rate
	# print project_doubles

	triple_rate = season_triples / season_plate_appearances
	prject_triples = triple_rate * projected_plate_appearences
	project_triples_points = prject_triples * bs.T

	home_run_rate = season_home_runs / season_plate_appearances
	projected_home_runs = home_run_rate * projected_plate_appearences
	project_home_runs_points = projected_home_runs * bs.HR

	projected_single_rate = (season_hits - season_doubles - \
	 season_triples - season_home_runs) / season_plate_appearances
	projected_singles = projected_single_rate * projected_plate_appearences
	project_singles_points = projected_singles * bs.S
	# print season_hits - season_doubles - \
	#  season_triples - season_home_runs
	# print projected_single_rate
	# print projected_singles

	run_rate = season_runs / season_plate_appearances
	projected_runs = run_rate * projected_plate_appearences
	project_runs_points = projected_runs * bs.R

	rbi_rate = season_rbis / season_plate_appearances
	projected_rbis = rbi_rate * projected_plate_appearences
	project_rbi_points = projected_rbis * bs.RBI

	strikeout_rate = season_strikeouts / season_plate_appearances
	projected_strikeouts = strikeout_rate * projected_plate_appearences
	project_strikeouts_points = projected_strikeouts * bs.SO

	stolen_base_rate = season_stolen_bases / season_plate_appearances
	projected_stolen_bases = stolen_base_rate * projected_plate_appearences
	project_stolen_base_points = projected_stolen_bases * bs.SB

	caught_stealing_rate = season_caught_stealing / season_plate_appearances
	projected_caught_stealing = caught_stealing_rate * projected_plate_appearences
	project_caught_stealng_points = projected_caught_stealing * bs.CS

	intentoinal_walk_rate = season_IBB / season_plate_appearances
	projected_IBBs = intentoinal_walk_rate * projected_plate_appearences
	project_IBB_points = projected_IBBs * bs.IBB

	hit_by_pitch_rate = season_HBP / season_plate_appearances
	projected_hit_by_pitch = hit_by_pitch_rate * projected_plate_appearences
	projected_hit_by_pitch_points = projected_hit_by_pitch * bs.HBP

	next_season_total = project_walk_points + project_double_points \
		+ project_triples_points + project_home_runs_points \
		+ project_singles_points + projected_runs + projected_rbis \
		+ project_strikeouts_points + project_stolen_base_points \
		+ project_caught_stealng_points + project_IBB_points \
		+ projected_hit_by_pitch_points

	print 'If he gets ' + str(projected_plate_appearences) + ' he\'ll get ' \
		+ str(next_season_total)

pa_extrapolator()