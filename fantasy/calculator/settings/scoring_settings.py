class ScoringSettings(object):

	class Batting(object):
		S = 1
		D = 2
		T = 3
		HR = 4
		BB = 1
		IBB = 1 # No longic for this yet
		HBP = 1 # No longic for this yet
		CI = 1 # No longic for this yet
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
		HRA = -2.0
		INN = 3.0
		K = 1.0
		W = 4.0
		L = -3.0
		S = 5.0
		QS = 0.0 # No longic for this yet

	# def calculate_off
