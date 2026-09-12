# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
# ]
# ///

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell
def _(mo):
    # === CSS (identisch zur AEZ-/Kläranlagen-Familie) ===
    mo.Html("""<style>
    :root {
        --bg:#1a1a2e; --panel:#16213e; --border:#0f3460;
        --accent:#e94560; --ok:#00b894; --warn:#fdcb6e;
        --danger:#e17055; --txt:#dfe6e9; --val:#74b9ff;
    }
    .pls { background:var(--bg); color:var(--txt); padding:12px; border-radius:8px; font-family:'Consolas','Courier New',monospace; }
    .pls-hdr { background:linear-gradient(90deg,var(--panel),var(--border)); padding:10px 20px; border-radius:6px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border:1px solid var(--border); flex-wrap:wrap; gap:8px; }
    .pls-hdr h2 { margin:0; color:#74b9ff; font-size:1.3em; }
    .pls-st { display:flex; gap:15px; align-items:center; font-size:0.85em; flex-wrap:wrap; }
    .pls-dot { width:10px; height:10px; border-radius:50%; display:inline-block; margin-right:4px; animation:pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
    .pls-c { background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:12px; margin-bottom:10px; }
    .pls-c h3 { margin:0 0 8px 0; color:#74b9ff; font-size:1em; border-bottom:1px solid var(--border); padding-bottom:6px; }
    .pls-c h4 { margin:8px 0 4px 0; color:#9fb3c8; font-size:0.9em; }
    .c-v { color:var(--val); } .c-ok { color:var(--ok); } .c-w { color:var(--warn); } .c-d { color:var(--danger); }
    .pls-g2 { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
    .pls-g3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; }
    .pls-bar { height:16px; border-radius:3px; background:#2d3436; overflow:hidden; margin:4px 0; }
    .pls-bar-f { height:100%; border-radius:3px; transition:width 0.5s; }
    .pls-sep { border-top:1px solid var(--border); margin:8px 0; padding-top:8px; }
    .pls-emi { border-collapse:separate; border-spacing:0; font-size:0.9em; width:100%; }
    .pls-emi th { text-align:left; padding:7px 14px; color:#74b9ff; border-bottom:2px solid #0f3460; background:#0f1a30; white-space:nowrap; }
    .pls-emi td { padding:6px 14px; border-bottom:1px solid #0f3460; white-space:nowrap; }
    .pls-emi tr:hover { background:#1e2d4d; }
    .pls-note { color:#8497ab; font-size:0.78em; line-height:1.5; margin-top:6px; }
    </style>""")
    return


@app.cell
def _(mo):
    # === BRENNSTOFF (Müllbunker) ===
    hu = mo.ui.slider(start=7.0, stop=13.0, step=0.1, value=10.0,
                      label="Heizwert Hu [MJ/kg]", show_value=True)
    wasser = mo.ui.slider(start=15, stop=45, step=1, value=28,
                          label="Wassergehalt [%]", show_value=True)
    chlor = mo.ui.slider(start=0.2, stop=1.5, step=0.05, value=0.8,
                         label="Chlorgehalt [%]", show_value=True)
    schwefel = mo.ui.slider(start=0.05, stop=0.50, step=0.01, value=0.20,
                            label="Schwefelgehalt [%]", show_value=True)
    hg_geh = mo.ui.slider(start=0.5, stop=6.0, step=0.1, value=2.0,
                          label="Quecksilbergehalt [mg/kg]", show_value=True)
    asche = mo.ui.slider(start=15, stop=32, step=1, value=22,
                         label="Aschegehalt [%]", show_value=True)
    return asche, chlor, hg_geh, hu, schwefel, wasser


@app.cell
def _(mo):
    # === FEUERUNG ===
    durchsatz = mo.ui.slider(start=10.0, stop=33.2, step=0.4, value=32.0,
                             label="Durchsatz gesamt (2 Linien) [t/h]", show_value=True)
    lam = mo.ui.slider(start=1.3, stop=2.2, step=0.05, value=1.7,
                       label="Luftüberschusszahl λ [-]", show_value=True)
    stuetz = mo.ui.switch(value=False, label="Stützfeuerung (Erdgas) – hält ≥ 850 °C")
    return durchsatz, lam, stuetz


@app.cell
def _(mo):
    # === RAUCHGASREINIGUNG ===
    grob = mo.ui.switch(value=True,
                        label="Grobentstaubung: Elektrofilter vorgeschaltet")
    entstauber = mo.ui.dropdown(
        options=["Elektrofilter (η ≈ 99,5 %)", "Gewebefilter (η ≈ 99,9 %)"],
        value="Gewebefilter (η ≈ 99,9 %)", label="Feinentstaubung")
    sorbens = mo.ui.dropdown(
        options=["Kalkhydrat Ca(OH)₂", "Natriumbicarbonat NaHCO₃"],
        value="Natriumbicarbonat NaHCO₃", label="Sorbens (saure Gase)")
    beta = mo.ui.slider(start=1.0, stop=3.5, step=0.1, value=2.5,
                        label="Stöchiometrieverhältnis β [-]", show_value=True)
    nasswaesche = mo.ui.switch(value=False, label="Nassverfahren (Wäscher statt Trockensorption)")
    entsticker = mo.ui.dropdown(
        options=["SNCR (η ≈ 40–70 %)", "SCR (η ≈ 70–93 %)"],
        value="SCR (η ≈ 70–93 %)", label="Entstickung")
    nh3 = mo.ui.slider(start=0.5, stop=2.0, step=0.05, value=1.1,
                       label="NH₃/NOₓ – molares Verhältnis [-]", show_value=True)
    akoks = mo.ui.slider(start=0.0, stop=3.0, step=0.1, value=2.0,
                         label="Aktivkoks-Dosierung [-]", show_value=True)
    return akoks, beta, entstauber, entsticker, grob, nasswaesche, nh3, sorbens


