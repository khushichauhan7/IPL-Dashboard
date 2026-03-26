# 🏏 IPL Match Insights Dashboard

A sleek, interactive Streamlit dashboard for IPL 2019–2024 match analysis with cool data-driven insights and a match predictor.

---

## 🚀 Quick Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate the dataset
```bash
python generate_data.py
```
This creates `matches.csv` (240 matches) and `player_stats.csv` (2400 records).

### 3. Run the dashboard
```bash
streamlit run app.py
```
Opens at **http://localhost:8501**

---

## 📊 What's Inside

### Tab 1 — Team Stats
- **Wins per team** (bar chart with team colours)
- **Win rate %** (horizontal bar)
- **Played vs Won bubble chart** — size = win rate
- **Season-wise wins heatmap** — spot consistency vs streaks

### Tab 2 — ⚡ Cool Insights
| Insight | What it shows |
|---|---|
| 🏃 Chasing vs Batting First | Teams chasing win ~52% — T20 target-clarity advantage |
| 🏟️ Home Ground Advantage | Which team dominates at home vs struggles away |
| 🪙 Toss = Victory? | Toss winners convert to match winners X% of the time |
| 📈 Season Trends | Multi-team win trend across 6 seasons |

### Tab 3 — Player Stats
- Top 12 run scorers (coloured by team)
- Top 12 wicket takers
- Best strike rates (min 200 balls)
- Team sixes comparison

### Tab 4 — 🔮 Match Predictor
- Select two teams + toss winner + toss decision + venue type
- Get win probability for each team
- Gauge chart for visual probability display
- Head-to-head history table

---

## 🔧 Tech Stack
- **Python 3.9+**
- **Pandas** — data wrangling
- **Streamlit** — web UI
- **Plotly** — interactive charts

---

## 📁 File Structure
```
ipl_dashboard/
├── app.py              ← Main Streamlit app
├── generate_data.py    ← Synthetic IPL data generator
├── matches.csv         ← Generated: 240 IPL matches
├── player_stats.csv    ← Generated: player performance records
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## 🎨 Features
- Dark cricket-themed UI (navy + gold)
- Fully interactive — filter by season and team
- Responsive sidebar controls
- Mobile-friendly layout

---

*Built with ❤️ using Python & Streamlit*
