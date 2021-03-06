import pandas as pd

rps_actions = ["Rock", "Paper", "Scissors"]
ROCK_PAPER_SCISSORS = {
    "actions": rps_actions,
    "p1_payoffs": pd.DataFrame(
        [
            [0, -1, 1],
            [1, 0, -1],
            [-1, 1, 0],
        ],
        index=rps_actions,
        columns=rps_actions,
    ),
    "p2_payoffs": pd.DataFrame(
        [
            [0, 1, -1],
            [-1, 0, 1],
            [1, -1, 0],
        ],
        index=rps_actions,
        columns=rps_actions,
    ),
}

prisoners_actions = ["Cooperate", "Defect"]
PRISONERS_DILEMMA = {
    "actions": prisoners_actions,
    "p1_payoffs": pd.DataFrame(
        [
            [-1, -3],
            [0, -2],
        ],
        index=prisoners_actions,
        columns=prisoners_actions,
    ),
    "p2_payoffs": pd.DataFrame(
        [
            [-1, 0],
            [-3, -2],
        ],
        index=prisoners_actions,
        columns=prisoners_actions,
    ),
}

stag_hunt_actions = ["Stag", "Hare"]
STAG_HUNT = {
    "actions": stag_hunt_actions,
    "p1_payoffs": pd.DataFrame(
        [
            [4, 1],
            [3, 2],
        ],
        index=stag_hunt_actions,
        columns=stag_hunt_actions,
    ),
    "p2_payoffs": pd.DataFrame(
        [
            [4, 3],
            [1, 2],
        ],
        index=stag_hunt_actions,
        columns=stag_hunt_actions,
    ),
}
