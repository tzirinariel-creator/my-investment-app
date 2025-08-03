# ===========================================
# calculator.py – כל החישובים גרים כאן
# ===========================================
import pandas as pd
from pathlib import Path

# -------- טוען את קובצי הגלם פעם אחת --------
def load_raw_data(data_dir: Path):
    # נתיבי קבצים
    sp_path   = data_dir / "sp500.csv"
    fx_path   = data_dir / "דולר-שקל.csv"
    home_path = data_dir / "מחירי דיור.xlsx"

    # קריאה
    df_sp = pd.read_csv(sp_path, parse_dates=["Date"])
    df_fx = pd.read_csv(fx_path, parse_dates=["Date"])
    df_home = pd.read_excel(home_path)

    # ניקוי נתוני דיור
    df_home["Date"] = pd.to_datetime(df_home["Year"].astype(str) + "Q" + df_home["Quarter"].astype(str))
    housing_long = df_home[["Date", "Investor_Net_Value"]].copy()
    housing_long = housing_long.dropna()

    # ניקוי נתוני מדד SP500 לדולרים והמרה לשקלים
    df_sp["Date"] = pd.to_datetime(df_sp["Date"])
    df_fx["Date"] = pd.to_datetime(df_fx["Date"])
    sp_merged = pd.merge(df_sp, df_fx, on="Date", how="inner")
    sp_merged["TR_Index_NIS"] = sp_merged["TR_Index"] * sp_merged["ILS"]

    return housing_long, sp_merged


# -------- מריץ סימולציה לפי שנים וסכום --------
def run_simulation(housing_long, sp_fx,
                   start_year: int, end_year: int, amount: int):
    """
    מחזיר DataFrame עם:
    Date | Real_Estate_Norm | SP500_Norm
    (תואם למה שהשתמשת במחברת)
    """
    # TODO: הדבק כאן את הפונקציה המלאה שלך מה-Colab,
    # כולל חישובי שכירות, מס, משכנתא, וכו'.
    # בינתיים נחזיר None כך שהאפליקציה תציג הודעת שגיאה ולא תקרוס.
    return None


# =========================================================
# 📈 Simulate Fixed Investment Over Time
# =========================================================

def simulate_fixed_investment(start_date: str, amount: float, housing_df: pd.DataFrame, sp_df: pd.DataFrame):
    # Filter data from start date
    housing = housing_df[housing_df["Date"] >= pd.to_datetime(start_date)].copy()
    sp = sp_df[sp_df["Date"] >= pd.to_datetime(start_date)].copy()

    # Normalize values – investment starts at 'amount'
    housing["Value_NIS"] = housing["Investor_Net_Value"] / housing["Investor_Net_Value"].iloc[0] * amount
    sp["Value_NIS"] = sp["TR_Index_NIS"] / sp["TR_Index_NIS"].iloc[0] * amount

    return housing[["Date", "Value_NIS"]], sp[["Date", "Value_NIS"]]

