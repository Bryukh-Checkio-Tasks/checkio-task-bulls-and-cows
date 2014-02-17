from math import hypot
from checkio.signals import ON_CONNECT
from checkio import api
from checkio.referees.multicall import CheckiORefereeMulti

from tests import TESTS
from random import shuffle

MAX_STEP = 8

def rand_seq():
    digits = list(range(10))
    shuffle(digits)
    return "".join(str(x) for x in digits[:4])


def initial_referee(data):
    return {"goal": data or rand_seq(),
            "input": [],
            "step": 0}


def process_referee(referee_data, user_result):
    goal = referee_data['goal']
    referee_data['step'] += 1
    if referee_data['step'] > MAX_STEP:
        referee_data.update({"result": False, "result_addon": "Too many moves."})
        return referee_data
    if not isinstance(user_result, str) or len(user_result) != 4 or not user_result.isdigit():
        referee_data.update({"result": False, "result_addon": "The function should return a string with 4 digits."})
        return referee_data
    bulls = cows = 0
    for i, d in enumerate(user_result):
        if goal[i] == d:
            bulls += 1
        elif d in goal:
            cows += 1
    last_result = "{0} {1}B{2}C".format(user_result, bulls, cows)
    referee_data["input"].append("{0} {1}B{2}C".format(user_result, bulls, cows))
    referee_data["last_guess"] = user_result
    referee_data["last_result"] = last_result

    referee_data.update({"result": True, "result_addon": "Next Step"})
    return referee_data



def is_win_referee(referee_data):
    if not referee_data["result"]:
        return False
    referee_data["is_win"] = referee_data["last_guess"] == referee_data["goal"]
    return referee_data["is_win"]

api.add_listener(
    ON_CONNECT,
    CheckiORefereeMulti(
        tests=TESTS,
        initial_referee=initial_referee,
        process_referee=process_referee,
        is_win_referee=is_win_referee,
        ).on_ready)
