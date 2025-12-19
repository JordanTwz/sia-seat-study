# Regenerate the 6‑panel figure directly as a PNG (same layout & styling)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from PIL import Image

# ---------- Load data ----------
df_core = pd.read_excel("df_ratings_all (2).xlsx", sheet_name="df_ratings_all")
df_melt = pd.read_excel("df_ratings_melt.xlsx")

# Filter to positive & significant slopes
dff = df_core[(df_core["slope_hour"] > 0) & (df_core["significant"] == True)].copy()
dff["Gender"] = dff["Gender"].map(lambda x: "Female" if str(x).lower().startswith("f") else "Male")
dff["past_flights"] = dff["past_flights"].astype(str)
dff["sitting_duration"] = dff["sitting_duration"].astype(str)

# Melted file (one row per subject)
dfm = df_melt[(df_melt["slope_hour"] > 0) & (df_melt["Significant"] == True)][
    ["subject","past_flights","slope_hour"]
].drop_duplicates("subject")

def map_pf(val):
    s = str(val).lower().strip()
    if s in {"0","zero","none","no flights"}: return "0"
    if "more" in s and "15" in s: return "More than 15"
    if "6" in s and "15" in s: return "6-15"
    if "1" in s and "5" in s: return "1-5"
    if "0" in s and "5" in s: return "1-5"
    return str(val)

dfm["past_flights_std"] = dfm["past_flights"].astype(str).map(map_pf)
pf_order = ["0","1-5","6-15","More than 15"]
dfm["past_flights_std"] = pd.Categorical(dfm["past_flights_std"], categories=pf_order, ordered=True)

# ---------- Plot helpers ----------
def scatter_panel(x, y, xlabel, title, outfile):
    fig, ax = plt.subplots(figsize=(6,4.5), dpi=200)
    ax.scatter(x, y, alpha=0.6)
    # dashed OLS
    X = sm.add_constant(np.asarray(x,float))
    beta = sm.OLS(np.asarray(y,float), X).fit().params
    xx = np.linspace(min(x), max(x), 100)
    yy = beta[0] + beta[1]*xx
    ax.plot(xx, yy, "--", color="black", linewidth=1.4, alpha=0.7)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Discomfort increase per hour (slope)")
    ax.set_title(title)
    fig.savefig(outfile, dpi=200, bbox_inches="tight")
    plt.close(fig)

def box_panel(cats, vals, xlabel, title, outfile, dot_color):
    cats = pd.Categorical(cats)
    grouped = [np.array(vals)[cats.codes==i] for i in range(len(cats.categories))]
    fig, ax = plt.subplots(figsize=(6,4.5), dpi=200)
    bp = ax.boxplot(grouped, labels=list(cats.categories), patch_artist=True)
    for b in bp["boxes"]: b.set_alpha(0.5)
    rng = np.random.default_rng(42)
    for i,g in enumerate(grouped):
        if len(g)==0: continue
        ax.plot(rng.normal(i+1,0.05,len(g)), g, "o", color=dot_color, alpha=0.75, markersize=3)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Discomfort increase per hour (slope)")
    ax.set_title(title)
    fig.savefig(outfile, dpi=200, bbox_inches="tight")
    plt.close(fig)

# ---------- Generate PNGs ----------
paths = {}

paths["height"] = "panel_height.png"
scatter_panel(dff["Height"], dff["slope_hour"], "Height (cm)", "Discomfort vs Height", paths["height"])

paths["weight"] = "panel_weight.png"
scatter_panel(dff["Weight"], dff["slope_hour"], "Weight (kg)", "Discomfort vs Weight", paths["weight"])

paths["age"] = "panel_age.png"
scatter_panel(dff["Age"], dff["slope_hour"], "Age (years)", "Discomfort vs Age", paths["age"])

paths["sex"] = "panel_sex.png"
sexc = pd.Categorical(dff["Gender"], categories=["Male","Female"], ordered=True)
box_panel(sexc, dff["slope_hour"], "Sex", "Discomfort vs Sex", paths["sex"], "#000000")

paths["flights"] = "panel_flights.png"
pfc = dfm.dropna(subset=["past_flights_std"])
box_panel(pfc["past_flights_std"], pfc["slope_hour"],
          "Flights in past year", "Discomfort vs Flights in past year",
          paths["flights"], "#2ca02c")

paths["sitting"] = "panel_sitting.png"
sd = dff.copy()
levels_sd = sorted(sd["sitting_duration"].unique(), key=str)
sd["sitting_duration"] = pd.Categorical(sd["sitting_duration"], categories=levels_sd, ordered=True)
box_panel(sd["sitting_duration"], sd["slope_hour"],
          "Habitual daily sitting duration", "Discomfort vs Habitual daily sitting duration",
          paths["sitting"], "#d62728")

# ---------- Combine into 2×3 layout ----------
imgs = [Image.open(paths[k]) for k in ["height","weight","age","sex","flights","sitting"]]
w, h = imgs[0].size
W = 3*w
H = 2*h

combined = Image.new("RGB", (W, H), "white")
positions = [(0,0), (w,0), (2*w,0), (0,h), (w,h), (2*w,h)]
for im,pos in zip(imgs, positions):
    combined.paste(im, pos)

combined_path = "figure_6panel_combined.png"
combined.save(combined_path)

combined_path
