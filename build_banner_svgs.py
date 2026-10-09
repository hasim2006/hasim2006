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

# 2. Ambient Floating Particles for Tech Atmosphere (Centered around cx=590, cy=215)
NUM_PARTICLES = 140
np.random.seed(42)
particles = []
cx_center, cy_center = 590.0, 215.0
for i in range(NUM_PARTICLES):
    angle = np.random.uniform(0, 2 * math.pi)
    dist = np.random.uniform(120, 260)
    px = cx_center + dist * math.cos(angle)
    py = cy_center + (dist * 0.75) * math.sin(angle)
    r = np.random.uniform(1.0, 2.2)
    dx = np.random.uniform(-18, 18)
    dy = np.random.uniform(-18, 18)
    particles.append((px, py, r, dx, dy))

# 3. Build SVG Generator (Borderless, Edge-to-Edge Matching Side Borders)
def build_banner_svg(theme="dark"):
    is_dark = (theme == "dark")
    chrome_col = "#22D3EE" if is_dark else "#0891B2"
    border_col = "#1E293B" if is_dark else "#CBD5E1"
    portrait_col = "#A78BFA" if is_dark else "#7C3AED"
    
    runs = runs_dark if is_dark else runs_light
    
    scale = 1.15
    photo_w = 300 * scale # 345
    photo_h = 340 * scale # 391
    ox = cx_center - photo_w / 2 # 417.5
    oy = cy_center - photo_h / 2 # 19.5
    
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 430" width="100%" height="100%">')
    svg.append('<defs>')
    
    svg.append('''
      <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>
        <stop offset="50%" stop-color="#22D3EE" stop-opacity="0.45"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="edgeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.85"/>
        <stop offset="25%" stop-color="#22D3EE" stop-opacity="0.25"/>
        <stop offset="50%" stop-color="#A78BFA" stop-opacity="0.15"/>
        <stop offset="75%" stop-color="#10B981" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="#10B981" stop-opacity="0.85"/>
      </linearGradient>
      <radialGradient id="haloGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.24"/>
        <stop offset="60%" stop-color="#A78BFA" stop-opacity="0.08"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </radialGradient>
    ''')
    
    svg.append('</defs>')
    
    # Fully transparent background: NO ENCLOSED BOX, merges directly with page background
    svg.append('<rect width="1180" height="430" fill="none"/>')
    
    # =========================================================================
    # SIDE BORDER ALIGNMENT: Full width edge-to-edge lines touching side borders (0 to 1180)
    # =========================================================================
    svg.append(f'''
    <!-- Top & Bottom Edge Accents matching the container side borders -->
    <line x1="0" y1="2" x2="1180" y2="2" stroke="url(#edgeGrad)" stroke-width="1.2"/>
    <line x1="0" y1="428" x2="1180" y2="428" stroke="url(#edgeGrad)" stroke-width="1.2"/>
    
    <!-- Left Side Border Tech Marker (x=0) -->
    <path d="M 0 16 H 24 M 0 414 H 24" stroke="{chrome_col}" stroke-width="2" opacity="0.8"/>
    <circle cx="2" cy="16" r="2.5" fill="{chrome_col}"/>
    <circle cx="2" cy="414" r="2.5" fill="{chrome_col}"/>
    
    <!-- Right Side Border Tech Marker (x=1180) -->
    <path d="M 1180 16 H 1156 M 1180 414 H 1156" stroke="{chrome_col}" stroke-width="2" opacity="0.8"/>
    <circle cx="1178" cy="16" r="2.5" fill="{chrome_col}"/>
    <circle cx="1178" cy="414" r="2.5" fill="{chrome_col}"/>
    ''')
    
    # =========================================================================
    # CENTER STAGE: PROMINENT PORTRAIT (Borderless, Free of Box)
    # =========================================================================
    # Halo and concentric reticle rings around portrait
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="215" fill="url(#haloGlow)"/>')
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="190" stroke="{border_col}" stroke-width="1" stroke-dasharray="4 6" fill="none"/>')
    svg.append(f'<circle cx="{cx_center}" cy="{cy_center}" r="228" stroke="{chrome_col}22" stroke-width="1" stroke-dasharray="2 12" fill="none"/>')
    
    # Floating Ambient Cyber Particles
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
    svg.append(f'<clipPath id="portraitClip"><rect x="{cx_center - 185}" y="20" width="370" height="390" rx="14"/></clipPath>')
    svg.append('<g clip-path="url(#portraitClip)">')
    
    # Permanent High-Resolution Dithered Portrait
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
      <rect x="{cx_center - 175}" y="25" width="350" height="26" fill="url(#scanGrad)" opacity="0.8">
        <animate attributeName="y" values="25; 380; 25" dur="4.2s" repeatCount="indefinite"/>
      </rect>
    ''')
    svg.append('</g>') # End portraitClip
    
    svg.append('</svg>')
    return "\n".join(svg)

print("Compiling dark and light borderless SVGs...")
dark_svg_code = build_banner_svg("dark")
light_svg_code = build_banner_svg("light")

# Validate XML syntax with ElementTree
ET.fromstring(dark_svg_code)
ET.fromstring(light_svg_code)
print("XML validation PASSED for both borderless SVGs!")

dark_path = os.path.join(output_dir, "dark.svg")
light_path = os.path.join(output_dir, "light.svg")

with open(dark_path, "w", encoding="utf-8") as f:
    f.write(dark_svg_code)
with open(light_path, "w", encoding="utf-8") as f:
    f.write(light_svg_code)

print(f"dark.svg successfully written: {len(dark_svg_code)/1024:.1f} KB")
print(f"light.svg successfully written: {len(light_svg_code)/1024:.1f} KB")