@app.cell
def _(np):
    # =========================================================================
    #  MVA-MODELL  –  Ursache-Wirkungs-Kette
    #  Müllbunker → Feuerung → Rohgas → Rauchgasreinigung → Reingas
    #  Alle Gaskonzentrationen als Tagesmittelwert-Äquivalent, bezogen auf
    #  11 % O₂, trockenes Abgas, Normzustand (vereinfacht, didaktisch).
    # =========================================================================

    # 17. BImSchV – Tagesmittelwerte (Fassung 2024), bestehende Anlage
    GW = dict(
        Staub=5.0, Cges=10.0, CO=50.0, HCl=8.0, HF=1.0, SO2=40.0,
        NOx=150.0, NH3=10.0, Hg=0.03, PCDDF=0.1, CdTl=0.05, SM=0.5,
    )
    # strengere Neuanlagen-Werte (Hinweis): HCl 6, SO2 30, NOx 100

    def modell(hu, wasser, chlor, schwefel, hg_geh, asche,
               durchsatz, lam, stuetz,
               grob, entstauber, sorbens, beta, nasswaesche, entsticker, nh3, akoks):
        # ---------------- Feuerung ----------------
        # Feuerraumtemperatur: steigt mit Heizwert, sinkt mit Wasser & Luftüberschuss
        T = 1000 + (hu - 10.0) * 100 - (wasser - 28) * 20 - (lam - 1.7) * 150
        if stuetz:
            T = max(T, 870.0)
        T = float(np.clip(T, 600, 1350))
        krit_850 = T >= 850.0

        # Sauerstoff im Abgas aus Luftüberschuss
        o2 = 21.0 * (lam - 1.0) / lam            # Vol-% (trocken, näherungsweise)

        # Verbrennungsgüte g ∈ [0..1]: optimal bei T≥900 und 1.5≤λ≤2.0
        g_T = float(np.clip((T - 780) / 120.0, 0, 1))          # 0 bei 780°C, 1 ab 900°C
        if lam < 1.45:
            g_L = float(np.clip((lam - 1.25) / 0.20, 0, 1))    # Luftmangel
        elif lam > 2.0:
            g_L = float(np.clip((2.3 - lam) / 0.3, 0, 1))      # Auskühlung
        else:
            g_L = 1.0
        g = g_T * g_L

        # ---------------- Rohgas (vor Reinigung) ----------------
        # unvollständige Verbrennung → CO, Cges, Dioxin-Bildung steigen
        CO_roh = 8.0 + (1 - g) * 1600
        Cges_roh = 1.0 + (1 - g) * 70
        # saure Schadgase aus Brennstoffgehalten
        HCl_roh = chlor * 1000.0
        SO2_roh = schwefel * 1500.0
        HF_roh = chlor * 8.0
        Staub_roh = asche * 130.0
        Hg_roh = hg_geh * 0.13
        # NOx: Brennstoff-NOx (≈ konstant) + thermisches NOx (ab ~1100 °C) + O₂-Einfluss
        NOx_roh = (170 + max(0.0, (T - 1100)) * 0.16) * (1 + (o2 - 9.0) * 0.015)
        # PCDD/F: Grundbildung + De-novo bei schlechter Verbrennung
        PCDDF_roh = 2.0 + (1 - g) * 9.0

        # ---------------- Rauchgasreinigung ----------------
        # 1) Entstaubung – zweistufig: Grobentstaubung (E-Filter, früh) + Feinentstaubung
        eta_grob = 0.97 if grob else 0.0          # Grobentstaubung scheidet das Gros der Flugasche ab
        eta_fein = 0.999 if "Gewebe" in entstauber else 0.995
        gewebe = "Gewebe" in entstauber
        eta_staub = 1 - (1 - eta_grob) * (1 - eta_fein)   # Gesamtabscheidung
        # 2) saure Gase: Wirkungsgrad steigt mit β (Sättigung), Bicarbonat etwas besser
        k = 2.4 if "Natrium" in sorbens else 2.0
        eta_hcl = 1 - np.exp(-k * beta)
        eta_so2 = 1 - np.exp(-(k - 0.6) * beta)
        eta_hf = 1 - np.exp(-(k + 0.3) * beta)
        if nasswaesche:
            eta_hcl = max(eta_hcl, 0.997)
            eta_so2 = max(eta_so2, 0.99)
            eta_hf = max(eta_hf, 0.995)
        # 3) Entstickung
        if "SCR" in entsticker:
            eta_nox = min(0.93, 0.85 * nh3)
            nh3_slip = max(0.0, (nh3 - 1.0)) * 4.0 + 1.0
        else:  # SNCR
            eta_nox = min(0.70, 0.58 * nh3)
            nh3_slip = max(0.0, (nh3 - 1.05)) * 13.0 + 2.0
        # 4) Aktivkoks → Hg und PCDD/F; Gewebefilter verbessert die Abscheidung
        bonus = 0.4 if gewebe else 0.0
        eta_hg = 1 - np.exp(-(1.3 + bonus) * akoks)
        eta_pcddf = 1 - np.exp(-(1.6 + bonus) * akoks)

        # ---------------- Reingas (nach Reinigung) ----------------
        Staub_r = Staub_roh * (1 - eta_staub)
        HCl_r = HCl_roh * (1 - eta_hcl)
        SO2_r = SO2_roh * (1 - eta_so2)
        HF_r = HF_roh * (1 - eta_hf)
        NOx_r = NOx_roh * (1 - eta_nox)
        Hg_r = Hg_roh * (1 - eta_hg)
        PCDDF_r = PCDDF_roh * (1 - eta_pcddf)
        CO_r = CO_roh           # durch RGR praktisch unbeeinflusst (Feuerungsgröße)
        Cges_r = Cges_roh
        NH3_r = nh3_slip
        # partikelgebundene Schwermetalle ~ proportional zum Reststaub
        SM_r = Staub_r * 0.012
        CdTl_r = Staub_r * 0.0025

        reingas = dict(Staub=Staub_r, Cges=Cges_r, CO=CO_r, HCl=HCl_r, HF=HF_r,
                       SO2=SO2_r, NOx=NOx_r, NH3=NH3_r, Hg=Hg_r, PCDDF=PCDDF_r,
                       CdTl=CdTl_r, SM=SM_r)
        rohgas = dict(Staub=Staub_roh, Cges=Cges_roh, CO=CO_roh, HCl=HCl_roh,
                      HF=HF_roh, SO2=SO2_roh, NOx=NOx_roh, Hg=Hg_roh, PCDDF=PCDDF_roh)
        eta = dict(staub=eta_staub, grob=eta_grob, fein=eta_fein,
                   hcl=eta_hcl, so2=eta_so2, hf=eta_hf,
                   nox=eta_nox, hg=eta_hg, pcddf=eta_pcddf)

        # ---------------- Energie / Turbine ----------------
        Q_th = durchsatz * 1000.0 * hu / 3600.0      # MW (t/h·MJ/kg → MW)
        P_el = Q_th * 0.13
        P_fw = Q_th * 0.30
        E_el_a = P_el * 8000 / 1000                  # GWh/a
        m_schlacke = durchsatz * 0.25                # t/h
        m_flugstaub = durchsatz * 0.02               # t/h
        V_abgas = durchsatz * 5000.0                 # Nm³/h (≈5000 Nm³/t)

        # Verweilzeit (Nachbrennzone, grob): höher bei niedrigem Durchsatz
        verweilzeit = float(np.clip(2.6 - (durchsatz / 33.2) * 0.7, 1.6, 2.6))

        # ---------------- Betrieb & Kosten (orientierende Richtwerte) ----------------
        # Rohgas-Schadstofffrachten [kg/h] aus Konzentration × Abgasvolumenstrom
        f_hcl = HCl_roh * V_abgas / 1e6
        f_so2 = SO2_roh * V_abgas / 1e6
        wet = bool(nasswaesche)
        if wet:
            # Nasswäsche mit Kalkmilch, nahe stöchiometrisch → Gips (verwertbar)
            sorbens_name = "Kalkmilch"
            sorbens_stoech = f_hcl * 74.0 / (2 * 36.5) + f_so2 * 74.0 / 64.0
            sorbens_kg = sorbens_stoech * 1.05
            sorbens_preis = 0.12
            gips_kg = f_so2 * 172.0 / 64.0          # CaSO4·2H2O, verwertbar
            sorptionsrueck_kg = sorbens_kg * 0.15   # geringer Abschlämm-Reststoff
            abwasser_txt = "abwasserfrei (Eindampfung)"
            hilfs_kw = P_el * 1000 * 0.04 + 350     # Pumpen + Wiederaufheizung
            invest = "hoch"
        else:
            if "Natrium" in sorbens:
                sorbens_name = "NaHCO₃"
                sorbens_stoech = f_hcl * 84.0 / 36.5 + f_so2 * 2 * 84.0 / 64.0
                beta_eff = min(beta, 1.6)           # reaktiver → niedrigere Stöchiometrie
                sorbens_preis = 0.35
            else:
                sorbens_name = "Ca(OH)₂"
                sorbens_stoech = f_hcl * 74.0 / (2 * 36.5) + f_so2 * 74.0 / 64.0
                beta_eff = beta
                sorbens_preis = 0.18
            sorbens_kg = sorbens_stoech * beta_eff
            gips_kg = 0.0
            sorptionsrueck_kg = sorbens_kg * 1.3    # Salze + unreagiertes Sorbens + Reststaub
            abwasser_txt = "keines (trocken)"
            hilfs_kw = P_el * 1000 * 0.015 + 60
            invest = "mittel" if "SCR" in entsticker else "niedrig"
        # Wiederaufheizung für Tail-End-SCR
        if "SCR" in entsticker and not wet:
            hilfs_kw += 250
        # NH₃-/Aktivkoks-Verbrauch
        f_nox_red = max(0.0, (NOx_roh - NOx_r)) * V_abgas / 1e6
        nh3_kg = f_nox_red * (17.0 / 46.0) * nh3
        akoks_kg = akoks * V_abgas / 1e6 * 40.0
        # Reststoffe gesamt [t/a]
        rest_flugasche_a = m_flugstaub * 8000 if grob else 0.0
        rest_sorption_a = sorptionsrueck_kg / 1000 * 8000
        gips_a = gips_kg / 1000 * 8000
        # Betriebskosten [€/h] – orientierend
        k_reag = sorbens_kg * sorbens_preis + nh3_kg * 0.30 + akoks_kg * 0.60
        k_entsorg = (m_flugstaub if grob else 0.0) * 250 + sorptionsrueck_kg / 1000 * 180 - gips_kg / 1000 * 15
        k_energie = hilfs_kw * 0.12
        k_summe = k_reag + k_entsorg + k_energie
        opex_eur_t = k_summe / max(1e-6, durchsatz)
        betrieb = dict(
            sorbens_name=sorbens_name, sorbens_kg=sorbens_kg, sorbens_ta=sorbens_kg * 8,
            nh3_kg=nh3_kg, akoks_kg=akoks_kg,
            rest_flugasche_a=rest_flugasche_a, rest_sorption_a=rest_sorption_a, gips_a=gips_a,
            abwasser_txt=abwasser_txt, hilfs_kw=hilfs_kw, invest=invest, wet=wet,
            k_reag=k_reag, k_entsorg=k_entsorg, k_energie=k_energie,
            opex_eur_t=opex_eur_t,
        )

        # Compliance
        verstoesse = [p for p, v in reingas.items() if v > GW[p] + 1e-9]
        compliant = (len(verstoesse) == 0) and krit_850

        return dict(
            T=T, krit_850=krit_850, o2=o2, g=g, verweilzeit=verweilzeit,
            rohgas=rohgas, reingas=reingas, eta=eta, betrieb=betrieb,
            Q_th=Q_th, P_el=P_el, P_fw=P_fw, E_el_a=E_el_a,
            m_schlacke=m_schlacke, m_flugstaub=m_flugstaub, V_abgas=V_abgas,
            verstoesse=verstoesse, compliant=compliant,
        )
    return GW, modell


