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

    # TODO: כאן תכניס את כל קוד הניקוי/איחוד שעשית במחברת
    # df_home ---> housing_long   (צריך לכלול Investor_Net_Value)
    # df_sp + df_fx ---> sp_fx    (צריך לכלול TR_Index_NIS)

    # כדי שהאפליקציה לא תקרוס בשלב ראשון, נחזיר את הטבלאות הגולמיות
    return df_home, df_sp.join(df_fx, how="inner")


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
