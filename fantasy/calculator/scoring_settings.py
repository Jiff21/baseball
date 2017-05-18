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

	class Pitching(object):
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

	# def calculate_off_rate(old_total, thing_total, new_total, scoring):

	#     def __init__(self):
	# 		self.rate = thing_total / old_total
	# 		self.projected_things = rate * new_total
	# 		self.projected_total = projected_things * scoring
	# 		return self.projected_total