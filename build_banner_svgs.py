import os
import math
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import xml.etree.ElementTree as ET

# Input image
img_path = r"c:\Users\hasim\OneDrive\Desktop\github'\WhatsApp Image 2026-10-09 at 8.49.45 PM.jpeg"
output_dir = r"c:\Users\hasim\OneDrive\Desktop\github'\hasim2006"
os.makedirs(output_dir, exist_ok=True)

# 1. Prepare Full Image Dithering
img_rgb = Image.open(img_path).convert("RGB")
crop_box = (60, 10, 692, 726)
cropped = img_rgb.crop(crop_box).resize((300, 340), Image.Resampling.LANCZOS)

enhancer = ImageEnhance.Contrast(cropped)
c1 = enhancer.enhance(1.3)
c2 = ImageOps.autocontrast(c1, cutoff=1)
c3 = c2.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
gray = c3.convert("L")
arr_gray = np.array(gray, dtype=np.float32)
h, w = arr_gray.shape # 340, 300

def full_dither_dark(mat_in):
    mat = mat_in.copy()
    dots = np.zeros((h, w), dtype=bool)
    for y in range(h):
        xs = range(w) if y % 2 == 0 else range(w - 1, -1, -1)
        step = 1 if y % 2 == 0 else -1
        for x in xs:
            old_val = mat[y, x]
            new_val = 255.0 if old_val >= 128.0 else 0.0
            dots[y, x] = (new_val == 255.0)
            err = old_val - new_val
            if step == 1:
                if x + 1 < w: mat[y, x + 1] += err * (7.0 / 16.0)
                if y + 1 < h:
                    if x - 1 >= 0: mat[y + 1, x - 1] += err * (3.0 / 16.0)
                    mat[y + 1, x] += err * (5.0 / 16.0)
                    if x + 1 < w: mat[y + 1, x + 1] += err * (1.0 / 16.0)
            else:
                if x - 1 >= 0: mat[y, x - 1] += err * (7.0 / 16.0)
                if y + 1 < h:
                    if x + 1 < w: mat[y + 1, x + 1] += err * (3.0 / 16.0)
                    mat[y + 1, x] += err * (5.0 / 16.0)
                    if x - 1 >= 0: mat[y + 1, x - 1] += err * (1.0 / 16.0)
    return dots

def full_dither_light(mat_in):
    mat = 255.0 - mat_in.copy()
    dots = np.zeros((h, w), dtype=bool)
    for y in range(h):
        xs = range(w) if y % 2 == 0 else range(w - 1, -1, -1)
        step = 1 if y % 2 == 0 else -1
        for x in xs:
            old_val = mat[y, x]
            new_val = 255.0 if old_val >= 128.0 else 0.0
            dots[y, x] = (new_val == 255.0)
            err = old_val - new_val
            if step == 1:
                if x + 1 < w: mat[y, x + 1] += err * (7.0 / 16.0)
                if y + 1 < h:
                    if x - 1 >= 0: mat[y + 1, x - 1] += err * (3.0 / 16.0)
                    mat[y + 1, x] += err * (5.0 / 16.0)
                    if x + 1 < w: mat[y + 1, x + 1] += err * (1.0 / 16.0)
            else:
                if x - 1 >= 0: mat[y, x - 1] += err * (7.0 / 16.0)
                if y + 1 < h:
                    if x + 1 < w: mat[y + 1, x + 1] += err * (3.0 / 16.0)
                    mat[y + 1, x] += err * (5.0 / 16.0)
                    if x - 1 >= 0: mat[y + 1, x - 1] += err * (1.0 / 16.0)
    return dots

dots_dark = full_dither_dark(arr_gray)
dots_light = full_dither_light(arr_gray)

def extract_runs(dot_matrix):
    runs = []
    for y in range(h):
        in_run = False
        start_x = 0
        for x in range(w):
            if dot_matrix[y, x]:
                if not in_run:
                    in_run = True
                    start_x = x
            else:
                if in_run:
                    runs.append((y, start_x, x - start_x))
                    in_run = False
        if in_run:
            runs.append((y, start_x, w - start_x))
    return runs

runs_dark = extract_runs(dots_dark)
runs_light = extract_runs(dots_light)
print(f"Extracted runs - Dark: {len(runs_dark)}, Light: {len(runs_light)}")

