import os
import math
import xml.etree.ElementTree as ET

output_dir = r"c:\Users\hasim\OneDrive\Desktop\github'\hasim2006"
os.makedirs(output_dir, exist_ok=True)

def build_water_glass_svg(theme="dark"):
    is_dark = (theme == "dark")
    bg_col = "#0A101F" if is_dark else "#F8FAFC"
    card_bg = "#070c17" if is_dark else "#FFFFFF"
    border_col = "#1E293B" if is_dark else "#E2E8F0"
    chrome_col = "#22D3EE" if is_dark else "#0891B2"
    purple_col = "#A78BFA" if is_dark else "#7C3AED"
    emerald_col = "#10B981"
    amber_col = "#F59E0B"
    text_muted = "#64748B"
    text_label = "#94A3B8" if is_dark else "#475569"
    text_val = "#F8FAFC" if is_dark else "#0F172A"
    glass_stroke = "#67E8F9" if is_dark else "#0284C7"
    glass_rim = "#22D3EE" if is_dark else "#0EA5E9"
    water_fill_top = "#22D3EE"
    water_fill_mid = "#0284C7"
    water_fill_bot = "#0F172A" if is_dark else "#0369A1"

    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 540" width="100%" height="100%">')
    svg.append('<defs>')
    
    # Gradients & Filters
    svg.append(f'''
      <linearGradient id="waterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="{water_fill_top}" stop-opacity="0.85"/>
        <stop offset="40%" stop-color="{water_fill_mid}" stop-opacity="0.90"/>
        <stop offset="100%" stop-color="{water_fill_bot}" stop-opacity="0.95"/>
      </linearGradient>

      <linearGradient id="waveBackGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.5"/>
        <stop offset="100%" stop-color="{water_fill_mid}" stop-opacity="0.7"/>
      </linearGradient>

      <linearGradient id="glassSpecLeft" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.45"/>
        <stop offset="60%" stop-color="#FFFFFF" stop-opacity="0.1"/>
        <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
      </linearGradient>

      <linearGradient id="glassSpecRight" x1="100%" y1="0%" x2="0%" y2="0%">
        <stop offset="0%" stop-color="#67E8F9" stop-opacity="0.4"/>
        <stop offset="100%" stop-color="#67E8F9" stop-opacity="0"/>
      </linearGradient>

      <linearGradient id="nozzleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{purple_col}"/>
        <stop offset="100%" stop-color="{chrome_col}"/>
      </linearGradient>

      <radialGradient id="dropGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#A5F3FC" stop-opacity="1"/>
        <stop offset="60%" stop-color="{chrome_col}" stop-opacity="0.9"/>
        <stop offset="100%" stop-color="{chrome_col}" stop-opacity="0"/>
      </radialGradient>

      <radialGradient id="glassAura" cx="50%" cy="65%" r="50%">
        <stop offset="0%" stop-color="{chrome_col}" stop-opacity="0.18"/>
        <stop offset="60%" stop-color="{purple_col}" stop-opacity="0.06"/>
        <stop offset="100%" stop-color="{chrome_col}" stop-opacity="0"/>
      </radialGradient>

      <!-- Glass Clip Path for Liquid -->
      <!-- Glass inner silhouette: top width 216, bottom width 176, height 230 -->
      <clipPath id="glassInnerClip">
        <path d="M 232 230 
                 L 248 450 
                 Q 250 460 262 460 
                 L 418 460 
                 Q 430 460 432 450 
                 L 448 230 Z"/>
      </clipPath>
    ''')

    svg.append('<style>')
    svg.append(f'''
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&amp;display=swap');
      text {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}
      .title {{ fill: {text_muted}; font-size: 13px; font-weight: 500; }}
      .sec-hdr {{ fill: {chrome_col}; font-size: 13px; font-weight: 700; letter-spacing: 1.5px; }}
      .card-hdr {{ fill: {chrome_col}; font-size: 11px; font-weight: 700; letter-spacing: 1px; }}
      .lbl {{ fill: {text_label}; font-size: 13px; font-weight: 500; }}
      .val {{ fill: {text_val}; font-size: 13px; font-weight: 600; }}
      .sub {{ fill: {text_muted}; font-size: 11px; }}
      .glass-label {{ fill: {text_label}; font-size: 10px; font-weight: 600; }}
      .pill-text {{ fill: {chrome_col}; font-size: 12px; font-weight: 700; }}
      .pill-bg {{ fill: {chrome_col}1F; stroke: {chrome_col}; stroke-width: 1; }}
    ''')
    svg.append('</style>')
    svg.append('</defs>')

    # 1. Main Background Card
    svg.append(f'<rect width="1180" height="540" rx="14" fill="{bg_col}" stroke="{border_col}" stroke-width="1.5"/>')

    # Window Top Header Bar
    svg.append(f'<line x1="0" y1="44" x2="1180" y2="44" stroke="{border_col}" stroke-width="1"/>')
    svg.append('<circle cx="26" cy="22" r="5.5" fill="#EF4444"/>')
    svg.append('<circle cx="44" cy="22" r="5.5" fill="#F59E0B"/>')
    svg.append('<circle cx="62" cy="22" r="5.5" fill="#10B981"/>')
    svg.append(f'<text x="590" y="27" text-anchor="middle" class="title">contributions.reservoir --fluid-sim</text>')

    # Status Pill on Top Right
    svg.append('<g>')
    svg.append(f'<rect x="990" y="10" width="168" height="24" rx="12" class="pill-bg"/>')
    svg.append(f'<circle cx="1006" cy="22" r="4" fill="{chrome_col}">')
    svg.append('<animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>')
    svg.append('</circle>')
    svg.append(f'<text x="1080" y="26" text-anchor="middle" class="pill-text">HYDRATED · 84 COMMITS</text>')
    svg.append('</g>')

    # Subtitle Header
    svg.append(f'<text x="36" y="74" class="sec-hdr">CONTRIBUTION.RESERVOIR</text>')
    svg.append(f'<text x="250" y="74" fill="{text_muted}" font-size="11">· COMMITS CONDENSING AS WATER · REAL-TIME HYDRO DYNAMICS</text>')

    # Canvas Area (34 to 1146, y=88 to 488)
    svg.append(f'<rect x="34" y="88" width="1112" height="404" rx="10" fill="{card_bg}" stroke="{border_col}" stroke-width="1"/>')

    # Cybernetic Grid inside Canvas
    svg.append(f'''
      <g stroke="{border_col}" stroke-width="0.5" stroke-dasharray="2 6" opacity="0.6">
        <line x1="34" y1="200" x2="1146" y2="200"/>
        <line x1="34" y1="320" x2="1146" y2="320"/>
        <line x1="34" y1="440" x2="1146" y2="440"/>
        <line x1="560" y1="88" x2="560" y2="492"/>
      </g>
    ''')

    # =========================================================================
    # LEFT HALF: THE GLASS & FALLING CONTRIBUTION DROPLETS
    # Glass Center: X = 340, Y = 160 (rim) to 465 (base)
    # =========================================================================
    gx = 340 # Center X of glass
    
    # Ambient aura behind the glass
    svg.append(f'<ellipse cx="{gx}" cy="350" rx="170" ry="140" fill="url(#glassAura)"/>')

    # 1. COMMIT DISPENSER / NOZZLE at top (y=105 to y=140)
    svg.append(f'''
      <g>
        <!-- Dispenser Housing -->
        <rect x="{gx - 55}" y="100" width="110" height="24" rx="6" fill="{card_bg}" stroke="{chrome_col}" stroke-width="1.2"/>
        <text x="{gx}" y="116" text-anchor="middle" fill="{chrome_col}" font-size="10" font-weight="700">COMMIT DISPENSER</text>
        
        <!-- Nozzle Pipe -->
        <path d="M {gx - 14} 124 L {gx - 8} 142 L {gx + 8} 142 L {gx + 14} 124 Z" fill="{card_bg}" stroke="{chrome_col}" stroke-width="1"/>
        <circle cx="{gx}" cy="142" r="5" fill="{chrome_col}33"/>
        
        <!-- Droplet Ready at Nozzle tip -->
        <ellipse cx="{gx}" cy="144" rx="3.5" ry="4.5" fill="{chrome_col}">
          <animate attributeName="ry" values="4; 6; 4" dur="1.8s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.6; 1; 0.6" dur="1.8s" repeatCount="indefinite"/>
        </ellipse>
      </g>
    ''')

    # 2. CONTINUOUS FALLING CONTRIBUTION DROPLETS (Dropping one by one)
    # Falling from y=146 to y=252 (water level)
    # Droplet 1: cycle 2.2s
    svg.append(f'''
      <!-- Droplet 1 -->
      <g>
        <path d="M {gx} 146 Q {gx + 4} 154 {gx} 158 Q {gx - 4} 154 {gx} 146 Z" fill="url(#dropGlow)">
          <animateTransform attributeName="transform" type="translate"
            values="0,0; 0,106" keyTimes="0; 1" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="opacity"
            values="1; 1; 0.2; 0" keyTimes="0; 0.88; 0.96; 1" dur="2.2s" repeatCount="indefinite"/>
        </path>
      </g>
      
      <!-- Droplet 2 (interleaved 1.1s later) -->
      <g>
        <path d="M {gx} 146 Q {gx + 4} 154 {gx} 158 Q {gx - 4} 154 {gx} 146 Z" fill="url(#dropGlow)">
          <animateTransform attributeName="transform" type="translate"
            values="0,-53; 0,106; 0,0; 0,0" keyTimes="0; 0.5; 0.501; 1" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="opacity"
            values="1; 0.2; 0; 0" keyTimes="0; 0.44; 0.48; 1" dur="2.2s" repeatCount="indefinite"/>
        </path>
      </g>
    ''')

    # 3. SPLASH RIPPLES ON WATER SURFACE (Triggered when drops enter)
    svg.append(f'''
      <g transform="translate({gx}, 252)">
        <!-- Ripple 1 -->
        <ellipse cx="0" cy="0" rx="4" ry="1.5" fill="none" stroke="{chrome_col}" stroke-width="1.8">
          <animate attributeName="rx" values="3; 46" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="ry" values="1; 12" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.9; 0" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="stroke-width" values="1.8; 0.3" dur="2.2s" repeatCount="indefinite"/>
        </ellipse>
        
        <!-- Ripple 2 (secondary phase) -->
        <ellipse cx="0" cy="0" rx="3" ry="1" fill="none" stroke="#A5F3FC" stroke-width="1.5">
          <animate attributeName="rx" values="2; 38" begin="1.1s" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="ry" values="0.8; 10" begin="1.1s" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.9; 0" begin="1.1s" dur="2.2s" repeatCount="indefinite"/>
        </ellipse>

        <!-- Splash beads jumping up -->
        <circle cx="-6" cy="0" r="1.8" fill="{chrome_col}">
          <animate attributeName="cy" values="0; -14; 0" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="cx" values="-2; -12; -6" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="1; 0.8; 0" dur="2.2s" repeatCount="indefinite"/>
        </circle>
        <circle cx="6" cy="0" r="1.8" fill="{chrome_col}">
          <animate attributeName="cy" values="0; -16; 0" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="cx" values="2; 14; 6" dur="2.2s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="1; 0.8; 0" dur="2.2s" repeatCount="indefinite"/>
        </circle>
      </g>
    ''')

    # 4. WATER BODY INSIDE THE GLASS (Clipped to glass shape)
    # Filled from y=250 to 460
    svg.append('<g clip-path="url(#glassInnerClip)">')
    
    # Deep water base
    svg.append(f'<rect x="220" y="250" width="240" height="220" fill="url(#waterGrad)"/>')
    
    # Animated undulating liquid surface (Two interactive sine waves)
    # Wave 1 (cyan top wave)
    svg.append(f'''
      <path fill="{water_fill_top}" opacity="0.75"
        d="M 220 252 
           Q 275 244 340 252 
           Q 405 260 460 252 
           L 460 264 L 220 264 Z">
        <animate attributeName="d"
          values="M 220 252 Q 275 244 340 252 Q 405 260 460 252 L 460 264 L 220 264 Z;
                  M 220 252 Q 275 260 340 252 Q 405 244 460 252 L 460 264 L 220 264 Z;
                  M 220 252 Q 275 244 340 252 Q 405 260 460 252 L 460 264 L 220 264 Z"
          dur="3.6s" repeatCount="indefinite"/>
      </path>
    ''')
    
    # Wave 2 (secondary translucent wave)
    svg.append(f'''
      <path fill="url(#waveBackGrad)"
        d="M 220 252 
           Q 285 258 340 250 
           Q 395 242 460 252 
           L 460 264 L 220 264 Z">
        <animate attributeName="d"
          values="M 220 252 Q 285 258 340 250 Q 395 242 460 252 L 460 264 L 220 264 Z;
                  M 220 252 Q 285 244 340 254 Q 395 262 460 252 L 460 264 L 220 264 Z;
                  M 220 252 Q 285 258 340 250 Q 395 242 460 252 L 460 264 L 220 264 Z"
          dur="4.2s" repeatCount="indefinite"/>
      </path>
    ''')

    # Rising air bubbles inside water (like champagne / carbonated commits)
    bubble_coords = [
        (280, 440, 2.8, 12, 3.2),
        (320, 420, 2.2, -8, 2.6),
        (355, 450, 3.4, 10, 4.0),
        (385, 430, 2.0, -12, 2.9),
        (300, 390, 2.5, 6, 3.5),
        (370, 370, 3.0, -6, 3.8),
    ]
    for bx, by, br, bdx, bdur in bubble_coords:
        svg.append(f'''
          <circle cx="{bx}" cy="{by}" r="{br}" fill="#A5F3FC" opacity="0.65">
            <animate attributeName="cy" values="{by}; 254" dur="{bdur}s" repeatCount="indefinite"/>
            <animate attributeName="cx" values="{bx}; {bx + bdx}; {bx}" dur="{bdur}s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0; 0.75; 0.9; 0" dur="{bdur}s" repeatCount="indefinite"/>
          </circle>
        ''')

    svg.append('</g>') # End glassInnerClip

    # 5. THE GLASS CONTAINER (TUMBLER / BEAKER) SILHOUETTE
    # Glass outer walls
    svg.append(f'''
      <!-- Thick solid glass bottom base -->
      <path d="M 244 452 
               Q 248 468 262 468 
               L 418 468 
               Q 432 468 436 452 
               L 432 458 
               L 248 458 Z" 
            fill="{chrome_col}22" stroke="{glass_stroke}" stroke-width="2"/>
            
      <!-- Main Glass Walls -->
      <path d="M 230 170 
               L 246 450 
               Q 248 464 262 464 
               L 418 464 
               Q 432 464 434 450 
               L 450 170" 
            fill="none" stroke="{glass_stroke}" stroke-width="2.5" stroke-linecap="round"/>

      <!-- Top Glass Oval Rim -->
      <ellipse cx="{gx}" cy="170" rx="110" ry="16" fill="none" stroke="{glass_rim}" stroke-width="2.5"/>
      <ellipse cx="{gx}" cy="170" rx="106" ry="13" fill="{card_bg}" fill-opacity="0.2" stroke="{glass_rim}" stroke-width="1" stroke-dasharray="4 6"/>

      <!-- Vertical Glass Specular Highlights (Left & Right sheen) -->
      <path d="M 238 185 L 252 445" stroke="url(#glassSpecLeft)" stroke-width="7" stroke-linecap="round"/>
      <path d="M 442 185 L 428 445" stroke="url(#glassSpecRight)" stroke-width="4" stroke-linecap="round"/>
    ''')

    # 6. MEASUREMENT LEVEL GRADUATION TICKS ON GLASS (Right Side)
    levels = [
        (205, "100%", "OVERFLOW"),
        (252, " 84%", "CURRENT FILL · 84 COMMITS"),
        (305, " 60%", "CONSISTENT FLOW"),
        (360, " 40%", "WARMING UP"),
        (415, " 20%", "BASE VOLUME"),
    ]
    for ly, pct, ldesc in levels:
        is_current = ("84%" in pct)
        tick_col = amber_col if is_current else chrome_col
        line_w = 26 if is_current else 14
        svg.append(f'<line x1="438" y1="{ly}" x2="{438 + line_w}" y2="{ly}" stroke="{tick_col}" stroke-width="1.8"/>')
        if is_current:
            # Active Indicator Arrow & Badge
            svg.append(f'''
              <polygon points="{438 + line_w + 4},{ly} {438 + line_w + 12},{ly - 5} {438 + line_w + 12},{ly + 5}" fill="{amber_col}"/>
              <rect x="{438 + line_w + 16}" y="{ly - 10}" width="78" height="20" rx="4" fill="{amber_col}22" stroke="{amber_col}" stroke-width="1"/>
              <text x="{438 + line_w + 22}" y="{ly + 4}" fill="{amber_col}" font-size="10" font-weight="700">84 COMMITS</text>
            ''')
        else:
            svg.append(f'<text x="{438 + line_w + 8}" y="{ly + 3.5}" class="glass-label">{pct}</text>')

    # Glass Base Label
    svg.append(f'<text x="{gx}" y="486" text-anchor="middle" fill="{chrome_col}" font-size="11" font-weight="700" letter-spacing="1.5">HYDRAULIC CAPACITY: 100 COMMITS</text>')

    # =========================================================================
    # RIGHT HALF: HYDRATION & TELEMETRY DASHBOARD
    # X = 580 to 1120
    # =========================================================================
    rx = 590
    
    # Section Header
    svg.append(f'<text x="{rx}" y="118" class="card-hdr">TELEMETRY // CONTRIBUTION HYDRO-DYNAMICS</text>')
    svg.append(f'<line x1="{rx}" y1="128" x2="1120" y2="128" stroke="{border_col}" stroke-width="1"/>')

    # Card 1: TOTAL VOLUME & FILL METER
    svg.append(f'''
      <!-- Card 1 -->
      <g transform="translate({rx}, 144)">
        <rect width="530" height="74" rx="8" fill="{card_bg}" stroke="{border_col}" stroke-width="1"/>
        <text x="18" y="26" class="lbl">RESERVOIR VOLUME</text>
        <text x="18" y="54" fill="{text_val}" font-size="22" font-weight="700">84.0 <tspan font-size="13" fill="{text_muted}">COMMITS CONDENSED</tspan></text>
        <text x="512" y="32" text-anchor="end" fill="{emerald_col}" font-size="14" font-weight="700">84% FULL</text>
        
        <!-- Progress bar background -->
        <rect x="260" y="44" width="252" height="10" rx="5" fill="{border_col}"/>
        <!-- Progress bar fill -->
        <rect x="260" y="44" width="212" height="10" rx="5" fill="url(#waterGrad)"/>
      </g>
    ''')

    # Card 2: CONDENSATION STREAM / FLOW RATE
    svg.append(f'''
      <!-- Card 2 -->
      <g transform="translate({rx}, 232)">
        <rect width="255" height="108" rx="8" fill="{card_bg}" stroke="{border_col}" stroke-width="1"/>
        <text x="18" y="26" class="lbl">FLOW VELOCITY</text>
        <text x="18" y="56" fill="{chrome_col}" font-size="22" font-weight="700">ACTIVE</text>
        <text x="18" y="76" class="sub">1 DROP = 1 GIT COMMIT</text>
        <text x="18" y="94" fill="{emerald_col}" font-size="11" font-weight="600">● 100% UNINTERRUPTED</text>
      </g>
      
      <!-- Card 3 -->
      <g transform="translate({rx + 275}, 232)">
        <rect width="255" height="108" rx="8" fill="{card_bg}" stroke="{border_col}" stroke-width="1"/>
        <text x="18" y="26" class="lbl">PURITY INDEX</text>
        <text x="18" y="56" fill="{purple_col}" font-size="22" font-weight="700">99.8%</text>
        <text x="18" y="76" class="sub">CLEAN CODE &amp; TESTED</text>
        <text x="18" y="94" fill="{chrome_col}" font-size="11" font-weight="600">● ZERO MEMORY LEAKS</text>
      </g>
    ''')

    # Card 4: FLUID COMPOSITION (Stack breakdown)
    svg.append(f'''
      <!-- Card 4: Composition -->
      <g transform="translate({rx}, 354)">
        <rect width="530" height="98" rx="8" fill="{card_bg}" stroke="{border_col}" stroke-width="1"/>
        <text x="18" y="24" class="lbl">FLUID INGREDIENTS</text>
        <text x="512" y="24" text-anchor="end" class="sub">TOTAL COMMITS: 84</text>
        
        <!-- Multi-colored segment bar -->
        <rect x="18" y="36" width="494" height="12" rx="6" fill="{border_col}"/>
        <!-- TypeScript (70.6%) -->
        <rect x="18" y="36" width="348" height="12" rx="6" fill="#3178C6"/>
        <!-- JavaScript (10.3%) -->
        <rect x="366" y="36" width="51" height="12" fill="#F7DF1E"/>
        <!-- Python (9.1%) -->
        <rect x="417" y="36" width="45" height="12" fill="#38BDF8"/>
        <!-- CSS / HTML (10%) -->
        <rect x="462" y="36" width="50" height="12" rx="6" fill="#10B981"/>

        <!-- Legend Items -->
        <g font-size="10.5" font-weight="600" transform="translate(18, 74)">
          <circle cx="6" cy="-4" r="4" fill="#3178C6"/>
          <text x="16" y="0" fill="{text_val}">TS 70.6%</text>

          <circle cx="130" cy="-4" r="4" fill="#F7DF1E"/>
          <text x="140" y="0" fill="{text_val}">JS 10.3%</text>

          <circle cx="250" cy="-4" r="4" fill="#38BDF8"/>
          <text x="260" y="0" fill="{text_val}">Python 9.1%</text>

          <circle cx="380" cy="-4" r="4" fill="#10B981"/>
          <text x="390" y="0" fill="{text_val}">Web UI 10%</text>
        </g>
      </g>
    ''')

    # Card 5: Bottom Hydro Status line outside canvas
    svg.append(f'''
      <line x1="34" y1="462" x2="1146" y2="462" stroke="{border_col}" stroke-width="1"/>
      <g font-size="11" fill="{text_muted}">
        <text x="50" y="480">RESERVOIR: MOHAMMAD HASIM · VESSEL: 1000ml PYREX · CONDENSER: CONTINUOUS INTEGRATION</text>
        <text x="1130" y="480" text-anchor="end" fill="{emerald_col}">STATUS: HYDRATED &amp; SHIPPING DAILY (100% OK)</text>
      </g>
    ''')

    svg.append(f'''
      <text x="44" y="520" fill="{text_muted}" font-size="11">HYDRO.SIMULATION v1.0 · COMMITS TRANSFORMED TO FLUID · GITHUB PROFILE HASIM2006</text>
      <text x="1136" y="520" text-anchor="end" fill="{chrome_col}" font-size="11" font-weight="600">STAY HYDRATED · KEEP SHIPPING</text>
    ''')

    svg.append('</svg>')
    return "\n".join(svg)

print("Building contribution_glass_dark.svg and contribution_glass_light.svg...")
glass_dark = build_water_glass_svg("dark")
glass_light = build_water_glass_svg("light")

# Validate XML
ET.fromstring(glass_dark)
ET.fromstring(glass_light)
print("XML validation PASSED for Contribution Water Glass SVGs!")

dark_path = os.path.join(output_dir, "contribution_glass_dark.svg")
light_path = os.path.join(output_dir, "contribution_glass_light.svg")

with open(dark_path, "w", encoding="utf-8") as f:
    f.write(glass_dark)
with open(light_path, "w", encoding="utf-8") as f:
    f.write(glass_light)

print(f"Generated {dark_path} ({len(glass_dark)/1024:.1f} KB)")
print(f"Generated {light_path} ({len(glass_light)/1024:.1f} KB)")
