import numpy as np

from app.karma.consts import MAX_BAN_THRESHOLD


def sigmoid_function(time: int, threshold: int):
	return 1 / (1 + np.exp(-(time - threshold)))


def calc_ban_karma(time: int, server_karma: int, player_karma: int, threshold: int = MAX_BAN_THRESHOLD) -> float:
	if server_karma > player_karma:
		k = player_karma / server_karma
	else:
		k = server_karma / player_karma

	return sigmoid_function(time, threshold) * k


def calc_like_karma():
	pass
