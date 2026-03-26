import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

teams = ['CSK', 'MI', 'RCB', 'KKR', 'DC', 'SRH', 'PBKS', 'RR', 'GT', 'LSG']

venues_home = {
    'CSK': 'MA Chidambaram Stadium',
    'MI': 'Wankhede Stadium',
    'RCB': 'M. Chinnaswamy Stadium',
    'KKR': 'Eden Gardens',
    'DC': 'Arun Jaitley Stadium',
    'SRH': 'Rajiv Gandhi International Stadium',
    'PBKS': 'Punjab Cricket Association Stadium',
    'RR': 'Sawai Mansingh Stadium',
    'GT': 'Narendra Modi Stadium',
    'LSG': 'BRSABV Ekana Cricket Stadium',
}

players = {
    'CSK': ['MS Dhoni', 'Ruturaj Gaikwad', 'Devon Conway', 'Deepak Chahar', 'Ravindra Jadeja'],
    'MI': ['Rohit Sharma', 'Ishan Kishan', 'Suryakumar Yadav', 'Jasprit Bumrah', 'Hardik Pandya'],
    'RCB': ['Virat Kohli', 'Faf du Plessis', 'Glenn Maxwell', 'Mohammed Siraj', 'Dinesh Karthik'],
    'KKR': ['Shreyas Iyer', 'Venkatesh Iyer', 'Sunil Narine', 'Andre Russell', 'Pat Cummins'],
    'DC': ['David Warner', 'Prithvi Shaw', 'Axar Patel', 'Anrich Nortje', 'Rishabh Pant'],
    'SRH': ['Shikhar Dhawan', 'Abhishek Sharma', 'Umran Malik', 'Marco Jansen', 'Heinrich Klaasen'],
    'PBKS': ['Shikhar Dhawan', 'Jonny Bairstow', 'Liam Livingstone', 'Arshdeep Singh', 'Sam Curran'],
    'RR': ['Sanju Samson', 'Jos Buttler', 'Yashasvi Jaiswal', 'Trent Boult', 'Ravichandran Ashwin'],
    'GT': ['Hardik Pandya', 'Shubman Gill', 'David Miller', 'Mohammed Shami', 'Rashid Khan'],
    'LSG': ['KL Rahul', 'Quinton de Kock', 'Marcus Stoinis', 'Avesh Khan', 'Ravi Bishnoi'],
}

matches = []
player_stats = []

match_id = 1
seasons = [2019, 2020, 2021, 2022, 2023, 2024]

for season in seasons:
    team_pairs = [(t1, t2) for i, t1 in enumerate(teams) for t2 in teams[i+1:]]
    random.shuffle(team_pairs)
    season_matches = team_pairs[:40]  # ~40 matches per season

    for team1, team2 in season_matches:
        venue = random.choice([venues_home[team1], venues_home[team2]])
        is_neutral = random.random() < 0.1

        toss_winner = random.choice([team1, team2])
        toss_decision = random.choice(['bat', 'field'])

        # Batting first team
        if toss_decision == 'bat':
            batting_first = toss_winner
            fielding_first = team2 if toss_winner == team1 else team1
        else:
            fielding_first = toss_winner
            batting_first = team2 if toss_winner == team1 else team1
        chasing_team = fielding_first

        # Winner logic - toss winner wins 55% of time, chasing wins 52%
        if random.random() < 0.52:
            winner = chasing_team
            win_type = 'wickets'
            margin = random.randint(1, 9)
        else:
            winner = batting_first
            win_type = 'runs'
            margin = random.randint(1, 50)

        home_team = team1
        is_home_win = (winner == home_team)

        matches.append({
            'match_id': match_id,
            'season': season,
            'date': f"{season}-{random.randint(3,5):02d}-{random.randint(1,30):02d}",
            'team1': team1,
            'team2': team2,
            'venue': venue,
            'toss_winner': toss_winner,
            'toss_decision': toss_decision,
            'batting_first': batting_first,
            'chasing_team': chasing_team,
            'winner': winner,
            'win_type': win_type,
            'margin': margin,
            'is_neutral_venue': is_neutral,
            'home_team': home_team,
        })
        match_id += 1

matches_df = pd.DataFrame(matches)

# Player performance stats
for _, match in matches_df.iterrows():
    for team in [match['team1'], match['team2']]:
        team_players = players[team]
        for player in team_players:
            runs = max(0, int(np.random.exponential(28)))
            balls_faced = max(runs, int(runs / (0.8 + random.random() * 0.8))) if runs > 0 else random.randint(0, 5)
            strike_rate = round((runs / balls_faced * 100) if balls_faced > 0 else 0, 2)
            wickets = np.random.choice([0, 0, 0, 1, 1, 2, 3, 4], p=[0.45, 0.2, 0.1, 0.1, 0.06, 0.05, 0.03, 0.01])
            fours = int(runs * 0.3 / 4)
            sixes = int(runs * 0.15 / 6)
            player_stats.append({
                'match_id': match['match_id'],
                'season': match['season'],
                'team': team,
                'player': player,
                'runs': runs,
                'balls_faced': balls_faced,
                'strike_rate': strike_rate,
                'wickets': wickets,
                'fours': fours,
                'sixes': sixes,
            })

players_df = pd.DataFrame(player_stats)
matches_df.to_csv('/home/claude/ipl_dashboard/matches.csv', index=False)
players_df.to_csv('/home/claude/ipl_dashboard/player_stats.csv', index=False)
print(f"Generated {len(matches_df)} matches and {len(players_df)} player records")
