import streamlit as st
from prizepicks_scraper import get_prizepicks_wnba_props
from odds_api import get_odds_from_rapidapi
from ev_calculator import calculate_best_parlays

st.title("WNBA PrizePicks 2-Pick Optimizer")

selected_stat = st.selectbox("Select stat type:", ["points", "rebounds", "assists"])

with st.spinner("Scraping PrizePicks and sportsbook odds..."):
    pp_props = get_prizepicks_wnba_props(stat_filter=selected_stat)
    fd_odds = get_odds_from_rapidapi()

    if not pp_props:
        st.error("Failed to retrieve PrizePicks props data.")
    elif not fd_odds:
        st.error("Failed to retrieve sportsbook odds data.")
    else:
        results = calculate_best_parlays(pp_props, fd_odds, stat_filter=selected_stat)

        if not results:
            st.warning("No +EV parlays found for the selected stat.")
        else:
            st.subheader("Top +EV 2-Pick Parlays")
            for pick in results:
                st.markdown(f"**{pick['player1']} OVER {pick['line1']} {pick['stat1']}**")
                st.markdown(f"**{pick['player2']} OVER {pick['line2']} {pick['stat2']}**")
                st.markdown(f"**Expected Value (EV): {pick['ev']:.2f}**\n---")
