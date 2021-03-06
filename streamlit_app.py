import numpy as np
import pandas as pd
import streamlit as st

import presets
from solver import solve


st.write("#### An RM-based Nash Equilibrium solver for 2-player normal-form games")

st.write(
    "Regret matching algorithm based on the RPS example in:"
    " http://modelai.gettysburg.edu/2013/cfr/cfr.pdf"
)

game = st.selectbox(
    "Select a game",
    [
        "Custom Game",
        "Rock Paper Scissors",
        "Prisoners Dilemma",
        "Stag Hunt",
    ],
)

if game == "Custom Game":
    actions = st.text_input("Enter comma separated actions:")
    actions = [m.strip() for m in actions.split(",") if m != ""]
    p1_payoffs = pd.DataFrame(0, index=actions, columns=actions)
    p2_payoffs = pd.DataFrame(0, index=actions, columns=actions)

elif game == "Rock Paper Scissors":
    actions = presets.ROCK_PAPER_SCISSORS["actions"]
    p1_payoffs = presets.ROCK_PAPER_SCISSORS["p1_payoffs"]
    p2_payoffs = presets.ROCK_PAPER_SCISSORS["p2_payoffs"]

elif game == "Prisoners Dilemma":
    actions = presets.PRISONERS_DILEMMA["actions"]
    p1_payoffs = presets.PRISONERS_DILEMMA["p1_payoffs"]
    p2_payoffs = presets.PRISONERS_DILEMMA["p2_payoffs"]

elif game == "Stag Hunt":
    actions = presets.STAG_HUNT["actions"]
    p1_payoffs = presets.STAG_HUNT["p1_payoffs"]
    p2_payoffs = presets.STAG_HUNT["p2_payoffs"]

else:
    raise ValueError("Invalid game")


# List of bugs:
# * st.data_editor does not support string indexes
# * st.data_editor does not work with st.columns
# * rerunning the page resets the data editor in the frontend (but not the
#   value of the widget stored on the backend)
if len(actions) > 0:
    with st.expander("Player 1's (Row-player) Payoff Matrix"):
        p1_payoffs = st.data_editor(p1_payoffs, key="p1_payoffs")
        st.write(p1_payoffs)

    with st.expander("Player 2's (Colummn-player) Payoff Matrix"):
        p2_payoffs = st.data_editor(p2_payoffs, key="p2_payoffs")
        st.write(p2_payoffs)

    if st.button("Solve!"):
        solution, strategy_samples = solve(actions, p1_payoffs, p2_payoffs)
        st.write("#### (Approximate) Nash Equilibrium Solution")
        st.write(solution)

        st.write("#### P1 Strategy vs Iterations")
        st.line_chart(strategy_samples["p1"])

        st.write("#### P2 Strategy vs Iterations")
        st.line_chart(strategy_samples["p2"])
