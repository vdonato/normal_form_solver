import numpy as np
import pandas as pd


def regret_matching_strategy(cum_regret, cum_strategy):
    strategy = np.array([r if r > 0 else 0 for r in cum_regret])
    normalizing_sum = sum(strategy)

    if normalizing_sum == 0:
        # On the first iteration, we just play a pure strategy that picks the
        # first action for simplicity. There's a chance that this might run into
        # some weird boundary condition for certain games so that the strategy
        # doesn't converge, but I haven't run into this in practice.
        strategy[0] = 1
    else:
        strategy /= normalizing_sum

    return strategy


def calculate_regrets(my_action, opp_action, actions, payoff_matrix, row_player=False):
    regrets = np.zeros(len(actions))
    my_action_idx = actions.index(my_action)
    opp_action_idx = actions.index(opp_action)

    for action_idx, action in enumerate(actions):
        if row_player:
            r = (
                payoff_matrix.iat[action_idx, opp_action_idx]
                - payoff_matrix.iat[my_action_idx, opp_action_idx]
            )
        else:
            r = (
                payoff_matrix.iat[opp_action_idx, action_idx]
                - payoff_matrix.iat[opp_action_idx, my_action_idx]
            )

        regrets[action_idx] = r

    return regrets


def average_strategy(actions, cum_strategies, iterations):
    return {
        p: {
            actions[i]: cum_freq / iterations
            for i, cum_freq in enumerate(cum_strategies[p])
        }
        for p in ["p1", "p2"]
    }


def solve(actions, p1_payoffs, p2_payoffs, iterations=10_000):
    num_actions = len(p1_payoffs)

    cum_regrets = {"p1": np.zeros(num_actions), "p2": np.zeros(num_actions)}
    cum_strategies = {"p1": np.zeros(num_actions), "p2": np.zeros(num_actions)}
    strategy_samples = {"p1": pd.DataFrame(), "p2": pd.DataFrame()}

    for i in range(iterations):
        p1_strategy = regret_matching_strategy(cum_regrets["p1"], cum_strategies["p1"])
        p2_strategy = regret_matching_strategy(cum_regrets["p2"], cum_strategies["p2"])

        if i == 0:
            p1_sample = p1_strategy
            p2_sample = p2_strategy
        else:
            avg_strats = average_strategy(actions, cum_strategies, i)
            p1_sample = avg_strats["p1"]
            p2_sample = avg_strats["p2"]

        strategy_samples["p1"] = pd.concat(
            [
                strategy_samples["p1"],
                pd.DataFrame([p1_sample], columns=actions),
            ],
            ignore_index=True,
        )
        strategy_samples["p2"] = pd.concat(
            [
                strategy_samples["p2"],
                pd.DataFrame([p2_sample], columns=actions),
            ],
            ignore_index=True,
        )

        cum_strategies["p1"] += p1_strategy
        cum_strategies["p2"] += p2_strategy

        p1_action = np.random.choice(actions, p=p1_strategy)
        p2_action = np.random.choice(actions, p=p2_strategy)

        cum_regrets["p1"] += calculate_regrets(
            p1_action, p2_action, actions, p1_payoffs, row_player=True
        )
        cum_regrets["p2"] += calculate_regrets(
            p2_action, p1_action, actions, p2_payoffs, row_player=False
        )

    return average_strategy(actions, cum_strategies, iterations), strategy_samples
