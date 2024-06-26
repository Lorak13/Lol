import streamlit as st
import random
from collections import defaultdict

def run_simulation(iterations, team_strengths, debug_mode):
    record_counter = defaultdict(lambda: defaultdict(int))
    debug_info = []  # Initialize a list to store debug info

    teams = {
        name: {"strength": team_strengths[name], "wins": 0, "losses": 0} 
        for name in team_strengths
    }

    initial_records = {
    'G2': {'wins': 1, 'losses': 1},
    'GEN': {'wins': 2, 'losses': 0},
    'JDG': {'wins': 2, 'losses': 0},
    'LNG': {'wins': 1, 'losses': 1},
    'NRG': {'wins': 0, 'losses': 0},
    'MAD': {'wins': 0, 'losses': 0},
    'T1': {'wins': 0, 'losses': 0},
    'C9': {'wins': 0, 'losses': 0},
    'KT': {'wins': 0, 'losses': 0},
    'WBG': {'wins': 0, 'losses': 0},
    'BLG': {'wins': 0, 'losses': 0},
    'FNC': {'wins': 0, 'losses': 0},
    'DK': {'wins': 0, 'losses': 1},
    'BDS': {'wins': 0, 'losses': 1},
    'TL': {'wins': 0, 'losses': 1},
    'GAM': {'wins': 0, 'losses': 1},
    }
    
    for i in range(iterations):

        teams = {
            name: {
                "strength": team_strengths[name],
                "wins": initial_records[name]['wins'],
                "losses": initial_records[name]['losses']
            }
            for name in team_strengths
        }

        if debug_mode:
            debug_info.append(f"Running iteration {i}")

        teams['JDG']['wins'] = 2
        teams['JDG']['losses'] = 0
        teams['GEN']['wins'] = 2
        teams['GEN']['losses'] = 0
        teams['LNG']['wins'] = 0
        teams['LNG']['losses'] = 2
        teams['G2']['wins'] = 0
        teams['G2']['losses'] = 2
            
        def simulate_match(team1, team2):
            total_strength = team1['strength'] + team2['strength']
            rand_num = random.random()
            return 'team1' if rand_num < (team1['strength'] / total_strength) else 'team2'

            # Round 1 matchups
        round1_matchups = [("G2", "GEN"), ("JDG", "LNG"), ("NRG", "MAD"), ("T1", "C9"),
                    ("KT", "WBG"), ("BLG", "FNC"), ("DK", "BDS"), ("TL", "GAM")]

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
        3: [(1, 1), (2, 0), (0, 2)]  # Changed to 2-0 and 0-2 instead of 2, 3, 4, 5
        }

            # Round 2-3 simulation
        for round_num, records in record_lookup.items():
                for wins, losses in records:
                    available_teams = [name for name, team in teams.items() if team['wins'] == wins and team['losses'] == losses]
                    random.shuffle(available_teams)
                    while len(available_teams) >= 2:
                        team1_name = available_teams.pop()
                        team2_name = available_teams.pop()
                        team1 = teams[team1_name]
                        team2 = teams[team2_name]
                        if team1['wins'] < 2 and team1['losses'] < 2 and team2['wins'] < 2 and team2['losses'] < 2:
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
            if debug_mode:
                st.write(f"Debug: Updating record for {team_name}: {record}")  # Debugging line
        
        if debug_mode:
                debug_info.append(f"Updating record for {team_name}: {record}")
                st.write(f"Debug: Final record counter {record_counter}")  # Debugging line
    
    return record_counter, debug_info

def show_results(record_counter):
    ordered_records = ['2-0', '2-1', '1-2', '0-2']
    st.write("Results:")

    # Create a table layout
    header = "| Team | 2-0 | 2-1 | 1-2 | 0-2 |"
    separator = "|------|-----|-----|-----|-----|"
    st.write(header)
    st.write(separator)

    for team_name in team_strengths:  # This ensures that even teams with no results are shown
        records = record_counter.get(team_name, {})
        total = sum(records.values())
        row = f"| {team_name} | "
        for record in ordered_records:
            count = records.get(record, 0)
            percentage = (count / total if total else 0) * 100
            row += f"{percentage:.2f}% | "
        st.write(row)

st.title("Lol World Swiss Tool")
st.write("This is a simple Streamlit app that simulates League of Legends World Swiss Matches.")

# Create sliders for each team's strength
team_names = ["T1", "TL", "C9", "MAD", "GEN", "GAM", "JDG", "BDS", "G2", "DK", "NRG", "WBG", "FNC", "LNG", "BLG", "KT"]
team_strengths = {}

for name in team_names:
    team_strengths[name] = st.slider(f"Strength of {name}", 1, 100, 50)

# Slider for the number of iterations
iterations = st.slider("Number of Simulations", 100, 100000, 50000)

debug_mode = st.checkbox("Enable Debugging")
record_counter = None
debug_info = []

# Run Simulation Button
if st.button("Run Simulation"):
    st.write("Button was clicked. Running simulation now...")  # Debugging line
    record_counter, debug_info = run_simulation(iterations, team_strengths, debug_mode)
    show_results(record_counter)
  #  if debug_mode:
   #     for info in debug_info:
    #        st.write(info)
