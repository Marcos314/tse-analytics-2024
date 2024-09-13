
#%%
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sn
from adjustText import adjust_text


#%%
with open("partidos.sql", "r") as open_file:
    query = open_file.read()

engine = sqlalchemy.create_engine('sqlite:///../data/database_br.db')

df = pd.read_sql_query(query, engine)
df.head()

#%%
tx_gen_feminino = df["total_gen_feminino"].sum() / df["total_candidaturas"].sum()
tx_cor_raca_preta = df["total_cor_raca_preta"].sum() / df["total_candidaturas"].sum()
tx_cor_raca_nao_branca = df["total_cor_raca_nao_branca"].sum() / df["total_candidaturas"].sum()
tx_cor_raca_preta_parda = df["total_cor_raca_preta_parda"].sum() / df["total_candidaturas"].sum()

#%%

plt.figure(dpi=500)

sn.scatterplot(data=df,
        x="tx_gen_feminino_BR",
        y="tx_cor_raca_preta_BR",
        size="total_candidaturas",
        sizes=(5,300),
        palette='viridis',
        alpha=0.6
)
texts = []
for i in df['SG_PARTIDO']:
    data = df[df["SG_PARTIDO"]==i]
    x = data['tx_gen_feminino_BR'].values[0]
    y = data['tx_cor_raca_preta_BR'].values[0]
    texts.append(plt.text(x, y, i, fontsize=9))

adjust_text(texts,
    force_points=0.0002,
    force_text=0.3,
    expand_points=(0.5, 0.75),
    expand_text=(0.5, 0.75),
    only_move={'points':'y', 'text':'xy'},
    arrowprops=dict(arrowstyle="->", color='black', lw=0.5),
    pull_threshold=1000,
    hue=["cluster_BR"],
)

plt.grid(True)
plt.title("Cor vs Genero - Eleições 2024")
plt.xlabel("Taxa de Mulheres")
plt.ylabel("Taxa de Pessoas Pretas")

plt.hlines(y = tx_cor_raca_preta, xmin = 0.3, xmax = 0.55,  colors="black", alpha=0.6, linestyles='--', label=f"% Pessoas Pretas Geral: {100*tx_cor_raca_preta:.0f}%")
plt.vlines(x = tx_gen_feminino, ymin = 0.05, ymax = 0.35,  colors="tomato", alpha=0.6, linestyles='--', label=f"% Mulheres Geral: {100*tx_gen_feminino:.0f}%")

handles, labels = plt.gca().get_legend_handles_labels()
handles = handles[5:]
labels = labels[5:]

plt.legend(handles=handles, labels=labels)


plt.savefig("../img/partidos_cor_gen_1.png")

# %%
plt.figure(dpi=500)

sn.scatterplot(data=df,
        x="tx_gen_feminino_BR",
        y="tx_cor_raca_preta_BR"
)
texts = []
for i in df['SG_PARTIDO']:
    data = df[df["SG_PARTIDO"]==i]
    x = data['tx_gen_feminino_BR'].values[0]
    y = data['tx_cor_raca_preta_BR'].values[0]
    texts.append(plt.text(x, y, i, fontsize=9))

adjust_text(texts,
    force_points=0.0002,
    force_text=0.3,
    expand_points=(0.5, 0.75),
    expand_text=(0.5, 0.75),
    only_move={'points':'y', 'text':'xy'},
    arrowprops=dict(arrowstyle="->", color='black', lw=0.5),
    pull_threshold=1000,

)

plt.grid(True)
plt.title("Cor vs Genero - Eleições 2024")
plt.xlabel("Taxa de Mulheres")
plt.ylabel("Taxa de Pessoas Pretas")

plt.hlines(y = tx_cor_raca_preta, xmin = 0.3, xmax = 0.55,  colors="black", alpha=0.6, linestyles='--', label=f"% Pessoas Pretas Geral: {100*tx_cor_raca_preta:.0f}%")
plt.vlines(x = tx_gen_feminino, ymin = 0.05, ymax = 0.35,  colors="tomato", alpha=0.6, linestyles='--', label=f"% Mulheres Geral: {100*tx_gen_feminino:.0f}%")

plt.legend()


plt.savefig("../img/partidos_cor_gen_2.png")

#%%
from sklearn import cluster
X = df[["tx_gen_feminino_BR", "tx_cor_raca_preta_BR"]]
model = cluster.KMeans(n_clusters=5)
model.fit(X)

df["cluster_BR"] = model.labels_

df.groupby("cluster_BR")["tx_gen_feminino_BR"].count()
# %%
