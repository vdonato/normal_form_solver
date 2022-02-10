import numpy as np
import pandas as pd
import streamlit as st

from solver import solve


# TODO: Add some presets: RPS, Prisoners Dilemma, an asymmetric game?


st.write("#### An RM-based Nash Equilibrium solver for 2-player normal-form games")

st.write(
    "Regret matching algorithm based on the RPS example in:"
    " http://modelai.gettysburg.edu/2013/cfr/cfr.pdf"
)

actions = st.text_input("Enter comma separated actions:")
actions = [m.strip() for m in actions.split(",") if m != ""]
zeros = pd.DataFrame(0, index=actions, columns=actions)

# List of bugs:
# * st.data_editor does not support string indexes
# * st.data_editor does not work with st.columns
# * rerunning the page resets the data editor in the frontend (but not the
#   value of the widget stored on the backend)
if len(actions) > 0:
    with st.expander("Player 1's (Row-player) Payoff Matrix"):
        p1_payoffs = st.data_editor(zeros, key="p1_payoffs")
        st.write(p1_payoffs)

    with st.expander("Player 2's (Colummn-player) Payoff Matrix"):
        p2_payoffs = st.data_editor(zeros, key="p2_payoffs")
        st.write(p2_payoffs)

    # TODO: Add some nice plots to show the strategies converging to equilibrium.
    if st.button("Solve!"):
        st.write(solve(actions, p1_payoffs, p2_payoffs))
