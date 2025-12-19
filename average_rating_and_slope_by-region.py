import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14

CSV_PATH = "df_ratings_all_raw(in).csv"   # update if needed
df = pd.read_csv(CSV_PATH)

# ----- helpers -----
def ols_slope_p(x, y):
    n = len(y)
    if n < 3 or np.all(np.isnan(y)): return np.nan, np.nan
    x = x.astype(float); y = y.astype(float)
    xm, ym = x.mean(), np.nanmean(y)
    Sxx = np.nansum((x - xm)**2); Sxy = np.nansum((x - xm)*(y - ym))
    if Sxx == 0: return np.nan, np.nan
    beta1 = Sxy / Sxx
    yhat = beta1*(x - xm) + ym
    resid = y - yhat
    s2 = np.nansum(resid**2) / (n - 2)
    se = np.sqrt(s2 / Sxx)
    if se == 0: return beta1, 0.0 if beta1 != 0 else 1.0
    try:
        from scipy.stats import t as tdist
        tstat = beta1 / se
        p = 2 * (1 - tdist.cdf(abs(tstat), df=n-2))
    except Exception:
        from math import erf, sqrt
        tstat = beta1 / se
        p = 2 * (1 - 0.5*(1 + erf(abs(tstat)/np.sqrt(2))))
    return beta1, p

def slope_only(y):
    x = np.arange(len(y))
    return ols_slope_p(x, y)[0]

# ----- order rows within subject -----
if "end_time" in df.columns:
    df["_t"] = pd.to_datetime(df["end_time"], errors="coerce")
    df["_order"] = df.groupby("subject").cumcount()
    df = df.sort_values(["subject", "_t", "_order"])
else:
    df["_order"] = df.groupby("subject").cumcount()
    df = df.sort_values(["subject", "_order"])

# ----- pick n=152: overall slope > 0 and p < 0.10 -----
keepers = []
for sub, g in df.groupby("subject"):
    y = g["overall_rating"].to_numpy(float)
    s, p = ols_slope_p(np.arange(len(y)), y)
    if not np.isnan(s) and s > 0 and p < 0.10:
        keepers.append(sub)

# ----- combine left/right into regions -----
regions = ["Buttock","Pelvis","Lower Back","Upper Back","Upper Thigh","Lower Thigh"]
dfc = pd.DataFrame({
    "subject": df["subject"].values,
    "Buttock": df[["left_butt","right_butt"]].mean(axis=1),
    "Pelvis": df[["left_pelvis","right_pelvis"]].mean(axis=1),
    "Lower Back": df["lower_back"].values,
    "Upper Back": df["upper_back"].values,
    "Upper Thigh": df[["left_upper_thigh","right_upper_thigh"]].mean(axis=1),
    "Lower Thigh": df[["left_lower_thigh","right_lower_thigh"]].mean(axis=1),
}).loc[lambda d: d["subject"].isin(keepers)]

# per-subject averages and slopes (per hour = x3)
avg_by_subj   = dfc.groupby("subject")[regions].mean()
slopes_entry  = dfc.groupby("subject").apply(
    lambda g: pd.Series({r: slope_only(g[r].to_numpy(float)) for r in regions})
)
slopes_hour   = slopes_entry * 3.0

# order requested by prof
order = ["Upper Back","Lower Back","Pelvis","Buttock","Upper Thigh","Lower Thigh"]
avg_by_subj = avg_by_subj[order]
slopes_hour = slopes_hour[order]

# common style (gray points; black medians/means)
boxprops    = dict(color="black")
medianprops = dict(color="black", linewidth=2)
whiskerprops= dict(color="black")
capprops    = dict(color="black")

# ---- Combined figure: Average Rating + Slope by Region (SVG) ----
fig, axes = plt.subplots(1, 2, figsize=(16, 5))

axes[0].boxplot([avg_by_subj[c].dropna().values for c in order],
                labels=order, showfliers=True,
                boxprops=boxprops, medianprops=medianprops,
                whiskerprops=whiskerprops, capprops=capprops)
for i, c in enumerate(order, start=1):
    y = avg_by_subj[c].dropna().values
    x = np.random.normal(i, 0.05, size=len(y))
    axes[0].scatter(x, y, s=10, alpha=0.7, c="lightgray", edgecolors="none")
    axes[0].scatter(i, y.mean(), marker="D", s=30, c="black")
axes[0].set_ylabel("Average Rating (0-10)")
axes[0].set_title("Average Rating by Region")
axes[0].set_xticklabels(order, rotation=30, ha="right")
axes[0].grid(False)

axes[1].boxplot([slopes_hour[c].dropna().values for c in order],
                labels=order, showfliers=True,
                boxprops=boxprops, medianprops=medianprops,
                whiskerprops=whiskerprops, capprops=capprops)
for i, c in enumerate(order, start=1):
    y = slopes_hour[c].dropna().values
    x = np.random.normal(i, 0.05, size=len(y))
    axes[1].scatter(x, y, s=10, alpha=0.7, c="lightgray", edgecolors="none")
    axes[1].scatter(i, y.mean(), marker="D", s=30, c="black")
axes[1].axhline(0, color="lightgray", linewidth=1)  # zero reference line
axes[1].set_ylabel("Slope (rating per hour)")
axes[1].set_title("Slope by Region")
axes[1].set_xticklabels(order, rotation=30, ha="right")
axes[1].grid(False)

plt.tight_layout()
out_svg = "average_rating_and_slope_by_region_n152_bw.svg"
plt.savefig(out_svg, format="svg", bbox_inches="tight")
plt.close(fig)

print("Saved SVG to :", out_svg)
