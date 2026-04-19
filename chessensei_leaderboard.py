import streamlit as st
import pandas as pd
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ChessSensei Leaderboard",
    page_icon="♟",
    layout="wide",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    #MainMenu, footer, header { visibility: hidden; }
    .stApp { background-color: #f5f5f5; }

    .main-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 800;
        color: #1a1a2e;
        letter-spacing: -1px;
        margin-bottom: 0;
    }
    .main-sub {
        text-align: center;
        font-size: 0.95rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .live-badge {
        display: inline-block;
        background: #dcfce7;
        color: #16a34a;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }
    .podium-card {
        background: white;
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #e9ecef;
        height: 100%;
    }
    .podium-card.gold   { border-top: 4px solid #f59e0b; }
    .podium-card.silver { border-top: 4px solid #9ca3af; }
    .podium-card.bronze { border-top: 4px solid #cd7c2f; }
    .podium-name  { font-size: 1rem; font-weight: 700; color: #1a1a2e; margin: 0.4rem 0 0.1rem; }
    .podium-score { font-size: 2rem; font-weight: 800; }
    .podium-level { font-size: 0.75rem; color: #6c757d; background: #f3f4f6;
                    border-radius: 8px; padding: 2px 8px; display: inline-block; }
    .podium-sub   { font-size: 0.78rem; color: #6c757d; margin-top: 0.3rem; }
    .metric-box {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        border: 1px solid #e9ecef;
        text-align: center;
    }
    .metric-label { font-size: 0.72rem; color: #6c757d; font-weight: 600;
                    text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 1.8rem; font-weight: 800; color: #1a1a2e; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONFIG — update SHEET_ID if sheet changes
# ─────────────────────────────────────────────
SHEET_ID   = "1xZuOsdeyY_3q30m7RkJPTEbs5uJZJt7kFtCbAM_0KuI"
SHEET_NAME = "Testing"   # exact tab name

# Max possible score per week for each category — adjust if needed
PUZZLE_MAX  = 5
TOURNEY_MAX = 5
HW_MAX      = 5


# ─────────────────────────────────────────────
# DATA LOADER — cached 30s for real-time feel
# ─────────────────────────────────────────────
@st.cache_data(ttl=30)
def load_data():
    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    )
    df = pd.read_csv(url)

    cols_needed = [
        "Student_Name", "Student_ID", "Level",
        "Total_Scheduled", "Total_Completed",
        "P_W1", "P_W2", "P_W3", "P_W4",
        "T_W1", "T_W2", "T_W3", "T_W4",
        "H_W1", "H_W2", "H_W3", "H_W4",
    ]
    df = df[cols_needed].copy()
    df = df[df["Student_Name"].notna() & (df["Student_Name"].str.strip() != "")]
    df = df.reset_index(drop=True)

    score_cols = [c for c in cols_needed if c not in ["Student_Name", "Student_ID", "Level"]]
    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # ── Score calculation ──
    df["Attendance"]    = (df["Total_Completed"] / df["Total_Scheduled"] * 100).round(1)
    df["Puzzle_Score"]  = (df[["P_W1","P_W2","P_W3","P_W4"]].mean(axis=1) / PUZZLE_MAX  * 100).round(1)
    df["Tourney_Score"] = (df[["T_W1","T_W2","T_W3","T_W4"]].mean(axis=1) / TOURNEY_MAX * 100).round(1)
    df["HW_Score"]      = (df[["H_W1","H_W2","H_W3","H_W4"]].mean(axis=1) / HW_MAX      * 100).round(1)

    # Equal weight — 25% each
    df["Total_Score"] = (
        df["Attendance"]    * 0.25 +
        df["Puzzle_Score"]  * 0.25 +
        df["Tourney_Score"] * 0.25 +
        df["HW_Score"]      * 0.25
    ).round(1)

    df = df.sort_values("Total_Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def medal(rank):
    return {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "")

def podium_cls(rank):
    return {1: "gold", 2: "silver", 3: "bronze"}.get(rank, "")

def score_color(s):
    if s >= 80: return "#16a34a"
    if s >= 60: return "#d97706"
    return "#dc2626"


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown('<div class="main-title">♟ ChessSensei Leaderboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="main-sub"><span class="live-badge">● LIVE</span>'
    '&nbsp;&nbsp;Auto-refreshes every 30 seconds</div>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
with st.spinner("Fetching latest scores from Google Sheets..."):
    df = load_data()

last_refresh = time.strftime("%I:%M:%S %p")

# ─────────────────────────────────────────────
# SUMMARY METRICS
# ─────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
metrics = [
    ("Total Students",  str(len(df))),
    ("Average Score",   f"{df['Total_Score'].mean():.1f}"),
    ("Top Score",       f"{df['Total_Score'].max():.1f}"),
    ("Last Synced",     last_refresh),
]
for col, (label, val) in zip([m1, m2, m3, m4], metrics):
    with col:
        st.markdown(
            f'<div class="metric-box">'
            f'<div class="metric-label">{label}</div>'
            f'<div class="metric-value" style="font-size:{"1.1rem" if label=="Last Synced" else "1.8rem"}">{val}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PODIUM — TOP 3  (order: Silver | Gold | Bronze)
# ─────────────────────────────────────────────
st.markdown("### 🏆 Top 3 Champions")
top3 = df.head(min(3, len(df)))
display_order = [1, 0, 2] if len(top3) == 3 else list(range(len(top3)))
pcols = st.columns(3)

for ci, ri in enumerate(display_order):
    if ri >= len(top3):
        continue
    row  = top3.iloc[ri]
    rank = int(row["Rank"])
    with pcols[ci]:
        st.markdown(f"""
        <div class="podium-card {podium_cls(rank)}">
            <div style="font-size:2.2rem">{medal(rank)}</div>
            <div class="podium-name">{row['Student_Name']}</div>
            <span class="podium-level">{row['Level']} · ID {int(row['Student_ID'])}</span>
            <div class="podium-score" style="color:{score_color(row['Total_Score'])}">
                {row['Total_Score']}
            </div>
            <div class="podium-sub">
                Attendance {row['Attendance']}% &nbsp;|&nbsp; Puzzles {row['Puzzle_Score']:.0f}
            </div>
            <div class="podium-sub">
                Homework {row['HW_Score']:.0f} &nbsp;|&nbsp; Tournament {row['Tourney_Score']:.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FULL RANKINGS TABLE
# ─────────────────────────────────────────────
st.markdown("### 📋 Full Rankings")

# Header row
h1, h2, h3, h4, h5, h6, h7 = st.columns([0.5, 2.2, 0.9, 1.1, 1, 1, 1])
headers = ["RANK", "STUDENT", "SCORE", "ATTENDANCE", "PUZZLES", "HOMEWORK", "TOURNAMENT"]
for col, hdr in zip([h1, h2, h3, h4, h5, h6, h7], headers):
    col.markdown(
        f"<span style='font-size:0.72rem;color:#9ca3af;font-weight:700;'>{hdr}</span>",
        unsafe_allow_html=True
    )

st.markdown("<hr style='margin:4px 0 8px;border-color:#e9ecef;'>", unsafe_allow_html=True)

for _, row in df.iterrows():
    rank = int(row["Rank"])
    c1, c2, c3, c4, c5, c6, c7 = st.columns([0.5, 2.2, 0.9, 1.1, 1, 1, 1])

    # Rank
    with c1:
        label = medal(rank) if rank <= 3 else str(rank)
        st.markdown(
            f"<div style='font-size:1rem;font-weight:700;color:#6c757d;"
            f"padding-top:6px;text-align:center'>{label}</div>",
            unsafe_allow_html=True
        )

    # Name + ID
    with c2:
        st.markdown(
            f"<div style='padding-top:4px'>"
            f"<span style='font-size:0.95rem;font-weight:600;color:#1a1a2e'>{row['Student_Name']}</span><br>"
            f"<span style='font-size:0.75rem;color:#9ca3af'>ID {int(row['Student_ID'])} · {row['Level']}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    # Score pill
    with c3:
        color = score_color(row["Total_Score"])
        st.markdown(
            f"<div style='background:{color};color:white;border-radius:20px;"
            f"padding:4px 12px;font-size:0.88rem;font-weight:700;"
            f"display:inline-block;margin-top:6px'>{row['Total_Score']}</div>",
            unsafe_allow_html=True
        )

    # Attendance with mini bar
    with c4:
        pct = min(100, max(0, int(row["Attendance"])))
        bar = pct * 0.9  # scale to px (max ~90px)
        st.markdown(
            f"<div style='padding-top:6px'>"
            f"<span style='font-size:0.85rem;font-weight:600;color:#374151'>{pct}%</span>"
            f"<div style='background:#f3f4f6;border-radius:4px;height:5px;width:90px;margin-top:3px'>"
            f"<div style='background:#3b82f6;border-radius:4px;height:5px;width:{bar}px'></div>"
            f"</div></div>",
            unsafe_allow_html=True
        )

    # Puzzle / HW / Tourney
    for col, key in zip([c5, c6, c7], ["Puzzle_Score", "HW_Score", "Tourney_Score"]):
        with col:
            val = row[key]
            col_c = score_color(val)
            st.markdown(
                f"<div style='font-size:0.88rem;font-weight:600;color:{col_c};padding-top:8px'>"
                f"{val:.0f}<span style='font-size:0.7rem;color:#9ca3af'>/100</span></div>",
                unsafe_allow_html=True
            )

    # Thin divider between rows
    st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# WEEK-BY-WEEK BREAKDOWN (expander)
# ─────────────────────────────────────────────
with st.expander("📊 View Week-by-Week Breakdown"):
    breakdown = df[["Rank","Student_Name","Level",
                     "P_W1","P_W2","P_W3","P_W4",
                     "T_W1","T_W2","T_W3","T_W4",
                     "H_W1","H_W2","H_W3","H_W4"]].copy()
    breakdown = breakdown.rename(columns={"Student_Name":"Name"})
    st.dataframe(breakdown.set_index("Rank"), use_container_width=True)

# ─────────────────────────────────────────────
# FORMULA EXPLAINER
# ─────────────────────────────────────────────
with st.expander("ℹ️ How is the Total Score calculated?"):
    st.markdown("""
    **Total Score = Equal average of 4 components (25% each)**

    | Component | Formula | Weight |
    |---|---|---|
    | **Attendance** | (Total_Completed ÷ Total_Scheduled) × 100 | 25% |
    | **Puzzles** | Mean(P_W1–P_W4) ÷ 5 × 100 | 25% |
    | **Homework** | Mean(H_W1–H_W4) ÷ 5 × 100 | 25% |
    | **Tournament** | Mean(T_W1–T_W4) ÷ 5 × 100 | 25% |

    > All weekly scores are assumed out of **5**. Change `PUZZLE_MAX`, `TOURNEY_MAX`, `HW_MAX` at the top of the file if different.

    **Score colour coding:** 🟢 ≥80 · 🟡 60–79 · 🔴 <60
    """)

# ─────────────────────────────────────────────
# FOOTER + AUTO-REFRESH
# ─────────────────────────────────────────────
st.markdown(
    f"<div style='text-align:center;font-size:0.75rem;color:#d1d5db;margin-top:1rem'>"
    f"ChessSensei · Live data from Google Sheets · Synced at {last_refresh}</div>",
    unsafe_allow_html=True
)

time.sleep(30)
st.rerun()
