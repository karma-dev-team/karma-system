import decimal

import numpy as np

from app.karma.consts import MAX_BAN_THRESHOLD, SCALE_FACTOR, WARN_BASE_DELTA, LIKE_BASE_DELTA

Number = int | float | decimal.Decimal


def timed_sigmoid_function(time: Number, threshold: Number):
	return 1 / (1 + np.exp(-(time - threshold)))


def sigmoid_function(x: Number, threshold: Number, scale_factor=SCALE_FACTOR) -> Number:
	return 1 / (1 + np.exp(-scale_factor * (x - threshold)))


def calc_karma_koef(server_karma: Number, player_karma: Number) -> Number:
	if server_karma > player_karma:
		k = player_karma / server_karma
	else:
		k = server_karma / player_karma

	return k


def calc_ban_karma(
	time: Number,
	server_karma: Number,
	player_karma: Number,
	threshold: Number = MAX_BAN_THRESHOLD,
) -> Number:
	return timed_sigmoid_function(time, threshold) * calc_karma_koef(server_karma, player_karma)


def calc_like_karma(
	server_karma: Number,
	player_karma: Number
) -> Number:
	return sigmoid_function(calc_karma_koef(server_karma, player_karma), LIKE_BASE_DELTA)


def calc_warn_karma(
	server_karma: Number,
	player_karma: Number,
) -> Number:
	return sigmoid_function(calc_karma_koef(server_karma, player_karma), WARN_BASE_DELTA)


def calc_perma_ban_karma(
	server_karma: Number,
	player_karma: Number,
	threshold: Number = MAX_BAN_THRESHOLD,
) -> Number:
	pass
