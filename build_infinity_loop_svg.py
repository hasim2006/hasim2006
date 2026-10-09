import os
import math
import xml.etree.ElementTree as ET

output_dir = r"c:\Users\hasim\OneDrive\Desktop\github'\hasim2006"
os.makedirs(output_dir, exist_ok=True)

def build_infinity_loop_svg(theme="dark"):
    is_dark = (theme == "dark")
    bg_col = "#0A101F" if is_dark else "#F8FAFC"
    card_bg = "#070c17" if is_dark else "#FFFFFF"
    border_col = "#1E293B" if is_dark else "#E2E8F0"
    chrome_col = "#22D3EE" if is_dark else "#0891B2"
    purple_col = "#A78BFA" if is_dark else "#7C3AED"
    accent_purple = "#8B5CF6"
    emerald_col = "#10B981"
    amber_col = "#F59E0B"
    text_muted = "#64748B"
    text_label = "#94A3B8" if is_dark else "#475569"
    text_val = "#F8FAFC" if is_dark else "#0F172A"
    grid_dot = "#1E293B" if is_dark else "#E2E8F0"

    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 440" width="100%" height="100%">')
    svg.append('<defs>')

    # Gradients & Filters
    svg.append(f'''
      <linearGradient id="infGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="{chrome_col}"/>
        <stop offset="35%" stop-color="#38BDF8"/>
        <stop offset="50%" stop-color="{accent_purple}"/>
        <stop offset="65%" stop-color="{purple_col}"/>
        <stop offset="100%" stop-color="{emerald_col}"/>
      </linearGradient>

      <linearGradient id="cometGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1"/>
        <stop offset="40%" stop-color="{chrome_col}" stop-opacity="0.8"/>
        <stop offset="100%" stop-color="{chrome_col}" stop-opacity="0"/>
      </linearGradient>

      <radialGradient id="centerAura" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{accent_purple}" stop-opacity="0.35"/>
        <stop offset="60%" stop-color="{chrome_col}" stop-opacity="0.10"/>
        <stop offset="100%" stop-color="{accent_purple}" stop-opacity="0"/>
      </radialGradient>

      <radialGradient id="leftAura" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{chrome_col}" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="{chrome_col}" stop-opacity="0"/>
      </radialGradient>

      <radialGradient id="rightAura" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{emerald_col}" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="{emerald_col}" stop-opacity="0"/>
      </radialGradient>

      <pattern id="canvasDots" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
        <circle cx="12" cy="12" r="1.1" fill="{grid_dot}" opacity="0.8"/>
      </pattern>
    ''')

    svg.append('<style>')
    svg.append(f'''
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&amp;display=swap');
      text {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}
      .title {{ fill: {text_muted}; font-size: 13px; font-weight: 500; }}
      .sec-hdr {{ fill: {accent_purple}; font-size: 13px; font-weight: 700; letter-spacing: 1.5px; }}
      .node-hdr {{ font-size: 12px; font-weight: 700; }}
      .node-sub {{ font-size: 10px; font-weight: 500; fill: {text_label}; }}
      .pill-text {{ fill: {accent_purple}; font-size: 12px; font-weight: 700; }}
      .pill-bg {{ fill: {accent_purple}1F; stroke: {accent_purple}; stroke-width: 1; }}
    ''')
    svg.append('</style>')
    svg.append('</defs>')

    # 1. Background Frame
    svg.append(f'<rect width="1180" height="440" rx="14" fill="{bg_col}" stroke="{border_col}" stroke-width="1.5"/>')

    # Top Header Bar
    svg.append(f'<line x1="0" y1="44" x2="1180" y2="44" stroke="{border_col}" stroke-width="1"/>')
    svg.append('<circle cx="26" cy="22" r="5.5" fill="#EF4444"/>')
    svg.append('<circle cx="44" cy="22" r="5.5" fill="#F59E0B"/>')
    svg.append('<circle cx="62" cy="22" r="5.5" fill="#10B981"/>')
    svg.append(f'<text x="590" y="27" text-anchor="middle" class="title">lifecycle.sh --infinite-loop</text>')

    # Top Right Pill
    svg.append('<g>')
    svg.append(f'<rect x="990" y="10" width="168" height="24" rx="12" class="pill-bg"/>')
    svg.append(f'<circle cx="1006" cy="22" r="4" fill="{accent_purple}">')
    svg.append('<animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>')
    svg.append('</circle>')
    svg.append(f'<text x="1080" y="26" text-anchor="middle" class="pill-text">∞ INFINITE FLOW</text>')
    svg.append('</g>')

    # Header Subtitle
    svg.append(f'<text x="36" y="74" class="sec-hdr">CONTINUOUS.LIFECYCLE</text>')
    svg.append(f'<text x="245" y="74" fill="{text_muted}" font-size="11">· NEVER-ENDING DEVELOPMENT &amp; DELIVERY LOOP · CODE → SHIP → REPEAT</text>')

    # Main Inner Canvas
    svg.append(f'<rect x="34" y="88" width="1112" height="300" rx="10" fill="{card_bg}" stroke="{border_col}" stroke-width="1"/>')
    svg.append(f'<rect x="34" y="88" width="1112" height="300" rx="10" fill="url(#canvasDots)"/>')

    # Background glowing auras
    cx, cy = 590, 235
    svg.append(f'<circle cx="{cx - 280}" cy="{cy}" r="140" fill="url(#leftAura)"/>')
    svg.append(f'<circle cx="{cx + 280}" cy="{cy}" r="140" fill="url(#rightAura)"/>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="150" fill="url(#centerAura)"/>')

    # =========================================================================
    # THE INFINITY LOOP (Lemniscate Cubic Beziers)
    # Center: (590, 235)
    # Left apex: (270, 235)
    # Right apex: (910, 235)
    # =========================================================================
    # Path:
    # Start at center (590, 235), loop around right wing, cross center, loop around left wing, return to center.
    inf_d = f"M {cx} {cy} C {cx + 140} {cy - 125}, {cx + 340} {cy - 125}, {cx + 340} {cy} C {cx + 340} {cy + 125}, {cx + 140} {cy + 125}, {cx} {cy} C {cx - 140} {cy - 125}, {cx - 340} {cy - 125}, {cx - 340} {cy} C {cx - 340} {cy + 125}, {cx - 140} {cy + 125}, {cx} {cy} Z"

    # Outer faint glow tube
    svg.append(f'<path d="{inf_d}" stroke="url(#infGrad)" stroke-width="12" stroke-linecap="round" fill="none" opacity="0.18"/>')
    # Medium glow track
    svg.append(f'<path d="{inf_d}" stroke="url(#infGrad)" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.65"/>')
    # Core sharp laser rail
    svg.append(f'<path d="{inf_d}" stroke="#F8FAFC" stroke-width="1.8" stroke-linecap="round" fill="none" opacity="0.9"/>')

    # Traveling Energy Comet 1 (moving along the infinity figure-8)
    svg.append(f'''
      <!-- Traveling Particle Pulse 1 -->
      <g>
        <circle r="5" fill="#FFFFFF">
          <animateMotion path="{inf_d}" dur="4.6s" repeatCount="indefinite"/>
        </circle>
        <circle r="12" fill="{chrome_col}" opacity="0.5">
          <animateMotion path="{inf_d}" dur="4.6s" repeatCount="indefinite"/>
        </circle>
      </g>
      
      <!-- Traveling Particle Pulse 2 (Half phase shifted) -->
      <g>
        <circle r="4.5" fill="#FFFFFF">
          <animateMotion path="{inf_d}" dur="4.6s" begin="2.3s" repeatCount="indefinite"/>
        </circle>
        <circle r="11" fill="{accent_purple}" opacity="0.5">
          <animateMotion path="{inf_d}" dur="4.6s" begin="2.3s" repeatCount="indefinite"/>
        </circle>
      </g>
    ''')

    # Micro trailing stars along infinity curve
    for i in range(12):
        t_phase = (i / 12) * 4.6
        svg.append(f'''
          <circle r="2.2" fill="{chrome_col}">
            <animateMotion path="{inf_d}" dur="4.6s" begin="{t_phase:.2f}s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.8; 0.2; 0.8" dur="1.8s" repeatCount="indefinite"/>
          </circle>
        ''')

    # =========================================================================
    # NODES ON THE INFINITY LOOP
    # =========================================================================
    # Nodes on Left Wing:
    # 1. PLAN (390, 145)
    # 2. CODE (250, 235)
    # 3. BUILD (390, 325)
    
    # Nodes on Right Wing:
    # 4. TEST (790, 145)
    # 5. DEPLOY (930, 235)
    # 6. MONITOR (790, 325)
    
    nodes = [
        # (name, sub, x, y, col)
        ("PLAN", "ARCHITECT", cx - 200, cy - 88, chrome_col),
        ("CODE", "PYTHON · REACT", cx - 340, cy, chrome_col),
        ("BUILD", "NEXT.JS · VITE", cx - 200, cy + 88, "#38BDF8"),
        
        ("TEST", "VERIFY &amp; BENCH", cx + 200, cy - 88, purple_col),
        ("DEPLOY", "VERCEL · CLOUD", cx + 340, cy, emerald_col),
        ("MONITOR", "METRICS &amp; LOGS", cx + 200, cy + 88, amber_col),
    ]

    for label, sub, nx, ny, ncol in nodes:
        svg.append(f'''
          <g transform="translate({nx}, {ny})">
            <!-- Node Outer Glow -->
            <circle r="18" fill="{ncol}22" stroke="{ncol}" stroke-width="1.8"/>
            <circle r="5" fill="{ncol}">
              <animate attributeName="r" values="4; 6.5; 4" dur="2s" repeatCount="indefinite"/>
            </circle>
            <!-- Label -->
            <text x="0" y="-24" text-anchor="middle" fill="{text_val}" class="node-hdr">{label}</text>
            <text x="0" y="32" text-anchor="middle" class="node-sub">{sub}</text>
          </g>
        ''')

    # =========================================================================
    # MASTER CROSSOVER NODE AT CENTER: HASIM.CORE
    # (590, 235)
    # =========================================================================
    svg.append(f'''
      <g transform="translate({cx}, {cy})">
        <!-- Concentric Pulsing Ring -->
        <circle r="36" fill="none" stroke="{accent_purple}" stroke-width="1.5" opacity="0.7">
          <animate attributeName="r" values="32; 44; 32" dur="2.4s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.7; 0.15; 0.7" dur="2.4s" repeatCount="indefinite"/>
        </circle>
        
        <circle r="26" fill="{card_bg}" stroke="{chrome_col}" stroke-width="2.2"/>
        <circle r="20" fill="{accent_purple}33"/>
        <circle r="9" fill="{accent_purple}">
          <animate attributeName="fill" values="{accent_purple}; {chrome_col}; {accent_purple}" dur="3.6s" repeatCount="indefinite"/>
        </circle>
        
        <!-- Center Emblem / Text -->
        <text x="0" y="3" text-anchor="middle" fill="{text_val}" font-size="10" font-weight="700">CI / CD</text>
        <text x="0" y="-36" text-anchor="middle" fill="{accent_purple}" font-size="12" font-weight="700" letter-spacing="1.5">⚡ HASIM.CORE</text>
        <text x="0" y="48" text-anchor="middle" fill="{text_label}" font-size="9.5" font-weight="600">CONTINUOUS SHIP ENGINE</text>
      </g>
    ''')

    # Bottom status bar inside canvas
    svg.append(f'<line x1="34" y1="358" x2="1146" y2="358" stroke="{border_col}" stroke-width="1"/>')
    svg.append(f'''
      <g font-size="11" fill="{text_muted}">
        <text x="50" y="375">TOPOLOGY: INFINITE LEMNISCATE · CYCLE DURATION: 4.6s · ACTIVE NODES: 6 DOMAINS</text>
        <text x="1130" y="375" text-anchor="end" fill="{emerald_col}">● ZERO DOWNTIME PIPELINE (100% OK)</text>
      </g>
    ''')

    # Bottom footer line outside canvas
    svg.append(f'''
      <text x="44" y="418" fill="{text_muted}" font-size="11">INFINITE.DEV v3.0 · NEVER-ENDING EXPANSION · GITHUB PROFILE HASIM2006</text>
      <text x="1136" y="418" text-anchor="end" fill="{chrome_col}" font-size="11" font-weight="600">IDEATE · BUILD · SHIP · REPEAT</text>
    ''')

    svg.append('</svg>')
    return "\n".join(svg)

print("Building infinity_loop_dark.svg and infinity_loop_light.svg...")
inf_dark = build_infinity_loop_svg("dark")
inf_light = build_infinity_loop_svg("light")

# Validate XML
ET.fromstring(inf_dark)
ET.fromstring(inf_light)
print("XML validation PASSED for Infinity Loop SVGs!")

dark_path = os.path.join(output_dir, "infinity_loop_dark.svg")
light_path = os.path.join(output_dir, "infinity_loop_light.svg")

with open(dark_path, "w", encoding="utf-8") as f:
    f.write(inf_dark)
with open(light_path, "w", encoding="utf-8") as f:
    f.write(inf_light)

print(f"Generated {dark_path} ({len(inf_dark)/1024:.1f} KB)")
print(f"Generated {light_path} ({len(inf_light)/1024:.1f} KB)")
