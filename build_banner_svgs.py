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

# 2. Ambient Floating Particles for Tech Atmosphere (Centered around cx=590, cy=255)
NUM_PARTICLES = 140
np.random.seed(42)
particles = []
cx_center, cy_center = 590.0, 255.0
for i in range(NUM_PARTICLES):
    angle = np.random.uniform(0, 2 * math.pi)
    dist = np.random.uniform(120, 260)
    px = cx_center + dist * math.cos(angle)
    py = cy_center + (dist * 0.75) * math.sin(angle)
    r = np.random.uniform(1.0, 2.2)
    dx = np.random.uniform(-18, 18)
    dy = np.random.uniform(-18, 18)
    particles.append((px, py, r, dx, dy))

# 3. Build SVG Generator
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
    
    # Scale and center photo in the center stage (Clear, prominent, unconstrained)
    scale = 1.15
    photo_w = 300 * scale # 345
    photo_h = 340 * scale # 391
    ox = cx_center - photo_w / 2 # 417.5
    oy = cy_center - photo_h / 2 + 8 # 67.5
    
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 500" width="100%" height="100%">')
    svg.append('<defs>')
    
    # Gradients & Filters
    svg.append('''
      <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>
        <stop offset="50%" stop-color="#22D3EE" stop-opacity="0.45"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </linearGradient>
      <radialGradient id="haloGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.22"/>
        <stop offset="60%" stop-color="#A78BFA" stop-opacity="0.08"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="reticleGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#A78BFA" stop-opacity="0.14"/>
        <stop offset="100%" stop-color="#A78BFA" stop-opacity="0"/>
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
      .sec-hdr {{ fill: {chrome_col}; font-size: 12.5px; font-weight: 700; letter-spacing: 1.5px; }}
      .vertex-mark {{ fill: {chrome_col}; }}
      .vertex-coord {{ fill: {chrome_col}99; font-size: 9.5px; font-family: monospace; font-weight: 600; }}
      .bracket {{ stroke: {chrome_col}; stroke-width: 2.2; fill: none; }}
    ''')
    svg.append('</style>')
    svg.append('</defs>')
    
    # 1. Main Background Card (Merged seamlessly with background color)
    svg.append(f'<rect width="1180" height="500" rx="12" fill="{bg_col}" stroke="{border_col}" stroke-width="1.2"/>')
    
    # =========================================================================
    # CORNERS, EDGES & VERTICES (Requested: corners and edges with vertices)
    # =========================================================================
    svg.append(f'''
    <!-- Vertices & Corner Brackets -->
    <g>
      <!-- Vertex 1: Top-Left (20, 20) -->
      <path d="M 20 54 V 20 H 54" class="bracket"/>
      <circle cx="20" cy="20" r="3.5" class="vertex-mark"/>
      <text x="26" y="68" class="vertex-coord">V1 [0,0]</text>
      
      <!-- Vertex 2: Top-Right (1160, 20) -->
      <path d="M 1160 54 V 20 H 1126" class="bracket"/>
      <circle cx="1160" cy="20" r="3.5" class="vertex-mark"/>
      <text x="1108" y="68" class="vertex-coord">V2 [1180,0]</text>
      
      <!-- Vertex 3: Bottom-Left (20, 480) -->
      <path d="M 20 446 V 480 H 54" class="bracket"/>
      <circle cx="20" cy="480" r="3.5" class="vertex-mark"/>
      <text x="26" y="438" class="vertex-coord">V3 [0,500]</text>
      
      <!-- Vertex 4: Bottom-Right (1160, 480) -->
      <path d="M 1160 446 V 480 H 1126" class="bracket"/>
      <circle cx="1160" cy="480" r="3.5" class="vertex-mark"/>
      <text x="1090" y="438" class="vertex-coord">V4 [1180,500]</text>
      
      <!-- Midpoint Crosshair Vertices (+) -->
      <g stroke="{chrome_col}88" stroke-width="1">
        <!-- Top Edge Crosshair -->
        <line x1="590" y1="14" x2="590" y2="26"/>
        <line x1="584" y1="20" x2="596" y2="20"/>
        
        <!-- Bottom Edge Crosshair -->
        <line x1="590" y1="474" x2="590" y2="486"/>
        <line x1="584" y1="480" x2="596" y2="480"/>
        
        <!-- Left Edge Crosshair -->
        <line x1="14" y1="250" x2="26" y2="250"/>
        <line x1="20" y1="244" x2="20" y2="256"/>
        
        <!-- Right Edge Crosshair -->
        <line x1="1154" y1="250" x2="1166" y2="250"/>
        <line x1="1160" y1="244" x2="1160" y2="256"/>
      </g>
    </g>
    ''')
    
    # Top Chrome Header Bar
    svg.append(f'<line x1="20" y1="44" x2="1160" y2="44" stroke="{border_col}" stroke-width="1"/>')
    svg.append('<circle cx="60" cy="32" r="5" class="traffic-red"/>')
    svg.append('<circle cx="76" cy="32" r="5" class="traffic-yellow"/>')
    svg.append('<circle cx="92" cy="32" r="5" class="traffic-green"/>')
    svg.append('<text x="590" y="36" text-anchor="middle" class="title">terminal // portrait.id --live</text>')
    
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
    # CENTER STAGE: MOHAMMAD HASIM PORTRAIT (Pure, prominent, no side clutter)
    # =========================================================================
    # Halos and subtle cybernetic rings around portrait
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="210" fill="url(#haloGlow)"/>')
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="185" stroke="{border_col}" stroke-width="1" stroke-dasharray="4 6" fill="none"/>')
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="225" stroke="{chrome_col}22" stroke-width="1" stroke-dasharray="2 12" fill="none"/>')
    
    # Header tag above portrait
    svg.append(f'''
    <text x="{cx_center}" y="70" text-anchor="middle" class="sec-hdr">PORTRAIT.ID // MOHAMMAD HASIM · FULL-STACK &amp; AI DEVELOPER</text>
    ''')
    
    # Floating Ambient Cyber Particles around portrait
    svg.append(f'<g id="ambient-particles" fill="{chrome_col}">')
    for px, py, r, dx, dy in particles:
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" opacity="0.65">')
        svg.append(f'''<animate attributeName="cx"
          values="{px:.1f}; {px + dx:.1f}; {px - dx*0.5:.1f}; {px:.1f}"
          dur="5.6s" repeatCount="indefinite"/>''')
        svg.append(f'''<animate attributeName="cy"
          values="{py:.1f}; {py + dy:.1f}; {py - dy*0.5:.1f}; {py:.1f}"
          dur="5.6s" repeatCount="indefinite"/>''')
        svg.append('</circle>')
    svg.append('</g>')
    
    # Clip-path to frame portrait cleanly
    svg.append(f'<clipPath id="portraitClip"><rect x="{cx_center - 185}" y="76" width="370" height="375" rx="8"/></clipPath>')
    svg.append('<g clip-path="url(#portraitClip)">')
    
    # Permanent High-Resolution Dithered Portrait (Always Visible)
    path_runs = []
    for y, sx, length in runs:
        px = ox + sx * scale
        py = oy + y * scale
        pw = length * scale
        ph = scale
        path_runs.append(f'M {px:.1f} {py:.1f} h {pw:.1f} v {ph:.1f} h -{pw:.1f} Z')
    photo_d = " ".join(path_runs)
    
    svg.append(f'<path fill="{portrait_col}" d="{photo_d}" shape-rendering="crispEdges"/>')
    
    # Cybernetic Scanning Laser Beam
    svg.append(f'''
      <rect x="{cx_center - 175}" y="80" width="350" height="26" fill="url(#scanGrad)" opacity="0.8">
        <animate attributeName="y" values="80; 430; 80" dur="4.2s" repeatCount="indefinite"/>
      </rect>
    ''')
    svg.append('</g>') # End portraitClip
    
    # Bottom HUD Status Footer Bar
    svg.append(f'<line x1="20" y1="458" x2="1160" y2="458" stroke="{border_col}" stroke-width="1"/>')
    svg.append(f'''
    <g font-size="11" fill="{text_muted}">
      <text x="60" y="476">SYS: LINUX_x86_64 · STATUS: 200 OK · PORTRAIT: MOHAMMAD HASIM · REPO: hasim2006/hasim2006</text>
      <text x="1120" y="476" text-anchor="end" fill="{chrome_col}">HUD.CORE // v4.0 · B.TECH CSE</text>
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
