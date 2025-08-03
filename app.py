# ===========================================
# app.py – מפעיל את האתר Streamlit
# ===========================================
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
from calculator import load_raw_data, run_simulation

DATA_DIR = Path(__file__).parent / "data"

# טוען נתונים גולמיים פעם אחת בלבד
housing_long, sp_fx = load_raw_data(DATA_DIR)

MIN_YEAR, MAX_YEAR = 1995, 2023
st.title("💰 Investment Explorer – נדל״ן מול S&P 500")

# ממשק בחירת שנים וסכום
col1, col2 = st.columns(2)
with col1:
    start_year = st.slider("שנת התחלה", MIN_YEAR, MAX_YEAR - 1, 2000)
with col2:
    end_year = st.slider("שנת סיום", MIN_YEAR + 1, MAX_YEAR, 2015)

amount = st.number_input("₪ השקעה התחלתית", 10_000, 5_000_000, 200_000, step=10_000)

# כפתור הרצה
if st.button("הרץ סימולציה"):
    df = run_simulation(housing_long, sp_fx, start_year, end_year, amount)

    if df is None or df.empty:
        st.error("⚠️ החישוב עוד לא מוכן – צריך להשלים את run_simulation ב-calculator.py")
        st.stop()

    # חישוב תוצאות
    final_re = df["Real_Estate_Norm"].iloc[-1]
    final_sp = df["SP500_Norm"].iloc[-1]
    roi_re = (final_re - amount) / amount * 100
    roi_sp = (final_sp - amount) / amount * 100
    winner = "🏠 נדל״ן" if final_re > final_sp else "📈 S&P 500"

    # גרף
    fig = go.Figure()
    fig.add_scatter(x=df["Date"], y=df["Real_Estate_Norm"],
                    mode="lines", name=f"🏠 נדל״ן ({roi_re:.1f}%)")
    fig.add_scatter(x=df["Date"], y=df["SP500_Norm"],
                    mode="lines", name=f"📈 S&P 500 ({roi_sp:.1f}%)")
    fig.add_scatter(x=[df["Date"].iloc[0], df["Date"].iloc[-1]],
                    y=[amount, amount], mode="lines",
                    name="השקעה התחלתית", line=dict(dash="dash"))
    fig.update_layout(template="plotly_white",
                      title=f"₪{amount:,.0f} • {start_year}-{end_year}",
                      yaxis_title="שווי (₪)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # טבלת סיכום
    st.markdown(f"""
### 📊 סיכום  
| מדד | 🏠 נדל״ן | 📈 S&P 500 |
|-----|---------|-----------|
| שווי סופי (₪) | ₪{final_re:,.0f} | ₪{final_sp:,.0f} |
| תשואה כוללת (%) | {roi_re:.1f}% | {roi_sp:.1f}% |
| רווח (₪) | ₪{final_re - amount:,.0f} | ₪{final_sp - amount:,.0f} |

**המנצח**: **{winner}**
""")
