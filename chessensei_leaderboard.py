import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="Chessensei Student Leaderboard",
    page_icon="♟",
    layout="wide",
)

LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAQ4BDgDASIAAhEBAxEB/8QAHQABAAICAwEBAAAAAAAAAAAAAAcIBQYCAwQBCf/EAF0QAAIBAwIDBQQFCAQKBQkGBwABAgMEBQYRBxIhCBMxQVEUYXGBIjJSkaEVQmJygpKxwQkjM6IWJFNjc6Oys8LRQ5PS4fAXGCU0NUR1g8NWZGV0lNMnNjdUVbTx/8QAGwEBAAMBAQEBAAAAAAAAAAAAAAQFBgMCAQf/xAA5EQEAAgEDAwEEBwgCAgMBAAAAAQIDBAUREiExQRMyUWEiQnGBkaGxFBUjM1LB0fAG4SQ0YmPC8f/aAAwDAQACEQMRAD8AuWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/2Q=="
logo_html = f'<img src="data:image/png;base64,{LOGO_B64}" style="height:56px;object-fit:contain;">'

st.markdown(f"""
<style>
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stApp {{ background: linear-gradient(135deg, #0f0c29, #1a1a4e, #24243e); min-height: 100vh; }}
    .stars-container {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; overflow: hidden; }}
    .star {{ position: absolute; background: white; border-radius: 50%; animation: floatStar linear infinite; opacity: 0; }}
    @keyframes floatStar {{ 0% {{ transform: translateY(100vh) scale(0); opacity: 0; }} 10% {{ opacity: 1; }} 90% {{ opacity: 0.8; }} 100% {{ transform: translateY(-10vh) scale(1); opacity: 0; }} }}
    .glitter {{ position: absolute; width: 6px; height: 6px; border-radius: 50%; animation: glitterAnim ease-in-out infinite; opacity: 0; }}
    @keyframes glitterAnim {{ 0%,100% {{ opacity: 0; transform: scale(0) rotate(0deg); }} 50% {{ opacity: 1; transform: scale(1.5) rotate(180deg); }} }}
    .top-bar {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; padding: 0 0.5rem; }}
    .logo-wrap {{ display: flex; align-items: center; }}
    .live-badge {{ display: inline-block; background: rgba(34,197,94,0.2); color: #22c55e; font-size: 0.75rem; font-weight: 700; padding: 3px 12px; border-radius: 20px; border: 1px solid #22c55e; letter-spacing: 1px; animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0%,100% {{ box-shadow: 0 0 0 0 rgba(34,197,94,0.4); }} 50% {{ box-shadow: 0 0 0 6px rgba(34,197,94,0); }} }}
    .main-title {{ text-align: center; font-size: 2.6rem; font-weight: 900; background: linear-gradient(90deg, #FFD700, #FFA500, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; margin-bottom: 0; animation: shimmer 3s ease-in-out infinite; }}
    @keyframes shimmer {{ 0%,100% {{ filter: brightness(1); }} 50% {{ filter: brightness(1.4); }} }}
    .main-sub {{ text-align: center; font-size: 0.9rem; color: #a0aec0; margin-bottom: 1.2rem; }}
    .search-label {{ font-size: 0.7rem; color: #a0aec0; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 5px; }}
    .found-banner {{ background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.4); border-radius: 12px; padding: 12px 16px; margin-bottom: 12px; display: flex; align-items: center; gap: 14px; }}
    .found-avatar {{ width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; font-weight: 700; flex-shrink: 0; }}
    .found-name {{ font-size: 1rem; font-weight: 700; color: #f7fafc; }}
    .found-meta {{ font-size: 0.75rem; color: #a0aec0; margin-top: 2px; }}
    .found-score {{ margin-left: auto; font-size: 2rem; font-weight: 900; color: #FFD700; }}
    .found-rank {{ font-size: 0.75rem; color: #a0aec0; text-align: right; }}
    .score-breakdown {{ display: flex; gap: 16px; margin-top: 6px; flex-wrap: wrap; }}
    .breakdown-item {{ text-align: center; }}
    .breakdown-val {{ font-size: 0.9rem; font-weight: 700; color: #f7fafc; }}
    .breakdown-lbl {{ font-size: 0.65rem; color: #718096; text-transform: uppercase; }}
    .metric-box {{ background: rgba(255,255,255,0.07); border-radius: 14px; padding: 1rem 1.2rem; border: 1px solid rgba(255,255,255,0.12); text-align: center; backdrop-filter: blur(10px); }}
    .metric-label {{ font-size: 0.72rem; color: #a0aec0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; }}
    .metric-value {{ font-size: 1.9rem; font-weight: 800; color: #FFD700; }}
    .podium-card {{ background: rgba(255,255,255,0.07); border-radius: 18px; padding: 1.4rem 1rem; text-align: center; border: 1px solid rgba(255,255,255,0.12); backdrop-filter: blur(10px); transition: transform 0.2s; }}
    .podium-card:hover {{ transform: translateY(-4px); }}
    .podium-card.gold {{ border-top: 4px solid #FFD700; box-shadow: 0 0 20px rgba(255,215,0,0.3); }}
    .podium-card.silver {{ border-top: 4px solid #C0C0C0; box-shadow: 0 0 20px rgba(192,192,192,0.2); }}
    .podium-card.bronze {{ border-top: 4px solid #CD7F32; box-shadow: 0 0 20px rgba(205,127,50,0.2); }}
    .podium-name {{ font-size: 1rem; font-weight: 700; color: #f7fafc; margin: 0.5rem 0 0.2rem; }}
    .podium-score {{ font-size: 2.2rem; font-weight: 900; }}
    .podium-trainer {{ font-size: 0.75rem; padding: 2px 10px; border-radius: 10px; display: inline-block; margin-top: 4px; background: rgba(255,255,255,0.1); color: #e2e8f0; }}
    .podium-sub {{ font-size: 0.76rem; color: #a0aec0; margin-top: 0.4rem; }}
    .lb-header-row {{ display: grid; grid-template-columns: 50px 1fr 80px 100px 70px 70px 70px; gap: 8px; padding: 0 1rem 6px; font-size: 0.7rem; color: #718096; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 8px; }}
    .lb-row {{ display: grid; grid-template-columns: 50px 1fr 80px 100px 70px 70px 70px; gap: 8px; align-items: center; background: rgba(255,255,255,0.05); border-radius: 12px; padding: 0.75rem 1rem; margin-bottom: 7px; border: 1px solid rgba(255,255,255,0.07); transition: background 0.2s, transform 0.15s; animation: fadeIn 0.4s ease forwards; }}
    .lb-row:hover {{ background: rgba(255,255,255,0.1); transform: translateX(4px); border-color: rgba(255,215,0,0.3); }}
    .lb-row.highlighted {{ border: 2px solid #f59e0b; background: rgba(245,158,11,0.1); }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .rank-num {{ font-size: 1rem; font-weight: 800; color: #718096; text-align: center; }}
    .player-name {{ font-size: 0.95rem; font-weight: 700; color: #f7fafc; }}
    .trainer-tag {{ font-size: 0.68rem; padding: 1px 8px; border-radius: 8px; font-weight: 600; display: inline-block; margin-top: 2px; }}
    .score-pill {{ border-radius: 20px; padding: 3px 12px; font-size: 0.85rem; font-weight: 800; display: inline-block; text-align: center; min-width: 58px; }}
    .score-green {{ background: rgba(22,163,74,0.25); color: #4ade80; border: 1px solid rgba(22,163,74,0.4); }}
    .score-amber {{ background: rgba(217,119,6,0.25); color: #fbbf24; border: 1px solid rgba(217,119,6,0.4); }}
    .score-red {{ background: rgba(220,38,38,0.25); color: #f87171; border: 1px solid rgba(220,38,38,0.4); }}
    .sub-score {{ font-size: 0.82rem; font-weight: 600; color: #a0aec0; }}
    .trainer-card {{ background: rgba(255,255,255,0.06); border-radius: 14px; padding: 1rem 1.2rem; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 8px; display: flex; align-items: center; gap: 1rem; transition: transform 0.15s; }}
    .trainer-card:hover {{ transform: translateX(4px); }}
    .trainer-rank {{ font-size: 1.5rem; min-width: 36px; text-align: center; }}
    .trainer-name {{ font-size: 0.95rem; font-weight: 700; color: #f7fafc; flex: 1; }}
    .trainer-meta {{ font-size: 0.75rem; color: #a0aec0; }}
    .trainer-score-pill {{ background: rgba(255,215,0,0.15); color: #FFD700; border: 1px solid rgba(255,215,0,0.3); border-radius: 20px; padding: 4px 14px; font-size: 0.88rem; font-weight: 800; }}
    .section-title {{ font-size: 1.2rem; font-weight: 800; color: #f7fafc; margin: 1.5rem 0 0.8rem; display: flex; align-items: center; gap: 8px; }}
    .section-title::after {{ content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.1); }}
    .results-count {{ font-size: 0.75rem; color: #718096; margin-bottom: 8px; text-align: right; }}
</style>
<div class="stars-container" id="starsContainer"></div>
<script>
(function() {{
    const container = document.getElementById('starsContainer');
    if (!container) return;
    const colors = ['#FFD700','#FFA500','#ffffff','#87CEEB','#DDA0DD','#98FB98'];
    for (let i = 0; i < 40; i++) {{
        const el = document.createElement('div');
        const isGlitter = Math.random() > 0.6;
        el.className = isGlitter ? 'glitter' : 'star';
        const size = Math.random() * (isGlitter ? 6 : 3) + 1;
        el.style.cssText = `left: ${{Math.random()*100}}%;width: ${{size}}px;height: ${{size}}px;animation-duration: ${{Math.random()*10+6}}s;animation-delay: ${{Math.random()*8}}s;background: ${{colors[Math.floor(Math.random()*colors.length)]}};`;
        container.appendChild(el);
    }}
}})();
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FIX 1: TRAINER_COLORS extended to 10
# ─────────────────────────────────────────────
TRAINER_COLORS = {
    0: ("rgba(99,102,241,0.25)",  "#818cf8"),
    1: ("rgba(236,72,153,0.25)",  "#f472b6"),
    2: ("rgba(20,184,166,0.25)",  "#2dd4bf"),
    3: ("rgba(245,158,11,0.25)",  "#fbbf24"),
    4: ("rgba(239,68,68,0.25)",   "#f87171"),
    5: ("rgba(34,197,94,0.25)",   "#4ade80"),
    6: ("rgba(168,85,247,0.25)",  "#c084fc"),
    7: ("rgba(14,165,233,0.25)",  "#38bdf8"),
    8: ("rgba(249,115,22,0.25)",  "#fb923c"),
    9: ("rgba(6,182,212,0.25)",   "#5eead4"),
}

SHEET_NAME = "Quality_April_26"

TRAINER_SHEETS = {
    "Sheet 1":  "1xZuOsdeyY_3q30m7RkJPTEbs5uJZJt7kFtCbAM_0KuI",
    "Sheet 2":  "1ZmFeO3Qw_9U0RYatrN24EgyFLcn8jnXxf7MyhdaFxkU",
    "Sheet 3":  "1G7YWQTCaKyP3vrOwo_K94SHjHVTTToD3INJhtk8es-M",
    "Sheet 4":  "1YAeGYFkYyyfmTUq5XY4QHMsNustd76LRSzUxRIF_2ZY",
    "Sheet 5":  "1rEC1sRtPVisf8wdNgAhq6iFhZeIV6ZVXxG6KMXSYV0I",
    "Sheet 6":  "1CnkAIeIazUPlkvk3ubHK0E00skVmuQP90gcLrKF_414",
    "Sheet 7":  "1lr1tWzVsoCKzqOc2THyl2KPiHi_lFUaJnGR-BaGgMJI",
    "Sheet 8":  "1Ih_4U-s5Gsg2GweVN3NKWAJZygPtMJhws8ZlgEliNUQ",
    "Sheet 9":  "1EcrXnW9NVK_R1AQ8TU_h8H6GX6fyAPkXa6C7UoJLAMI",
    "Sheet 10": "1djRs8tTDBE0p06VR7uWJUZpSQwQrtjZ_HEVAeAVuO0U",
}

PUZZLE_MAX  = 5
TOURNEY_MAX = 5
HW_MAX      = 5

@st.cache_data(ttl=30)
def load_all_data():
    all_dfs = []
    for idx, (sheet_key, sheet_id) in enumerate(TRAINER_SHEETS.items()):
        if not sheet_id.strip():
            continue
        try:
            url = (
                f"https://docs.google.com/spreadsheets/d/{sheet_id}"
                f"/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
            )
            df = pd.read_csv(url)
            if df.empty:
                continue

            cols = list(df.columns)
            seen = {}
            new_cols = []
            for c in cols:
                if c in seen:
                    seen[c] += 1
                    new_cols.append(f"{c}_{seen[c]}")
                else:
                    seen[c] = 0
                    new_cols.append(c)
            df.columns = new_cols

            required = [
                "Student_Name", "Student_ID", "Trainer_Name", "Level",
                "Total_Scheduled", "Total_Completed",
                "P_W1","P_W2","P_W3","P_W4",
                "T_W1","T_W2","T_W3","T_W4",
                "H_W1","H_W2","H_W3","H_W4",
            ]
            missing = [c for c in required if c not in df.columns]
            if missing:
                st.warning(f"⚠️ {sheet_key}: missing columns {missing} — skipped")
                continue

            df = df[required].copy()
            df = df[df["Student_Name"].notna() & (df["Student_Name"].str.strip() != "")]
            df = df.reset_index(drop=True)
            df["Trainer_Color_Idx"] = idx

            num_cols = [c for c in required if c not in
                        ["Student_Name","Student_ID","Trainer_Name","Level"]]
            for col in num_cols:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

            all_dfs.append(df)

        except Exception as e:
            st.warning(f"⚠️ {sheet_key}: {e} — skipped")

    if not all_dfs:
        st.error("❌ No data loaded. Check sheet IDs and make sure sheets are public.")
        st.stop()

    df_all = pd.concat(all_dfs, ignore_index=True)

    # ── FIX 2: Safe attendance — fillna(1) prevents division by zero / NaN ──
    df_all["Total_Completed"] = pd.to_numeric(df_all["Total_Completed"], errors="coerce").fillna(0)
    df_all["Total_Scheduled"] = pd.to_numeric(df_all["Total_Scheduled"], errors="coerce").fillna(1)
    df_all["Total_Scheduled"] = df_all["Total_Scheduled"].replace(0, 1)  # prevent div/0

    df_all["Attendance"]    = (df_all["Total_Completed"] / df_all["Total_Scheduled"] * 100).round(1)
    df_all["Puzzle_Score"]  = (df_all[["P_W1","P_W2","P_W3","P_W4"]].mean(axis=1) / PUZZLE_MAX  * 100).round(1)
    df_all["Tourney_Score"] = (df_all[["T_W1","T_W2","T_W3","T_W4"]].mean(axis=1) / TOURNEY_MAX * 100).round(1)
    df_all["HW_Score"]      = (df_all[["H_W1","H_W2","H_W3","H_W4"]].mean(axis=1) / HW_MAX      * 100).round(1)

    df_all["Total_Score"] = (
        df_all["Attendance"]    * 0.25 +
        df_all["Puzzle_Score"]  * 0.25 +
        df_all["Tourney_Score"] * 0.25 +
        df_all["HW_Score"]      * 0.25
    ).round(1)

    # Fill any remaining NaN with 0
    df_all["Attendance"]    = df_all["Attendance"].fillna(0)
    df_all["Total_Score"]   = df_all["Total_Score"].fillna(0)
    df_all["Puzzle_Score"]  = df_all["Puzzle_Score"].fillna(0)
    df_all["HW_Score"]      = df_all["HW_Score"].fillna(0)
    df_all["Tourney_Score"] = df_all["Tourney_Score"].fillna(0)

    df_all = df_all.sort_values("Total_Score", ascending=False).reset_index(drop=True)
    df_all["Rank"] = df_all.index + 1
    return df_all

def medal(rank):
    return {1:"🥇", 2:"🥈", 3:"🥉"}.get(rank, "")

def podium_cls(rank):
    return {1:"gold", 2:"silver", 3:"bronze"}.get(rank, "")

def score_cls(s):
    if s >= 80: return "score-green"
    if s >= 60: return "score-amber"
    return "score-red"

def score_color(s):
    if s >= 80: return "#4ade80"
    if s >= 60: return "#fbbf24"
    return "#f87171"

def initials(name):
    parts = str(name).strip().split()
    return "".join(p[0] for p in parts[:2]).upper()

# ── FIX 3: safe_int helper — handles NaN safely everywhere ──
def safe_int(val):
    try:
        v = float(val)
        if v != v:  # NaN check
            return 0
        return max(0, min(100, int(v)))
    except:
        return 0

with st.spinner("⚡ Fetching live scores..."):
    df = load_all_data()

last_refresh = time.strftime("%I:%M:%S %p")
all_trainers = sorted(df["Trainer_Name"].dropna().unique().tolist())

trainer_color_map = {}
for i, t in enumerate(all_trainers):
    # FIX 2b: % 10 not % 7
    trainer_color_map[t] = i % 10

# ── HEADER ──
st.markdown(f"""
<div class="top-bar">
    <div style="flex:1"></div>
    <div style="text-align:center;flex:2">
        <div class="main-title">♟ Chessensei Student Leaderboard</div>
        <div class="main-sub">
            <span class="live-badge">● LIVE</span>
            &nbsp;&nbsp;Auto-refreshes every 60 seconds · All Trainers Combined
        </div>
    </div>
    <div class="logo-wrap" style="flex:1;justify-content:flex-end">
        {logo_html}
    </div>
</div>
""", unsafe_allow_html=True)

# ── METRICS ──
m1, m2, m3, m4, m5 = st.columns(5)
metrics = [
    ("Total Students",  str(len(df))),
    ("Trainers Active", str(df["Trainer_Name"].nunique())),
    ("Average Score",   f"{df['Total_Score'].mean():.1f}"),
    ("Top Score",       f"{df['Total_Score'].max():.1f}"),
    ("Last Synced",     last_refresh),
]
for col, (label, val) in zip([m1, m2, m3, m4, m5], metrics):
    with col:
        fsize = "1.1rem" if label == "Last Synced" else "1.8rem"
        st.markdown(
            f'<div class="metric-box">'
            f'<div class="metric-label">{label}</div>'
            f'<div class="metric-value" style="font-size:{fsize}">{val}</div>'
            f'</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── DUAL SEARCH ──
col_s1, col_s2 = st.columns(2)
with col_s1:
    st.markdown('<div class="search-label">🔍 Search Student</div>', unsafe_allow_html=True)
    student_search = st.text_input("student_search", label_visibility="collapsed",
                                   placeholder="Type student name...", key="student_q")
with col_s2:
    st.markdown('<div class="search-label">👨‍🏫 Search Trainer</div>', unsafe_allow_html=True)
    trainer_search = st.text_input("trainer_search", label_visibility="collapsed",
                                   placeholder="Type trainer name...", key="trainer_q")

st.markdown('<div class="search-label" style="margin-bottom:8px">Quick Filter by Trainer</div>',
            unsafe_allow_html=True)
pill_options = ["All"] + all_trainers
selected_trainer = st.radio("trainer_filter", pill_options,
                            horizontal=True, label_visibility="collapsed", key="trainer_pill")

# ── FILTERS ──
filtered = df.copy()
if selected_trainer != "All":
    filtered = filtered[filtered["Trainer_Name"] == selected_trainer]
if trainer_search.strip():
    filtered = filtered[filtered["Trainer_Name"].str.contains(
        trainer_search.strip(), case=False, na=False)]

student_found = None
if student_search.strip():
    mask = filtered["Student_Name"].str.contains(student_search.strip(), case=False, na=False)
    if mask.any():
        student_found = filtered[mask].iloc[0]
    filtered = filtered[mask]

# ── FOUND BANNER ──
if student_found is not None:
    cidx = trainer_color_map.get(student_found["Trainer_Name"], 0)
    bg, fg = TRAINER_COLORS.get(cidx, ("rgba(99,102,241,0.25)", "#818cf8"))
    sc = score_color(student_found["Total_Score"])
    att_val = safe_int(student_found["Attendance"])
    st.markdown(f"""
    <div class="found-banner">
        <div class="found-avatar" style="background:{bg};color:{fg}">
            {initials(student_found['Student_Name'])}
        </div>
        <div style="flex:1">
            <div class="found-name">{student_found['Student_Name']}</div>
            <div class="found-meta">
                Trainer: {student_found['Trainer_Name']} &nbsp;·&nbsp;
                Level: {student_found['Level']} &nbsp;·&nbsp;
                Rank: #{int(student_found['Rank'])}
            </div>
            <div class="score-breakdown">
                <div class="breakdown-item">
                    <div class="breakdown-val">{att_val}%</div>
                    <div class="breakdown-lbl">Attendance</div>
                </div>
                <div class="breakdown-item">
                    <div class="breakdown-val">{student_found['Puzzle_Score']:.0f}</div>
                    <div class="breakdown-lbl">Puzzles</div>
                </div>
                <div class="breakdown-item">
                    <div class="breakdown-val">{student_found['HW_Score']:.0f}</div>
                    <div class="breakdown-lbl">Homework</div>
                </div>
                <div class="breakdown-item">
                    <div class="breakdown-val">{student_found['Tourney_Score']:.0f}</div>
                    <div class="breakdown-lbl">Tournament</div>
                </div>
            </div>
        </div>
        <div style="text-align:right">
            <div class="found-score" style="color:{sc}">{student_found['Total_Score']}</div>
            <div class="found-rank">Rank #{int(student_found['Rank'])} of {len(df)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
elif student_search.strip():
    st.warning(f"No student found matching **{student_search}**")

# ── PODIUM ──
if selected_trainer == "All" and not student_search.strip() and not trainer_search.strip():
    st.markdown('<div class="section-title">🏆 Top 3 Champions</div>', unsafe_allow_html=True)
    top3  = df.head(min(3, len(df)))
    order = [1, 0, 2] if len(top3) == 3 else list(range(len(top3)))
    pcols = st.columns(3)
    for ci, ri in enumerate(order):
        if ri >= len(top3):
            continue
        row  = top3.iloc[ri]
        rank = int(row["Rank"])
        cidx = trainer_color_map.get(row["Trainer_Name"], 0)
        _, fg = TRAINER_COLORS.get(cidx, ("", "#e2e8f0"))
        att_p = safe_int(row["Attendance"])
        with pcols[ci]:
            st.markdown(f"""
            <div class="podium-card {podium_cls(rank)}">
                <div style="font-size:2.5rem">{medal(rank)}</div>
                <div class="podium-name">{row['Student_Name']}</div>
                <div class="podium-trainer" style="color:{fg}">{row['Trainer_Name']}</div>
                <div class="podium-score" style="color:{score_color(row['Total_Score'])}">
                    {row['Total_Score']}
                </div>
                <div class="podium-sub">
                    📅 {att_p}% &nbsp;·&nbsp;
                    🧩 {row['Puzzle_Score']:.0f} &nbsp;·&nbsp;
                    📚 {row['HW_Score']:.0f} &nbsp;·&nbsp;
                    🏆 {row['Tourney_Score']:.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── LEADERBOARD TABLE ──
filter_label = ""
if selected_trainer != "All":     filter_label = f" — {selected_trainer}"
if trainer_search.strip():        filter_label = f" — matching '{trainer_search}'"
if student_search.strip():        filter_label = f" — matching '{student_search}'"

st.markdown(f'<div class="section-title">📋 Full Rankings{filter_label}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="results-count">{len(filtered)} student(s) shown</div>', unsafe_allow_html=True)
st.markdown("""
<div class="lb-header-row">
    <div>Rank</div><div>Student · Trainer</div><div>Score</div>
    <div>Attendance</div><div>Puzzles</div><div>HW</div><div>Tourney</div>
</div>
""", unsafe_allow_html=True)

for _, row in filtered.iterrows():
    rank  = int(row["Rank"])
    cidx  = trainer_color_map.get(row["Trainer_Name"], 0)
    bg, fg = TRAINER_COLORS.get(cidx, ("rgba(255,255,255,0.1)", "#e2e8f0"))
    sc    = score_cls(row["Total_Score"])
    pct   = safe_int(row["Attendance"])   # ← FIX 3 applied here
    bar_w = int(pct * 0.7)
    rank_display = medal(rank) if rank <= 3 else f"#{rank}"
    is_found = (student_search.strip() and
                student_search.strip().lower() in str(row["Student_Name"]).lower())
    row_class = "lb-row highlighted" if is_found else "lb-row"

    st.markdown(f"""
    <div class="{row_class}">
        <div class="rank-num">{rank_display}</div>
        <div>
            <div class="player-name">{row['Student_Name']}</div>
            <span class="trainer-tag" style="background:{bg};color:{fg};border:1px solid {fg}50">
                {row['Trainer_Name']}
            </span>
        </div>
        <div><span class="score-pill {sc}">{row['Total_Score']}</span></div>
        <div>
            <div class="sub-score">{pct}%</div>
            <div style="background:rgba(255,255,255,0.1);border-radius:4px;height:4px;width:70px;margin-top:3px">
                <div style="background:#3b82f6;border-radius:4px;height:4px;width:{bar_w}px"></div>
            </div>
        </div>
        <div class="sub-score">{row['Puzzle_Score']:.0f}</div>
        <div class="sub-score">{row['HW_Score']:.0f}</div>
        <div class="sub-score">{row['Tourney_Score']:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# ── TRAINER LEADERBOARD ──
if selected_trainer == "All" and not student_search.strip() and not trainer_search.strip():
    st.markdown('<div class="section-title">👨‍🏫 Trainer Leaderboard</div>', unsafe_allow_html=True)
    st.caption("Ranked by average student score per trainer")
    trainer_stats = (
        df.groupby("Trainer_Name")
        .agg(
            Students    = ("Student_Name", "count"),
            Avg_Score   = ("Total_Score",  "mean"),
            Avg_Attend  = ("Attendance",   "mean"),
            Top_Student = ("Student_Name",
                           lambda x: x.iloc[df.loc[x.index,"Total_Score"].values.argmax()]),
        )
        .reset_index()
    )
    trainer_stats["Avg_Score"]  = trainer_stats["Avg_Score"].round(1)
    trainer_stats["Avg_Attend"] = trainer_stats["Avg_Attend"].fillna(0).round(0)
    trainer_stats = trainer_stats.sort_values("Avg_Score", ascending=False).reset_index(drop=True)
    trainer_medals = ["🥇","🥈","🥉"]
    for i, row in trainer_stats.iterrows():
        cidx   = trainer_color_map.get(row["Trainer_Name"], 0)
        bg, fg = TRAINER_COLORS.get(cidx, ("rgba(255,255,255,0.06)", "#e2e8f0"))
        tm     = trainer_medals[i] if i < 3 else f"#{i+1}"
        st.markdown(f"""
        <div class="trainer-card" style="border-left:3px solid {fg}">
            <div class="trainer-rank">{tm}</div>
            <div style="flex:1">
                <div class="trainer-name" style="color:{fg}">{row['Trainer_Name']}</div>
                <div class="trainer-meta">
                    {int(row['Students'])} students &nbsp;·&nbsp;
                    Avg Attendance {int(row['Avg_Attend'])}% &nbsp;·&nbsp;
                    Top: {row['Top_Student']}
                </div>
            </div>
            <div class="trainer-score-pill">{row['Avg_Score']}</div>
        </div>
        """, unsafe_allow_html=True)

with st.expander("ℹ️ How is the score calculated?"):
    st.markdown("""
    **Total Score = Equal average of 4 components (25% each)**

    | Component | Formula | Weight |
    |---|---|---|
    | **Attendance** | (Total_Completed ÷ Total_Scheduled) × 100 | 25% |
    | **Puzzles** | Mean(P_W1–P_W4) ÷ 5 × 100 | 25% |
    | **Homework** | Mean(H_W1–H_W4) ÷ 5 × 100 | 25% |
    | **Tournament** | Mean(T_W1–T_W4) ÷ 5 × 100 | 25% |

    **Score colours:** 🟢 ≥80 · 🟡 60–79 · 🔴 <60
    """)

st.markdown(
    f"<div style='text-align:center;font-size:0.72rem;color:#4a5568;margin-top:2rem'>"
    f"♟ Chessensei · Live from Google Sheets · {last_refresh}</div>",
    unsafe_allow_html=True
)

time.sleep(60)
st.rerun()
