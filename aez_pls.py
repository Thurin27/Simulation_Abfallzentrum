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
def _():
    # ── Konfiguration ────────────────────────────────────────────────
    # Deploy-URLs. Nach dem Deployment hier die echten Adressen eintragen.
    # MVA-Spoke-App (mva_pls) – Link im Lageplan und im MVA-Tab:
    MVA_URL = "mva/"
    # Grundriss-Planer (eigenständige HTML-Seite, z. B. docs/grundriss/index.html).
    # Relative Adresse funktioniert, wenn sie neben dieser App liegt:
    GRUNDRISS_URL = "grundriss/"
    return GRUNDRISS_URL, MVA_URL


@app.cell
def _(mo):
    # === CSS Styles (identisch zum Kläranlagen-PLS, damit beide Betriebe eine Familie bilden) ===
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
    .pls-overview-tbl { border-collapse:separate; border-spacing:14px 2px; font-size:0.88em; color:#ffffff; background:#16213e; border-radius:4px; }
    .pls-overview-tbl th { text-align:left; padding:8px 16px !important; color:#74b9ff; border-bottom:2px solid #0f3460; background:#0f1a30; white-space:nowrap; }
    .pls-overview-tbl td { padding:6px 16px !important; border-bottom:1px solid #0f3460; white-space:nowrap; }
    .pls-overview-tbl tr:hover { background:#1e2d4d; }
    .c-v { color:var(--val); } .c-ok { color:var(--ok); } .c-w { color:var(--warn); } .c-d { color:var(--danger); }
    .pls-g2 { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
    .pls-g3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; }
    .pls-bar { height:16px; border-radius:3px; background:#2d3436; overflow:hidden; margin:4px 0; }
    .pls-bar-f { height:100%; border-radius:3px; transition:width 0.5s; }
    .pls-sep { border-top:1px solid var(--border); margin:8px 0; padding-top:8px; }
    .pls-soon { color:#b2bec3; font-size:0.9em; line-height:1.6; }
    .pls-soon ul { margin:6px 0 0 0; padding-left:18px; }
    .pls-soon li { margin:3px 0; }
    .pls-badge { display:inline-block; font-size:0.72em; padding:2px 8px; border-radius:10px; background:#0f3460; color:#74b9ff; border:1px solid #285a8c; margin-left:8px; vertical-align:middle; }
    </style>""")
    return


@app.cell
def _(mo):
    # === BETRIEBSVORGABEN (Leitstand) ===
    # Treiber des Gesamt-Stoff- und Energiebilanzmodells der Übersicht.
    muell_t = mo.ui.slider(start=300, stop=800, step=5, value=675,
                           label="Hausmüll-Anlieferung [t/d]", show_value=True)
    sortier_t = mo.ui.slider(start=0, stop=300, step=5, value=120,
                             label="Sperr-/Gewerbeabfall → Sortierung [t/d]", show_value=True)
    bio_t = mo.ui.slider(start=0, stop=200, step=5, value=90,
                         label="Bioabfall → Vergärung [t/d]", show_value=True)
    ks_t = mo.ui.slider(start=0, stop=100, step=2, value=40,
                        label="Klärschlamm (entwässert) [t/d]", show_value=True)
    heizwert = mo.ui.slider(start=8.0, stop=13.0, step=0.1, value=10.0,
                            label="Heizwert Hausmüll Hu [MJ/kg]", show_value=True)
    niederschlag = mo.ui.slider(start=0.0, stop=30.0, step=0.5, value=2.0,
                                label="Niederschlag (Deponie) [mm/d]", show_value=True)
    return bio_t, heizwert, ks_t, muell_t, niederschlag, sortier_t


@app.cell
def _():
    # =========================================================================
    #  LS 6.1 – Wertstoffsortieranlage (RecyTech GmbH)
    #  Transparentes Massenbilanz- und Wirtschaftlichkeitsmodell einer
    #  mechanischen Aufbereitung. Die Reihenfolge der Aggregate ist FREI
    #  wählbar – die Stufen werden in der gewählten Folge auf den Stoffstrom
    #  angewandt. Reihenfolge und Auswahl wirken direkt auf Ausbeute, Reinheit
    #  und Wirtschaftlichkeit (keine starr vorgegebene Musterlösung).
    # =========================================================================
    S_MATS = ["PET", "PE", "PP", "Folie", "FKN", "Fe", "Al", "PPK", "Rest"]
    S_PRESETS = {
        "Gemischte Wertstofftonne": dict(PET=10, PE=10, PP=8, Folie=10, FKN=5, Fe=8, Al=3, PPK=20, Rest=26),
        "Kunststoffreich (LVP)":    dict(PET=15, PE=14, PP=12, Folie=14, FKN=6, Fe=5, Al=4, PPK=10, Rest=20),
        "Papier-/Kartonreich":      dict(PET=7, PE=7, PP=5, Folie=6, FKN=4, Fe=6, Al=2, PPK=40, Rest=23),
    }
    # Preise Sekundärrohstoffe (€/t) und Ziel-Material je Produkt.
    # Folie ist KEIN Produkt (Störstoff) → kein Preis, kein Ziel-Eintrag.
    S_PREIS = dict(PET=260, PE=190, PP=190, FKN=120, Fe=140, Al=950, PPK=85)
    S_ZIEL = {"Fe-Metalle": "Fe", "Al / NE-Metalle": "Al", "PPK (Papier/Karton)": "PPK",
              "Getränkekartons (FKN)": "FKN", "PET": "PET", "PE": "PE", "PP": "PP"}
    # Aggregate-Metadaten. base=Standardlinie, opt=Optimierungsstufe.
    # fb = Fließbild-Label (| = Zeilenumbruch)
    S_STAGES = {
        "sieb":   dict(label="Siebanlage",            fb="Siebanlage",              sub="Klassierung",     col="#fdcb6e", invest=200000, kw=15, foot=(8, 3), rolle="base"),
        "folie":  dict(label="Folienabscheider",      fb="Folien-|abscheider",      sub="Folie raus",      col="#00cec9", invest=180000, kw=15, foot=(4, 3), rolle="opt"),
        "wind":   dict(label="Windsichter",           fb="Windsichter",             sub="Papier/Leicht",   col="#00b894", invest=120000, kw=25, foot=(4, 3), rolle="base"),
        "magnet": dict(label="Magnetabscheider",      fb="Magnetab-|scheider",      sub="Fe",              col="#e17055", invest=60000,  kw=8,  foot=(2, 2), rolle="base"),
        "eddy":   dict(label="Wirbelstromabscheider", fb="Wirbelstrom-|abscheider", sub="Al / NE",         col="#e84393", invest=150000, kw=20, foot=(3, 2), rolle="base"),
        "nirfkn": dict(label="NIR-FKN (Kartons)",     fb="NIR-FKN",                 sub="Getränkekartons", col="#e0a458", invest=350000, kw=20, foot=(5, 3), rolle="opt"),
        "nir":    dict(label="NIR-Sortierung",        fb="NIR-|Sortierung",         sub="PET · PE · PP",   col="#a29bfe", invest=600000, kw=30, foot=(6, 3), rolle="base"),
        "nir2":   dict(label="NIR-Nachsortierung",    fb="NIR-Nach-|sortierung",    sub="Ausbeute ↑",      col="#6c8cff", invest=500000, kw=25, foot=(6, 3), rolle="opt"),
    }
    S_ORDER = ["sieb", "folie", "wind", "magnet", "eddy", "nirfkn", "nir", "nir2"]

    def sortiermodell(durchsatz, comp, sequence, betriebsstd,
                      strompreis=0.20, personal_fte=3, lohn_fte=60000, overhead_a=120000):
        ENTSORG = dict(sortierrest=-55.0, siebrest=-70.0, folien=0.0)   # Folie: kostenneutrale Verwertung
        MATS = S_MATS

        seq, seen = [], set()
        for k in sequence:
            if k in S_STAGES and k not in seen:
                seq.append(k)
                seen.add(k)

        s = sum(comp.values()) or 1.0
        main = {m: durchsatz * comp[m] / s for m in MATS}
        produkte, reste = {}, {}
        stage_out = []   # je angewandter Stufe: (key, [(name, masse, reinheit|None, kind), ...])

        def pull(eta):
            prod = {}
            for m in MATS:
                moved = main[m] * eta.get(m, 0.0)
                prod[m] = moved
                main[m] -= moved
            return prod

        def merge(store, name, prod):
            if name in store:
                for m in MATS:
                    store[name][m] += prod[m]
            else:
                store[name] = dict(prod)

        def emit(name, prod, kind):
            merge(produkte if kind == "prod" else reste, name, prod)
            masse = sum(prod.values())
            reinheit = None if kind == "rest" else ((prod[S_ZIEL[name]] / masse) if masse > 1e-9 else 0.0)
            return (name, masse, reinheit, kind)

        def apply_stage(key):
            o = []
            if key == "sieb":
                o.append(emit("Siebrest (Feinfraktion)", pull({m: (0.55 if m == "Rest" else 0.03) for m in MATS}), "rest"))
            elif key == "folie":
                # Dedizierte Folienabscheidung (Folienabsaugung / NIR-Folie): zieht Folie früh raus,
                # bevor sie Papier (Windsichter) und Kunststoffe (NIR) verschmutzt.
                eta = {m: {"Folie": 0.90, "PPK": 0.02, "Rest": 0.02}.get(m, 0.005) for m in MATS}
                o.append(emit("Folien (→ Verwertung)", pull(eta), "rest"))
            elif key == "wind":
                # Windsichtung: Leichtgut = Papier + Folie (+ leichter Rest). Air-Klassierung kann
                # Folie nicht sauber vom Papier trennen → Rest-Folie verschmutzt die PPK-Fraktion.
                eta = {m: {"PPK": 0.80, "Folie": 0.50, "Rest": 0.12}.get(m, 0.01) for m in MATS}
                o.append(emit("PPK (Papier/Karton)", pull(eta), "prod"))
            elif key == "magnet":
                o.append(emit("Fe-Metalle", pull({m: (0.95 if m == "Fe" else 0.004) for m in MATS}), "prod"))
            elif key == "eddy":
                gesamt = sum(main.values()) + 1e-9
                penalty = min(0.45, (main["Fe"] / gesamt) * 2.5)   # Rest-Fe stört Wirbelstrom
                eta = {m: (0.85 * (1 - penalty) if m == "Al" else (0.20 if m == "Fe" else 0.01)) for m in MATS}
                o.append(emit("Al / NE-Metalle", pull(eta), "prod"))
            elif key == "nirfkn":
                o.append(emit("Getränkekartons (FKN)", pull({m: (0.85 if m == "FKN" else 0.02) for m in MATS}), "prod"))
            elif key == "nir":
                # Fremdstoffe (v. a. Folie) senken NIR-Ausbeute UND -Reinheit → Reihenfolge zählt
                gesamt = sum(main.values()) + 1e-9
                dirt = sum(main[m] for m in MATS if m not in ("PET", "PE", "PP")) / gesamt
                rec = 0.92 * (1 - 0.6 * dirt)
                cc = dict(PET=0.02, PE=0.02, PP=0.02, Folie=0.05, FKN=0.03, Fe=0.05, Al=0.05, PPK=0.04, Rest=0.04)
                for poly in ["PET", "PE", "PP"]:
                    o.append(emit(poly, pull({m: (rec if m == poly else cc[m]) for m in MATS}), "prod"))
            elif key == "nir2":
                # Nachsortierung: gewinnt Rest-Polymer aus dem Strom (Ausbeute ↑)
                for poly in ["PET", "PE", "PP"]:
                    o.append(emit(poly, pull({m: (0.85 if m == poly else 0.015) for m in MATS}), "prod"))
            return o

        for k in seq:
            stage_out.append((k, apply_stage(k)))
        reste["Sortierrest (→ EBS/MVA)"] = dict(main)

        ergebnis, erloes_a = [], 0.0
        for name, prod in produkte.items():
            masse = sum(prod.values())
            reinheit = (prod[S_ZIEL[name]] / masse) if masse > 1e-9 else 0.0
            basis = S_PREIS[S_ZIEL[name]]
            eff = basis * max(0.0, min(1.0, (reinheit - 0.65) / 0.30))   # <65% wertlos, ab 95% voll
            m_a = masse * betriebsstd
            erl = m_a * eff
            erloes_a += erl
            ergebnis.append(dict(name=name, masse=masse, m_a=m_a, reinheit=reinheit,
                                 basis=basis, eff_preis=eff, erloes=erl, kind="produkt"))
        entsorg_a = 0.0
        for name, prod in reste.items():
            masse = sum(prod.values())
            m_a = masse * betriebsstd
            key = ("siebrest" if "Sieb" in name else ("folien" if "Folien" in name else "sortierrest"))
            kost = m_a * ENTSORG[key]
            entsorg_a += kost
            ergebnis.append(dict(name=name, masse=masse, m_a=m_a, reinheit=None,
                                 basis=ENTSORG[key], eff_preis=ENTSORG[key], erloes=kost, kind="rest"))

        inv = 400000 + sum(S_STAGES[k]["invest"] for k in seq)
        kw = 20 + sum(S_STAGES[k]["kw"] for k in seq)
        energie_a = kw * betriebsstd * strompreis
        personal_a = personal_fte * lohn_fte
        wartung_a = inv * 0.04
        betrieb_a = energie_a + personal_a + wartung_a + overhead_a
        deckung_a = erloes_a + entsorg_a - betrieb_a
        amort = inv / deckung_a if deckung_a > 0 else None

        foot = [("Aufgabe / Dosierung", (6, 4))]
        for k in seq:
            foot.append((S_STAGES[k]["label"], S_STAGES[k]["foot"]))
        foot.append(("Ballenpresse / Output", (5, 4)))
        foot_sum = sum(L * B for _, (L, B) in foot)

        return dict(seq=seq, ergebnis=ergebnis, stage_out=stage_out, erloes_a=erloes_a,
                    entsorg_a=entsorg_a, energie_a=energie_a, personal_a=personal_a,
                    wartung_a=wartung_a, overhead_a=overhead_a, betrieb_a=betrieb_a,
                    deckung_a=deckung_a, amort=amort, inv=inv, kw=kw,
                    t_a=durchsatz * betriebsstd, foot=foot, foot_sum=foot_sum)
    return S_ORDER, S_PRESETS, S_STAGES, sortiermodell


@app.cell
def _(S_ORDER, S_PRESETS, S_STAGES, mo):
    # === LS 6.1 – Bedienelemente Sortieranlage ===
    # Aggregate über 9 Positionen FREI anordnen (Reihenfolge = Verfahrenskonzept).
    s_preset = mo.ui.dropdown(options=list(S_PRESETS.keys()),
                              value="Gemischte Wertstofftonne", label="Input-Zusammensetzung")
    s_durchsatz = mo.ui.slider(start=1.0, stop=10.0, step=0.5, value=5.0,
                               label="Durchsatz [t/h]", show_value=True)
    s_stunden = mo.ui.dropdown(options={"Einschicht (2000 h/a)": 2000,
                                        "Zweischicht (4000 h/a)": 4000,
                                        "Dreischicht (6000 h/a)": 6000},
                               value="Zweischicht (4000 h/a)", label="Betriebszeit")
    _leer = "— (leer)"
    _opts = [_leer] + [S_STAGES[k]["label"] for k in S_ORDER]
    # Standard-Belegung = funktionierende 5er-Grundlinie (Optimierung über freie Positionen)
    s_pos1 = mo.ui.dropdown(options=_opts, value="Siebanlage", label="Position 1")
    s_pos2 = mo.ui.dropdown(options=_opts, value="Windsichter", label="Position 2")
    s_pos3 = mo.ui.dropdown(options=_opts, value="Magnetabscheider", label="Position 3")
    s_pos4 = mo.ui.dropdown(options=_opts, value="Wirbelstromabscheider", label="Position 4")
    s_pos5 = mo.ui.dropdown(options=_opts, value="NIR-Sortierung", label="Position 5")
    s_pos6 = mo.ui.dropdown(options=_opts, value=_leer, label="Position 6")
    s_pos7 = mo.ui.dropdown(options=_opts, value=_leer, label="Position 7")
    s_pos8 = mo.ui.dropdown(options=_opts, value=_leer, label="Position 8")
    s_pos9 = mo.ui.dropdown(options=_opts, value=_leer, label="Position 9")
    return (s_durchsatz, s_pos1, s_pos2, s_pos3, s_pos4, s_pos5, s_pos6,
            s_pos7, s_pos8, s_pos9, s_preset, s_stunden)


@app.cell
def _(GRUNDRISS_URL, MVA_URL, S_PRESETS, S_STAGES, bio_t, heizwert, ks_t, mo,
      muell_t, niederschlag, s_durchsatz, s_pos1, s_pos2, s_pos3, s_pos4,
      s_pos5, s_pos6, s_pos7, s_pos8, s_pos9, s_preset, s_stunden, sortier_t,
      sortiermodell):
    # =========================================================================
    #  AEZ-LEITSTAND – Aufbau
    #  -----------------------------------------------------------------------
    #  Diese App ist der zentrale Hub ("Leitstand") des virtuellen
    #  Abfallentsorgungszentrums. Die ÜBERSICHT ist voll funktionsfähig:
    #  ein transparentes Gesamt-Stoff-/Energiebilanzmodell, getrieben von den
    #  Betriebsvorgaben oben. Die Einzelanlagen sind als Gerüst angelegt und
    #  werden Schritt für Schritt vertieft (geplant als eigene, verlinkte
    #  Marimo-Apps nach dem Hub-and-Spoke-Muster).
    # =========================================================================

    # ---------- kleine Helfer (Stil identisch zum Kläranlagen-PLS) ----------
    def vc(val, wl=None, dl=None, wh=None, dh=None):
        try:
            x = float(str(val).replace(",", "."))
        except (ValueError, TypeError):
            return "c-v"
        if dl is not None and x < dl: return "c-d"
        if wl is not None and x < wl: return "c-w"
        if dh is not None and x > dh: return "c-d"
        if wh is not None and x > wh: return "c-w"
        return "c-v"

    def vr(label, val, unit, cls=None, **kw):
        # cls: entweder direkt als CSS-Klasse (4. Positionsargument) oder via
        # Schwellen-Keywords (wl/dl/wh/dh) automatisch über vc() bestimmt.
        if cls is None:
            cls = vc(val, **kw) if kw else "c-v"
        return (f'<tr><td style="padding:3px 8px 3px 0;color:#b2bec3;white-space:nowrap">{label}</td>'
                f'<td style="padding:3px 0 3px 8px;white-space:nowrap;font-weight:bold" class="{cls}">{val}&ensp;{unit}</td></tr>')

    def vtbl(rows):
        return f'<table style="border-collapse:collapse">{rows}</table>'

    def bar(pct, color="#0984e3"):
        pct = max(0, min(100, pct))
        return f'<div class="pls-bar"><div class="pls-bar-f" style="width:{pct}%;background:{color}"></div></div>'

    # ---------- Gesamt-Stoff- und Energiebilanz (leicht, transparent) -------
    m_muell = muell_t.value
    m_sortier = sortier_t.value
    m_bio = bio_t.value
    m_ks = ks_t.value
    Hu = heizwert.value
    regen = niederschlag.value

    # Sortieranlage: grobe Trennung in Wertstoffe / Reststoff zur MVA
    wertstoff_quote = 0.35
    m_wertstoff = m_sortier * wertstoff_quote
    m_reststoff = m_sortier * (1 - wertstoff_quote)        # → Müllbunker / MVA

    # Klärschlammtrocknung: entwässert (~25 % TS) → getrocknet (~65 % TS)
    m_ks_tr = m_ks * 0.40                                   # Masse nach Trocknung → Mitverbrennung
    Hu_ks = 8.0
    Hu_rest = 12.0

    # MVA-Aufgabe (Kapazität: 2 Linien × 16,6 t/h = 33,2 t/h ≈ 797 t/d)
    m_mva = m_muell + m_reststoff + m_ks_tr
    kap_mva = 2 * 16.6 * 24
    ausl_mva = m_mva / kap_mva * 100

    # massengewichteter Misch-Heizwert
    Hu_mix = ((m_muell * Hu) + (m_reststoff * Hu_rest) + (m_ks_tr * Hu_ks)) / max(1e-6, m_mva)

    # thermische Leistung [MW]: t/d → kg/s × MJ/kg
    Q_th = (m_mva * 1000 * Hu_mix) / 86400.0
    eta_el, eta_th = 0.13, 0.30                            # KWK (MVA-typisch: viel Wärmeauskopplung)
    P_el = Q_th * eta_el                                   # MW (brutto)
    P_fw = Q_th * eta_th                                   # MW Fernwärme
    E_el_d = P_el * 24                                      # MWh/d brutto
    eigenbedarf = 0.16
    E_el_netto = E_el_d * (1 - eigenbedarf)
    E_el_a = P_el * 8000 / 1000                            # GWh/a (≈8000 Vollbenutzungsstunden)

    # Verbrennungsreststoffe
    m_schlacke = m_mva * 0.27                               # → Schlackeaufbereitung → Deponie
    m_filterstaub = m_mva * 0.03                            # RGR-Reststoffe → Sonderdeponie

    # Vergärung / Kompost
    biogas_spez = 100                                       # m³ Biogas / t Bioabfall
    V_biogas = m_bio * biogas_spez                          # m³/d
    ch4_anteil = 0.58
    bhkw_kwh_pro_m3 = 6.0 * ch4_anteil / 0.55              # ~ Energiegehalt
    E_bio_d = V_biogas * 6.0 * 0.40 / 1000                  # MWh/d el (η_el BHKW ~40 %)
    m_kompost = m_bio * 0.40

    # Deponie-Sickerwasser (offene Einbaufläche ~ 12 ha, Sickerquote ~0,3)
    flaeche_offen_ha = 12
    sicker_quote = 0.30
    V_sicker = regen * flaeche_offen_ha * 1e4 / 1000 * sicker_quote   # m³/d

    # Inputsumme / Verwertungs- bzw. Beseitigungsquote (grob)
    m_input = m_muell + m_sortier + m_bio + m_ks
    m_stofflich = m_wertstoff + m_kompost
    m_thermisch = m_mva
    quote_stofflich = m_stofflich / max(1e-6, m_input) * 100

    # ---------- Header ----------
    hdr = f'''<div class="pls"><div class="pls-hdr">
        <h2>♻️ Abfall- &amp; Energiezentrum Schwierbach – Leitstand</h2>
        <div class="pls-st">
            <span><span class="pls-dot" style="background:#00b894"></span> ONLINE</span>
            <span>Input: {m_input:.0f} t/d</span>
            <span>MVA: {ausl_mva:.0f}&nbsp;%</span>
            <span>Netz: {P_el:.1f} MW</span>
        </div>
    </div></div>'''

    # ---------- Verbundschema (Lageplan / Stoff- & Energieströme) ----------
    # Inline-SVG mit festen Koordinaten. Farbige Konturen unterscheiden die
    # Anlagentypen (PLS-Konvention) – keine didaktischen Hinweise im Schema.
    def box(x, y, w, h, stroke, title, *lines, tcol=None, href=None):
        tcol = tcol or "#dfe6e9"
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#2d3436" stroke="{stroke}" stroke-width="{3 if href else 2}"/>']
        cx = x + w / 2
        out.append(f'<text x="{cx}" y="{y+19}" fill="{stroke}" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold">{title}</text>')
        for i, ln in enumerate(lines):
            out.append(f'<text x="{cx}" y="{y+37+i*15}" fill="{tcol}" text-anchor="middle" font-size="10" font-family="monospace">{ln}</text>')
        if href:
            out.append(f'<text x="{cx}" y="{y+h-9}" fill="#74b9ff" text-anchor="middle" font-size="9.5" font-family="monospace" font-weight="bold">🔗 Simulation öffnen ▸</text>')
            return f'<a href="{href}" target="_blank" rel="noopener" style="cursor:pointer">{"".join(out)}</a>'
        return "".join(out)

    # Farbcodierte Pfeilspitzen (eine Marker-Definition je Strom-Farbe).
    FLOWCOL = {
        "in": "#5b9bd5", "dampf": "#e17055", "bio": "#00b894",
        "schlacke": "#b2bec3", "wasser": "#74b9ff", "ks": "#a29bfe",
    }
    _mk = "".join(
        f'<marker id="mk_{k}" markerWidth="11" markerHeight="9" refX="8.5" refY="4.5" '
        f'orient="auto" markerUnits="userSpaceOnUse">'
        f'<path d="M0,0 L9,4.5 L0,9 L2.4,4.5 Z" fill="{v}"/></marker>'
        for k, v in FLOWCOL.items()
    )

    def _round_path(pts, r=12):
        # Orthogonaler Pfad mit abgerundeten Ecken (quadratische Bögen).
        if len(pts) < 2:
            return ""
        d = [f'M {pts[0][0]},{pts[0][1]}']
        for i in range(1, len(pts) - 1):
            (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
            import math as _m
            d1 = _m.hypot(x1 - x0, y1 - y0)
            d2 = _m.hypot(x2 - x1, y2 - y1)
            rr = min(r, d1 / 2, d2 / 2)
            ax = x1 - (x1 - x0) / max(d1, 1e-6) * rr
            ay = y1 - (y1 - y0) / max(d1, 1e-6) * rr
            bx = x1 + (x2 - x1) / max(d2, 1e-6) * rr
            by = y1 + (y2 - y1) / max(d2, 1e-6) * rr
            d.append(f'L {ax:.1f},{ay:.1f} Q {x1},{y1} {bx:.1f},{by:.1f}')
        d.append(f'L {pts[-1][0]},{pts[-1][1]}')
        return " ".join(d)

    def flow(pts, key="in", label="", lx=None, ly=None, dash=False):
        # pts: Liste orthogonaler Stützpunkte (x,y). Farbe über key (FLOWCOL).
        col = FLOWCOL.get(key, "#5b9bd5")
        d = ' stroke-dasharray="6,4"' if dash else ""
        seg = (f'<path d="{_round_path(pts)}" fill="none" stroke="{col}" stroke-width="2.4" '
               f'stroke-linejoin="round" stroke-linecap="round" marker-end="url(#mk_{key})"{d}/>')
        if label and lx is not None:
            seg += (f'<text x="{lx}" y="{ly}" fill="#9fb3c8" text-anchor="middle" '
                    f'font-size="9" font-family="monospace">{label}</text>')
        return seg

    schema = f'''<svg viewBox="0 0 1240 720" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;background:#0a1428;border-radius:6px">
      <defs>{_mk}</defs>

      <!-- Anlieferung -->
      {box(20, 300, 130, 110, "#74b9ff", "Anlieferung", "Waage", f"{m_input:.0f} t/d", "Eingangskontrolle")}

      <!-- Vorbehandlung / Annahme -->
      {box(210, 40, 150, 70, "#6c5ce7", "Müllbunker", f"{m_muell:.0f} t/d", "Kran / Mischung")}
      {box(210, 230, 150, 70, "#fdcb6e", "Sortieranlage", f"{m_sortier:.0f} t/d", "Vorschaltanlage")}
      {box(210, 420, 150, 70, "#00b894", "Bioabfall-Annahme", f"{m_bio:.0f} t/d")}
      {box(210, 560, 150, 70, "#a29bfe", "Klärschlammtrocknung", f"{m_ks:.0f} t/d ein", f"{m_ks_tr:.0f} t/d getr.")}

      <!-- Prozessstufe -->
      {box(440, 40, 170, 100, "#e17055", "MVA – 2 Linien", f"Aufgabe {m_mva:.0f} t/d", f"Auslastung {ausl_mva:.0f} %", f"Q̇th {Q_th:.0f} MW", href=MVA_URL)}
      {box(440, 410, 170, 90, "#00b894", "Vergärung", f"Biogas {V_biogas:.0f} m³/d", f"CH₄ ~{ch4_anteil*100:.0f} %")}

      <!-- Nachbehandlung / Energie -->
      {box(690, 40, 160, 70, "#dfe6e9", "Rauchgasreinigung", "mehrstufig", "17. BImSchV", tcol="#9fb3c8")}
      {box(690, 200, 160, 90, "#fdcb6e", "Energiezentrale", f"P_el {P_el:.1f} MW", f"P_fw {P_fw:.0f} MW", "Turbine + BHKW")}
      {box(690, 410, 160, 70, "#00b894", "Kompostierung", f"{m_kompost:.0f} t/d", "Gärrest → Kompost")}
      {box(690, 560, 160, 70, "#b2bec3", "Schlackeaufbereitung", f"{m_schlacke:.0f} t/d", "Metallrückgewinnung")}

      <!-- Senken -->
      {box(930, 40, 130, 70, "#b2bec3", "Kamin", "Reingas", "Emissionsmessung", tcol="#9fb3c8")}
      {box(930, 210, 150, 70, "#74b9ff", "Strom / Fernwärme", f"{E_el_netto:.0f} MWh/d", "ins Netz")}
      {box(930, 520, 150, 110, "#e94560", "Deponie (DK II)", "41 ha", f"Schlacke {m_schlacke:.0f} t/d", f"Sickerw. {V_sicker:.0f} m³/d")}

      <!-- Ströme: Anlieferung → Annahme (Verteiler-Manifold) -->
      {flow([(150, 322), (178, 322), (178, 75), (210, 75)], "in", "Hausmüll", lx=179, ly=69)}
      {flow([(150, 345), (186, 345), (186, 265), (210, 265)], "in", "Sperrmüll", lx=179, ly=259)}
      {flow([(150, 388), (170, 388), (170, 455), (210, 455)], "in", "Bioabfall", lx=184, ly=449)}
      {flow([(150, 402), (162, 402), (162, 595), (210, 595)], "ks", "Klärschl.", lx=184, ly=589)}

      <!-- Annahme → Prozess -->
      {flow([(360, 75), (440, 75)], "in")}
      {flow([(360, 265), (398, 265), (398, 110), (440, 110)], "in", "Reststoff", lx=380, ly=256)}
      {flow([(360, 595), (420, 595), (420, 132), (440, 132)], "ks", "Mitverbr.", lx=393, ly=586, dash=True)}
      {flow([(360, 455), (440, 455)], "bio")}

      <!-- MVA → RGR → Kamin -->
      {flow([(610, 70), (690, 70)], "in", "Rohgas", lx=650, ly=62)}
      {flow([(850, 75), (930, 75)], "in")}

      <!-- MVA → Energiezentrale (Dampf) -->
      {flow([(560, 140), (560, 245), (690, 245)], "dampf", "Dampf", lx=584, ly=200)}
      {flow([(850, 245), (930, 245)], "dampf")}

      <!-- Vergärung → Energiezentrale (Biogas) + Kompost -->
      {flow([(610, 425), (638, 425), (638, 290), (690, 290)], "bio", "Biogas", lx=624, ly=340, dash=True)}
      {flow([(610, 455), (690, 455)], "bio", "Gärrest", lx=650, ly=447)}

      <!-- MVA → Schlacke → Aufbereitung → Deponie -->
      {flow([(610, 120), (655, 120), (655, 595), (690, 595)], "schlacke", "Schlacke", lx=672, ly=550)}
      {flow([(850, 595), (890, 595), (890, 560), (930, 560)], "schlacke")}

      <!-- Deponie → Sickerwasser -->
      {flow([(1005, 630), (1005, 690)], "wasser", "Sickerwasser → Behandlung", lx=1005, ly=705, dash=True)}

      <!-- Labor (zentrale Überwachung) -->
      <rect x="930" y="330" width="150" height="90" rx="6" fill="#16213e" stroke="#74b9ff" stroke-width="1.5" stroke-dasharray="3,3"/>
      <text x="1005" y="362" fill="#74b9ff" text-anchor="middle" font-size="12" font-family="monospace" font-weight="bold">Labor</text>
      <text x="1005" y="382" fill="#9fb3c8" text-anchor="middle" font-size="10" font-family="monospace">Eigenüberwachung</text>
      <text x="1005" y="398" fill="#9fb3c8" text-anchor="middle" font-size="10" font-family="monospace">Emission · Sickerw.</text>
    </svg>'''

    # ---------- Übersicht ----------
    overview = mo.Html(f'''<div class="pls">
      <div class="pls-c" style="overflow-x:auto">
        <h3>Verbundschema – Stoff- und Energieströme (Betriebspunkt aus Leitstand-Vorgaben)</h3>
        {schema}
      </div>
      <div class="pls-g3">
        <div class="pls-c"><h3>⚖️ Stoffstrombilanz</h3>
          {vtbl(
              vr("Input gesamt", f"{m_input:.0f}", "t/d")
              + vr("→ thermisch (MVA)", f"{m_thermisch:.0f}", "t/d")
              + vr("→ Wertstoffe (Sortierung)", f"{m_wertstoff:.0f}", "t/d")
              + vr("→ Kompost", f"{m_kompost:.0f}", "t/d")
              + vr("Schlacke → Deponie", f"{m_schlacke:.0f}", "t/d")
              + vr("RGR-Reststoffe", f"{m_filterstaub:.0f}", "t/d")
          )}
          <div class="pls-sep"></div>
          {vtbl(vr("stoffl. Verwertungsquote", f"{quote_stofflich:.0f}", "%"))}
          {bar(quote_stofflich, '#00b894' if quote_stofflich > 30 else '#fdcb6e')}
        </div>
        <div class="pls-c"><h3>⚡ Energiebilanz (MVA + BHKW)</h3>
          {vtbl(
              vr("therm. Leistung Q̇th", f"{Q_th:.0f}", "MW")
              + vr("Misch-Heizwert", f"{Hu_mix:.1f}", "MJ/kg")
              + vr("Strom brutto", f"{P_el:.1f}", "MW")
              + vr("Strom netto", f"{E_el_netto:.0f}", "MWh/d")
              + vr("davon BHKW (Biogas)", f"{E_bio_d:.1f}", "MWh/d")
              + vr("Fernwärme", f"{P_fw:.0f}", "MW")
              + vr("Stromertrag", f"{E_el_a:.0f}", "GWh/a")
          )}
        </div>
        <div class="pls-c"><h3>🏭 Anlagen-Status</h3>
          <table class="pls-overview-tbl">
            <tr><th>Anlage</th><th>Kennwert</th><th>Status</th></tr>
            <tr><td>MVA (2 Linien)</td><td>{ausl_mva:.0f} % / {kap_mva:.0f} t/d</td><td><span class="c-{'ok' if ausl_mva<=100 else 'd'}">●</span> {'Betrieb' if ausl_mva<=100 else 'Überlast'}</td></tr>
            <tr><td>Rauchgasreinigung</td><td>17. BImSchV</td><td><span class="c-ok">●</span> Betrieb</td></tr>
            <tr><td>Sortieranlage</td><td>{m_sortier:.0f} t/d</td><td><span class="c-{'ok' if m_sortier>0 else 'w'}">●</span> {'Betrieb' if m_sortier>0 else 'Stillstand'}</td></tr>
            <tr><td>Vergärung</td><td>{V_biogas:.0f} m³/d</td><td><span class="c-{'ok' if m_bio>0 else 'w'}">●</span> {'Betrieb' if m_bio>0 else 'Stillstand'}</td></tr>
            <tr><td>Klärschlammtrocknung</td><td>{m_ks:.0f} t/d</td><td><span class="c-{'ok' if m_ks>0 else 'w'}">●</span> {'Betrieb' if m_ks>0 else 'Stillstand'}</td></tr>
            <tr><td>Deponie (DK II)</td><td>41 ha</td><td><span class="c-ok">●</span> Einbau</td></tr>
          </table>
        </div>
      </div>
    </div>''')

    # ---------- Gerüst-Helfer für noch zu vertiefende Anlagen ----------
    def geruest(titel, beschreibung, subtabs):
        items = "".join(f"<li>{s}</li>" for s in subtabs)
        return mo.Html(f'''<div class="pls">
          <div class="pls-c">
            <h3>{titel} <span class="pls-badge">in Vorbereitung</span></h3>
            <div class="pls-soon">
              {beschreibung}
              <div class="pls-sep"></div>
              <b>Geplante Unter-Tabs:</b>
              <ul>{items}</ul>
            </div>
          </div>
        </div>''')

    mva = mo.Html(f'''<div class="pls">
      <div class="pls-c" style="border-color:#e94560">
        <h3>🔥 Müllverbrennungsanlage (MVA) – eigene Simulation</h3>
        <div class="pls-soon">
          Die MVA ist das Simulationsherzstück und als eigenständige App umgesetzt (Hub-and-Spoke).
          Sie bildet die vollständige Kette ab: Müllbunker → Feuerung (850-°C-Kriterium, O₂/CO) →
          mehrstufige Rauchgasreinigung → Reingasvergleich mit der 17. BImSchV → Turbine, dazu einen
          Verfahrensvergleich (Trocken-/Nassverfahren, SNCR/SCR, Betriebskosten).
          <div class="pls-sep"></div>
          <div style="margin:10px 0">
            <a href="{MVA_URL}" target="_blank" rel="noopener"
               style="display:inline-block;background:#e94560;color:#ffffff;font-weight:bold;
               text-decoration:none;padding:12px 24px;border-radius:6px;font-family:monospace;font-size:1.05em">
               🔥 MVA-Simulation öffnen ▸</a>
          </div>
          <span style="color:#8497ab;font-size:0.85em">Öffnet die MVA-App in einem neuen Tab.
          Führt der Link ins Leere, ist oben in der Datei die Konstante <b>MVA_URL</b> auf die echte
          Deploy-Adresse zu setzen.</span>
        </div>
      </div>
    </div>''')

    # ---------- Sortieranlage (LS 6.1, RecyTech GmbH) – frei anordenbar ------
    _scomp = S_PRESETS[s_preset.value]
    _lab2key = {S_STAGES[_k]["label"]: _k for _k in S_STAGES}
    _sequence = []
    for _d in [s_pos1, s_pos2, s_pos3, s_pos4, s_pos5, s_pos6, s_pos7, s_pos8, s_pos9]:
        _kk = _lab2key.get(_d.value)
        if _kk:
            _sequence.append(_kk)
    _sr = sortiermodell(s_durchsatz.value, _scomp, _sequence, s_stunden.value)
    _seq = _sr["seq"]

    def _fliessbild():
        # Spalten: Aufgabe + je angewandter Stufe (mit ihren Ausschleusungen) + Sortierrest
        _stufen = [(None, "Wertstofftonne", f"{s_durchsatz.value:.1f} t/h", "#74b9ff", [])]
        for _k, _outs in _sr["stage_out"]:
            _st = S_STAGES[_k]
            _stufen.append((_k, _st["fb"], _st["sub"], _st["col"], _outs))
        _stufen.append((None, "Sortierrest", "→ EBS/MVA", "#b2bec3", []))
        _W, _GAP = 128, 34
        _n = len(_stufen)
        _wid = 20 + _n * (_W + _GAP)
        p = [f'<svg viewBox="0 0 {_wid} 320" xmlns="http://www.w3.org/2000/svg" '
             f'style="width:100%;min-width:{min(_wid, 1180)}px;height:auto;background:#0a1428;border-radius:6px">']
        p.append('<defs>'
                 '<marker id="fb_a" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8 L2,4 Z" fill="#5b9bd5"/></marker>'
                 '<marker id="fb_p" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8 L2,4 Z" fill="#7f8fa6"/></marker>'
                 '</defs>')
        _yt = 34
        _cols = []
        for _i, (_k, _lab, _sub, _col, _outs) in enumerate(_stufen):
            _x = 20 + _i * (_W + _GAP)
            _cx = _x + _W / 2
            _cols.append((_cx, _outs))
            p.append(f'<rect x="{_x}" y="{_yt}" width="{_W}" height="58" rx="6" fill="#2d3436" stroke="{_col}" stroke-width="2"/>')
            _ls = _lab.split("|")
            for _j, _ln in enumerate(_ls):
                p.append(f'<text x="{_cx}" y="{_yt+19+_j*13}" fill="{_col}" text-anchor="middle" font-size="11" font-family="monospace" font-weight="bold">{_ln}</text>')
            p.append(f'<text x="{_cx}" y="{_yt+52}" fill="#9fb3c8" text-anchor="middle" font-size="8.5" font-family="monospace">{_sub}</text>')
            if _i < _n - 1:
                _xn = 20 + (_i + 1) * (_W + _GAP)
                p.append(f'<line x1="{_x+_W}" y1="{_yt+29}" x2="{_xn}" y2="{_yt+29}" stroke="#5b9bd5" stroke-width="2.4" stroke-linecap="round" marker-end="url(#fb_a)"/>')

        def _chip(cx, y, rec, w=140):
            _name, _masse, _reinheit, _kind = rec
            x0 = cx - w / 2
            col = "#7f8fa6" if _kind == "rest" else "#00b894"
            p.append(f'<rect x="{x0:.0f}" y="{y}" width="{w}" height="36" rx="5" fill="#16213e" stroke="{col}" stroke-width="1.4"/>')
            p.append(f'<text x="{cx}" y="{y+14}" fill="#dfe6e9" text-anchor="middle" font-size="9" font-family="monospace" font-weight="bold">{_name.split(" (")[0]}</text>')
            rh = "" if _reinheit is None else f" · {_reinheit*100:.0f}%"
            p.append(f'<text x="{cx}" y="{y+28}" fill="#9fb3c8" text-anchor="middle" font-size="8.5" font-family="monospace">{_masse:.2f} t/h{rh}</text>')

        for _cx, _outs in _cols:
            if not _outs:
                continue
            if len(_outs) == 1:
                p.append(f'<line x1="{_cx}" y1="{_yt+58}" x2="{_cx}" y2="150" stroke="#7f8fa6" stroke-width="2" stroke-linecap="round" marker-end="url(#fb_p)"/>')
                _chip(_cx, 154, _outs[0])
            else:
                p.append(f'<line x1="{_cx}" y1="{_yt+58}" x2="{_cx}" y2="112" stroke="#7f8fa6" stroke-width="2" stroke-linecap="round"/>')
                for _j, _rec in enumerate(_outs):
                    _yy = 114 + _j * 46
                    _chip(_cx, _yy, _rec)
                    if _j < len(_outs) - 1:
                        p.append(f'<line x1="{_cx}" y1="{_yy+36}" x2="{_cx}" y2="{_yy+46}" stroke="#7f8fa6" stroke-width="1.4"/>')
        p.append('</svg>')
        return "".join(p)

    # Kontext-Karte (Lernsituation)
    _ctx = mo.Html('''<div class="pls"><div class="pls-c">
        <h3>🔀 Wertstoffsortieranlage</h3>
        <div class="pls-soon">
          <b>Rahmenbedingungen:</b> Fraktionen Kunststoffe (PET, PE, PP), Metalle (Fe, Al), Papier/Karton ·
          Durchsatz ca. 5 t/h · Halle 40 m × 20 m = 800 m², 8 m Höhe · 400 V, Druckluft, Kran 5 t.
          <div class="pls-sep"></div>
          <span style="color:#8497ab;font-size:0.9em">Die neun Positionen sind <b>frei belegbar</b>
          (leere Positionen = Stufe entfällt).</span>
        </div>
    </div></div>''')

    # Massenbilanz-Tabelle (dunkler Zellhintergrund, damit Marimo die Tabelle
    # nicht hell einfärbt → hellgraue Schrift bliebe sonst auf Weiß unlesbar)
    _tdst = "padding:6px 12px;border-bottom:1px solid #0f3460;font-family:monospace;white-space:nowrap;background:#16213e"
    _thst = "padding:6px 12px;border-bottom:2px solid #0f3460;font-family:monospace;white-space:nowrap;background:#0f1a30;color:#74b9ff"
    _rows = ""
    for _e in _sr["ergebnis"]:
        _isp = _e["reinheit"] is not None
        _rh = f"{_e['reinheit']*100:.0f} %" if _isp else "—"
        _rhc = "#00b894" if (_isp and _e["reinheit"] >= 0.85) else ("#fdcb6e" if (_isp and _e["reinheit"] >= 0.6) else ("#e17055" if _isp else "#8497ab"))
        _erl = _e["erloes"]
        _erlc = "#00b894" if _erl > 0 else "#e17055"
        _namecol = "#dfe6e9" if _isp else "#9fb3c8"
        _rows += (f'<tr>'
                  f'<td style="{_tdst};color:{_namecol};font-weight:bold">{_e["name"]}</td>'
                  f'<td style="{_tdst};color:#dfe6e9;text-align:right">{_e["masse"]:.2f}</td>'
                  f'<td style="{_tdst};color:#9fb3c8;text-align:right">{_e["m_a"]:,.0f}</td>'
                  f'<td style="{_tdst};color:{_rhc};text-align:right">{_rh}</td>'
                  f'<td style="{_tdst};color:#9fb3c8;text-align:right">{_e["eff_preis"]:.0f}</td>'
                  f'<td style="{_tdst};color:{_erlc};text-align:right;font-weight:bold">{_erl/1000:,.0f}</td>'
                  f'</tr>')
    _bilanz = (f'<table style="border-collapse:collapse;font-size:0.85em;width:100%">'
               f'<tr>'
               f'<th style="{_thst};text-align:left">Fraktion</th>'
               f'<th style="{_thst};text-align:right">t/h</th>'
               f'<th style="{_thst};text-align:right">t/a</th>'
               f'<th style="{_thst};text-align:right">Reinheit</th>'
               f'<th style="{_thst};text-align:right">€/t</th>'
               f'<th style="{_thst};text-align:right">k€/a</th>'
               f'</tr>{_rows}</table>')

    # Wirtschaftlichkeit
    _amort = f"{_sr['amort']:.1f} a" if _sr["amort"] else "kein Gewinn"
    _amc = "c-ok" if (_sr["amort"] and _sr["amort"] < 5) else ("c-w" if _sr["amort"] else "c-d")
    _deckc = "c-ok" if _sr["deckung_a"] > 0 else "c-d"

    _body = mo.Html(f'''<div class="pls">
      <div class="pls-c" style="overflow-x:auto"><h3>Verfahrensfließbild (aktive Konfiguration)</h3>
        {_fliessbild()}
        <p style="color:#8497ab;font-size:0.8em;margin-top:6px">Grüne Ausschleusungen = verkaufsfähige Wertstofffraktionen · graue = Reststoffe. Reinheit &lt; 50 % ⇒ nicht vermarktbar.</p>
      </div>
      <div class="pls-g2">
        <div class="pls-c"><h3>⚖️ Massen- &amp; Erlösbilanz</h3>{_bilanz}
          <p style="color:#8497ab;font-size:0.78em;margin-top:6px">€/t = effektiver Erlös nach Reinheitsabschlag (Reststoffe: Entsorgungskosten). k€/a bei {s_stunden.value:,} h/a.</p>
        </div>
        <div class="pls-c"><h3>💶 Wirtschaftlichkeit (Richtwerte)</h3>
          {vtbl(
              vr("Durchsatz", f"{_sr['t_a']:,.0f}", "t/a")
              + vr("Investition", f"{_sr['inv']/1000:,.0f}", "k€")
              + vr("Erlöse Wertstoffe", f"{_sr['erloes_a']/1000:,.0f}", "k€/a", "c-ok")
              + vr("Entsorgung Reste", f"{_sr['entsorg_a']/1000:,.0f}", "k€/a", "c-d")
              + vr("Betriebskosten", f"{_sr['betrieb_a']/1000:,.0f}", "k€/a", "c-w")
          )}
          <div class="pls-sep"></div>
          {vtbl(
              vr("Deckungsbeitrag", f"{_sr['deckung_a']/1000:,.0f}", "k€/a", _deckc)
              + vr("Amortisation", _amort, "", _amc)
          )}
          <p style="color:#8497ab;font-size:0.78em;margin-top:6px">Betriebskosten = Energie ({_sr['kw']:.0f} kW) + Personal (3 VZ) + Wartung (4 % Invest) + Overhead. Ohne Finanzierung, Transport, Annahmeentgelte, Preisschwankungen.</p>
        </div>
      </div>
    </div>''')

    # Grundriss-Planer – eigenständige Seite (Drag & Drop), per Link geöffnet
    _grundriss_head = mo.Html(f'''<div class="pls"><div class="pls-c" style="border-color:#00cec9">
        <h3>📐 Grundriss-Planer – Halle 40 m × 20 m (interaktiv)</h3>
        <div class="pls-soon">
          Aggregate aus der Palette anklicken (fügt eine maßstäbliche Box ein) oder eigene Box mit L × B erstellen,
          dann per Ziehen platzieren. Doppelklick dreht um 90°, ✕ löscht. Wartungsabstände und Verkehrswege planen
          die Teilgruppen selbst.
          <div style="margin:10px 0">
            <a href="{GRUNDRISS_URL}" target="_blank" rel="noopener"
               style="display:inline-block;background:#00cec9;color:#0a1428;font-weight:bold;text-decoration:none;
               padding:12px 24px;border-radius:6px;font-family:monospace;font-size:1.05em">
               📐 Grundriss-Planer öffnen ▸</a>
          </div>
          <span style="color:#8497ab;font-size:0.85em">Öffnet den Planer in einem neuen Tab (volle Fläche zum Planen).
          Führt der Link ins Leere, ist oben in der Datei die Konstante <b>GRUNDRISS_URL</b> auf die Deploy-Adresse
          der Planer-Seite zu setzen.</span>
        </div>
    </div></div>''')

    _seqhead = mo.Html('<div class="pls"><div class="pls-c" style="margin-bottom:6px;padding:8px 12px">'
                       '<b style="color:#74b9ff">🔧 Verfahrenskonzept – Aggregate frei anordnen</b>'
                       '<span style="color:#8497ab;font-size:0.85em">&ensp;(Positionen von links nach rechts = Durchlaufreihenfolge · Doppelbelegung wird ignoriert)</span>'
                       '</div></div>')
    sortierung = mo.vstack([
        _ctx,
        mo.hstack([s_preset, s_durchsatz, s_stunden], justify="start", gap=1, wrap=True),
        _seqhead,
        mo.hstack([s_pos1, s_pos2, s_pos3, s_pos4, s_pos5], justify="start", gap=1, wrap=True),
        mo.hstack([s_pos6, s_pos7, s_pos8, s_pos9], justify="start", gap=1, wrap=True),
        _body,
        _grundriss_head,
    ])

    vergaerung = geruest(
        "🌱 Vergärung & Kompostierung",
        "Anaerobe Biologie – verwandt mit dem Faulturm der Kläranlage: Raumbelastung, Verweilzeit und "
        "Temperatur bestimmen Biogasausbeute (→ BHKW) und Gärrest (→ Kompostierung).",
        ["Annahme / Voraufbereitung",
         "Fermenter (Temperatur, Verweilzeit, Raumbelastung)",
         "Biogas & BHKW (CH₄-Gehalt, Stromertrag)",
         "Kompostierung (Rotte, Reifegrad)"])

    deponie = geruest(
        "⛰️ Deponie (DK II)",
        "Schwerpunkt Sickerwasser – die direkte fachliche Brücke zur Abwasserbehandlung. "
        "Authentizitätshinweis: Eine reale DK-II-Deponie nimmt bewusst nur reaktionsarme, "
        "nicht gasbildende Stoffe auf; für die Sickerwasser-Lernsituationen empfiehlt sich daher ein "
        "bewusst als „klassisch“ benanntes Deponie-Modell.",
        ["Einbau (Schlacke, Bauschutt, mineralische Abfälle)",
         "Sickerwasser (Menge & Beschaffenheit → Behandlung)",
         "Deponiegas (sofern modelliert)",
         "Setzung / Nachsorge"])

    energie = geruest(
        "🔌 Energie & Klärschlamm",
        "Energetische Verknüpfung des Betriebs: Dampf aus der MVA → Turbine → Strom und Fernwärme; "
        "Biogas → BHKW. Die Klärschlammtrocknung verbindet das AEZ wörtlich mit der Kläranlage "
        "(Schlamm wird angeliefert, getrocknet und mitverbrannt).",
        ["Dampf / Turbine (Wirkungsgrade, KWK)",
         "Fernwärmenetz (Abnahme, Vorlauf/Rücklauf)",
         "Klärschlammtrocknung (TS-Anhebung, Wärmebedarf)"])

    labor = geruest(
        "🔬 Labor",
        "Zentrale Eigenüberwachung des Verbunds – die analytische Klammer über alle Anlagen.",
        ["Eigenüberwachung (Probenahme, Protokolle)",
         "Emissionsanalytik (kontinuierlich & periodisch)",
         "Sickerwasser- & Eluatanalytik"])

    fliessschema = mo.Html('''<div class="pls"><div class="pls-c">
        <h3>📐 R&I-Fließschema <span class="pls-badge">in Vorbereitung</span></h3>
        <div class="pls-soon">Hier wird – analog zur Kläranlage – ein DIN EN ISO 10628-konformes
        R&I-Fließschema des AEZ eingebettet, mit Referenz- und Aufgabenversion (bewusste Fehler).</div>
    </div></div>''')

    # ---------- Tab-Assemblierung (Hub-Struktur) ----------
    tabs = mo.ui.tabs({
        "🏭 Gesamtbetrieb": mo.ui.tabs({
            "Übersicht": overview,
            "Fließschema": fliessschema,
        }, lazy=True),
        "🔥 MVA": mva,
        "🔀 Sortierung": sortierung,
        "🌱 Vergärung & Kompost": vergaerung,
        "⛰️ Deponie": deponie,
        "🔌 Energie & Klärschlamm": energie,
        "🔬 Labor": labor,
    }, lazy=True)

    # Leitstand-Kontrollzentrum über den Tabs
    kontroll_kopf = mo.Html('''<div class="pls"><div class="pls-hdr" style="margin-bottom:8px">
        <h2 style="font-size:1.15em">🎛️ Kontrollzentrum – Betriebsvorgaben</h2>
        <div class="pls-st"><span style="color:#8497ab;font-size:0.82em">Anlieferungsmengen, Heizwert und Niederschlag steuern die Live-Bilanz der Übersicht</span></div>
    </div></div>''')
    panel = mo.vstack([
        kontroll_kopf,
        mo.hstack([muell_t, sortier_t, bio_t], justify="start", gap=2, wrap=True),
        mo.hstack([ks_t, heizwert, niederschlag], justify="start", gap=2, wrap=True),
    ])

    mo.output.replace(mo.vstack([mo.Html(hdr), panel, tabs]))
    return


if __name__ == "__main__":
    app.run()
