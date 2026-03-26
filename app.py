import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Match Insights Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background: #0d1117; }

    .metric-card {
        background: linear-gradient(135deg, #1e2a3a 0%, #162032 100%);
        border: 1px solid #2d4a6b;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .metric-card .label {
        font-size: 13px;
        color: #8ca3c0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-card .value {
        font-size: 36px;
        font-weight: 700;
        color: #f0c040;
    }
    .metric-card .sub {
        font-size: 12px;
        color: #5a7a9a;
        margin-top: 4px;
    }

    .insight-card {
        background: linear-gradient(135deg, #1a2640 0%, #111d2e 100%);
        border-left: 4px solid #f0c040;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 8px 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
    }
    .insight-card .insight-title {
        font-size: 15px;
        font-weight: 700;
        color: #f0c040;
        margin-bottom: 6px;
    }
    .insight-card .insight-text {
        font-size: 13px;
        color: #a0b8d0;
        line-height: 1.5;
    }

    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #e8f0ff;
        border-bottom: 2px solid #f0c040;
        padding-bottom: 8px;
        margin: 24px 0 16px 0;
    }

    .team-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin: 2px;
    }

    div[data-testid="stSidebar"] {
        background: #0d1117;
        border-right: 1px solid #1e2a3a;
    }

    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #8ca3c0 !important;
        font-size: 13px !important;
    }

    .prediction-box {
        background: linear-gradient(135deg, #1a3a20 0%, #0f2015 100%);
        border: 1px solid #2a6a30;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    .prediction-winner {
        font-size: 28px;
        font-weight: 700;
        color: #4ade80;
        margin: 12px 0;
    }
    .prediction-confidence {
        font-size: 14px;
        color: #86efac;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #0d1117;
        border-bottom: 1px solid #1e2a3a;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8ca3c0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #f0c040;
        border-bottom: 2px solid #f0c040;
    }
</style>
""", unsafe_allow_html=True)

# ── Team colours ──────────────────────────────────────────────────────────────
TEAM_COLORS = {
    'CSK': '#f7d000', 'MI': '#004ba0', 'RCB': '#cc0000',
    'KKR': '#3a225d', 'DC': '#0050d8', 'SRH': '#f7550f',
    'PBKS': '#d71920', 'RR': '#ff69b4', 'GT': '#1c2951', 'LSG': '#a2e6fa',
}

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    matches = pd.read_csv('matches.csv', parse_dates=['date'])
    players = pd.read_csv('player_stats.csv')
    return matches, players

matches_df, players_df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/8/84/Indian_Premier_League_Official_Logo.svg",
             width=120, use_column_width=False)
    st.markdown("## 🏏 IPL Insights")
    st.markdown("---")

    seasons = sorted(matches_df['season'].unique())
    selected_seasons = st.multiselect(
        "📅 Season(s)",
        options=seasons,
        default=seasons,
    )

    all_teams = sorted(matches_df['team1'].unique())
    selected_teams = st.multiselect(
        "🏟️ Teams",
        options=all_teams,
        default=all_teams,
    )

    st.markdown("---")
    st.markdown("### 🔮 Match Predictor")
    pred_team1 = st.selectbox("Team 1", all_teams, index=0)
    pred_team2 = st.selectbox("Team 2", all_teams, index=1)
    pred_toss = st.selectbox("Toss Won By", [pred_team1, pred_team2])
    pred_decision = st.selectbox("Toss Decision", ["field", "bat"])
    pred_venue_type = st.radio("Venue Type", ["Home for Team 1", "Home for Team 2", "Neutral"])
    predict_btn = st.button("🎯 Predict Winner", use_container_width=True)

    st.markdown("---")
    st.caption("📊 Data: IPL 2019–2024 | 240 matches")

# ── Filter data ───────────────────────────────────────────────────────────────
filtered = matches_df[
    matches_df['season'].isin(selected_seasons) &
    (matches_df['team1'].isin(selected_teams) | matches_df['team2'].isin(selected_teams))
].copy()

filtered_players = players_df[
    players_df['season'].isin(selected_seasons) &
    players_df['team'].isin(selected_teams)
].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='font-size:32px; font-weight:800; color:#f0c040; margin-bottom:4px;'>
🏏 IPL Match Insights Dashboard
</h1>
<p style='color:#5a7a9a; font-size:14px; margin-top:0;'>
Season 2019–2024 · Real-time insights · Predictive analytics
</p>
""", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
total_matches = len(filtered)
total_teams = filtered['team1'].nunique()
avg_margin_runs = int(filtered[filtered['win_type'] == 'runs']['margin'].mean())
avg_margin_wkts = round(filtered[filtered['win_type'] == 'wickets']['margin'].mean(), 1)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class='metric-card'>
        <div class='label'>Total Matches</div>
        <div class='value'>{total_matches}</div>
        <div class='sub'>across {len(selected_seasons)} seasons</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class='metric-card'>
        <div class='label'>Teams Active</div>
        <div class='value'>{len(selected_teams)}</div>
        <div class='sub'>franchises competing</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class='metric-card'>
        <div class='label'>Avg Win Margin</div>
        <div class='value'>{avg_margin_runs}</div>
        <div class='sub'>runs (when batting 1st wins)</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class='metric-card'>
        <div class='label'>Avg Chase Win</div>
        <div class='value'>{avg_margin_wkts}</div>
        <div class='sub'>wickets in hand</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Team Stats", "⚡ Cool Insights", "🌟 Player Stats", "🔮 Predictor"]
)

