import os
import re
import matplotlib.pyplot as plt

# ==========================================================
# 🔍 Extraction des données
# ==========================================================
pattern = re.compile(
    r"resultat_model19_adv_([0-9]+)_pgdstep_([0-9]+)\.txt",
    re.IGNORECASE
)

re_clean = re.compile(r"test acc on clean examples \(%\):\s*([0-9.]+)")
re_fgsm  = re.compile(r"test acc on FGM adversarial examples \(%\):\s*([0-9.]+)")
re_pgd   = re.compile(r"test acc on PGD adversarial examples \(%\):\s*([0-9.]+)")

results = []

for fname in os.listdir("."):
    m = pattern.search(fname)
    if not m:
        continue

    adv_str = m.group(1)*10
    step_str = m.group(2)*10

    # Conversion correcte : "001" → 0.001, "01" → 0.01
    adv = int(adv_str) / (10 ** len(adv_str))*10
    pgdstep = int(step_str) / (10 ** len(step_str))*10

    with open(fname, "r", encoding="utf-8") as f:
        text = f.read()

    clean_m = re_clean.search(text)
    fgsm_m = re_fgsm.search(text)
    pgd_m = re_pgd.search(text)

    if clean_m and fgsm_m and pgd_m:
        results.append({
            "fname": fname,
            "adv": adv,
            "pgdstep": pgdstep,
            "clean": float(clean_m.group(1)),
            "fgsm": float(fgsm_m.group(1)),
            "pgd": float(pgd_m.group(1)),
        })

if not results:
    raise RuntimeError("Aucun fichier trouvé ou aucun résultat lisible.")

# ==========================================================
# 🧾 Vérification console
# ==========================================================
print("\n--- Fichiers lus ---")
for r in results:
    print(f"{r['fname']:60s}  adv={r['adv']:.3f}  pgdstep={r['pgdstep']:.3f}")

# ==========================================================
# 📊 Préparation graphique
# ==========================================================
results = sorted(results, key=lambda x: (x["pgdstep"], x["adv"]))
unique_steps = sorted(set(r["pgdstep"] for r in results))

plt.figure(figsize=(10, 6))

# Tracer Clean et FGSM (moyennés sur tous les steps)
adv_unique = sorted(set(r["adv"] for r in results))
clean_avg = []
fgsm_avg = []

for adv in adv_unique:
    vals = [r for r in results if r["adv"] == adv]
    clean_avg.append(sum(r["clean"] for r in vals) / len(vals))
    fgsm_avg.append(sum(r["fgsm"] for r in vals) / len(vals))

plt.plot(adv_unique, clean_avg, '^-', color='green', label="Clean Accuracy (moy.)")
plt.plot(adv_unique, fgsm_avg, 's--', color='orange', label="FGSM Attack (moy.)")

# Tracer PGD pour chaque step distinct
first = True
for step in unique_steps:
    subset = [r for r in results if r["pgdstep"] == step]
# Tracer PGD en une seule courbe pour tous les steps
    adv_all = [r["adv"] for r in results]
    pgd_all = [r["pgd"] for r in results]

# Tri par adv pour que la ligne aille de gauche à droite
    adv_all, pgd_all = zip(*sorted(zip(adv_all, pgd_all)))

    if first:
        plt.plot(adv_all, pgd_all, marker='o', linestyle='--', color='blue', label="PGD")
        first = False
    else:
        plt.plot(adv_all, pgd_all, marker='o', linestyle='--', color='blue')

# Affichage des steps au-dessus de chaque point
    switch = 0
    for r in results:
        if switch:
           plt.text(r["adv"], r["pgd"] + 1.5, f"{r['pgdstep']:.3f}",
                    ha="right", va="center", fontsize=12, color="black", rotation=0)
           switch = 0
        else:
             plt.text(r["adv"], r["pgd"] + 0.5, f"{r['pgdstep']:.3f}",
                      ha="left", va="center", fontsize=12, color="black", rotation=0)
             switch = 1

# ==========================================================
# 🎨 Mise en forme du graphique
# ==========================================================
plt.xlabel("Attacker budget (adv)")
plt.ylabel("Accuracy (%)")
plt.title("Accuracy vs Attacker Budget\n(Clean, FGSM et PGD pour différents steps)")
plt.grid(True)
plt.tight_layout()

# ==========================================================
# 🧩 Bloc de gestion de la légende — activer / modifier ici
# ==========================================================
# 🔹 Pour activer la légende → décommente la ligne suivante :
plt.legend(title="Légende")
#

plt.show()