@app.cell
def _(GW, akoks, asche, beta, chlor, durchsatz, entstauber, entsticker,
      grob, hg_geh, hu, lam, modell, mo, nasswaesche, nh3, schwefel, sorbens,
      stuetz, wasser):
    c = modell(
        hu.value, wasser.value, chlor.value, schwefel.value, hg_geh.value, asche.value,
        durchsatz.value, lam.value, stuetz.value,
        grob.value, entstauber.value, sorbens.value, beta.value, nasswaesche.value,
        entsticker.value, nh3.value, akoks.value,
    )

    # ---------------- Helfer ----------------
    def vr(label, val, unit, cls="c-v"):
        return (f'<tr><td style="padding:3px 8px 3px 0;color:#b2bec3;white-space:nowrap">{label}</td>'
                f'<td style="padding:3px 0 3px 8px;white-space:nowrap;font-weight:bold" class="{cls}">{val}&ensp;{unit}</td></tr>')

    def vtbl(rows):
        return f'<table style="border-collapse:collapse">{rows}</table>'

    def bar(pct, color="#0984e3"):
        pct = max(0, min(100, pct))
        return f'<div class="pls-bar"><div class="pls-bar-f" style="width:{pct}%;background:{color}"></div></div>'

    def fmt(v):
        return f"{v:.3f}" if v < 1 else (f"{v:.2f}" if v < 10 else f"{v:.0f}")

    # ---------------- Header ----------------
    st_col = "#00b894" if c["compliant"] else "#e17055"
    st_txt = "EINHALTUNG" if c["compliant"] else "ÜBERSCHREITUNG"
    hdr = f'''<div class="pls"><div class="pls-hdr">
        <h2>🔥 Müllverbrennungsanlage – Prozessleitsystem</h2>
        <div class="pls-st">
            <span><span class="pls-dot" style="background:{st_col}"></span> {st_txt}</span>
            <span>Feuerraum: {c["T"]:.0f} °C</span>
            <span>O₂: {c["o2"]:.1f} %</span>
            <span>P_el: {c["P_el"]:.1f} MW</span>
        </div>
    </div></div>'''
    return bar, c, fmt, hdr, mo, vr, vtbl


@app.cell
def _(GW, c, fmt, mo):
    # === VERFAHRENSSCHEMA (Übersicht) ===
    def box(x, y, w, h, stroke, title, *lines):
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#2d3436" stroke="{stroke}" stroke-width="2"/>']
        cx = x + w / 2
        out.append(f'<text x="{cx}" y="{y+18}" fill="{stroke}" text-anchor="middle" font-size="11" font-family="monospace" font-weight="bold">{title}</text>')
        for i, ln in enumerate(lines):
            out.append(f'<text x="{cx}" y="{y+34+i*13}" fill="#dfe6e9" text-anchor="middle" font-size="9" font-family="monospace">{ln}</text>')
        return "".join(out)

    def arr(x1, x2, y):
        return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#5b9bd5" stroke-width="2.5" marker-end="url(#ah)"/>'

    _rg, _rn = c["rohgas"], c["reingas"]
    _t850 = "#00b894" if c["krit_850"] else "#e17055"

    schema = f'''<svg viewBox="0 0 1240 280" xmlns="http://www.w3.org/2000/svg" style="width:100%;min-width:1000px;height:auto;background:#0a1428;border-radius:6px">
      <defs><marker id="ah" markerWidth="9" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,9 3.5,0 7" fill="#5b9bd5"/></marker></defs>
      {box(20, 90, 120, 80, "#6c5ce7", "Müllbunker", "Kran/Mischung", "Aufgabe")}
      {box(170, 90, 130, 80, _t850, "Feuerung/Rost", f"{c['T']:.0f} °C", f"O₂ {c['o2']:.1f} %", f"τ ≈ {c['verweilzeit']:.1f} s")}
      {box(330, 90, 120, 80, "#e17055", "Kessel", "40 bar/400 °C", "Dampf")}
      {box(480, 90, 120, 80, "#dfe6e9", "Entstaubung", f"Staub", f"→ {fmt(_rn['Staub'])}")}
      {box(630, 90, 130, 80, "#fdcb6e", "Saure Gase", f"HCl→{fmt(_rn['HCl'])}", f"SO₂→{fmt(_rn['SO2'])}")}
      {box(790, 90, 120, 80, "#00b894", "Entstickung", f"NOₓ→{fmt(_rn['NOx'])}", "SNCR/SCR")}
      {box(940, 90, 130, 80, "#b2bec3", "Aktivkoks", f"Hg→{fmt(_rn['Hg'])}", f"PCDD/F→{fmt(_rn['PCDDF'])}")}
      {box(1100, 90, 120, 80, "#74b9ff", "Kamin", "Reingas", "kont. Messung")}
      {arr(140, 170, 130)}{arr(300, 330, 130)}{arr(450, 480, 130)}{arr(600, 630, 130)}
      {arr(760, 790, 130)}{arr(910, 940, 130)}{arr(1070, 1100, 130)}
      <text x="235" y="205" fill="{_t850}" text-anchor="middle" font-size="10" font-family="monospace">{'✓ 850 °C / 2 s erfüllt' if c['krit_850'] else '✗ 850-°C-Kriterium verletzt'}</text>
      <text x="620" y="245" fill="#8497ab" text-anchor="middle" font-size="9" font-family="monospace">Rohgas: HCl {fmt(_rg['HCl'])} · SO₂ {fmt(_rg['SO2'])} · NOₓ {fmt(_rg['NOx'])} · Staub {fmt(_rg['Staub'])} · CO {fmt(_rg['CO'])}  (mg/m³)</text>
    </svg>'''

    n_ok = sum(1 for p, v in c["reingas"].items() if v <= GW[p])
    ampel_col = "#00b894" if c["compliant"] else "#e17055"
    uebersicht = mo.Html(f'''<div class="pls">
      <div class="pls-c" style="overflow-x:auto"><h3>Verfahrenskette (Live-Betriebspunkt)</h3>{schema}</div>
      <div class="pls-c" style="border-color:{ampel_col}">
        <h3 style="color:{ampel_col}">{'✅ Anlage hält alle Grenzwerte ein' if c['compliant'] else '⚠️ Grenzwertüberschreitung'}</h3>
        <p style="font-size:0.9em;margin:4px 0">{n_ok} von {len(GW)} Reingas-Parametern im Grenzwert{'' if c['krit_850'] else ' · zusätzlich: 850-°C-Kriterium verletzt'}.
        {'' if c['compliant'] else ' Betroffen: ' + ', '.join(c['verstoesse'])}</p>
      </div>
    </div>''')
    return (uebersicht,)


@app.cell
def _(asche, c, chlor, fmt, hg_geh, hu, mo, schwefel, vr, vtbl, wasser):
    # === MÜLLBUNKER ===
    _rg = c["rohgas"]
    bunker = mo.vstack([
        mo.Html('<div class="pls"><div class="pls-c"><h3>🗑 Müllbunker – Brennstoffeigenschaften</h3>'
                '<p style="font-size:0.88em;color:#b2bec3;margin:2px 0">Über den Greiferkran wird der Müll gemischt und homogenisiert. '
                'Zusammensetzung und Heizwert bestimmen Verbrennung und Rohgasfrachten.</p></div></div>'),
        mo.hstack([hu, wasser, asche], justify="start", gap=1, wrap=True),
        mo.hstack([chlor, schwefel, hg_geh], justify="start", gap=1, wrap=True),
        mo.Html(f'''<div class="pls"><div class="pls-g2">
          <div class="pls-c"><h3>📥 Brennstoff</h3>{vtbl(
              vr("Heizwert Hu", f"{hu.value:.1f}", "MJ/kg")
              + vr("Wassergehalt", f"{wasser.value:.0f}", "%")
              + vr("Aschegehalt", f"{asche.value:.0f}", "%")
              + vr("Chlorgehalt", f"{chlor.value:.2f}", "%")
              + vr("Schwefelgehalt", f"{schwefel.value:.2f}", "%")
              + vr("Quecksilber", f"{hg_geh.value:.1f}", "mg/kg")
          )}</div>
          <div class="pls-c"><h3>🌫 Resultierende Rohgasfracht</h3>{vtbl(
              vr("HCl (aus Cl)", f"{fmt(_rg['HCl'])}", "mg/m³", "c-w")
              + vr("SO₂ (aus S)", f"{fmt(_rg['SO2'])}", "mg/m³", "c-w")
              + vr("Staub (aus Asche)", f"{fmt(_rg['Staub'])}", "mg/m³", "c-w")
              + vr("Hg (aus Brennstoff)", f"{fmt(_rg['Hg'])}", "mg/m³", "c-w")
              + vr("Abgasvolumenstrom", f"{c['V_abgas']:,.0f}", "Nm³/h")
          )}
          <p class="pls-note">Höherer Cl-/S-/Aschegehalt erhöht direkt die Rohgasfracht – die Reinigung muss entsprechend mehr leisten.</p>
          </div>
        </div></div>'''),
    ])
    return (bunker,)