# ════════════════════════════════════════════════════════════════
# TAB 1 — TEAM STATS
# ════════════════════════════════════════════════════════════════
with tab1:
    # Compute per-team stats
    def team_stats(df):
        rows = []
        for team in all_teams:
            if team not in selected_teams:
                continue
            played = len(df[(df['team1'] == team) | (df['team2'] == team)])
            won = len(df[df['winner'] == team])
            win_pct = round(won / played * 100, 1) if played else 0
            rows.append({'Team': team, 'Played': played, 'Won': won,
                         'Lost': played - won, 'Win%': win_pct})
        return pd.DataFrame(rows).sort_values('Won', ascending=False)

    ts = team_stats(filtered)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-header'>🏆 Wins Per Team</div>", unsafe_allow_html=True)
        colors = [TEAM_COLORS.get(t, '#888') for t in ts['Team']]
        fig_wins = go.Figure(go.Bar(
            x=ts['Team'], y=ts['Won'],
            marker_color=colors,
            text=ts['Won'], textposition='outside',
            hovertemplate='<b>%{x}</b><br>Wins: %{y}<extra></extra>',
        ))
        fig_wins.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#c0d0e0',
            xaxis=dict(showgrid=False, title=''),
            yaxis=dict(showgrid=True, gridcolor='#1e2a3a', title='Wins'),
            margin=dict(t=20, b=20),
            height=340,
        )
        st.plotly_chart(fig_wins, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-header'>📈 Win Rate (%)</div>", unsafe_allow_html=True)
        ts_sorted = ts.sort_values('Win%', ascending=True)
        fig_pct = go.Figure(go.Bar(
            x=ts_sorted['Win%'], y=ts_sorted['Team'],
            orientation='h',
            marker_color=[TEAM_COLORS.get(t, '#888') for t in ts_sorted['Team']],
            text=[f"{v}%" for v in ts_sorted['Win%']], textposition='outside',
            hovertemplate='<b>%{y}</b><br>Win Rate: %{x}%<extra></extra>',
        ))
        fig_pct.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#c0d0e0',
            xaxis=dict(showgrid=True, gridcolor='#1e2a3a', title='Win %', range=[0, 80]),
            yaxis=dict(showgrid=False),
            margin=dict(t=20, b=20),
            height=340,
        )
        st.plotly_chart(fig_pct, use_container_width=True)

    # Matches played vs won (bubble)
    st.markdown("<div class='section-header'>⚖️ Played vs Won (All Teams)</div>", unsafe_allow_html=True)
    fig_bubble = go.Figure()
    for _, row in ts.iterrows():
        fig_bubble.add_trace(go.Scatter(
            x=[row['Played']], y=[row['Won']],
            mode='markers+text',
            marker=dict(
                size=row['Win%'] * 0.9,
                color=TEAM_COLORS.get(row['Team'], '#888'),
                opacity=0.85,
                line=dict(width=2, color='white'),
            ),
            text=[row['Team']],
            textposition='top center',
            hovertemplate=f"<b>{row['Team']}</b><br>Played: {row['Played']}<br>Won: {row['Won']}<br>Win%: {row['Win%']}%<extra></extra>",
        ))
    fig_bubble.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#c0d0e0',
        xaxis=dict(showgrid=True, gridcolor='#1e2a3a', title='Matches Played'),
        yaxis=dict(showgrid=True, gridcolor='#1e2a3a', title='Matches Won'),
        height=360,
        margin=dict(t=20),
    )
    # Add diagonal reference line
    max_val = ts['Played'].max()
    fig_bubble.add_shape(type='line', x0=0, y0=0, x1=max_val, y1=max_val/2,
                          line=dict(dash='dot', color='#2d4a6b', width=1))
    st.plotly_chart(fig_bubble, use_container_width=True)

    # Season-wise wins heatmap
    st.markdown("<div class='section-header'>📅 Season-Wise Wins Heatmap</div>", unsafe_allow_html=True)
    heat_data = []
    for team in selected_teams:
        row = {'Team': team}
        for season in seasons:
            s_df = filtered[filtered['season'] == season]
            row[str(season)] = len(s_df[s_df['winner'] == team])
        heat_data.append(row)
    heat_df = pd.DataFrame(heat_data).set_index('Team')
    fig_heat = px.imshow(
        heat_df,
        color_continuous_scale='YlOrRd',
        text_auto=True,
        aspect='auto',
    )
    fig_heat.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#c0d0e0',
        coloraxis_showscale=False,
        height=340,
        margin=dict(t=10),
    )
    st.plotly_chart(fig_heat, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# TAB 2 — COOL INSIGHTS
# ════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-header'>⚡ Data-Driven Insights</div>", unsafe_allow_html=True)

    # ── Insight 1: Chasing advantage ─────────────────────────────
    chase_wins = len(filtered[filtered['winner'] == filtered['chasing_team']])
    bat_first_wins = total_matches - chase_wins
    chase_pct = round(chase_wins / total_matches * 100, 1)
    bat_pct = round(bat_first_wins / total_matches * 100, 1)

    ins1, ins2 = st.columns([1, 1.5])
    with ins1:
        st.markdown(f"""
        <div class='insight-card'>
            <div class='insight-title'>🏃 Chasing vs Batting First</div>
            <div class='insight-text'>
                Teams chasing win <b style='color:#f0c040;'>{chase_pct}%</b> of matches —
                a clear advantage in the T20 format where target clarity drives aggressive batting.
                Batting first wins only <b style='color:#f0c040;'>{bat_pct}%</b> of the time.
            </div>
        </div>""", unsafe_allow_html=True)

    with ins2:
        fig_donut = go.Figure(go.Pie(
            labels=['Chasing Wins', 'Batting First Wins'],
            values=[chase_wins, bat_first_wins],
            hole=0.6,
            marker_colors=['#4ade80', '#f97316'],
            textinfo='label+percent',
            textfont_size=13,
        ))
        fig_donut.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#c0d0e0',
            showlegend=False,
            height=240,
            margin=dict(t=10, b=10),
            annotations=[dict(text=f'<b>{chase_pct}%</b><br>Chase', x=0.5, y=0.5,
                              font_size=16, showarrow=False, font_color='#4ade80')]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

    # ── Insight 2: Home advantage per team ───────────────────────
    home_rows = []
    for team in selected_teams:
        home_matches = filtered[filtered['home_team'] == team]
        if len(home_matches) < 3:
            continue
        home_wins = len(home_matches[home_matches['winner'] == team])
        away_matches = filtered[
            ((filtered['team1'] == team) | (filtered['team2'] == team)) &
            (filtered['home_team'] != team)
        ]
        away_wins = len(away_matches[away_matches['winner'] == team])
        home_pct = round(home_wins / len(home_matches) * 100, 1) if len(home_matches) else 0
        away_pct = round(away_wins / len(away_matches) * 100, 1) if len(away_matches) else 0
        home_rows.append({
            'Team': team, 'Home Win%': home_pct, 'Away Win%': away_pct,
            'Home Advantage': home_pct - away_pct
        })

    home_df = pd.DataFrame(home_rows).sort_values('Home Advantage', ascending=False)
    best_home = home_df.iloc[0]['Team'] if len(home_df) else 'N/A'
    best_home_adv = home_df.iloc[0]['Home Advantage'] if len(home_df) else 0

    ins3, ins4 = st.columns([1.5, 1])
    with ins3:
        fig_home = go.Figure()
        fig_home.add_trace(go.Bar(
            name='Home Win%',
            x=home_df['Team'],
            y=home_df['Home Win%'],
            marker_color='#4ade80',
        ))
        fig_home.add_trace(go.Bar(
            name='Away Win%',
            x=home_df['Team'],
            y=home_df['Away Win%'],
            marker_color='#f97316',
        ))
        fig_home.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#c0d0e0',
            legend=dict(orientation='h', yanchor='bottom', y=1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#1e2a3a', title='Win %'),
            height=300,
            margin=dict(t=40, b=10),
        )
        st.plotly_chart(fig_home, use_container_width=True)

    with ins4:
        st.markdown(f"""
        <div class='insight-card'>
            <div class='insight-title'>🏟️ Home Ground Advantage</div>
            <div class='insight-text'>
                <b style='color:#f0c040;'>{best_home}</b> benefits most from home ground,
                winning <b style='color:#4ade80;'>{best_home_adv:+.1f}%</b> more at home vs away.
                Familiar pitches, crowd support, and no travel fatigue make a real difference.
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Insight 3: Toss advantage ────────────────────────────────
    toss_wins_match = len(filtered[filtered['toss_winner'] == filtered['winner']])
    toss_win_pct = round(toss_wins_match / total_matches * 100, 1)

    # Toss decision effectiveness
    field_won = filtered[filtered['toss_decision'] == 'field']
    bat_won = filtered[filtered['toss_decision'] == 'bat']
    field_chase_wins = len(field_won[field_won['winner'] == field_won['chasing_team']])
    bat_chase_wins = len(bat_won[bat_won['winner'] == bat_won['chasing_team']])

    ins5, ins6 = st.columns([1, 1.5])
    with ins5:
        st.markdown(f"""
        <div class='insight-card'>
            <div class='insight-title'>🪙 Toss = Victory?</div>
            <div class='insight-text'>
                Toss winners convert to match winners <b style='color:#f0c040;'>{toss_win_pct}%</b>
                of the time. Teams increasingly choose to field first — letting the pitch settle
                and using target-clarity to their batting advantage.
            </div>
        </div>""", unsafe_allow_html=True)

    with ins6:
        # Toss decision pie
        field_count = len(filtered[filtered['toss_decision'] == 'field'])
        bat_count = len(filtered[filtered['toss_decision'] == 'bat'])
        fig_toss = go.Figure(go.Pie(
            labels=['Choose to Field', 'Choose to Bat'],
            values=[field_count, bat_count],
            hole=0.55,
            marker_colors=['#60a5fa', '#f472b6'],
            textinfo='label+percent',
        ))
        fig_toss.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#c0d0e0',
            showlegend=False,
            height=240,
            margin=dict(t=10, b=10),
        )
        st.plotly_chart(fig_toss, use_container_width=True)

    st.markdown("---")

    # ── Insight 4: Season trend ──────────────────────────────────
    st.markdown("<div class='section-header'>📈 Season Performance Trends</div>", unsafe_allow_html=True)
    season_team_wins = {}
    for team in selected_teams:
        wins_by_season = []
        for s in seasons:
            s_df = filtered[filtered['season'] == s]
            w = len(s_df[s_df['winner'] == team])
            wins_by_season.append(w)
        season_team_wins[team] = wins_by_season

    fig_trend = go.Figure()
    for team, wins in season_team_wins.items():
        fig_trend.add_trace(go.Scatter(
            x=seasons, y=wins,
            mode='lines+markers',
            name=team,
            line=dict(color=TEAM_COLORS.get(team, '#888'), width=2),
            marker=dict(size=8),
            hovertemplate=f'<b>{team}</b><br>Season: %{{x}}<br>Wins: %{{y}}<extra></extra>',
        ))
    fig_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#c0d0e0',
        legend=dict(orientation='v', font_size=11),
        xaxis=dict(showgrid=False, title='Season', dtick=1),
        yaxis=dict(showgrid=True, gridcolor='#1e2a3a', title='Wins'),
        height=360,
        margin=dict(t=10),
    )
    st.plotly_chart(fig_trend, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# TAB 3 — PLAYER STATS
# ════════════════════════════════════════════════════════════════
with tab3:
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("<div class='section-header'>🏏 Top Run Scorers</div>", unsafe_allow_html=True)
        top_batsmen = (
            filtered_players.groupby('player')['runs']
            .sum().reset_index()
            .sort_values('runs', ascending=False)
            .head(12)
        )
        top_batsmen['color'] = top_batsmen['player'].apply(
            lambda p: TEAM_COLORS.get(
                filtered_players[filtered_players['player'] == p]['team'].mode().iloc[0]
                if not filtered_players[filtered_players['player'] == p].empty else '#888', '#888'
            )
        )
        fig_bat = go.Figure(go.Bar(
            x=top_batsmen['runs'], y=top_batsmen['player'],
            orientation='h',
            marker_color=top_batsmen['color'],
            text=top_batsmen['runs'], textposition='outside',
        ))
        fig_bat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#c0d0e0',
            xaxis=dict(showgrid=True, gridcolor='#1e2a3a', title='Total Runs'),
            yaxis=dict(showgrid=False, categoryorder='total ascending'),
            height=420,
            margin=dict(t=10, l=10),
        )
        st.plotly_chart(fig_bat, use_container_width=True)

    with col_p2:
        st.markdown("<div class='section-header'>🎳 Top Wicket Takers</div>", unsafe_allow_html=True)
        top_bowlers = (
            filtered_players.groupby('player')['wickets']
            .sum().reset_index()
            .sort_values('wickets', ascending=False)
            .head(12)
        )
        top_bowlers['color'] = top_bowlers['player'].apply(
            lambda p: TEAM_COLORS.get(
                filtered_players[filtered_players['player'] == p]['team'].mode().iloc[0]
                if not filtered_players[filtered_players['player'] == p].empty else '#888', '#888'
            )
        )
        fig_bowl = go.Figure(go.Bar(
            x=top_bowlers['wickets'], y=top_bowlers['player'],
            orientation='h',
            marker_color=top_bowlers['color'],
            text=top_bowlers['wickets'], textposition='outside',
        ))
        fig_bowl.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#c0d0e0',
            xaxis=dict(showgrid=True, gridcolor='#1e2a3a', title='Total Wickets'),
            yaxis=dict(showgrid=False, categoryorder='total ascending'),
            height=420,
            margin=dict(t=10, l=10),
        )
        st.plotly_chart(fig_bowl, use_container_width=True)

    # Strike rate leaders
    st.markdown("<div class='section-header'>⚡ Best Strike Rate (min 200 balls faced)</div>", unsafe_allow_html=True)
    sr_df = (
        filtered_players.groupby('player')
        .agg(total_runs=('runs', 'sum'), total_balls=('balls_faced', 'sum'))
        .reset_index()
    )
    sr_df = sr_df[sr_df['total_balls'] >= 200].copy()
    sr_df['SR'] = round(sr_df['total_runs'] / sr_df['total_balls'] * 100, 1)
    sr_df = sr_df.sort_values('SR', ascending=False).head(10)

    fig_sr = go.Figure(go.Bar(
        x=sr_df['player'], y=sr_df['SR'],
        marker=dict(
            color=sr_df['SR'],
            colorscale='RdYlGn',
            showscale=False,
        ),
        text=sr_df['SR'], textposition='outside',
        hovertemplate='<b>%{x}</b><br>SR: %{y}<extra></extra>',
    ))
    fig_sr.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#c0d0e0',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#1e2a3a', title='Strike Rate'),
        height=320,
        margin=dict(t=10),
    )
    st.plotly_chart(fig_sr, use_container_width=True)

    # Team sixes comparison
    st.markdown("<div class='section-header'>💥 Sixes Hit Per Team</div>", unsafe_allow_html=True)
    sixes_df = (
        filtered_players.groupby('team')['sixes']
        .sum().reset_index()
        .sort_values('sixes', ascending=False)
    )
    fig_sixes = go.Figure(go.Bar(
        x=sixes_df['team'], y=sixes_df['sixes'],
        marker_color=[TEAM_COLORS.get(t, '#888') for t in sixes_df['team']],
        text=sixes_df['sixes'], textposition='outside',
    ))
    fig_sixes.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#c0d0e0',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#1e2a3a', title='Total Sixes'),
        height=300,
        margin=dict(t=10),
    )
    st.plotly_chart(fig_sixes, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# TAB 4 — PREDICTOR
# ════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-header'>🔮 Match Outcome Predictor</div>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#8ca3c0; font-size:13px;'>
    Uses historical win rates, home advantage, and toss/decision factors to predict the likely winner.
    Configure the matchup in the sidebar and click <b>Predict Winner</b>.
    </p>
    """, unsafe_allow_html=True)

    def predict_winner(t1, t2, toss_w, decision, venue_type, df):
        total = len(df)

        def win_pct(team):
            played = len(df[(df['team1'] == team) | (df['team2'] == team)])
            won = len(df[df['winner'] == team])
            return won / played if played else 0.5

        base_t1 = win_pct(t1)
        base_t2 = win_pct(t2)

        # Normalise
        t1_score = base_t1 / (base_t1 + base_t2)
        t2_score = 1 - t1_score

        # Home advantage boost (+5%)
        if venue_type == "Home for Team 1":
            t1_score += 0.05
        elif venue_type == "Home for Team 2":
            t2_score += 0.05

        # Toss factor
        if toss_w == t1:
            if decision == 'field':
                t1_score += 0.03  # chasing advantage
            else:
                t1_score += 0.01
        else:
            if decision == 'field':
                t2_score += 0.03
            else:
                t2_score += 0.01

        total_score = t1_score + t2_score
        t1_prob = round(t1_score / total_score * 100, 1)
        t2_prob = round(t2_score / total_score * 100, 1)

        return (t1, t1_prob) if t1_prob >= t2_prob else (t2, t2_prob), t1_prob, t2_prob

    if predict_btn or True:  # always show comparison
        result, t1_prob, t2_prob = predict_winner(
            pred_team1, pred_team2, pred_toss, pred_decision, pred_venue_type, filtered
        )
        winner_name, win_prob = result

        p_col1, p_col2, p_col3 = st.columns([1, 1.2, 1])

        with p_col1:
            st.markdown(f"""
            <div style='text-align:center; padding:30px 0;'>
                <div style='font-size:42px;'>🏏</div>
                <div style='font-size:26px; font-weight:800; color:{TEAM_COLORS.get(pred_team1,"#888")};'>{pred_team1}</div>
                <div style='font-size:36px; font-weight:700; color:#60a5fa; margin-top:12px;'>{t1_prob}%</div>
                <div style='font-size:12px; color:#5a7a9a;'>Win Probability</div>
            </div>""", unsafe_allow_html=True)

        with p_col2:
            st.markdown(f"""
            <div class='prediction-box' style='margin-top:10px;'>
                <div style='font-size:13px; color:#86efac; letter-spacing:1px;'>PREDICTED WINNER</div>
                <div class='prediction-winner'>{winner_name}</div>
                <div class='prediction-confidence'>Confidence: {win_prob}%</div>
                <div style='margin-top:16px; font-size:12px; color:#4a6a5a;'>
                    Toss: {pred_toss} chose to {pred_decision}<br>
                    Venue: {pred_venue_type}
                </div>
            </div>""", unsafe_allow_html=True)

        with p_col3:
            st.markdown(f"""
            <div style='text-align:center; padding:30px 0;'>
                <div style='font-size:42px;'>🏏</div>
                <div style='font-size:26px; font-weight:800; color:{TEAM_COLORS.get(pred_team2,"#888")};'>{pred_team2}</div>
                <div style='font-size:36px; font-weight:700; color:#60a5fa; margin-top:12px;'>{t2_prob}%</div>
                <div style='font-size:12px; color:#5a7a9a;'>Win Probability</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gauge chart for probability
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=t1_prob,
            title={'text': f"{pred_team1} Win Probability", 'font': {'color': '#c0d0e0', 'size': 16}},
            number={'suffix': '%', 'font': {'color': '#f0c040', 'size': 40}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#5a7a9a'},
                'bar': {'color': TEAM_COLORS.get(pred_team1, '#888')},
                'bgcolor': '#1e2a3a',
                'bordercolor': '#2d4a6b',
                'steps': [
                    {'range': [0, 40], 'color': '#1a0d0d'},
                    {'range': [40, 60], 'color': '#1a1a0d'},
                    {'range': [60, 100], 'color': '#0d1a0d'},
                ],
                'threshold': {
                    'line': {'color': '#f0c040', 'width': 3},
                    'thickness': 0.8,
                    'value': 50,
                },
            },
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#c0d0e0',
            height=280,
            margin=dict(t=30, b=10),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        # H2H history
        st.markdown("<div class='section-header'>📜 Head-to-Head History</div>", unsafe_allow_html=True)
        h2h = filtered[
            ((filtered['team1'] == pred_team1) & (filtered['team2'] == pred_team2)) |
            ((filtered['team1'] == pred_team2) & (filtered['team2'] == pred_team1))
        ]
        h2h_t1 = len(h2h[h2h['winner'] == pred_team1])
        h2h_t2 = len(h2h[h2h['winner'] == pred_team2])
        h2h_total = len(h2h)

        hc1, hc2, hc3 = st.columns(3)
        with hc1:
            st.markdown(f"""<div class='metric-card'>
                <div class='label'>{pred_team1} Wins</div>
                <div class='value' style='color:{TEAM_COLORS.get(pred_team1,"#f0c040")};'>{h2h_t1}</div>
            </div>""", unsafe_allow_html=True)
        with hc2:
            st.markdown(f"""<div class='metric-card'>
                <div class='label'>Total Meetings</div>
                <div class='value'>{h2h_total}</div>
            </div>""", unsafe_allow_html=True)
        with hc3:
            st.markdown(f"""<div class='metric-card'>
                <div class='label'>{pred_team2} Wins</div>
                <div class='value' style='color:{TEAM_COLORS.get(pred_team2,"#f0c040")};'>{h2h_t2}</div>
            </div>""", unsafe_allow_html=True)

        if h2h_total > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            recent_h2h = h2h.sort_values('date', ascending=False).head(6)[
                ['season', 'winner', 'win_type', 'margin', 'toss_winner', 'toss_decision']
            ].rename(columns={
                'season': 'Season', 'winner': 'Winner', 'win_type': 'Win By',
                'margin': 'Margin', 'toss_winner': 'Toss', 'toss_decision': 'Decision'
            })
            st.dataframe(
                recent_h2h.style.applymap(
                    lambda v: f"color: {TEAM_COLORS.get(v, '#c0d0e0')}; font-weight:bold" if v in TEAM_COLORS else "",
                    subset=['Winner', 'Toss']
                ),
                use_container_width=True,
                hide_index=True,
            )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#1e2a3a; margin-top:40px;'>
<p style='text-align:center; color:#2d4a6b; font-size:12px;'>
🏏 IPL Match Insights Dashboard · Built with Python, Pandas & Streamlit · Data: IPL 2019–2024
</p>
""", unsafe_allow_html=True)
