# 🏏 IPL Match Insights Dashboard

A sleek, interactive **Streamlit dashboard** that dives deep into IPL data (2019–2024), uncovering trends, player performances, and match-winning patterns — with a built-in **match outcome predictor**.

---

## ✨ Highlights

* 📊 Interactive visualizations with real-time filtering
* 🔍 Deep insights into team & player performance
* 🤖 Match predictor with win probabilities
* 🎨 Clean, dark cricket-themed UI (navy + gold vibes)
* 📱 Responsive & easy to use

---

## 🚀 Quick Setup

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Generate dataset

```bash
python generate_data.py
```

This will create:

* `matches.csv` → 240 IPL matches
* `player_stats.csv` → 2400 player records

### 3️⃣ Run the dashboard

```bash
streamlit run app.py
```

📍 Opens automatically at:

```
http://localhost:8501
```

---
## Live Demo
https://dashboard--ipl.streamlit.app
---

## 📊 Dashboard Overview

### 🏆 Tab 1 — Team Stats

* Wins per team (team-colored bar charts)
* Win rate comparison (%)
* Played vs Won bubble chart (size = win rate)
* Season-wise heatmap → consistency vs dominance

---

### ⚡ Tab 2 — Cool Insights

| Insight                     | Description                                              |
| --------------------------- | -------------------------------------------------------- |
| 🏃 Chasing vs Batting First | Chasing teams win ~52% → advantage of knowing the target |
| 🏟️ Home Ground Advantage   | Teams that dominate at home vs struggle away             |
| 🪙 Toss Impact              | How often toss winners actually win matches              |
| 📈 Season Trends            | Multi-season performance comparison                      |

---

### 🧑‍💻 Tab 3 — Player Stats

* Top 12 run scorers (team-colored)
* Top 12 wicket takers
* Best strike rates (min 200 balls faced)
* Team-wise sixes comparison

---

### 🔮 Tab 4 — Match Predictor

Simulate match outcomes based on:

* Teams
* Toss winner
* Toss decision
* Venue type

📌 Output:

* Win probability for each team
* Interactive gauge chart
* Head-to-head comparison table

---

## 🛠️ Tech Stack

* **Python 3.9+**
* **Pandas** → Data processing
* **Streamlit** → UI framework
* **Plotly** → Interactive charts

---

## 📁 Project Structure

```
ipl_dashboard/
├── app.py              # Main Streamlit app
├── generate_data.py    # Synthetic data generator
├── matches.csv         # Generated match data
├── player_stats.csv    # Player performance data
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

---

## 🎯 Features

* 🎨 Dark cricket-inspired UI
* ⚡ Fast and interactive dashboards
* 🔄 Dynamic filtering (team, season, stats)
* 📊 Insight-driven visual storytelling
* 📱 Mobile-friendly layout

---

## 💡 Future Improvements

* Add real IPL dataset integration
* Machine learning-based prediction model
* Player vs player comparison
* Live match API integration

---

## ❤️ Built With Passion

Made using **Python + Streamlit**
