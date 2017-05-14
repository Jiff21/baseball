class ScoringSettings(object):

	print 'Loaded scoring settings'

	class Batting(object):
		S = 1
		D = 2
		T = 3
		HR = 4
		BB = 1
		IBB = 1
		HBP = 1
		R = 1
		RBI = 1
		SB = 2
		CS = -1
		SO = -1

	# def calculate_off_rate(old_total, thing_total, new_total, scoring):

	#     def __init__(self):
	# 		self.rate = thing_total / old_total
	# 		self.projected_things = rate * new_total
	# 		self.projected_total = projected_things * scoring
	# 		return self.projected_total