@app.cell
def _(bar, c, durchsatz, lam, mo, stuetz, vr, vtbl):
    # === FEUERUNG & KESSEL ===
    _t850 = "c-ok" if c["krit_850"] else "c-d"
    _gcol = "#00b894" if c["g"] > 0.85 else ("#fdcb6e" if c["g"] > 0.5 else "#e17055")
    _rg = c["rohgas"]

    def _feuerraum_svg():
        _T = c["T"]; _o2 = c["o2"]; _CO = c["rohgas"]["CO"]
        _krit = c["krit_850"]; _msl = c["m_schlacke"]; _lam = lam.value
        if _T >= 950:
            _fo, _fi = "#ff7b00", "#ffd24d"
        elif _T >= 850:
            _fo, _fi = "#e8590c", "#ff9d3d"
        else:
            _fo, _fi = "#922b21", "#c0392b"
        _band = "#00b894" if _krit else "#e17055"
        p = []
        p.append('<svg viewBox="0 0 880 480" xmlns="http://www.w3.org/2000/svg" style="width:100%;min-width:820px;height:auto;background:#0a1428;border-radius:6px">')
        p.append('<defs>')
        p.append('<linearGradient id="fr_bed" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a3825"/><stop offset="0.45" stop-color="#e8590c"/><stop offset="0.75" stop-color="#ffb24d"/><stop offset="1" stop-color="#b5651d"/></linearGradient>')
        p.append(f'<linearGradient id="fr_flame" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{_fo}"/><stop offset="1" stop-color="{_fi}"/></linearGradient>')
        p.append('<marker id="fr_air" markerWidth="8" markerHeight="8" refX="4" refY="7" orient="auto"><polygon points="0 7,4 0,8 7" fill="#4aa3df"/></marker>')
        p.append('<marker id="fr_gas" markerWidth="9" markerHeight="9" refX="4.5" refY="8" orient="auto"><polygon points="0 8,4.5 0,9 8" fill="#8497ab"/></marker>')
        p.append('</defs>')
        p.append('<path d="M170,80 L625,80 L625,405 L600,405 L170,350 Z" fill="#241a18" stroke="#6b4a3a" stroke-width="6"/>')
        p.append('<polygon points="40,20 150,20 125,70 65,70" fill="#2d3436" stroke="#6c5ce7" stroke-width="2"/>')
        p.append('<rect x="65" y="70" width="60" height="262" fill="#3a2c20" stroke="#6c5ce7" stroke-width="2"/>')
        p.append('<rect x="69" y="120" width="52" height="210" fill="#4a3826"/>')
        p.append('<text x="95" y="14" fill="#a29bfe" text-anchor="middle" font-size="11" font-family="monospace">Müllaufgabe</text>')
        p.append('<polygon points="170,335 600,400 600,414 170,349" fill="#3d4044" stroke="#8a9099" stroke-width="1.5"/>')
        for _i in range(1, 13):
            _fx = 170 + _i * (600 - 170) / 13
            _fy = 335 + _i * (400 - 335) / 13
            p.append(f'<line x1="{_fx:.0f}" y1="{_fy:.0f}" x2="{_fx:.0f}" y2="{_fy+13:.0f}" stroke="#5a6068" stroke-width="2"/>')
        p.append('<polygon points="170,312 600,388 600,400 170,335" fill="url(#fr_bed)"/>')
        for _fx in (300, 350, 400, 450):
            p.append(f'<path d="M{_fx},355 C{_fx-18},290 {_fx+14},250 {_fx},195 C{_fx-12},250 {_fx+20},300 {_fx},355 Z" fill="url(#fr_flame)" opacity="0.92"/>')
        p.append(f'<rect x="195" y="110" width="410" height="34" fill="{_band}" opacity="0.13" stroke="{_band}" stroke-width="1.5" stroke-dasharray="7,5"/>')
        p.append(f'<text x="400" y="131" fill="{_band}" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold">≥ 850 °C / 2 s — {"erfüllt" if _krit else "VERLETZT"}</text>')
        p.append(f'<text x="400" y="176" fill="{_fi}" text-anchor="middle" font-size="22" font-family="monospace" font-weight="bold">{_T:.0f} °C</text>')
        p.append('<text x="400" y="194" fill="#8497ab" text-anchor="middle" font-size="10" font-family="monospace">Feuerraum / Nachbrennzone</text>')
        for _k in range(4):
            _x0 = 175 + _k * 107
            _cx = _x0 + 45
            _gy = 335 + (_cx - 170) / (600 - 170) * (400 - 335)
            p.append(f'<rect x="{_x0}" y="{_gy+22:.0f}" width="90" height="40" fill="#16263a" stroke="#0f3460" stroke-width="1.5"/>')
            p.append(f'<line x1="{_cx}" y1="{_gy+58:.0f}" x2="{_cx}" y2="{_gy+8:.0f}" stroke="#4aa3df" stroke-width="2.5" marker-end="url(#fr_air)"/>')
        p.append(f'<text x="400" y="460" fill="#4aa3df" text-anchor="middle" font-size="11" font-family="monospace">Primärluft (Unterwind)  ·  λ = {_lam:.2f}</text>')
        for _yy in (215, 245):
            p.append(f'<line x1="133" y1="{_yy}" x2="172" y2="{_yy}" stroke="#4aa3df" stroke-width="2.5" marker-end="url(#fr_air)"/>')
            p.append(f'<line x1="705" y1="{_yy}" x2="623" y2="{_yy}" stroke="#4aa3df" stroke-width="2.5" marker-end="url(#fr_air)"/>')
        p.append('<text x="735" y="218" fill="#4aa3df" text-anchor="start" font-size="11" font-family="monospace">Sekundär-</text>')
        p.append('<text x="735" y="232" fill="#4aa3df" text-anchor="start" font-size="11" font-family="monospace">luft</text>')
        p.append('<rect x="450" y="20" width="110" height="62" fill="#1a2238" stroke="#8497ab" stroke-width="2"/>')
        p.append('<line x1="505" y1="80" x2="505" y2="26" stroke="#8497ab" stroke-width="3" marker-end="url(#fr_gas)"/>')
        p.append('<text x="505" y="15" fill="#8497ab" text-anchor="middle" font-size="11" font-family="monospace">→ Kessel (1. Zug)</text>')
        p.append(f'<text x="640" y="48" fill="#74b9ff" text-anchor="start" font-size="12" font-family="monospace" font-weight="bold">O₂ {_o2:.1f} %</text>')
        _cocol = "#00b894" if _CO < 50 else "#e17055"
        p.append(f'<text x="640" y="68" fill="{_cocol}" text-anchor="start" font-size="12" font-family="monospace" font-weight="bold">CO {_CO:.0f} mg/m³</text>')
        p.append('<path d="M600,400 L600,455 L685,455 L685,420 Z" fill="#16263a" stroke="#8a9099" stroke-width="2"/>')
        p.append('<path d="M604,432 q10,-6 20,0 t20,0 t20,0 t16,0" fill="none" stroke="#4aa3df" stroke-width="1.5"/>')
        p.append(f'<text x="642" y="475" fill="#dfe6e9" text-anchor="middle" font-size="11" font-family="monospace">Schlacke {_msl:.1f} t/h</text>')
        _zones = [("Trocknung", "~100–300 °C"), ("Zündung", "~300–600 °C"),
                  ("Hauptverbr.", "~900–1100 °C"), ("Ausbrand", "~600–800 °C")]
        for _k, (_nm, _rng) in enumerate(_zones):
            _cx = 175 + _k * 107 + 45
            p.append(f'<text x="{_cx}" y="430" fill="#9fb3c8" text-anchor="middle" font-size="9.5" font-family="monospace">{_nm}</text>')
            p.append(f'<text x="{_cx}" y="442" fill="#6b7d91" text-anchor="middle" font-size="8.5" font-family="monospace">{_rng}</text>')
        p.append('</svg>')
        return "".join(p)

    feuerung = mo.vstack([
        mo.Html('<div class="pls"><div class="pls-c"><h3>🔥 Feuerung & Kessel</h3>'
                '<p style="font-size:0.88em;color:#b2bec3;margin:2px 0">Auf dem Rost verbrennt der Müll bei über 850 °C. '
                'Die 17. BImSchV verlangt mind. 850 °C über ≥ 2 s nach der letzten Verbrennungsluftzufuhr – '
                'sonst steigen CO, organischer Kohlenstoff und das Dioxin-Risiko.</p></div></div>'),
        mo.hstack([durchsatz, lam], justify="start", gap=1, wrap=True),
        mo.hstack([stuetz], justify="start"),
        mo.Html(f'<div class="pls"><div class="pls-c" style="overflow-x:auto"><h3>Feuerraum-Querschnitt (Live-Betriebspunkt)</h3>{_feuerraum_svg()}</div></div>'),
        mo.Html(f'''<div class="pls"><div class="pls-g3">
          <div class="pls-c"><h3>🌡 Feuerraum</h3>{vtbl(
              vr("Temperatur", f"{c['T']:.0f}", "°C", _t850)
              + vr("850-°C-Kriterium", "erfüllt" if c['krit_850'] else "verletzt", "", _t850)
              + vr("Verweilzeit τ", f"{c['verweilzeit']:.1f}", "s", "c-ok" if c['verweilzeit']>=2 else "c-w")
              + vr("O₂ im Abgas", f"{c['o2']:.1f}", "%")
              + vr("λ", f"{lam.value:.2f}", "-")
          )}</div>
          <div class="pls-c"><h3>✅ Verbrennungsgüte</h3>{vtbl(vr("Güte", f"{c['g']*100:.0f}", "%"))}
            {bar(c['g']*100, _gcol)}
            {vtbl(
              vr("CO (Rohgas)", f"{_rg['CO']:.0f}", "mg/m³", "c-ok" if _rg['CO']<50 else "c-d")
              + vr("Cges (Rohgas)", f"{_rg['Cges']:.1f}", "mg/m³", "c-ok" if _rg['Cges']<10 else "c-d")
              + vr("NOₓ (Rohgas)", f"{_rg['NOx']:.0f}", "mg/m³")
            )}
            <p class="pls-note">Luftmangel (λ&lt;1,45) oder Auskühlung (λ&gt;2,0 / T&lt;850 °C) verschlechtern die Güte → CO und Cges steigen stark.</p>
          </div>
          <div class="pls-c"><h3>⚙️ Reststoffe & Kessel</h3>{vtbl(
              vr("Schlacke", f"{c['m_schlacke']:.1f}", "t/h")
              + vr("Kessel-Flugstaub", f"{c['m_flugstaub']:.2f}", "t/h")
              + vr("Dampf 40 bar/400 °C", "→ Turbine", "")
              + vr("therm. Leistung", f"{c['Q_th']:.0f}", "MW")
          )}</div>
        </div></div>'''),
    ])
    return (feuerung,)