# 2. Extract Official Vector Paths
scratch_dir = r"C:\Users\hasim\.gemini\antigravity-ide\brain\07f79cc6-5a49-4ae4-9eb2-aa15217407d9\scratch"
tree_py = ET.parse(os.path.join(scratch_dir, "python.svg"))
py_path_d = tree_py.getroot().find('{http://www.w3.org/2000/svg}path').attrib['d']

tree_re = ET.parse(os.path.join(scratch_dir, "react.svg"))
re_path_d = tree_re.getroot().find('{http://www.w3.org/2000/svg}path').attrib['d']

tree_js = ET.parse(os.path.join(scratch_dir, "javascript.svg"))
js_path_d = tree_js.getroot().find('{http://www.w3.org/2000/svg}path').attrib['d']

# 3. Ambient Floating Particles for Tech Atmosphere (Centered around cx=590, cy=270)
NUM_PARTICLES = 160
np.random.seed(42)
particles = []
cx_center, cy_center = 590.0, 270.0
for i in range(NUM_PARTICLES):
    angle = np.random.uniform(0, 2 * math.pi)
    dist = np.random.uniform(35, 160)
    px = cx_center + dist * math.cos(angle)
    py = cy_center + dist * math.sin(angle)
    r = np.random.uniform(1.0, 2.2)
    dx = np.random.uniform(-20, 20)
    dy = np.random.uniform(-20, 20)
    particles.append((px, py, r, dx, dy))

