from calculator.settings.logger import log
from calculator.full_season_forecaster.pitcher_inning_extrapelator import inning_extrapolator
import main

class PitchingExtrapolator(object):

	def __self__(self):
		log.debug('Running Pitcher extrapolator')

	def input_last_season_stats(self):
		season_innings = float(input(
			'How many Innings Pitched Last Season?\n\t\t\t\t\t\t'
		))
		season_starts = float(input(
			'How many Game Starts Last Season?\n\t\t\t\t\t\t'
		))
		season_era = float(input(
			'What was the ERA Last Season?\n\t\t\t\t\t\t'
		))
		season_home_runs = float(input(
			'How Many Home Runs Last Season?\n\t\t\t\t\t\t'
		))
		season_strikeouts = float(input(
			'How Many Strikeouts Last Season?\n\t\t\t\t\t\t'
		))
		season_win_total = float(input(
			'How Many Wins Last Season?\n\t\t\t\t\t\t'
		))
		season_loss_total = float(input(
			'How many Losses Last Season?\n\t\t\t\t\t\t'
		))
		season_hits_allowed = float(input(
			'How Many Hits Last Season?\n\t\t\t\t\t\t'
		))
		season_walk_total = float(input(
			'How Many Walks last season?\n\t\t\t\t\t\t'

		))
		projected_starts = float(input(
			'How many starts next season?\n\t\t\t\t\t\t'
		))
		projected_fip = float(input(
			'What was the FIP\n\t\t\t\t\t\t'
		))
		return season_innings, season_starts, season_era, season_win_total, season_loss_total, \
			season_hits_allowed, season_home_runs, season_walk_total, season_strikeouts, projected_starts, projected_fip


	def run(self):
		season_innings, season_starts, season_era, season_win_total, \
			 season_loss_total, season_hits_allowed, season_home_runs, \
			 season_walk_total, season_strikeouts, projected_starts, \
			 projected_fip = self.input_last_season_stats()
		new_season_total = inning_extrapolator(
			season_innings, season_starts, season_era, season_win_total, \
			season_loss_total, season_hits_allowed, season_home_runs, \
			season_walk_total, season_strikeouts, projected_starts, \
			projected_fip
		)
		print('The pitchers projected total is %d' %  new_season_total)
		self.do_next()

	def do_next(self):
		e_prompt = input(
			'What you want to do next? [(r)un again, (e)xit, (m)ain menu]' \
			'\n\t\t\t\t\t\t'
		)
		if e_prompt == 'r' or 'run' in e_prompt:
			self.run()
		elif e_prompt == 'm' or 'main' in e_prompt:
			main.main()
		else:
			exit()
