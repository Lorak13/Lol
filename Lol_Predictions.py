import streamlit as st
import random
from collections import defaultdict


def run_simulation(iterations, team_strengths):
    record_counter = defaultdict(lambda: defaultdict(int))

    teams = {
        name: {"strength": team_strengths[name], "wins": 0, "losses": 0} 
        for name in team_strengths
    }

    for _ in range(iterations):

        def simulate_match(team1, team2):
            total_strength = team1['strength'] + team2['strength']
            rand_num = random.random()
            return 'team1' if rand_num < (team1['strength'] / total_strength) else 'team2'

        teams = {
            "T1": {"strength": 8, "wins": 0, "losses": 0},
            "TL": {"strength": 1.5, "wins": 0, "losses": 0},
            "C9": {"strength": 1.5, "wins": 0, "losses": 0},
            "MAD": {"strength": 4, "wins": 0, "losses": 0},
            "GEN": {"strength": 9, "wins": 0, "losses": 0},
            "GAM": {"strength": 1.5, "wins": 0, "losses": 0},
            "JDG": {"strength": 10, "wins": 0, "losses": 0},
            "BDS": {"strength": 2, "wins": 0, "losses": 0},
            "G2": {"strength": 7, "wins": 0, "losses": 0},
            "DK": {"strength": 7, "wins": 0, "losses": 0},
            "NRG": {"strength": 1.5, "wins": 0, "losses": 0},
            "WBG": {"strength": 7, "wins": 0, "losses": 0},
            "FNC": {"strength": 5.5, "wins": 0, "losses": 0},
            "LNG": {"strength": 9, "wins": 0, "losses": 0},
            "BLG": {"strength": 8, "wins": 0, "losses": 0},
            "KT": {"strength": 7.5, "wins": 0, "losses": 0},
        }

            # Round 1 matchups
        round1_matchups = [("T1", "TL"), ("C9", "MAD"), ("GEN", "GAM"), ("JDG", "BDS"),
                              ("G2", "DK"), ("NRG", "WBG"), ("FNC", "LNG"), ("BLG", "KT")]

            # Round 1 simulation
        for team1_name, team2_name in round1_matchups:
                team1 = teams[team1_name]
                team2 = teams[team2_name]
                winner = simulate_match(team1, team2)
                if winner == 'team1':
                    team1['wins'] += 1
                    team2['losses'] += 1
                else:
                    team2['wins'] += 1
                    team1['losses'] += 1

            # Record lookup
        record_lookup = {
                2: [(1, 0), (0, 1)],
                3: [(2, 0), (1, 1), (0, 2)],
                4: [(2, 1), (1, 2)],
                5: [(2, 2)]
            }

            # Round 2-5 simulation
        for round_num, records in record_lookup.items():
                for wins, losses in records:
                    available_teams = [name for name, team in teams.items() if team['wins'] == wins and team['losses'] == losses]
                    random.shuffle(available_teams)
                    while len(available_teams) >= 2:
                        team1_name = available_teams.pop()
                        team2_name = available_teams.pop()
                        team1 = teams[team1_name]
                        team2 = teams[team2_name]
                        if team1['wins'] < 3 and team1['losses'] < 3 and team2['wins'] < 3 and team2['losses'] < 3:
                            winner = simulate_match(team1, team2)
                            if winner == 'team1':
                                team1['wins'] += 1
                                team2['losses'] += 1
                            else:
                                team2['wins'] += 1
                                team1['losses'] += 1

        for team_name, team in teams.items():
            record = f"{team['wins']}-{team['losses']}"
            record_counter[team_name][record] += 1

    return record_counter

def show_results(record_counter, team_strengths):
    ordered_records = ['3-0', '3-1', '3-2', '2-3', '1-3', '0-3']
    st.write("This table shows the probability for every team to finish with a certain record at the end of the swiss stage:")

    # Create a table layout
    header = "| Team | 3-0 | 3-1 | 3-2 | 2-3 | 1-3 | 0-3 | Qualification Probability |"
    separator = "|------|-----|-----|-----|-----|-----|-----|-------------------------|"
    st.write(header)
    st.write(separator)

    for team_name in team_strengths:  # This ensures that even teams with no results are shown
        records = record_counter.get(team_name, {})
        total = sum(records.values())
        row = f"| {team_name} | "
        qualification_prob = 0
        for record in ordered_records:
            count = records.get(record, 0)
            percentage = (count / total if total else 0) * 100
            if record in ['3-0', '3-1', '3-2']:
                qualification_prob += percentage
            row += f"{percentage:.2f}% | "
        row += f"{qualification_prob:.2f}% |"
        st.write(row)

st.title("Lol World Swiss Tool")
st.write("This is a simple Streamlit app that simulates League of Legends World Swiss Matches.")
st.write("Estimated team strength from 1-100 will dictate the win % in any matchup by formula: Team_Strength / (Team_strength + Opponent_Strength)")

# Create sliders for each team's strength
team_names = ["T1", "TL", "C9", "MAD", "GEN", "GAM", "JDG", "BDS", "G2", "DK", "NRG", "WBG", "FNC", "LNG", "BLG", "KT"]
team_strengths = {}

for name in team_names:
    team_strengths[name] = st.slider(f"Strength of {name}", 1, 100, 50)

# Slider for the number of iterations
iterations = st.slider("Number of Simulations", 100, 1000000, 50000)

# Run Simulation Button
if st.button("Run Simulation"):
    record_counter = run_simulation(iterations, team_strengths)
    show_results(record_counter)