@app.cell
def _(akoks, beta, c, entstauber, entsticker, grob, mo, nasswaesche, nh3,
      sorbens, vr, vtbl):
    # === RAUCHGASREINIGUNG ===
    _e = c["eta"]
    _rg, _rn = c["rohgas"], c["reingas"]

    def _stufe(titel, beschr, eff_rows):
        return (f'<div class="pls-c"><h3>{titel}</h3>'
                f'<p style="font-size:0.83em;color:#b2bec3;margin:2px 0 6px 0">{beschr}</p>'
                f'{vtbl(eff_rows)}</div>')

    def _rgr_svg():
        import math
        _grob = grob.value
        _gewebe = "Gewebe" in entstauber.value
        _scr = "SCR" in entsticker.value
        _comp = c["compliant"]
        _fs = c["m_flugstaub"]

        def _ok(v, lim):
            return "#00b894" if v <= lim else "#e17055"

        p = []
        p.append('<svg viewBox="0 0 1280 380" xmlns="http://www.w3.org/2000/svg" style="width:100%;min-width:1120px;height:auto;background:#0a1428;border-radius:6px">')
        p.append('<defs>')
        p.append('<marker id="rgr_g" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><polygon points="0 0,9 4.5,0 9" fill="#8497ab"/></marker>')
        p.append('<marker id="rgr_d" markerWidth="8" markerHeight="8" refX="4" refY="7" orient="auto"><polygon points="0 0,8 0,4 7" fill="#a29bfe"/></marker>')
        p.append('</defs>')
        # Rauchgasweg mit Farbverlauf schmutzig → sauber
        for _x0, _x1, _col in [(70, 92, "#7a6038"), (212, 272, "#6b5a3a"), (382, 472, "#5d6a52"), (622, 682, "#3a6a88"), (802, 935, "#3a6a88")]:
            p.append(f'<rect x="{_x0}" y="104" width="{_x1-_x0}" height="32" fill="{_col}" opacity="0.55"/>')
        p.append('<line x1="70" y1="120" x2="838" y2="120" stroke="#8497ab" stroke-width="2"/>')
        p.append('<line x1="900" y1="120" x2="935" y2="120" stroke="#8497ab" stroke-width="2"/>')
        for _xx in (90, 270, 470, 680, 933):
            p.append(f'<line x1="{_xx-14}" y1="120" x2="{_xx}" y2="120" stroke="#8497ab" stroke-width="2" marker-end="url(#rgr_g)"/>')
        # Rohgas-Eintritt
        p.append('<text x="40" y="96" fill="#8497ab" text-anchor="middle" font-size="11" font-family="monospace">Rohgas</text>')
        p.append('<text x="40" y="112" fill="#6b7d91" text-anchor="middle" font-size="9" font-family="monospace">v. Kessel</text>')
        if not _scr:
            p.append('<text x="40" y="150" fill="#00b894" text-anchor="middle" font-size="8.5" font-family="monospace">NOₓ: SNCR</text>')
            p.append('<text x="40" y="161" fill="#6b7d91" text-anchor="middle" font-size="8" font-family="monospace">im Feuerraum</text>')
        # 1) Grobentstaubung (Elektrofilter, früh)
        if _grob:
            p.append('<rect x="90" y="60" width="120" height="118" rx="5" fill="#16263a" stroke="#74b9ff" stroke-width="2"/>')
            for _px in range(102, 205, 14):
                p.append(f'<line x1="{_px}" y1="70" x2="{_px}" y2="150" stroke="#3a5a7d" stroke-width="3"/>')
            p.append('<text x="150" y="52" fill="#74b9ff" text-anchor="middle" font-size="11" font-family="monospace" font-weight="bold">Grobentstaubung</text>')
            p.append('<text x="150" y="171" fill="#6b7d91" text-anchor="middle" font-size="8.5" font-family="monospace">Elektrofilter</text>')
            p.append('<polygon points="90,178 210,178 165,210 135,210" fill="#16263a" stroke="#74b9ff" stroke-width="1.5"/>')
            p.append('<line x1="150" y1="210" x2="150" y2="238" stroke="#8497ab" stroke-width="2" marker-end="url(#rgr_g)"/>')
            p.append(f'<text x="150" y="252" fill="#8497ab" text-anchor="middle" font-size="9" font-family="monospace">Flugasche {_fs:.2f} t/h → Salzbergwerk</text>')
        else:
            p.append('<rect x="90" y="60" width="120" height="118" rx="5" fill="none" stroke="#6b7d91" stroke-width="1.5" stroke-dasharray="6,5"/>')
            p.append('<text x="150" y="115" fill="#fdcb6e" text-anchor="middle" font-size="10" font-family="monospace">ohne Grob-</text>')
            p.append('<text x="150" y="130" fill="#fdcb6e" text-anchor="middle" font-size="10" font-family="monospace">entstaubung</text>')
        # 2) Sorptionsreaktor + Aktivkoks
        p.append('<rect x="272" y="58" width="110" height="120" rx="5" fill="#16263a" stroke="#fdcb6e" stroke-width="2"/>')
        p.append('<text x="327" y="50" fill="#fdcb6e" text-anchor="middle" font-size="11" font-family="monospace" font-weight="bold">Sorptionsreaktor</text>')
        p.append('<polygon points="300,18 354,18 344,40 310,40" fill="#2d3436" stroke="#fdcb6e" stroke-width="1.5"/>')
        p.append(f'<text x="327" y="34" fill="#ffeaa7" text-anchor="middle" font-size="8" font-family="monospace">{"NaHCO₃" if "Natrium" in sorbens.value else "Ca(OH)₂"}</text>')
        p.append('<line x1="327" y1="40" x2="327" y2="58" stroke="#fdcb6e" stroke-width="2" marker-end="url(#rgr_d)"/>')
        if nasswaesche.value:
            p.append('<text x="327" y="174" fill="#74b9ff" text-anchor="middle" font-size="8" font-family="monospace">+ Nasswäsche</text>')
        # Aktivkoks-Eindüsung in den Kanal (vor dem Feinfilter)
        p.append('<polygon points="412,44 468,44 458,68 422,68" fill="#2d3436" stroke="#b2bec3" stroke-width="1.5"/>')
        p.append('<text x="440" y="38" fill="#dfe6e9" text-anchor="middle" font-size="9.5" font-family="monospace">Aktivkoks</text>')
        p.append('<line x1="440" y1="68" x2="440" y2="104" stroke="#b2bec3" stroke-width="2" marker-end="url(#rgr_d)"/>')
        # 3) Feinentstaubung
        p.append('<rect x="472" y="58" width="150" height="120" rx="5" fill="#16263a" stroke="#00cec9" stroke-width="2"/>')
        if _gewebe:
            p.append('<text x="547" y="50" fill="#00cec9" text-anchor="middle" font-size="11" font-family="monospace" font-weight="bold">Feinentstaubung</text>')
            p.append('<text x="547" y="171" fill="#6b7d91" text-anchor="middle" font-size="8.5" font-family="monospace">Gewebefilter</text>')
            for _bx in range(486, 610, 18):
                p.append(f'<rect x="{_bx}" y="70" width="11" height="74" rx="5" fill="#22344d" stroke="#3a5a7d" stroke-width="1"/>')
        else:
            p.append('<text x="547" y="50" fill="#00cec9" text-anchor="middle" font-size="11" font-family="monospace" font-weight="bold">Feinentstaubung</text>')
            p.append('<text x="547" y="171" fill="#6b7d91" text-anchor="middle" font-size="8.5" font-family="monospace">Elektrofilter</text>')
            for _px in range(486, 610, 15):
                p.append(f'<line x1="{_px}" y1="70" x2="{_px}" y2="150" stroke="#3a5a7d" stroke-width="3"/>')
        p.append('<polygon points="472,178 622,178 575,210 519,210" fill="#16263a" stroke="#00cec9" stroke-width="1.5"/>')
        p.append('<line x1="547" y1="210" x2="547" y2="238" stroke="#8497ab" stroke-width="2" marker-end="url(#rgr_g)"/>')
        p.append('<text x="547" y="252" fill="#8497ab" text-anchor="middle" font-size="9" font-family="monospace">Sorptionsrückstand → Verwertung</text>')
        # 4) Entstickung (Tail-End-SCR) bzw. SNCR-Hinweis
        if _scr:
            p.append('<rect x="682" y="62" width="120" height="116" rx="4" fill="#16263a" stroke="#00b894" stroke-width="2"/>')
            for _gx in range(690, 800, 12):
                p.append(f'<line x1="{_gx}" y1="68" x2="{_gx}" y2="172" stroke="#0f3a30" stroke-width="1"/>')
            for _gy in range(72, 175, 12):
                p.append(f'<line x1="688" y1="{_gy}" x2="800" y2="{_gy}" stroke="#0f3a30" stroke-width="1"/>')
            p.append('<text x="742" y="54" fill="#00b894" text-anchor="middle" font-size="11" font-family="monospace" font-weight="bold">Entstickung (SCR)</text>')
            p.append('<rect x="717" y="26" width="50" height="22" fill="#2d3436" stroke="#a29bfe" stroke-width="1.5"/>')
            p.append('<text x="742" y="41" fill="#a29bfe" text-anchor="middle" font-size="9" font-family="monospace">NH₃</text>')
            p.append('<line x1="742" y1="48" x2="742" y2="62" stroke="#a29bfe" stroke-width="2" marker-end="url(#rgr_d)"/>')
        else:
            p.append('<rect x="682" y="62" width="120" height="116" rx="4" fill="none" stroke="#6b7d91" stroke-width="1.5" stroke-dasharray="6,5"/>')
            p.append('<text x="742" y="54" fill="#00b894" text-anchor="middle" font-size="11" font-family="monospace" font-weight="bold">Entstickung</text>')
            p.append('<text x="742" y="116" fill="#6b7d91" text-anchor="middle" font-size="9" font-family="monospace">SNCR bereits</text>')
            p.append('<text x="742" y="130" fill="#6b7d91" text-anchor="middle" font-size="9" font-family="monospace">im Feuerraum</text>')
        # 5) Saugzug + Kamin
        p.append('<circle cx="870" cy="120" r="22" fill="#16263a" stroke="#8497ab" stroke-width="2"/>')
        for _ang in (0, 72, 144, 216, 288):
            _a = math.radians(_ang)
            p.append(f'<line x1="870" y1="120" x2="{870+16*math.cos(_a):.0f}" y2="{120+16*math.sin(_a):.0f}" stroke="#8497ab" stroke-width="2"/>')
        p.append('<text x="870" y="158" fill="#8497ab" text-anchor="middle" font-size="9" font-family="monospace">Saugzug</text>')
        _kcol = "#00b894" if _comp else "#e17055"
        p.append(f'<rect x="940" y="30" width="46" height="108" fill="#1a2238" stroke="{_kcol}" stroke-width="2.5"/>')
        p.append(f'<rect x="940" y="30" width="46" height="10" fill="{_kcol}"/>')
        p.append('<line x1="963" y1="30" x2="963" y2="8" stroke="#4aa3df" stroke-width="3" marker-end="url(#rgr_g)"/>')
        p.append('<text x="963" y="158" fill="#dfe6e9" text-anchor="middle" font-size="10" font-family="monospace">Kamin</text>')
        p.append(f'<text x="963" y="172" fill="{_kcol}" text-anchor="middle" font-size="8.5" font-family="monospace">kont. Messung</text>')
        p.append(f'<text x="1270" y="56" fill="{_kcol}" text-anchor="end" font-size="12" font-family="monospace" font-weight="bold">{"Reingas i.O." if _comp else "Überschreitung"}</text>')
        p.append('<text x="1270" y="72" fill="#6b7d91" text-anchor="end" font-size="8.5" font-family="monospace">bezogen auf 11 % O₂</text>')

        # Wertekarten direkt unter den Aggregaten
        def _card(cx, w, title, lines):
            _x0 = cx - w / 2
            out = [f'<rect x="{_x0:.0f}" y="270" width="{w}" height="{18+len(lines)*17}" rx="5" fill="#16213e" stroke="#0f3460" stroke-width="1.5"/>']
            out.append(f'<text x="{cx}" y="288" fill="#74b9ff" text-anchor="middle" font-size="10" font-family="monospace" font-weight="bold">{title}</text>')
            for _i, (_lab, _val, _col) in enumerate(lines):
                out.append(f'<text x="{_x0+10:.0f}" y="{306+_i*17}" fill="#9fb3c8" text-anchor="start" font-size="9.5" font-family="monospace">{_lab}</text>')
                out.append(f'<text x="{_x0+w-10:.0f}" y="{306+_i*17}" fill="{_col}" text-anchor="end" font-size="9.5" font-family="monospace" font-weight="bold">{_val}</text>')
            return "".join(out)

        if _grob:
            _grob_lines = [("η grob", f"{_e['grob']*100:.0f} %", "#00b894"),
                           ("Flugasche", f"{_fs:.2f} t/h", "#9fb3c8")]
        else:
            _grob_lines = [("Status", "umgangen", "#fdcb6e"),
                           ("Staublast", "→ Feinfilter", "#9fb3c8")]
        p.append(_card(150, 150, "Grobentstaubung", _grob_lines))
        p.append(_card(330, 160, "Saure Gase", [
            ("η HCl", f"{_e['hcl']*100:.1f} %", "#00b894"),
            ("HCl", f"{_rn['HCl']:.1f} mg/m³", _ok(_rn['HCl'], 8)),
            ("SO₂", f"{_rn['SO2']:.1f} mg/m³", _ok(_rn['SO2'], 40)),
        ]))
        p.append(_card(547, 180, "Feinfilter + Aktivkoks", [
            ("η Staub (ges.)", f"{_e['staub']*100:.2f} %", "#00b894"),
            ("Staub", f"{_rn['Staub']:.2f} mg/m³", _ok(_rn['Staub'], 5)),
            ("Hg", f"{_rn['Hg']:.3f} mg/m³", _ok(_rn['Hg'], 0.03)),
            ("PCDD/F", f"{_rn['PCDDF']:.3f} ng/m³", _ok(_rn['PCDDF'], 0.1)),
        ]))
        p.append(_card(742, 160, "Entstickung", [
            ("η NOₓ", f"{_e['nox']*100:.0f} %", "#00b894"),
            ("NOₓ", f"{_rn['NOx']:.0f} mg/m³", _ok(_rn['NOx'], 150)),
            ("NH₃-Schlupf", f"{_rn['NH3']:.1f} mg/m³", _ok(_rn['NH3'], 10)),
        ]))
        p.append('</svg>')
        return "".join(p)

    rgr = mo.vstack([
        mo.Html('<div class="pls"><div class="pls-c"><h3>🌫 Rauchgasreinigung – mehrstufig</h3>'
                '<p style="font-size:0.88em;color:#b2bec3;margin:2px 0">Reihenfolge: frühe Grobentstaubung (Elektrofilter) → Sorption der sauren Gase + Aktivkoks → '
                'Feinentstaubung (Gewebefilter) → Entstickung. NOₓ wird je nach Konzept im Feuerraum (SNCR) oder am Kettenende (SCR) gemindert. '
                'Schalter und Auswahlfelder verändern Aggregate und Reingaswerte live.</p></div></div>'),
        mo.hstack([grob, entstauber, sorbens], justify="start", gap=1, wrap=True),
        mo.hstack([beta, nh3, akoks], justify="start", gap=1, wrap=True),
        mo.hstack([entsticker, nasswaesche], justify="start", gap=1, wrap=True),
        mo.Html(f'<div class="pls"><div class="pls-c" style="overflow-x:auto"><h3>Räumliche Anordnung der Aggregate (Live-Werte)</h3>{_rgr_svg()}</div></div>'),
        mo.Html(f'''<div class="pls"><div class="pls-g2">
          {_stufe("1️⃣ Grobentstaubung (Elektrofilter)", "Früh nach dem Kessel – scheidet das Gros der Flugasche ab; diese geht separat ins Salzbergwerk und entlastet die nachfolgenden Stufen." + ("" if grob.value else " Derzeit umgangen – die volle Staublast trifft den Feinfilter."),
                 vr("Abscheidegrad", f"{_e['grob']*100:.0f}", "%", "c-ok" if grob.value else "c-w")
                 + vr("Status", "aktiv" if grob.value else "umgangen", "", "c-ok" if grob.value else "c-w")
                 + vr("Flugasche", f"{c['m_flugstaub']:.2f}", "t/h"))}
          {_stufe("2️⃣ Saure Gase", f"Sorption mit {sorbens.value} bei β = {beta.value:.1f}{' + Nasswäsche' if nasswaesche.value else ''}.",
                 vr("η HCl", f"{_e['hcl']*100:.1f}", "%", "c-ok")
                 + vr("η SO₂", f"{_e['so2']*100:.1f}", "%", "c-ok")
                 + vr("HCl Reingas", f"{_rn['HCl']:.2f}", "mg/m³", "c-ok" if _rn['HCl']<=8 else "c-d")
                 + vr("SO₂ Reingas", f"{_rn['SO2']:.2f}", "mg/m³", "c-ok" if _rn['SO2']<=40 else "c-d"))}
          {_stufe("3️⃣ Feinentstaubung", f"{entstauber.value} – scheidet Reststaub, Sorptionsprodukte und beladenen Aktivkoks als Filterkuchen ab.",
                 vr("Abscheidegrad (fein)", f"{_e['fein']*100:.2f}", "%", "c-ok")
                 + vr("Staub Rohgas", f"{_rg['Staub']:.0f}", "mg/m³")
                 + vr("Staub Reingas (ges.)", f"{_rn['Staub']:.2f}", "mg/m³", "c-ok" if _rn['Staub']<=5 else "c-d"))}
          {_stufe("4️⃣ Entstickung", f"{entsticker.value} – NH₃-Eindüsung reduziert NOₓ. Überdosierung → NH₃-Schlupf.",
                 vr("η NOₓ", f"{_e['nox']*100:.1f}", "%", "c-ok")
                 + vr("NOₓ Reingas", f"{_rn['NOx']:.1f}", "mg/m³", "c-ok" if _rn['NOx']<=150 else "c-d")
                 + vr("NH₃-Schlupf", f"{_rn['NH3']:.1f}", "mg/m³", "c-ok" if _rn['NH3']<=10 else "c-d"))}
          {_stufe("5️⃣ Aktivkoks (Adsorption)", "Eindüsung vor dem Feinfilter – bindet Quecksilber und Dioxine/Furane (PCDD/F), abgeschieden am Filterkuchen.",
                 vr("η Hg", f"{_e['hg']*100:.1f}", "%", "c-ok")
                 + vr("η PCDD/F", f"{_e['pcddf']*100:.1f}", "%", "c-ok")
                 + vr("Hg Reingas", f"{_rn['Hg']:.4f}", "mg/m³", "c-ok" if _rn['Hg']<=0.03 else "c-d")
                 + vr("PCDD/F Reingas", f"{_rn['PCDDF']:.4f}", "ng/m³", "c-ok" if _rn['PCDDF']<=0.1 else "c-d"))}
        </div></div>'''),
    ])
    return (rgr,)


