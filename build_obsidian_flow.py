import os
import math
import xml.etree.ElementTree as ET

output_dir = r"c:\Users\hasim\OneDrive\Desktop\github'\hasim2006"
os.makedirs(output_dir, exist_ok=True)

def build_obsidian_flow(theme="dark"):
    is_dark = (theme == "dark")
    bg_col = "#0A101F" if is_dark else "#F8FAFC"
    card_bg = "#070c17" if is_dark else "#FFFFFF"
    border_col = "#1E293B" if is_dark else "#E2E8F0"
    chrome_col = "#22D3EE" if is_dark else "#0891B2"
    purple_col = "#A78BFA" if is_dark else "#7C3AED"
    obsidian_purple = "#8B5CF6"
    emerald_col = "#10B981"
    amber_col = "#F59E0B"
    text_muted = "#64748B"
    text_label = "#94A3B8" if is_dark else "#475569"
    text_val = "#F8FAFC" if is_dark else "#0F172A"
    grid_dot = "#1E293B" if is_dark else "#E2E8F0"

    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 540" width="100%" height="100%">')
    svg.append('<defs>')
    
    # Gradients
    svg.append(f'''
      <radialGradient id="centerGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{obsidian_purple}" stop-opacity="0.30"/>
        <stop offset="60%" stop-color="{chrome_col}" stop-opacity="0.08"/>
        <stop offset="100%" stop-color="{obsidian_purple}" stop-opacity="0"/>
      </radialGradient>
      
      <radialGradient id="nodeGlowCyan" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{chrome_col}" stop-opacity="0.4"/>
        <stop offset="100%" stop-color="{chrome_col}" stop-opacity="0"/>
      </radialGradient>
      
      <radialGradient id="nodeGlowPurple" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{obsidian_purple}" stop-opacity="0.4"/>
        <stop offset="100%" stop-color="{obsidian_purple}" stop-opacity="0"/>
      </radialGradient>
      
      <radialGradient id="nodeGlowGreen" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{emerald_col}" stop-opacity="0.4"/>
        <stop offset="100%" stop-color="{emerald_col}" stop-opacity="0"/>
      </radialGradient>
      
      <radialGradient id="nodeGlowAmber" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="{amber_col}" stop-opacity="0.4"/>
        <stop offset="100%" stop-color="{amber_col}" stop-opacity="0"/>
      </radialGradient>
      
      <pattern id="dotPattern" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
        <circle cx="12" cy="12" r="1.1" fill="{grid_dot}" opacity="0.8"/>
      </pattern>
    ''')
    
    svg.append('<style>')
    svg.append(f'''
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&amp;display=swap');
      text {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}
      .title {{ fill: {text_muted}; font-size: 13px; font-weight: 500; }}
      .sec-hdr {{ fill: {obsidian_purple}; font-size: 13px; font-weight: 700; letter-spacing: 1.5px; }}
      .node-lbl {{ font-size: 12px; font-weight: 700; }}
      .sub-lbl {{ font-size: 10px; font-weight: 500; fill: {text_label}; }}
      .pill-text {{ fill: {obsidian_purple}; font-size: 12px; font-weight: 600; }}
      .obs-badge {{ fill: {obsidian_purple}1F; stroke: {obsidian_purple}; stroke-width: 1; }}
    ''')
    svg.append('</style>')
    svg.append('</defs>')
    
    # 1. Main Background Container
    svg.append(f'<rect width="1180" height="540" rx="14" fill="{bg_col}" stroke="{border_col}" stroke-width="1.5"/>')
    
    # Header bar
    svg.append(f'<line x1="0" y1="44" x2="1180" y2="44" stroke="{border_col}" stroke-width="1"/>')
    
    # Traffic lights
    svg.append('<circle cx="26" cy="22" r="5.5" fill="#EF4444"/>')
    svg.append('<circle cx="44" cy="22" r="5.5" fill="#F59E0B"/>')
    svg.append('<circle cx="62" cy="22" r="5.5" fill="#10B981"/>')
    
    # Header Title
    svg.append(f'<text x="590" y="27" text-anchor="middle" class="title">obsidian://vault/hasim2006/knowledge-graph.canvas</text>')
    
    # Obsidian Vault Badge on Right
    svg.append('<g>')
    svg.append(f'<rect x="990" y="10" width="168" height="24" rx="12" class="obs-badge"/>')
    svg.append(f'<circle cx="1006" cy="22" r="4" fill="{obsidian_purple}">')
    svg.append('<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>')
    svg.append('</circle>')
    svg.append(f'<text x="1080" y="26" text-anchor="middle" class="pill-text">OBSIDIAN GRAPH</text>')
    svg.append('</g>')
    
    # Top subtitle
    svg.append(f'<text x="36" y="74" class="sec-hdr">OBSIDIAN.FLOW</text>')
    svg.append(f'<text x="175" y="74" fill="{text_muted}" font-size="11">· NEURAL TECH ARCHITECTURE · FORCE-DIRECTED TOPOLOGY</text>')
    
    # Canvas frame
    svg.append(f'<rect x="34" y="88" width="1112" height="400" rx="10" fill="{card_bg}" stroke="{border_col}" stroke-width="1"/>')
    # Background dot grid inside canvas
    svg.append(f'<rect x="34" y="88" width="1112" height="400" rx="10" fill="url(#dotPattern)"/>')
    
    # Center ambient glow
    cx, cy = 590, 288
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="220" fill="url(#centerGlow)"/>')
    
    # =========================================================================
    # GRAPH TOPOLOGY: Nodes and Edges
    # =========================================================================
    
    # Center: HASIM.CORE
    # 4 Main Clusters:
    # 1. Frontend (top-left): (280, 185)
    # 2. Backend (top-right): (900, 185)
    # 3. Database (bottom-left): (290, 395)
    # 4. DevOps & Cloud (bottom-right): (890, 395)
    
    clusters = [
        ("frontend", 280, 185, chrome_col, "url(#nodeGlowCyan)"),
        ("backend", 900, 185, purple_col, "url(#nodeGlowPurple)"),
        ("database", 290, 395, emerald_col, "url(#nodeGlowGreen)"),
        ("devops", 890, 395, amber_col, "url(#nodeGlowAmber)"),
    ]
    
    satellites = {
        "frontend": [
            ("React 18", 120, 140, "UI Engine"),
            ("Next.js 14", 230, 115, "Full-Stack SPA"),
            ("TailwindCSS", 120, 230, "Utility Styles"),
            ("TypeScript", 230, 260, "Typed Safety"),
        ],
        "backend": [
            ("Python 3.12", 1060, 140, "Core Logic"),
            ("FastAPI", 950, 115, "Async APIs"),
            ("Node.js", 1060, 230, "V8 Engine"),
            ("Express", 950, 260, "Middleware"),
        ],
        "database": [
            ("MongoDB", 120, 360, "NoSQL Atlas"),
            ("MySQL", 180, 445, "Relational"),
            ("Firebase", 300, 455, "Real-Time DB"),
            ("REST APIs", 410, 420, "Endpoints"),
        ],
        "devops": [
            ("AWS &amp; GCP", 1060, 360, "Cloud Infra"),
            ("Vercel", 1000, 445, "Edge Edge"),
            ("Git &amp; GitHub", 880, 455, "Version Flow"),
            ("Postman", 770, 420, "API Testing"),
        ]
    }
    
    # 1. Draw Edges from Center to Clusters with flow animation
    for name, cl_x, cl_y, col, glow in clusters:
        # Curved bezier line
        # Control point slightly bowed
        mid_x = (cx + cl_x) / 2
        mid_y = (cy + cl_y) / 2 + (20 if cl_y > cy else -20)
        path_d = f"M {cx} {cy} Q {mid_x} {mid_y} {cl_x} {cl_y}"
        
        # Base faint line
        svg.append(f'<path d="{path_d}" stroke="{col}" stroke-width="1.8" opacity="0.3" fill="none"/>')
        
        # Animated pulse line
        svg.append(f'''
          <path d="{path_d}" stroke="{col}" stroke-width="2.2" stroke-dasharray="8 16" fill="none">
            <animate attributeName="stroke-dashoffset" values="0; -96" dur="2.4s" repeatCount="indefinite"/>
          </path>
        ''')
        
        # Traveling particle along path
        svg.append(f'''
          <circle r="3.2" fill="{col}">
            <animateMotion path="{path_d}" dur="2.4s" repeatCount="indefinite"/>
          </circle>
        ''')
        
    # 2. Draw Edges from Clusters to Satellites
    for cl_name, cl_x, cl_y, col, glow in clusters:
        for sat_label, sat_x, sat_y, sat_sub in satellites[cl_name]:
            path_d = f"M {cl_x} {cl_y} L {sat_x} {sat_y}"
            svg.append(f'<path d="{path_d}" stroke="{col}" stroke-width="1" stroke-dasharray="3 4" opacity="0.4" fill="none"/>')
            
            # Sub-pulse
            svg.append(f'''
              <path d="{path_d}" stroke="{col}" stroke-width="1.4" stroke-dasharray="4 12" opacity="0.8" fill="none">
                <animate attributeName="stroke-dashoffset" values="0; -48" dur="3.2s" repeatCount="indefinite"/>
              </path>
            ''')
            
            # Traveling micro-dot
            svg.append(f'''
              <circle r="2" fill="{col}">
                <animateMotion path="{path_d}" dur="3.2s" repeatCount="indefinite"/>
              </circle>
            ''')

    # 3. Inter-cluster cross links (Obsidian knowledge web)
    cross_links = [
        (280, 185, 900, 185, obsidian_purple), # Frontend <-> Backend
        (280, 185, 290, 395, chrome_col),     # Frontend <-> Database
        (900, 185, 890, 395, purple_col),     # Backend <-> DevOps
        (290, 395, 890, 395, emerald_col),    # Database <-> DevOps
    ]
    for x1, y1, x2, y2, c in cross_links:
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1" stroke-dasharray="2 6" opacity="0.25"/>')

    # 4. Render Satellite Nodes
    for cl_name, cl_x, cl_y, col, glow in clusters:
        for sat_label, sat_x, sat_y, sat_sub in satellites[cl_name]:
            # Satellite node circle
            svg.append(f'<g transform="translate({sat_x}, {sat_y})">')
            svg.append(f'<circle r="14" fill="{card_bg}" stroke="{col}" stroke-width="1.5"/>')
            svg.append(f'<circle r="4.5" fill="{col}">')
            svg.append('<animate attributeName="r" values="4; 5.5; 4" dur="2.8s" repeatCount="indefinite"/>')
            svg.append('</circle>')
            
            # Label
            svg.append(f'<text x="0" y="-18" text-anchor="middle" fill="{text_val}" font-size="11" font-weight="600">{sat_label}</text>')
            svg.append(f'<text x="0" y="27" text-anchor="middle" class="sub-lbl">{sat_sub}</text>')
            svg.append('</g>')

    # 5. Render Cluster Master Nodes
    for cl_name, cl_x, cl_y, col, glow in clusters:
        svg.append(f'<g transform="translate({cl_x}, {cl_y})">')
        svg.append(f'<circle r="48" fill="{glow}"/>')
        svg.append(f'<circle r="26" fill="{card_bg}" stroke="{col}" stroke-width="2"/>')
        svg.append(f'<circle r="20" fill="{col}1F"/>')
        svg.append(f'<circle r="7" fill="{col}">')
        svg.append('<animate attributeName="r" values="6; 8.5; 6" dur="2s" repeatCount="indefinite"/>')
        svg.append('</circle>')
        
        title_text = {
            "frontend": "FRONTEND.FLOW",
            "backend": "BACKEND.FLOW",
            "database": "DATABASE.FLOW",
            "devops": "DEVOPS.FLOW"
        }[cl_name]
        
        svg.append(f'<text x="0" y="-34" text-anchor="middle" fill="{col}" font-size="12" font-weight="700" letter-spacing="1">{title_text}</text>')
        svg.append('</g>')

    # 6. Render Central Master Hub: HASIM.CORE
    svg.append(f'<g transform="translate({cx}, {cy})">')
    # Pulse rings
    svg.append(f'''
      <circle r="38" fill="none" stroke="{obsidian_purple}" stroke-width="1.5" opacity="0.8">
        <animate attributeName="r" values="36; 48; 36" dur="3s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.8; 0.1; 0.8" dur="3s" repeatCount="indefinite"/>
      </circle>
      <circle r="34" fill="{card_bg}" stroke="{chrome_col}" stroke-width="2.5"/>
      <circle r="28" fill="{obsidian_purple}22"/>
      <circle r="12" fill="{chrome_col}">
        <animate attributeName="fill" values="{chrome_col}; {obsidian_purple}; {chrome_col}" dur="4s" repeatCount="indefinite"/>
      </circle>
      
      <!-- Center Labels -->
      <text x="0" y="4" text-anchor="middle" fill="{text_val}" font-size="11" font-weight="700">CORE</text>
      <text x="0" y="-44" text-anchor="middle" fill="{chrome_col}" font-size="13" font-weight="700" letter-spacing="1.5">⚡ HASIM.BRAIN</text>
      <text x="0" y="58" text-anchor="middle" fill="{text_label}" font-size="10.5" font-weight="500">FULL-STACK KNOWLEDGE GRAPH</text>
    ''')
    svg.append('</g>')
    
    # Status bar at bottom inside canvas
    svg.append(f'<line x1="34" y1="460" x2="1146" y2="460" stroke="{border_col}" stroke-width="1"/>')
    svg.append(f'''
      <g font-size="11" fill="{text_muted}">
        <text x="50" y="478">VAULT: mohammad-hasim · ENGINE: OBSIDIAN CANVAS · TOPOLOGY: BIPARTITE GRAPH</text>
        <text x="1130" y="478" text-anchor="end" fill="{emerald_col}">● ALL 18 NODES ACTIVE &amp; SYNCED (100%)</text>
      </g>
    ''')
    
    # Bottom info line outside canvas (y=518)
    svg.append(f'''
      <text x="44" y="518" fill="{text_muted}" font-size="11">OBSIDIAN.FLOW v2.4 · 24 LINKS · REAL-TIME DATA PROPAGATION · REPO: hasim2006/hasim2006</text>
      <text x="1136" y="518" text-anchor="end" fill="{obsidian_purple}" font-size="11" font-weight="600">CONNECTED SECOND BRAIN</text>
    ''')

    svg.append('</svg>')
    return "\n".join(svg)

print("Building obsidian_flow_dark.svg and obsidian_flow_light.svg...")
obs_dark = build_obsidian_flow("dark")
obs_light = build_obsidian_flow("light")

# Validate XML
ET.fromstring(obs_dark)
ET.fromstring(obs_light)
print("XML validation PASSED for obsidian flow SVGs!")

dark_path = os.path.join(output_dir, "obsidian_flow_dark.svg")
light_path = os.path.join(output_dir, "obsidian_flow_light.svg")

with open(dark_path, "w", encoding="utf-8") as f:
    f.write(obs_dark)
with open(light_path, "w", encoding="utf-8") as f:
    f.write(obs_light)

print(f"Generated {dark_path} ({len(obs_dark)/1024:.1f} KB)")
print(f"Generated {light_path} ({len(obs_light)/1024:.1f} KB)")
