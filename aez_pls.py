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
    # Deploy-URL der MVA-Spoke-App (mva_pls). Nach dem Deployment hier die
    # echte GitHub-Pages-URL eintragen – der Link im Lageplan und im MVA-Tab
    # zeigt dann direkt auf die Simulation.
    MVA_URL = "https://thurin27.github.io/mva_pls/"
    return (MVA_URL,)


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
def _(MVA_URL, bio_t, heizwert, ks_t, mo, muell_t, niederschlag, sortier_t):
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

    def vr(label, val, unit, **kw):
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
        <h2>♻️ Abfallentsorgungszentrum Asdonkshof – Leitstand</h2>
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

    def flow(x1, y1, x2, y2, label="", dash=False, col="#0984e3"):
        d = ' stroke-dasharray="5,3"' if dash else ""
        seg = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" '
               f'stroke-width="2.5" marker-end="url(#ah)"{d}/>')
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 4
            seg += f'<text x="{mx}" y="{my}" fill="#9fb3c8" text-anchor="middle" font-size="9" font-family="monospace">{label}</text>'
        return seg

    def flow_path(pts, label="", dash=False, col="#0984e3", lx=None, ly=None):
        # orthogonale Leitungsführung über Stützpunkte (saubere Korridore)
        d = ' stroke-dasharray="5,3"' if dash else ""
        pstr = " ".join(f"{x},{y}" for x, y in pts)
        seg = (f'<polyline points="{pstr}" fill="none" stroke="{col}" '
               f'stroke-width="2.5" marker-end="url(#ah)"{d}/>')
        if label and lx is not None:
            seg += f'<text x="{lx}" y="{ly}" fill="#9fb3c8" text-anchor="middle" font-size="9" font-family="monospace">{label}</text>'
        return seg

    schema = f'''<svg viewBox="0 0 1240 720" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;background:#0a1428;border-radius:6px">
      <defs><marker id="ah" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#0984e3"/></marker></defs>

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

      <!-- Ströme: Anlieferung → Annahme -->
      {flow(150, 330, 210, 90, "Hausmüll")}
      {flow(150, 350, 210, 265, "Sperrmüll")}
      {flow(150, 375, 210, 455, "Bioabfall")}
      {flow(150, 400, 210, 595, "Klärschl.")}

      <!-- Annahme → Prozess -->
      {flow(360, 75, 440, 80, "")}
      {flow(360, 255, 440, 105, "")}
      <text x="378" y="248" fill="#9fb3c8" text-anchor="middle" font-size="9" font-family="monospace">Reststoff</text>
      {flow_path([(360, 595), (405, 595), (405, 132), (440, 132)], "Mitverbr.", dash=True, lx=405, ly=350)}
      {flow(360, 455, 440, 455, "")}

      <!-- MVA → RGR → Kamin -->
      {flow(610, 70, 690, 75, "Rohgas")}
      {flow(850, 75, 930, 75, "")}

      <!-- MVA → Energiezentrale (Dampf) -->
      {flow(525, 140, 700, 200, "Dampf", col="#e17055")}
      {flow(850, 245, 930, 245, "")}

      <!-- Vergärung → Energiezentrale (Biogas) + Kompost -->
      {flow(610, 440, 690, 280, "Biogas", dash=True, col="#00b894")}
      {flow(610, 470, 690, 445, "Gärrest")}

      <!-- MVA → Schlacke → Aufbereitung → Deponie -->
      {flow_path([(610, 120), (650, 120), (650, 595), (690, 595)], "Schlacke", col="#b2bec3", lx=668, ly=545)}
      {flow(850, 600, 930, 575, "")}

      <!-- Deponie → Sickerwasser -->
      {flow(1005, 630, 1005, 690, "Sickerwasser → Behandlung", dash=True, col="#74b9ff")}

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

    sortierung = geruest(
        "🔀 Sortieranlage (Vorschaltanlage)",
        "Massenbilanz-Simulation: Input-Tonnage und -Zusammensetzung → Abscheidegrade je Fraktion → "
        "Output mit Ausbeute und Restverschmutzung. Reststoff wird der MVA zugeführt.",
        ["Input (Mengen & Zusammensetzung)",
         "Aggregate (Magnet- / Wirbelstromabscheider · Sieb · NIR)",
         "Fraktionen & Ausbeute (Fe, NE, Holz, Kunststoff, Reststoff)"])

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
        "Hinweis zur Authentizität: Die reale Asdonkshof-Deponie nimmt bewusst nur reaktionsarme, "
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