@app.cell
def _(GW, c, mo):
    # === EMISSIONEN – 17. BImSchV ===
    namen = dict(Staub="Gesamtstaub", Cges="Org. Stoffe (Cges)", CO="Kohlenmonoxid CO",
                 HCl="Chlorwasserstoff HCl", HF="Fluorwasserstoff HF", SO2="Schwefeldioxid SO₂",
                 NOx="Stickoxide NOₓ (als NO₂)", NH3="Ammoniak NH₃ (Schlupf)",
                 Hg="Quecksilber Hg", PCDDF="Dioxine/Furane (PCDD/F)",
                 CdTl="Σ Cd + Tl", SM="Σ Schwermetalle")
    einheit = dict(PCDDF="ng/m³")  # Rest mg/m³

    rows = ""
    for p in ["Staub", "Cges", "CO", "HCl", "HF", "SO2", "NOx", "NH3", "Hg", "PCDDF", "CdTl", "SM"]:
        v = c["reingas"][p]
        gw = GW[p]
        u = einheit.get(p, "mg/m³")
        ratio = v / gw * 100
        col = "#00b894" if v <= gw else "#e17055"
        amp = "●" if v <= gw else "▲"
        nk = 4 if gw < 0.2 else (3 if gw < 5 else (1 if gw < 60 else 0))
        roh = c["rohgas"].get(p)
        roh_s = f"{roh:.0f}" if (roh is not None and roh >= 10) else (f"{roh:.2f}" if roh is not None else "–")
        rows += (f'<tr><td>{namen[p]}</td>'
                 f'<td style="color:#8497ab">{roh_s}</td>'
                 f'<td style="font-weight:bold;color:{col}">{v:.{nk}f}</td>'
                 f'<td>{gw:g}</td><td>{u}</td>'
                 f'<td style="color:{col}">{ratio:.0f} %</td>'
                 f'<td style="color:{col};font-weight:bold">{amp}</td></tr>')

    head = "#00b894" if c["compliant"] else "#e17055"
    emissionen = mo.Html(f'''<div class="pls">
      <div class="pls-c" style="border-color:{head}">
        <h3 style="color:{head}">📋 Reingas im Vergleich zur 17. BImSchV {'– alle Werte eingehalten' if c['compliant'] else '– Überschreitung'}</h3>
        <table class="pls-emi">
          <tr><th>Parameter</th><th>Rohgas</th><th>Reingas</th><th>Grenzwert</th><th>Einheit</th><th>Ausschöpfung</th><th>Status</th></tr>
          {rows}
        </table>
        <p class="pls-note">Tagesmittelwerte nach 17. BImSchV (Fassung 2024), <b>bestehende Anlage</b>; bezogen auf 11 % O₂,
        trockenes Abgas, Normzustand. CO und Cges sind feuerungsbestimmt (nicht durch die RGR beeinflusst).
        Für Neuanlagen gelten teils strengere Werte (HCl 6, SO₂ 30, NOₓ 100 mg/m³).
        {'' if c['krit_850'] else ' <b style=\"color:#e17055\">Hinweis: 850-°C-/2-s-Kriterium derzeit verletzt.</b>'}</p>
      </div>
    </div>''')
    return (emissionen,)


