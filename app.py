import streamlit as st
from prizepicks_scraper import get_prizepicks_wnba_props

st.title("WNBA PrizePicks Player Props Viewer")

selected_stat = st.selectbox("Select stat type:", ["points", "rebounds", "assists"])

with st.spinner("Fetching PrizePicks WNBA player props..."):
    props = get_prizepicks_wnba_props(stat_filter=selected_stat)

if not props:
    st.error("Failed to retrieve PrizePicks props or no data available.")
else:
    st.subheader(f"WNBA Player Props for {selected_stat.capitalize()}")
    for prop in props:
        st.write(f"**{prop['player']}** - Line: {prop['line']} {prop['stat']}")
