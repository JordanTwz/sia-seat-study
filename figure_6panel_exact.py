import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 14

# Load data
df_core = pd.read_excel("df_ratings_all (2).xlsx", sheet_name="df_ratings_all")
df_melt = pd.read_excel("df_ratings_melt.xlsx")

# Filter
dff = df_core[(df_core["slope_hour"] > 0) & (df_core["significant"] == True)].copy()
dff["Gender"] = dff["Gender"].map(lambda x: "Female" if str(x).lower().startswith("f") else "Male")

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
dfm = dfm[dfm["past_flights_std"].isin(pf_order)]

# Helper plotting functions
def scatter_ax(ax, x, y, xlabel, title):
    ax.scatter(x, y, alpha=0.6)
    X = sm.add_constant(np.asarray(x,float))
    beta = sm.OLS(np.asarray(y,float), X).fit().params
    xx = np.linspace(min(x), max(x), 100)
    yy = beta[0] + beta[1]*xx
    ax.plot(xx, yy, "--", color="black", linewidth=1.2, alpha=0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Discomfort increase per hour (slope)")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)

def box_ax(ax, cats, vals, xlabel, title, dot_color):
    cats = pd.Categorical(cats)
    grouped = [np.array(vals)[cats.codes==i] for i in range(len(cats.categories))]
    bp = ax.boxplot(grouped, labels=list(cats.categories), patch_artist=True)
    for b in bp["boxes"]:
        b.set_alpha(0.5)
    rng = np.random.default_rng(42)
    for i,g in enumerate(grouped):
        if len(g)==0: continue
        ax.plot(rng.normal(i+1,0.05,len(g)), g, "o", color=dot_color, alpha=0.75, markersize=3)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Discomfort increase per hour (slope)")
    ax.set_title(title)
    ax.grid(True, axis="y", alpha=0.3)

# Create combined figure
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

scatter_ax(axes[0,0], dff["Height"], dff["slope_hour"], "Height (cm)", "Discomfort vs Height")
scatter_ax(axes[0,1], dff["Weight"], dff["slope_hour"], "Weight (kg)", "Discomfort vs Weight")
scatter_ax(axes[0,2], dff["Age"], dff["slope_hour"], "Age (years)", "Discomfort vs Age")

box_ax(axes[1,0], dff["Gender"], dff["slope_hour"], "Sex", "Discomfort vs Sex", "#000000")
box_ax(axes[1,1], dfm["past_flights_std"], dfm["slope_hour"], "Flights in past year", "Discomfort vs Flights in past year", "#2ca02c")

sd = dff.copy()
levels_sd = sorted(sd["sitting_duration"].unique(), key=str)
sd["sitting_duration"] = pd.Categorical(sd["sitting_duration"], categories=levels_sd, ordered=True)
box_ax(axes[1,2], sd["sitting_duration"], sd["slope_hour"], "Habitual daily sitting duration", "Discomfort vs Habitual sitting duration", "#d62728")

plt.tight_layout()

out_svg = "figure_6panel_exact.svg"
fig.savefig(out_svg, format="svg")

out_svg