@app.cell
def _(c, mo, vr, vtbl):
    # === TURBINE / KWK ===
    turbine = mo.Html(f'''<div class="pls">
      <div class="pls-c"><h3>⚡ Turbine & Kraft-Wärme-Kopplung</h3>
        <p style="font-size:0.88em;color:#b2bec3;margin:2px 0">Der Dampf (40 bar/400 °C) treibt die Turbine.
        In Kraft-Wärme-Kopplung entstehen Strom und Fernwärme; ein Drittel des Stroms deckt den Eigenbedarf.</p>
      </div>
      <div class="pls-g3">
        <div class="pls-c"><h3>🔥 Wärme</h3>{vtbl(
            vr("therm. Leistung Q̇th", f"{c['Q_th']:.0f}", "MW")
            + vr("Dampfparameter", "40 bar / 400 °C", "")
        )}</div>
        <div class="pls-c"><h3>⚡ Strom</h3>{vtbl(
            vr("el. Leistung (brutto)", f"{c['P_el']:.1f}", "MW")
            + vr("Stromertrag", f"{c['E_el_a']:.0f}", "GWh/a", "c-ok")
            + vr("Eigenbedarf (~⅓)", f"{c['P_el']/3:.1f}", "MW", "c-w")
        )}</div>
        <div class="pls-c"><h3>♨️ Fernwärme</h3>{vtbl(
            vr("Auskopplung", f"{c['P_fw']:.0f}", "MW", "c-ok")
            + vr("Hinweis", "saisonal, max. 30 MW", "")
        )}</div>
      </div>
    </div>''')
    return (turbine,)


