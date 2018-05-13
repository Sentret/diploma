import math

def cantor_pairing(x, y):
	return 0.5 * (x+y) * (x+y+1) + y

def inverse_cantor_pairing(z):
	w = (math.sqrt(8 * z + 1) - 1) / 2
	w = math.floor(w)
	t = w*(w+1)/2
	y = int(z - t)
	x = int(w - y)
	return [x,y]

