import os
import math
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import xml.etree.ElementTree as ET

# Input image
img_path = r"c:\Users\hasim\OneDrive\Desktop\github'\WhatsApp Image 2026-10-09 at 8.49.45 PM.jpeg"
output_dir = r"c:\Users\hasim\OneDrive\Desktop\github'\hasim2006"
os.makedirs(output_dir, exist_ok=True)

# 1. Prepare Full Image Dithering (No polygon mask - complete photographic presence)
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

# 3. Ambient Floating Particles for Tech Atmosphere (around logos, off during photo)
NUM_PARTICLES = 160
np.random.seed(42)
particles = []
cx_box, cy_box = 223.0, 331.0
for i in range(NUM_PARTICLES):
    angle = np.random.uniform(0, 2 * math.pi)
    dist = np.random.uniform(35, 145)
    px = cx_box + dist * math.cos(angle)
    py = cy_box + dist * math.sin(angle)
    r = np.random.uniform(1.0, 2.2)
    # Orbit displacement
    dx = np.random.uniform(-20, 20)
    dy = np.random.uniform(-20, 20)
    particles.append((px, py, r, dx, dy))

# 4. Build SVG Generator
def build_banner_svg(theme="dark"):
    is_dark = (theme == "dark")
    bg_col = "#0A101F" if is_dark else "#F8FAFC"
    panel_bg = "#070c17" if is_dark else "#FFFFFF"
    chrome_col = "#22D3EE" if is_dark else "#0891B2"
    border_col = "#1E293B" if is_dark else "#CBD5E1"
    portrait_col = "#A78BFA" if is_dark else "#7C3AED"
    accent_col = "#10B981"
    text_muted = "#64748B"
    text_label = "#94A3B8" if is_dark else "#475569"
    text_val = "#F8FAFC" if is_dark else "#0F172A"
    leader_col = "#334155" if is_dark else "#E2E8F0"
    
    runs = runs_dark if is_dark else runs_light
    
    # Scale and center photo in the 378x486 box
    # Box is x=34..412, y=88..574
    # Photo is 300x340
    scale = 1.14
    photo_w = 300 * scale # 342
    photo_h = 340 * scale # 387.6
    ox = 34 + (378 - photo_w) / 2 # 52.0
    oy = 88 + (486 - photo_h) / 2 + 10 # 147.2
    
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="100%" height="100%">')
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
        <stop offset="50%" stop-color="#22D3EE" stop-opacity="0.35"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </linearGradient>
      <radialGradient id="haloGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.18"/>
        <stop offset="70%" stop-color="#22D3EE" stop-opacity="0.04"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="pyGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#FACC15" stop-opacity="0.15"/>
        <stop offset="100%" stop-color="#38BDF8" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="jsGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.2"/>
        <stop offset="100%" stop-color="#FBBF24" stop-opacity="0"/>
      </radialGradient>
    ''')
    
    svg.append('<style>')
    svg.append(f'''
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&amp;display=swap');
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
      .sec-hdr {{ fill: {chrome_col}; font-size: 13px; font-weight: 700; letter-spacing: 1.5px; }}
      .row-lbl {{ fill: {text_label}; font-size: 14px; font-weight: 500; }}
      .row-val {{ fill: {text_val}; font-size: 14px; font-weight: 600; }}
      .leader {{ stroke: {leader_col}; stroke-dasharray: 2 4; stroke-width: 1.2; }}
      .accent {{ fill: {accent_col}; }}
    ''')
    svg.append('</style>')
    svg.append('</defs>')
    
    # 1. Main Background Card
    svg.append(f'<rect width="1180" height="610" rx="14" fill="{bg_col}" stroke="{border_col}" stroke-width="1.5"/>')
    
    # Header Bar
    svg.append(f'<line x1="0" y1="44" x2="1180" y2="44" stroke="{border_col}" stroke-width="1"/>')
    svg.append('<circle cx="26" cy="22" r="5.5" class="traffic-red"/>')
    svg.append('<circle cx="44" cy="22" r="5.5" class="traffic-yellow"/>')
    svg.append('<circle cx="62" cy="22" r="5.5" class="traffic-green"/>')
    svg.append('<text x="590" y="27" text-anchor="middle" class="title">profile.sh --live</text>')
    
    # LIVE indicator
    svg.append('<g>')
    svg.append('<circle cx="1004" cy="22" r="4.5" class="live-dot">')
    svg.append('<animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>')
    svg.append('</circle>')
    svg.append('<text x="1016" y="26" class="live-text">LIVE</text>')
    svg.append('</g>')
    
    # User Handle Pill
    svg.append('<g>')
    svg.append('<rect x="1066" y="10" width="98" height="24" rx="12" class="pill-bg"/>')
    svg.append('<text x="1115" y="26" text-anchor="middle" class="pill-text">@hasim2006</text>')
    svg.append('</g>')
    
    # 2. Left Panel: VISUAL.MAP Frame
    svg.append(f'<text x="36" y="74" class="sec-hdr">VISUAL.MAP</text>')
    
    # Dynamic Phase Subtitle at Header (Changes with active sequence)
    # 0s-4.5s: Photo, 4.5s-9s: Python, 9s-13.5s: React, 13.5s-17.5s: JS, 17.5s-18s: Photo
    svg.append(f'''
    <g font-size="11" fill="{text_muted}">
      <!-- Subtitle 0: Photo -->
      <text x="145" y="74">
        · PORTRAIT.ID // MOHAMMAD HASIM
        <animate attributeName="opacity"
          values="1; 1; 0; 0; 0; 0; 0; 0; 1; 1"
          keyTimes="0; 0.233; 0.261; 0.480; 0.720; 0.940; 0.961; 0.989; 1; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
      <!-- Subtitle 1: Python -->
      <text x="145" y="74" fill="#38BDF8">
        · CORE.STACK [01/03] // PYTHON
        <animate attributeName="opacity"
          values="0; 0; 1; 1; 0; 0; 0; 0"
          keyTimes="0; 0.250; 0.278; 0.472; 0.500; 0.750; 0.950; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
      <!-- Subtitle 2: React -->
      <text x="145" y="74" fill="#22D3EE">
        · CORE.STACK [02/03] // REACT
        <animate attributeName="opacity"
          values="0; 0; 1; 1; 0; 0; 0; 0"
          keyTimes="0; 0.489; 0.517; 0.711; 0.739; 0.850; 0.950; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
      <!-- Subtitle 3: JavaScript -->
      <text x="145" y="74" fill="#FBBF24">
        · CORE.STACK [03/03] // JAVASCRIPT
        <animate attributeName="opacity"
          values="0; 0; 1; 1; 0; 0; 0; 0"
          keyTimes="0; 0.728; 0.756; 0.944; 0.972; 0.980; 0.990; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
    </g>
    ''')
    
    # Left Panel Container Box (378 x 486)
    svg.append(f'<rect x="34" y="88" width="378" height="486" rx="10" fill="{panel_bg}" stroke="{border_col}" stroke-width="1"/>')
    # Corner brackets
    svg.append(f'<path d="M 44 98 h 10 M 44 98 v 10 M 402 98 h -10 M 402 98 v 10 M 44 564 h 10 M 44 564 v -10 M 402 564 h -10 M 402 564 v -10" stroke="{chrome_col}55" stroke-width="1.5" fill="none"/>')
    
    # Inner clip-path to ensure portrait stays cleanly within borders
    svg.append('<clipPath id="panelClip"><rect x="36" y="90" width="374" height="482" rx="8"/></clipPath>')
    
    svg.append('<g clip-path="url(#panelClip)">')
    
    # Subtle cybernetic background grid inside box
    svg.append(f'''
    <g stroke="{border_col}" stroke-width="0.5" stroke-dasharray="2 6" opacity="0.6">
      <line x1="36" y1="210" x2="410" y2="210"/>
      <line x1="36" y1="331" x2="410" y2="331"/>
      <line x1="36" y1="452" x2="410" y2="452"/>
      <line x1="160" y1="90" x2="160" y2="572"/>
      <line x1="284" y1="90" x2="284" y2="572"/>
    </g>
    ''')
    
    # =========================================================================
    # LAYER 1: FULL USER PHOTO (Dithered with pure photographic completeness)
    # Active: 0s - 4.5s & 17.5s - 18s
    # =========================================================================
    svg.append('<g id="layer-photo">')
    svg.append('''
      <animate attributeName="opacity"
        values="1; 1; 0; 0; 0; 0; 0; 0; 1; 1"
        keyTimes="0; 0.233; 0.261; 0.480; 0.720; 0.940; 0.961; 0.989; 1; 1"
        dur="18s" repeatCount="indefinite"/>
    ''')
    
    # Path d for all runs
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
      <rect x="44" y="100" width="358" height="28" fill="url(#scanGrad)" opacity="0.75">
        <animate attributeName="y" values="90; 530; 90" dur="4.2s" repeatCount="indefinite"/>
      </rect>
    ''')
    svg.append('</g>') # End layer-photo
    
    # =========================================================================
    # LAYER 2: PYTHON LOGO (Official Dual-Snake Emblem)
    # Active: 4.5s - 9.0s
    # =========================================================================
    svg.append('<g id="layer-python">')
    svg.append('''
      <animate attributeName="opacity"
        values="0; 0; 1; 1; 0; 0; 0; 0"
        keyTimes="0; 0.250; 0.278; 0.472; 0.500; 0.750; 0.950; 1"
        dur="18s" repeatCount="indefinite"/>
    ''')
    
    # Python Background Halo & Reticle
    svg.append(f'<circle cx="{cx_box}" cy="{cy_box}" r="115" fill="url(#pyGlow)"/>')
    svg.append(f'<circle cx="{cx_box}" cy="{cy_box}" r="92" stroke="#38BDF844" stroke-width="1.5" stroke-dasharray="6 8" fill="none"/>')
    svg.append(f'<circle cx="{cx_box}" cy="{cy_box}" r="120" stroke="#FACC1533" stroke-width="1" stroke-dasharray="2 12" fill="none"/>')
    
    # Scaled Python Path (scale 7.2 centered at cx_box, cy_box)
    py_scale = 7.2
    py_ox = cx_box - 12.0 * py_scale
    py_oy = cy_box - 12.0 * py_scale - 12.0
    
    svg.append(f'<g transform="translate({py_ox:.1f}, {py_oy:.1f}) scale({py_scale})">')
    svg.append(f'<path d="{py_path_d}" fill="url(#pyGrad)" filter="drop-shadow(0 0 4px #38BDF866)"/>')
    svg.append('</g>')
    
    # Tech Label & Badges for Python
    svg.append(f'<text x="{cx_box}" y="{cy_box + 96}" text-anchor="middle" fill="#FACC15" font-size="14" font-weight="700" letter-spacing="1.5">PYTHON 3.12</text>')
    svg.append(f'<text x="{cx_box}" y="{cy_box + 114}" text-anchor="middle" fill="{text_label}" font-size="10.5">FASTAPI · AI &amp; ML · NUMPY · BACKEND</text>')
    svg.append('</g>') # End layer-python
    
    # =========================================================================
    # LAYER 3: REACT LOGO (Spinning Atomic Orbitals & Nucleus)
    # Active: 9.0s - 13.5s
    # =========================================================================
    svg.append('<g id="layer-react">')
    svg.append('''
      <animate attributeName="opacity"
        values="0; 0; 1; 1; 0; 0; 0; 0"
        keyTimes="0; 0.489; 0.517; 0.711; 0.739; 0.850; 0.950; 1"
        dur="18s" repeatCount="indefinite"/>
    ''')
    
    # React Halo
    svg.append(f'<circle cx="{cx_box}" cy="{cy_box}" r="115" fill="url(#haloGlow)"/>')
    svg.append(f'<circle cx="{cx_box}" cy="{cy_box}" r="102" stroke="#22D3EE44" stroke-width="1" stroke-dasharray="4 6" fill="none"/>')
    
    # Rotating React Atom
    re_scale = 7.0
    re_ox = cx_box - 12.0 * re_scale
    re_oy = cy_box - 12.0 * re_scale - 12.0
    
    svg.append(f'<g transform="translate({re_ox:.1f}, {re_oy:.1f}) scale({re_scale})">')
    # Rotating outer orbital group
    svg.append(f'''
      <g transform-origin="12 12">
        <animateTransform attributeName="transform" type="rotate"
          from="0 12 12" to="360 12 12" dur="12s" repeatCount="indefinite"/>
        <path d="{re_path_d}" fill="url(#reactGrad)" filter="drop-shadow(0 0 5px #22D3EE88)"/>
      </g>
    ''')
    svg.append('</g>')
    
    # Tech Label & Badges for React
    svg.append(f'<text x="{cx_box}" y="{cy_box + 96}" text-anchor="middle" fill="#22D3EE" font-size="14" font-weight="700" letter-spacing="1.5">REACT 18</text>')
    svg.append(f'<text x="{cx_box}" y="{cy_box + 114}" text-anchor="middle" fill="{text_label}" font-size="10.5">NEXT.JS · HOOKS · VIRTUAL DOM · SPA</text>')
    svg.append('</g>') # End layer-react
    
    # =========================================================================
    # LAYER 4: JAVASCRIPT LOGO (Official JS Badge Emblem)
    # Active: 13.5s - 17.5s
    # =========================================================================
    svg.append('<g id="layer-js">')
    svg.append('''
      <animate attributeName="opacity"
        values="0; 0; 1; 1; 0; 0; 0; 0"
        keyTimes="0; 0.728; 0.756; 0.944; 0.972; 0.980; 0.990; 1"
        dur="18s" repeatCount="indefinite"/>
    ''')
    
    # JS Halo & Reticle
    svg.append(f'<circle cx="{cx_box}" cy="{cy_box}" r="115" fill="url(#jsGlow)"/>')
    svg.append(f'<rect x="{cx_box - 88}" y="{cy_box - 100}" width="176" height="176" rx="14" stroke="#FBBF2455" stroke-width="1.5" stroke-dasharray="8 6" fill="none"/>')
    
    # Scaled JS Emblem
    js_scale = 6.4
    js_ox = cx_box - 12.0 * js_scale
    js_oy = cy_box - 12.0 * js_scale - 12.0
    
    svg.append(f'<g transform="translate({js_ox:.1f}, {js_oy:.1f}) scale({js_scale})">')
    svg.append(f'<path d="{js_path_d}" fill="url(#jsGrad)" fill-rule="evenodd" filter="drop-shadow(0 0 6px #F59E0B77)"/>')
    svg.append('</g>')

    
    # Tech Label & Badges for JavaScript
    svg.append(f'<text x="{cx_box}" y="{cy_box + 96}" text-anchor="middle" fill="#FBBF24" font-size="14" font-weight="700" letter-spacing="1.5">JAVASCRIPT ES6+</text>')
    svg.append(f'<text x="{cx_box}" y="{cy_box + 114}" text-anchor="middle" fill="{text_label}" font-size="10.5">NODE.JS · ASYNC/AWAIT · REST · V8</text>')
    svg.append('</g>') # End layer-js
    
    # =========================================================================
    # LAYER 5: AMBIENT FLOATING CYBERNETIC PARTICLES
    # Active only during logo phases (completely hidden during photo phase!)
    # =========================================================================
    svg.append('<g id="ambient-particles" fill="#22D3EE">')
    # Disappear during photo, burst into life during logos
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
    
    # Dynamic Footer for Left Panel at y=594
    svg.append(f'''
    <g font-size="11" fill="{text_muted}">
      <text x="44" y="594">
        LOC: INDIA · ENCODING: UTF-8 · LATENCY: 18ms
        <animate attributeName="opacity"
          values="1; 1; 0; 0; 0; 0; 0; 0; 1; 1"
          keyTimes="0; 0.233; 0.261; 0.480; 0.720; 0.940; 0.961; 0.989; 1; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
      <text x="44" y="594" fill="#38BDF8">
        STACK: FASTAPI · PYTORCH · FLASK · NUMPY
        <animate attributeName="opacity"
          values="0; 0; 1; 1; 0; 0; 0; 0"
          keyTimes="0; 0.250; 0.278; 0.472; 0.500; 0.750; 0.950; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
      <text x="44" y="594" fill="#22D3EE">
        STACK: NEXT.JS · TAILWIND · REDUX · HOOKS
        <animate attributeName="opacity"
          values="0; 0; 1; 1; 0; 0; 0; 0"
          keyTimes="0; 0.489; 0.517; 0.711; 0.739; 0.850; 0.950; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
      <text x="44" y="594" fill="#FBBF24">
        STACK: TYPESCRIPT · EXPRESS · REST · V8
        <animate attributeName="opacity"
          values="0; 0; 1; 1; 0; 0; 0; 0"
          keyTimes="0; 0.728; 0.756; 0.944; 0.972; 0.980; 0.990; 1"
          dur="18s" repeatCount="indefinite"/>
      </text>
    </g>
    ''')
    
    # =========================================================================
    # RIGHT PANEL: SYSTEM.INFO (Verified Information, Clean Typography)
    # =========================================================================
    svg.append(f'<text x="442" y="74" class="sec-hdr">SYSTEM.INFO</text>')
    svg.append(f'<text x="560" y="74" fill="{text_muted}" font-size="11">· ACTIVE SESSION ID #266045105</text>')
    
    rows = [
        ("Subject", "Mohammad Hasim", 140, text_val),
        ("Role", "Full-Stack Developer", 185, chrome_col), # NO IoT!
        ("Origin", "India", 50, text_val),
        ("Education", "B.Tech CSE", 95, text_val), # NO IoT!
        ("Status", "Building + Learning + Shipping", 260, accent_col),
        ("ToolChain", "VS Code · Git · Postman · Vercel", 280, text_val),
        ("---", "", 0, ""),
        ("Core.Lang", "Python · JavaScript · Java · C", 270, text_val),
        ("Core.Frontend", "React · Next.js · HTML5 · CSS3", 265, text_val),
        ("Core.Backend", "Node.js · Express · FastAPI · Flask", 300, text_val),
        ("Core.Database", "MongoDB · MySQL · Firebase", 230, text_val),
        ("Core.Infra", "AWS · GCP · Vercel · Netlify", 235, text_val),
        ("---", "", 0, ""),
        ("Grid.Mail", "hasimsaudagar3@gmail.com", 225, text_val),
        ("Grid.LinkedIn", "in/mohammad-hasim-9992423a0", 240, chrome_col),
        ("Grid.GitHub", "github.com/hasim2006", 175, chrome_col),
        ("Grid.Portfolio", "portfolio-website.vercel.app", 235, accent_col)
    ]
    
    start_y = 112
    spacing = 25
    curr_y = start_y
    val_right_x = 1144
    
    for label, val, val_len, val_col in rows:
        if label == "---":
            svg.append(f'<line x1="442" y1="{curr_y - 8}" x2="1144" y2="{curr_y - 8}" stroke="{border_col}" stroke-width="1"/>')
            curr_y += 12
            continue
            
        svg.append(f'<text x="442" y="{curr_y}" class="row-lbl">{label}</text>')
        lbl_w = len(label) * 8.8
        dot_start_x = int(442 + lbl_w + 12)
        dot_end_x = int(val_right_x - val_len - 14)
        
        if dot_end_x > dot_start_x:
            svg.append(f'<line x1="{dot_start_x}" y1="{curr_y - 4}" x2="{dot_end_x}" y2="{curr_y - 4}" class="leader"/>')
            
        svg.append(f'''<text x="{val_right_x}" y="{curr_y}" text-anchor="end" textLength="{val_len}" lengthAdjust="spacingAndGlyphs" fill="{val_col}" font-size="14" font-weight="600">{val}</text>''')
        curr_y += spacing
        
    svg.append(f'<line x1="442" y1="565" x2="1144" y2="565" stroke="{border_col}" stroke-width="1"/>')
    svg.append(f'<text x="442" y="585" fill="{text_muted}" font-size="11">SYS: LINUX_x86_64 · STATUS: 200 OK · UPTIME: 99.98% · REPO: hasim2006/hasim2006</text>')
    
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