# 4. Build SVG Generator
def build_banner_svg(theme="dark"):
    is_dark = (theme == "dark")
    bg_col = "#0A101F" if is_dark else "#F8FAFC"
    chrome_col = "#22D3EE" if is_dark else "#0891B2"
    border_col = "#1E293B" if is_dark else "#CBD5E1"
    portrait_col = "#A78BFA" if is_dark else "#7C3AED"
    accent_col = "#10B981"
    text_muted = "#64748B"
    text_label = "#94A3B8" if is_dark else "#475569"
    text_val = "#F8FAFC" if is_dark else "#0F172A"
    
    runs = runs_dark if is_dark else runs_light
    
    # Scale and center photo in the center stage
    scale = 1.14
    photo_w = 300 * scale # 342
    photo_h = 340 * scale # 387.6
    ox = cx_center - photo_w / 2 # 419.0
    oy = cy_center - photo_h / 2 + 10 # 86.2
    
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 540" width="100%" height="100%">')
    svg.append('<defs>')
    
    # Gradients & Filters
    svg.append('''
      <linearGradient id="pyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#38BDF8"/>
        <stop offset="48%" stop-color="#38BDF8"/>
        <stop offset="52%" stop-color="#FACC15"/>
        <stop offset="100%" stop-color="#FACC15"/>
      </linearGradient>
      <linearGradient id="reactGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#22D3EE"/>
        <stop offset="100%" stop-color="#67E8F9"/>
      </linearGradient>
      <linearGradient id="jsGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#FBBF24"/>
        <stop offset="100%" stop-color="#F59E0B"/>
      </linearGradient>
      <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>
        <stop offset="50%" stop-color="#22D3EE" stop-opacity="0.4"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </linearGradient>
      <radialGradient id="haloGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.22"/>
        <stop offset="70%" stop-color="#22D3EE" stop-opacity="0.05"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="pyGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#FACC15" stop-opacity="0.18"/>
        <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="jsGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.22"/>
        <stop offset="100%" stop-color="#FBBF24" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="hudGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.08"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </radialGradient>
    ''')
    
    svg.append('<style>')
    svg.append(f'''
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&amp;display=swap');
      text {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}
      .traffic-red {{ fill: #EF4444; }}
      .traffic-yellow {{ fill: #F59E0B; }}
      .traffic-green {{ fill: #10B981; }}
      .chrome {{ fill: {chrome_col}; }}
      .title {{ fill: {text_muted}; font-size: 13px; font-weight: 500; }}
      .live-dot {{ fill: #EF4444; }}
      .live-text {{ fill: #EF4444; font-size: 12px; font-weight: 700; }}
      .pill-bg {{ fill: {chrome_col}1F; stroke: {chrome_col}; stroke-width: 1; }}
      .pill-text {{ fill: {chrome_col}; font-size: 13px; font-weight: 600; }}
      .sec-hdr {{ fill: {chrome_col}; font-size: 12px; font-weight: 700; letter-spacing: 1.5px; }}
      .hud-title {{ fill: {text_label}; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; }}
      .hud-val {{ fill: {text_val}; font-size: 12px; font-weight: 600; }}
      .hud-sub {{ fill: {text_muted}; font-size: 10px; }}
      .vertex-mark {{ fill: {chrome_col}; }}
      .vertex-coord {{ fill: {chrome_col}88; font-size: 9px; font-family: monospace; }}
      .bracket {{ stroke: {chrome_col}; stroke-width: 2; fill: none; }}
    ''')
    svg.append('</style>')
    svg.append('</defs>')
    
    # 1. Main Background Card (Merged with background color, transparent / same color)
    svg.append(f'<rect width="1180" height="540" rx="12" fill="{bg_col}" stroke="{border_col}" stroke-width="1.2"/>')
    
    # =========================================================================
    # CORNERS, EDGES & VERTICES (Requested: corners and edges with vertices)
    # =========================================================================
    # Tech vertices & brackets at 4 corners
    svg.append(f'''
    <!-- Vertices & Corner Brackets -->
    <g>
      <!-- Vertex 1: Top-Left (20, 20) -->
      <path d="M 20 54 V 20 H 54" class="bracket"/>
      <circle cx="20" cy="20" r="3.5" class="vertex-mark"/>
      <text x="28" y="32" class="vertex-coord">V1 [0,0]</text>
      
      <!-- Vertex 2: Top-Right (1160, 20) -->
      <path d="M 1160 54 V 20 H 1126" class="bracket"/>
      <circle cx="1160" cy="20" r="3.5" class="vertex-mark"/>
      <text x="1100" y="32" class="vertex-coord">V2 [1180,0]</text>
      
      <!-- Vertex 3: Bottom-Left (20, 520) -->
      <path d="M 20 486 V 520 H 54" class="bracket"/>
      <circle cx="20" cy="520" r="3.5" class="vertex-mark"/>
      <text x="28" y="512" class="vertex-coord">V3 [0,540]</text>
      
      <!-- Vertex 4: Bottom-Right (1160, 520) -->
      <path d="M 1160 486 V 520 H 1126" class="bracket"/>
      <circle cx="1160" cy="520" r="3.5" class="vertex-mark"/>
      <text x="1080" y="512" class="vertex-coord">V4 [1180,540]</text>
      
      <!-- Midpoint Crosshair Vertices (+) -->
      <g stroke="{chrome_col}88" stroke-width="1">
        <!-- Top Edge Crosshair -->
        <line x1="590" y1="14" x2="590" y2="26"/>
        <line x1="584" y1="20" x2="596" y2="20"/>
        
        <!-- Bottom Edge Crosshair -->
        <line x1="590" y1="514" x2="590" y2="526"/>
        <line x1="584" y1="520" x2="596" y2="520"/>
        
        <!-- Left Edge Crosshair -->
        <line x1="14" y1="270" x2="26" y2="270"/>
        <line x1="20" y1="264" x2="20" y2="276"/>
        
        <!-- Right Edge Crosshair -->
        <line x1="1154" y1="270" x2="1166" y2="270"/>
        <line x1="1160" y1="264" x2="1160" y2="276"/>
      </g>
    </g>
    ''')
    
    # Top Chrome Header Bar
    svg.append(f'<line x1="20" y1="44" x2="1160" y2="44" stroke="{border_col}" stroke-width="1"/>')
    svg.append('<circle cx="44" cy="32" r="5" class="traffic-red"/>')
    svg.append('<circle cx="60" cy="32" r="5" class="traffic-yellow"/>')
    svg.append('<circle cx="76" cy="32" r="5" class="traffic-green"/>')
    svg.append('<text x="590" y="36" text-anchor="middle" class="title">terminal // visual.core --stream</text>')
    
    # LIVE indicator
    svg.append('<g>')
    svg.append('<circle cx="1010" cy="32" r="4" class="live-dot">')
    svg.append('<animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>')
    svg.append('</circle>')
    svg.append('<text x="1022" y="36" class="live-text">LIVE</text>')
    svg.append('</g>')
    
    # User Handle Pill
    svg.append('<g>')
    svg.append('<rect x="1066" y="20" width="88" height="24" rx="12" class="pill-bg"/>')
    svg.append('<text x="1110" y="36" text-anchor="middle" class="pill-text">@hasim2006</text>')
    svg.append('</g>')
    
    # =========================================================================
    # CENTER STAGE: DYNAMIC VISUAL CORE (Photo & Sequential Tech Logos)
    # =========================================================================
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="170" fill="url(#hudGlow)"/>')
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="160" stroke="{border_col}" stroke-width="1" stroke-dasharray="4 6" fill="none"/>')
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="185" stroke="{chrome_col}22" stroke-width="1" stroke-dasharray="2 10" fill="none"/>')
    
    # Phase Subtitle above Center Stage (y=72)
    svg.append(f'''
    <g font-size="12" font-weight="700" letter-spacing="1.5" text-anchor="middle">
      <!-- Subtitle 0: Photo -->
      <text x="{cx_center}" y="74" fill="{chrome_col}">
        VISUAL.CORE · [00] // PORTRAIT.ID // MOHAMMAD HASIM
        <animate attributeName="opacity"
          values="1; 1; 0; 0; 0; 0; 0; 0; 1; 1"
          keyTimes="0; 0.233; 0.261; 0.480; 0.720; 0.940; 0.961; 0.989; 1; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
      <!-- Subtitle 1: Python -->
      <text x="{cx_center}" y="74" fill="#38BDF8">
        VISUAL.CORE · [01/03] // PYTHON 3.12 AI STACK
        <animate attributeName="opacity"
          values="0; 0; 1; 1; 0; 0; 0; 0"
          keyTimes="0; 0.250; 0.278; 0.472; 0.500; 0.750; 0.950; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
      <!-- Subtitle 2: React -->
      <text x="{cx_center}" y="74" fill="#22D3EE">
        VISUAL.CORE · [02/03] // REACT 18 NEXT.JS ECOSYSTEM
        <animate attributeName="opacity"
          values="0; 0; 1; 1; 0; 0; 0; 0"
          keyTimes="0; 0.489; 0.517; 0.711; 0.739; 0.850; 0.950; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
      <!-- Subtitle 3: JavaScript -->
      <text x="{cx_center}" y="74" fill="#FBBF24">
        VISUAL.CORE · [03/03] // JAVASCRIPT &amp; NODE.JS RUNTIME
        <animate attributeName="opacity"
          values="0; 0; 1; 1; 0; 0; 0; 0"
          keyTimes="0; 0.728; 0.756; 0.944; 0.972; 0.980; 0.990; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
    </g>
    ''')
    
    # Clip-path for center stage to keep scanner clean
    svg.append(f'<clipPath id="centerClip"><rect x="{cx_center - 180}" y="80" width="360" height="395" rx="10"/></clipPath>')
    svg.append('<g clip-path="url(#centerClip)">')
    
    # LAYER 1: FULL USER PHOTO
    svg.append('<g id="layer-photo">')
    svg.append('''
      <animate attributeName="opacity"
        values="1; 1; 0; 0; 0; 0; 0; 0; 1; 1"
        keyTimes="0; 0.233; 0.261; 0.480; 0.720; 0.940; 0.961; 0.989; 1; 1"
        dur="18s" repeatCount="indefinite"/>
    ''')
    
    path_runs = []
    for y, sx, length in runs:
        px = ox + sx * scale
        py = oy + y * scale
        pw = length * scale
        ph = scale
        path_runs.append(f'M {px:.1f} {py:.1f} h {pw:.1f} v {ph:.1f} h -{pw:.1f} Z')
    photo_d = " ".join(path_runs)
    
    svg.append(f'<path fill="{portrait_col}" d="{photo_d}" shape-rendering="crispEdges"/>')
    
    # Cybernetic Scanner Line across the photo
    svg.append(f'''
      <rect x="{cx_center - 170}" y="85" width="340" height="28" fill="url(#scanGrad)" opacity="0.8">
        <animate attributeName="y" values="85; 450; 85" dur="4.2s" repeatCount="indefinite"/>
      </rect>
    ''')
    svg.append('</g>') # End layer-photo
    
    # LAYER 2: PYTHON LOGO
    svg.append('<g id="layer-python">')
    svg.append('''
      <animate attributeName="opacity"
        values="0; 0; 1; 1; 0; 0; 0; 0"
        keyTimes="0; 0.250; 0.278; 0.472; 0.500; 0.750; 0.950; 1"
        dur="18s" repeatCount="indefinite"/>
    ''')
    
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="115" fill="url(#pyGlow)"/>')
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="92" stroke="#38BDF844" stroke-width="1.5" stroke-dasharray="6 8" fill="none"/>')
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="120" stroke="#FACC1533" stroke-width="1" stroke-dasharray="2 12" fill="none"/>')
    
    py_scale = 7.2
    py_ox = cx_center - 12.0 * py_scale
    py_oy = cy_center - 12.0 * py_scale - 12.0
    
    svg.append(f'<g transform="translate({py_ox:.1f}, {py_oy:.1f}) scale({py_scale})">')
    svg.append(f'<path d="{py_path_d}" fill="url(#pyGrad)" filter="drop-shadow(0 0 5px #38BDF877)"/>')
    svg.append('</g>')
    
    svg.append(f'<text x="{cx_center}" y="{cy_center + 96}" text-anchor="middle" fill="#FACC15" font-size="14" font-weight="700" letter-spacing="1.5">PYTHON 3.12</text>')
    svg.append(f'<text x="{cx_center}" y="{cy_center + 114}" text-anchor="middle" fill="{text_label}" font-size="10.5">FASTAPI · AI &amp; ML · NUMPY · BACKEND</text>')
    svg.append('</g>') # End layer-python
    
    # LAYER 3: REACT LOGO
    svg.append('<g id="layer-react">')
    svg.append('''
      <animate attributeName="opacity"
        values="0; 0; 1; 1; 0; 0; 0; 0"
        keyTimes="0; 0.489; 0.517; 0.711; 0.739; 0.850; 0.950; 1"
        dur="18s" repeatCount="indefinite"/>
    ''')
    
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="115" fill="url(#haloGlow)"/>')
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="102" stroke="#22D3EE44" stroke-width="1" stroke-dasharray="4 6" fill="none"/>')
    
    re_scale = 7.0
    re_ox = cx_center - 12.0 * re_scale
    re_oy = cy_center - 12.0 * re_scale - 12.0
    
    svg.append(f'<g transform="translate({re_ox:.1f}, {re_oy:.1f}) scale({re_scale})">')
    svg.append(f'''
      <g transform-origin="12 12">
        <animateTransform attributeName="transform" type="rotate"
          from="0 12 12" to="360 12 12" dur="12s" repeatCount="indefinite"/>
        <path d="{re_path_d}" fill="url(#reactGrad)" filter="drop-shadow(0 0 6px #22D3EE88)"/>
      </g>
    ''')
    svg.append('</g>')
    
    svg.append(f'<text x="{cx_center}" y="{cy_center + 96}" text-anchor="middle" fill="#22D3EE" font-size="14" font-weight="700" letter-spacing="1.5">REACT 18</text>')
    svg.append(f'<text x="{cx_center}" y="{cy_center + 114}" text-anchor="middle" fill="{text_label}" font-size="10.5">NEXT.JS · HOOKS · VIRTUAL DOM · SPA</text>')
    svg.append('</g>') # End layer-react
    
    # LAYER 4: JAVASCRIPT LOGO
    svg.append('<g id="layer-js">')
    svg.append('''
      <animate attributeName="opacity"
        values="0; 0; 1; 1; 0; 0; 0; 0"
        keyTimes="0; 0.728; 0.756; 0.944; 0.972; 0.980; 0.990; 1"
        dur="18s" repeatCount="indefinite"/>
    ''')
    
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="115" fill="url(#jsGlow)"/>')
    svg.append(f'<rect x="{cx_center - 88}" y="{cy_center - 100}" width="176" height="176" rx="14" stroke="#FBBF2455" stroke-width="1.5" stroke-dasharray="8 6" fill="none"/>')
    
    js_scale = 6.4
    js_ox = cx_center - 12.0 * js_scale
    js_oy = cy_center - 12.0 * js_scale - 12.0
    
    svg.append(f'<g transform="translate({js_ox:.1f}, {js_oy:.1f}) scale({js_scale})">')
    svg.append(f'<path d="{js_path_d}" fill="url(#jsGrad)" fill-rule="evenodd" filter="drop-shadow(0 0 6px #F59E0B77)"/>')
    svg.append('</g>')
    
    svg.append(f'<text x="{cx_center}" y="{cy_center + 96}" text-anchor="middle" fill="#FBBF24" font-size="14" font-weight="700" letter-spacing="1.5">JAVASCRIPT ES6+</text>')
    svg.append(f'<text x="{cx_center}" y="{cy_center + 114}" text-anchor="middle" fill="{text_label}" font-size="10.5">NODE.JS · ASYNC/AWAIT · REST · V8</text>')
    svg.append('</g>') # End layer-js
    
    # LAYER 5: AMBIENT FLOATING CYBERNETIC PARTICLES
    svg.append('<g id="ambient-particles" fill="#22D3EE">')
    svg.append('''
      <animate attributeName="opacity"
        values="0; 0; 0.85; 0.85; 0.85; 0.85; 0; 0"
        keyTimes="0; 0.250; 0.278; 0.700; 0.940; 0.960; 0.980; 1"
        dur="18s" repeatCount="indefinite"/>
    ''')
    for px, py, r, dx, dy in particles:
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}">')
        svg.append(f'''<animate attributeName="cx"
          values="{px:.1f}; {px + dx:.1f}; {px - dx*0.5:.1f}; {px:.1f}"
          dur="5.4s" repeatCount="indefinite"/>''')
        svg.append(f'''<animate attributeName="cy"
          values="{py:.1f}; {py + dy:.1f}; {py - dy*0.5:.1f}; {py:.1f}"
          dur="5.4s" repeatCount="indefinite"/>''')
        svg.append('</circle>')
    svg.append('</g>') # End ambient-particles
    
    svg.append('</g>') # End clip-path group
    
    # =========================================================================
    # LEFT HUD TELEMETRY WING (x=45..350)
    # =========================================================================
    svg.append(f'''
    <g transform="translate(48, 120)">
      <!-- Panel Header -->
      <text x="0" y="0" class="sec-hdr">01 // CORE ARCHITECTURE</text>
      <line x1="0" y1="10" x2="280" y2="10" stroke="{border_col}" stroke-width="1"/>
      
      <!-- Module 1: AI & ML -->
      <g transform="translate(0, 36)">
        <rect x="0" y="0" width="280" height="54" rx="8" fill="{chrome_col}0A" stroke="{border_col}" stroke-width="1"/>
        <text x="14" y="22" class="hud-title">AI &amp; MACHINE LEARNING</text>
        <text x="14" y="40" class="hud-sub">PyTorch · Transformers · World Models · NTRO</text>
      </g>
      
      <!-- Module 2: Full-Stack Engineering -->
      <g transform="translate(0, 106)">
        <rect x="0" y="0" width="280" height="54" rx="8" fill="{chrome_col}0A" stroke="{border_col}" stroke-width="1"/>
        <text x="14" y="22" class="hud-title">FULL-STACK SYSTEMS</text>
        <text x="14" y="40" class="hud-sub">React 18 · Next.js · Node.js · FastAPI · REST</text>
      </g>
      
      <!-- Module 3: Distributed & Cloud -->
      <g transform="translate(0, 176)">
        <rect x="0" y="0" width="280" height="54" rx="8" fill="{chrome_col}0A" stroke="{border_col}" stroke-width="1"/>
        <text x="14" y="22" class="hud-title">INFRASTRUCTURE &amp; CLOUD</text>
        <text x="14" y="40" class="hud-sub">AWS · GCP · Docker · Linux x86_64 · Vercel</text>
      </g>
      
      <!-- Live Pulse Wave Gauge -->
      <g transform="translate(0, 252)">
        <text x="0" y="0" font-size="10.5" fill="{text_muted}">TELEMETRY SPECTRUM</text>
        <g stroke="{chrome_col}" stroke-width="1.8" fill="none">
          <path d="M 0 16 L 35 16 L 45 4 L 55 28 L 65 10 L 75 22 L 85 16 L 160 16 L 170 2 L 180 30 L 190 16 L 280 16">
            <animate attributeName="stroke-dashoffset" values="0; 280" dur="4s" repeatCount="indefinite"/>
          </path>
        </g>
      </g>
    </g>
    ''')
    
    # =========================================================================
    # RIGHT HUD TELEMETRY WING (x=850..1130)
    # =========================================================================
    svg.append(f'''
    <g transform="translate(850, 120)">
      <!-- Panel Header -->
      <text x="0" y="0" class="sec-hdr">02 // SYSTEMS TELEMETRY</text>
      <line x1="0" y1="10" x2="280" y2="10" stroke="{border_col}" stroke-width="1"/>
      
      <!-- Metric 1: System Status -->
      <g transform="translate(0, 36)">
        <rect x="0" y="0" width="280" height="54" rx="8" fill="{accent_col}0A" stroke="{border_col}" stroke-width="1"/>
        <circle cx="20" cy="27" r="4.5" fill="{accent_col}">
          <animate attributeName="opacity" values="1; 0.2; 1" dur="1.8s" repeatCount="indefinite"/>
        </circle>
        <text x="36" y="23" font-size="12" font-weight="700" fill="{accent_col}">SYSTEM ACTIVE · SHIPPING</text>
        <text x="36" y="40" class="hud-sub">Continuous delivery pipeline online</text>
      </g>
      
      <!-- Metric 2: Origin & Base -->
      <g transform="translate(0, 106)">
        <rect x="0" y="0" width="280" height="54" rx="8" fill="{chrome_col}0A" stroke="{border_col}" stroke-width="1"/>
        <text x="14" y="22" class="hud-title">BASE &amp; TIMEZONE</text>
        <text x="14" y="40" class="hud-val">India · Asia/Kolkata (UTC +05:30)</text>
      </g>
      
      <!-- Metric 3: Uptime & Latency -->
      <g transform="translate(0, 176)">
        <rect x="0" y="0" width="280" height="54" rx="8" fill="{chrome_col}0A" stroke="{border_col}" stroke-width="1"/>
        <text x="14" y="22" class="hud-title">PIPELINE METRICS</text>
        <text x="14" y="40" class="hud-val">99.98% Uptime · 18ms Latency · 0 Leaks</text>
      </g>
      
      <!-- Network Signals / Bars -->
      <g transform="translate(0, 252)">
        <text x="0" y="0" font-size="10.5" fill="{text_muted}">NETWORK SIGNAL</text>
        <g fill="{chrome_col}">
          <rect x="0" y="10" width="8" height="12" rx="2"/>
          <rect x="14" y="6" width="8" height="16" rx="2"/>
          <rect x="28" y="2" width="8" height="20" rx="2"/>
          <rect x="42" y="-2" width="8" height="24" rx="2"/>
        </g>
        <text x="62" y="16" font-size="11" font-weight="700" fill="{chrome_col}">OPTIMAL (5/5)</text>
      </g>
    </g>
    ''')
    
    # Bottom HUD Status Footer Bar
    svg.append(f'<line x1="20" y1="495" x2="1160" y2="495" stroke="{border_col}" stroke-width="1"/>')
    svg.append(f'''
    <g font-size="11" fill="{text_muted}">
      <text x="36" y="515">SYS: LINUX_x86_64 · STATUS: 200 OK · PROTOCOL: HTTPS // ENCRYPTED · REPO: hasim2006/hasim2006</text>
      <text x="1144" y="515" text-anchor="end" fill="{chrome_col}">HUD.ENGINE // v3.4 · MOHAMMAD HASIM</text>
    </g>
    ''')
    
    svg.append('</svg>')
    return "\n".join(svg)

print("Compiling dark and light SVGs...")
dark_svg_code = build_banner_svg("dark")
light_svg_code = build_banner_svg("light")

# Validate XML syntax with ElementTree
ET.fromstring(dark_svg_code)
ET.fromstring(light_svg_code)
print("XML validation PASSED for both dark and light SVGs!")

dark_path = os.path.join(output_dir, "dark.svg")
light_path = os.path.join(output_dir, "light.svg")

with open(dark_path, "w", encoding="utf-8") as f:
    f.write(dark_svg_code)
with open(light_path, "w", encoding="utf-8") as f:
    f.write(light_svg_code)

print(f"dark.svg successfully written: {len(dark_svg_code)/1024:.1f} KB")
print(f"light.svg successfully written: {len(light_svg_code)/1024:.1f} KB")
