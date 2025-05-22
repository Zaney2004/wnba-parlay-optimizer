import streamlit as st
from prizepicks_scraper import get_prizepicks_wnba_props
from odds_api import get_odds_from_rapidapi
from ev_calculator import calculate_best_parlays

st.title("WNBA PrizePicks 2-Pick Optimizer")

selected_stat = st.selectbox("Select stat type:", ["points", "rebounds", "assists"])

with st.spinner("Scraping data from PrizePicks and sportsbooks via RapidAPI..."):
    pp_props = get_prizepicks_wnba_props(stat_filter=selected_stat)
    fd_odds = get_odds_from_rapidapi()

    if not pp_props or not fd_odds:
        st.error("Failed to retrieve props or odds. Try again later.")
    else:
        results = calculate_best_parlays(pp_props, fd_odds, stat_filter=selected_stat)

        st.subheader("Top +EV 2-Pick Parlays")
        for pick in results:
            st.markdown(f"**{pick['player1']} OVER {pick['line1']} {pick['stat1']}**")
            st.markdown(f"**{pick['player2']} OVER {pick['line2']} {pick['stat2']}**")
            st.markdown(f"**EV: {pick['ev']:.2f}**\n---")