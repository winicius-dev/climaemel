import pandas as pd

clima = pd.read_csv(
    "dados/clima_diario_2021_2025.csv",
    skiprows=11,
    header=None,
    names=["ano", "dia_ano", "temperatura_media", "precipitacao"]
)

for coluna in ["ano", "temperatura_media", "precipitacao"]:
    clima[coluna] = pd.to_numeric(clima[coluna], errors="coerce")

clima[["temperatura_media", "precipitacao"]] = (
    clima[["temperatura_media", "precipitacao"]].replace(-999, float("nan"))
)

clima_anual = clima.groupby("ano").agg(
    temperatura_media_anual=("temperatura_media", "mean"),
    precipitacao_total_anual=("precipitacao", "sum"),
    dias_com_temperatura=("temperatura_media", "count"),
    dias_com_precipitacao=("precipitacao", "count")
).reset_index()

tabela_mel = pd.read_csv(
    "dados/producao_mel.csv",
    sep=";",
    skiprows=4,
    header=None,
    encoding="utf-8"
)

linha_mel = tabela_mel.iloc[1, :]

anos = [2021, 2022, 2023, 2024, 2025]
valores = linha_mel.iloc[1:6].astype(int).tolist()

mel = pd.DataFrame({
    "ano": anos,
    "producao_kg": valores
})

resultado = clima_anual.merge(mel, on="ano", how="inner")

print("\nINDICADORES CLIMÁTICOS ANUAIS:")
print(clima_anual.round(2).to_string(index=False))

print("\nCLIMA E PRODUÇÃO DE MEL:")
print(resultado.round(2).to_string(index=False))

resultado.to_csv("dados/resumo_anual_clima_mel.csv", index=False)
print("\nArquivo salvo em dados/resumo_anual_clima_mel.csv")



import matplotlib.pyplot as plt

plt.figure(figsize=(9, 5))
plt.plot(resultado["ano"], resultado["producao_kg"], marker="o")

plt.title("Produção anual de mel em São Raimundo Nonato")
plt.xlabel("Ano")
plt.ylabel("Produção de mel (kg)")
plt.xticks(resultado["ano"])
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()