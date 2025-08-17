import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV
df = pd.read_csv("results.csv")

# Normalize column names
df = df.rename(columns={
    "stateUt_code": "State/UT Code",
    "stateUt": "State/UT",
    "constituencyNo": "Constituency No.",
    "constituencyName": "Constituency Name",
    "candidateName": "Candidate Name",
    "partyNames": "Party",
    "votes": "Votes",
    "status": "Status"
})

st.set_page_config(page_title="Election Results Dashboard", layout="wide")
st.title("🗳️ Election Results Analysis (2024)")
st.markdown("Interactive dashboard to explore and visualize Indian parliamentary election results (2024) with detailed constituency and party insights. [Gitlab↗](https://gitlab.com/cln35h/electionResults).")
st.markdown("---")

# Sidebar navigation
view = st.sidebar.radio("Choose View", ["Dashboard", "Constituency Analysis"])

# ---------------- Constituency Analysis ----------------
if view == "Dashboard":
    
    # Sidebar filters
    state = st.sidebar.selectbox("Filter by State/UT", ["All"] + sorted(df["State/UT"].unique()))
    party = st.sidebar.selectbox("Filter by Party", ["All"] + sorted(df["Party"].unique()))

    filtered = df.copy()
    if state != "All":
        filtered = filtered[filtered["State/UT"] == state]
    if party != "All":
        filtered = filtered[filtered["Party"] == party]

    # Filtered table
    st.subheader("List of candidates with Results")
    st.dataframe(filtered)

    # Candidate Votes Bar Chart
    st.markdown("---")
    st.subheader("Top Candidates by Votes")
    top_candidates = filtered.sort_values("Votes", ascending=False).head(10)
    fig = px.bar(top_candidates, x="Candidate Name", y="Votes", color="Party", text="Votes")
    st.plotly_chart(fig, use_container_width=True)
    
    # Party Performance Pie
    st.markdown("---")
    st.subheader("Party-wise Total Votes")
    party_votes = filtered.groupby("Party")["Votes"].sum().reset_index()
    fig2 = px.pie(party_votes, names="Party", values="Votes", title="Vote Share by Party")
    st.plotly_chart(fig2, use_container_width=True)

    # State-wise Seat Wins
    st.markdown("---")
    st.subheader("State-wise Constituency Wins")
    wins = df[df["Status"] == "Won"].groupby("State/UT")["Candidate Name"].count().reset_index()
    wins.columns = ["State/UT", "Seats Won"]
    fig3 = px.bar(wins, x="State/UT", y="Seats Won", title="Seats Won by State/UT")
    st.plotly_chart(fig3, use_container_width=True)

# ---------------- Overall Dashboard ----------------
elif view == "Constituency Analysis":
    state = st.sidebar.selectbox("Select State/UT", sorted(df["State/UT"].unique()))
    constituency = st.sidebar.selectbox(
        "Select Constituency",
        sorted(df[df["State/UT"] == state]["Constituency Name"].unique())
    )

    # Filter data for constituency
    cons_data = df[(df["State/UT"] == state) & (df["Constituency Name"] == constituency)]
    cons_data = cons_data.sort_values("Votes", ascending=False)

    if cons_data.empty:
        st.warning("No data available for this constituency.")
    else:
        # Winner, runner-up, NOTA
        winner = cons_data.iloc[0]
        runnerup = cons_data.iloc[1] if len(cons_data) > 1 else None
        nota = cons_data[cons_data["Party"].str.contains("NOTA", case=False, na=False)]

        # Compute totals
        total_votes = cons_data["Votes"].sum()
        rest_votes = total_votes - winner["Votes"]
        nota_votes = int(nota["Votes"].sum()) if not nota.empty else 0
        num_candidates = len(cons_data)

        # Display results
        st.subheader(f"[📍] {constituency} ({state})")
    
        st.markdown(f"""
        **Winner:** 🏆 {winner['Candidate Name']} ({winner['Party']}) with **{winner['Votes']} votes**  
        **Runner-up:** 🥈 {runnerup['Candidate Name']} ({runnerup['Party']}) with **{runnerup['Votes']} votes**  
        **Margin:** {winner['Votes'] - runnerup['Votes']} votes  
        **Winner vs Rest (incl. NOTA):** {winner['Votes']} vs {rest_votes} votes  
        **NOTA votes:** {nota_votes}  
        **No. of Candidates:** {num_candidates}
        """)
        st.markdown("---")

        # Plot vote distribution
        fig = px.bar(cons_data, x="Candidate Name", y="Votes", color="Party",
                     text="Votes", title=f"Vote Distribution in {constituency}",
                     hover_data=["Party"])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

        # Raw table
        st.subheader("Detailed Candidate-wise Results")
        st.dataframe(cons_data[["Candidate Name", "Party", "Votes", "Status"]])

# ---------------- Footer ----------------
st.markdown("---")
st.markdown(
    "Built with わエカヨꕷサ by ***Dinesh aka 学習者 aka cln35h*** using [ "
    "[Streamlit](https://streamlit.io/) + [Plotly](https://plotly.com/python/) ]"
)
st.markdown("---")