@app.cell
def _(c, mo, vr, vtbl):
    # === VERFAHRENSVERGLEICH – Betrieb & Kosten ===
    _b = c["betrieb"]
    _rn = c["reingas"]
    _icol = {"niedrig": "c-ok", "mittel": "c-w", "hoch": "c-d", "sehr hoch": "c-d"}.get(_b["invest"], "c-v")

    _gips_row = vr("Gips (verwertbar)", f"{_b['gips_a']:.0f}", "t/a", "c-ok") if _b["wet"] else vr("Gips", "—", "")

    _live = mo.Html(f'''<div class="pls">
      <div class="pls-c"><h3>⚖️ Betriebskennzahlen der aktuellen Konfiguration</h3>
        <p style="font-size:0.88em;color:#b2bec3;margin:2px 0">Orientierende Richtwerte aus dem aktuellen Betriebspunkt – sie zeigen, wie sich die Einstellungen
        (Sorbens, β, nass/trocken, SNCR/SCR, Grobentstaubung) auf Verbrauch, Reststoffe, Medien und Kosten auswirken.</p></div>
      <div class="pls-g4">
        <div class="pls-c"><h3>🧪 Reagenzien</h3>{vtbl(
            vr("Sorbens", _b["sorbens_name"], "")
            + vr("Verbrauch", f"{_b['sorbens_kg']:.0f}", "kg/h")
            + vr("≈ pro Jahr", f"{_b['sorbens_ta']:.0f}", "t/a")
            + vr("NH₃ (Entstickung)", f"{_b['nh3_kg']:.1f}", "kg/h")
            + vr("Aktivkoks", f"{_b['akoks_kg']:.1f}", "kg/h")
        )}</div>
        <div class="pls-c"><h3>🗑 Reststoffe</h3>{vtbl(
            vr("Flugasche (Grob)", f"{_b['rest_flugasche_a']:.0f}", "t/a")
            + vr("Sorptionsrückstand", f"{_b['rest_sorption_a']:.0f}", "t/a")
            + _gips_row
        )}</div>
        <div class="pls-c"><h3>💧 Medien & Energie</h3>{vtbl(
            vr("Abwasser", _b["abwasser_txt"], "", "c-ok" if not _b["wet"] else "c-w")
            + vr("Hilfsenergie", f"{_b['hilfs_kw']:.0f}", "kW")
            + vr("Investniveau", _b["invest"], "", _icol)
        )}</div>
        <div class="pls-c"><h3>💶 Betriebskosten (Richtwert)</h3>{vtbl(
            vr("Reagenzien", f"{_b['k_reag']:.0f}", "€/h")
            + vr("Reststoffentsorgung", f"{_b['k_entsorg']:.0f}", "€/h")
            + vr("Hilfsenergie", f"{_b['k_energie']:.0f}", "€/h")
            + vr("→ spez. Betriebskosten", f"{_b['opex_eur_t']:.1f}", "€/t", "c-v")
        )}
        <p class="pls-note">Nur RGR-Betriebsmittel/-Energie, ohne Personal/Instandhaltung/Kapital. Vergleichsgröße, kein Absolutwert.</p>
        </div>
      </div>
    </div>''')

    # --- Konzept-Vergleichsmatrix ---
    _spalten = ["Trockensorption Ca(OH)₂", "Kond. Trockensorpt. NaHCO₃",
                "Nassverfahren (2-stufig)", "Asdonkshof-Typ (Nass)"]
    _aktiv = {"Ca(OH)₂": 0, "NaHCO₃": 1, "Kalkmilch": 2}.get(_b["sorbens_name"], 0)
    _zeilen = [
        ("Saure Gase", ["Flugstrom + Gewebefilter", "Flugstrom + Gewebefilter", "2-stufiger Wäscher", "E-Filter → Sprühtrockner → E-Filter → 2-st. Wäscher"]),
        ("HCl/SO₂-Abscheidung", ["gut", "sehr gut", "sehr hoch", "sehr hoch"]),
        ("Reagenz", ["Kalkhydrat (günstig)", "Bicarbonat (teurer)", "Kalkmilch/NaOH", "Kalkmilch"]),
        ("Sorbensverbrauch", ["hoch (Überstöchiometrie)", "niedrigere Stöchiometrie", "gering", "gering"]),
        ("Reststoff", ["viel Sorptionsrückstand", "weniger, oft rezyklierbar", "wenig", "wenig + Salze"]),
        ("Nebenprodukt", ["–", "–", "Gips (verwertbar)", "Gips"]),
        ("Abwasser", ["keines", "keines", "zu behandeln/eindampfen", "abwasserfrei (Sprühtrockner)"]),
        ("Hilfsenergie", ["niedrig", "niedrig", "hoch (Pumpen, Aufheizung)", "hoch"]),
        ("Investkosten", ["niedrig", "niedrig–mittel", "hoch", "sehr hoch"]),
        ("Betriebskosten", ["mittel", "mittel (Reagenz teurer)", "Verbrauch gering, Energie hoch", "hoch (komplex)"]),
        ("Entstickung typ.", ["SNCR oder SCR", "SCR", "SCR/SNCR", "SCR-Kombikatalysator"]),
    ]
    _thst = "padding:7px 12px;text-align:left;border-bottom:2px solid #0f3460;white-space:nowrap;font-family:monospace;font-weight:bold"
    _th = f'<th style="background:#0f1a30;color:#dfe6e9;{_thst}">Kriterium</th>'
    for _i, _s in enumerate(_spalten):
        _hbg = "#1f4533" if _i == _aktiv else "#0f1a30"
        _hco = "#7bed9f" if _i == _aktiv else "#74b9ff"
        _mark = " ◄ aktiv" if _i == _aktiv else ""
        _th += f'<th style="background:{_hbg};color:{_hco};{_thst}">{_s}{_mark}</th>'
    _tdst = "padding:6px 12px;border-bottom:1px solid #0f3460;font-family:monospace;vertical-align:top"
    _trs = ""
    for _krit, _vals in _zeilen:
        _trs += f'<tr><td style="background:#13233e;color:#74b9ff;font-weight:bold;white-space:nowrap;{_tdst}">{_krit}</td>'
        for _i, _val in enumerate(_vals):
            _cbg = "#15301f" if _i == _aktiv else "#16213e"
            _trs += f'<td style="background:{_cbg};color:#dfe6e9;{_tdst}">{_val}</td>'
        _trs += "</tr>"

    _matrix = mo.Html(f'''<div class="pls">
      <div style="background:#16213e;border:1px solid #0f3460;border-radius:6px;padding:12px;overflow-x:auto">
        <h3 style="margin:0 0 8px 0;color:#74b9ff;font-size:1em;border-bottom:1px solid #0f3460;padding-bottom:6px">🔬 Verfahrensvergleich – Konzepte und ihre Auswirkungen</h3>
        <table style="border-collapse:collapse;font-size:0.82em">
          <tr>{_th}</tr>
          {_trs}
        </table>
        <p style="color:#8497ab;font-size:0.78em;line-height:1.5;margin-top:8px">Die aktuell eingestellte Variante ist hervorgehoben. Der Asdonkshof-Typ entspricht der realen Anlage:
        E-Filter 1 (~5.200 t/a) → Sprühtrockner (Eindüsung von MVA-Abwasser und Deponiesickerwasser) → E-Filter 2 (~3.100 t/a)
        → zweistufige Nasswäsche (Waschflüssigkeit + Kalkmilch → Gips) → SCR-Kombikatalysator → Aktivkoksfilter als letzte Stufe.</p>
      </div>
    </div>''')

    _trend = mo.Html('''<div class="pls"><div class="pls-g2">
      <div class="pls-c" style="border-color:#00b894"><h3 style="color:#00b894">✔ Vorteile Trocken/konditioniert</h3>
        <p style="font-size:0.86em;color:#dfe6e9;line-height:1.6">Niedrige Bau- und Betriebskosten, kein Abwasser, einfacher Aufbau (simultane Staub- und Schadgasabscheidung am Gewebefilter),
        gute Hg-/Dioxin-Abscheidung mit Aktivkoks. NaHCO₃ erlaubt niedrige Stöchiometrie und einen oft rezyklierbaren Reststoff.</p></div>
      <div class="pls-c" style="border-color:#e17055"><h3 style="color:#e17055">✘ Grenzen / Nachteile</h3>
        <p style="font-size:0.86em;color:#dfe6e9;line-height:1.6">Höherer Sorbensverbrauch und mehr Reststoff als nass; bei hoher HCl-Rohgasfracht wird einstufige Trockensorption
        unwirtschaftlich (Verbrauch steigt überproportional) → dann mehrstufig oder nass. Nass: sehr hohe HCl/SO₂-Abscheidung und Gips als Nebenprodukt,
        aber hohe Investition, Pumpen-/Aufheizenergie und Abwasserbehandlung (in DE: abwasserfrei → Eindampfung).</p></div>
    </div>
    <div class="pls-c" style="border-color:#74b9ff"><h3 style="color:#74b9ff">🧭 Worauf neuere Anlagen setzen</h3>
      <p style="font-size:0.88em;color:#dfe6e9;line-height:1.6">Der Trend der letzten ~10–15 Jahre geht klar zur <b>(konditionierten) Trockensorption mit Gewebefilter</b> –
      sie gilt heute als das wirtschaftlichste Verfahren. Weitere Kostenhebel: Bicarbonat mit Sorbensrezirkulation, kombinierte Hg-/Dioxin-Sorbentien,
      Vermeidung von Wiederaufheizung (Energie) und niedriger elektrischer Eigenbedarf. Bei der Entstickung ist <b>SNCR</b> deutlich günstiger als ein
      Katalysator (3–4× Investition), während <b>SCR</b> niedrigere NOₓ-Werte liefert und Dioxine mit abbaut – die Wahl ist also ein bewusster Kompromiss
      zwischen Emissionsanforderung und Kosten.</p>
    </div></div>''')

    vergleich = mo.vstack([_live, _matrix, _trend])
    return (vergleich,)


@app.cell
def _(bunker, emissionen, feuerung, hdr, mo, rgr, turbine, uebersicht, vergleich):
    # === TAB-STRUKTUR ===
    tabs = mo.ui.tabs({
        "📊 Übersicht": uebersicht,
        "🗑 Müllbunker": bunker,
        "🔥 Feuerung & Kessel": feuerung,
        "🌫 Rauchgasreinigung": rgr,
        "📋 Emissionen (17. BImSchV)": emissionen,
        "⚖️ Verfahrensvergleich": vergleich,
        "⚡ Turbine (KWK)": turbine,
    }, lazy=True)

    mo.output.replace(mo.vstack([mo.Html(hdr), tabs]))
    return


if __name__ == "__main__":
    app.run()
