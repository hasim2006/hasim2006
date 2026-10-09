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

# Geometry: Fine 12x14 grid for small pixel tiles ("joint with small pixcels to pixcels")
COLS, ROWS = 12, 14
scale = 1.15
photo_w = 300 * scale # 345
photo_h = 340 * scale # 391
cx_center, cy_center = 590.0, 215.0
ox = cx_center - photo_w / 2 # 417.5
oy = cy_center - photo_h / 2 # 19.5

# Total cycle duration: 30 seconds
# 0s - 10s: Progressive pixel-by-pixel decode & materialization (10 seconds)
# 10s - 25s: 100% fully assembled and stable portrait (15 full seconds)
# 25s - 28s: Shatters outward into small pieces ("choote pieces mai tut jaye")
# 28s - 30s: Dissolves and seamlessly restarts next cycle
CYCLE_DUR = 30.0

# 2. Extract runs per tile for Dark and Light
def extract_tile_runs(dot_matrix):
    tiles_data = []
    tile_idx = 0
    np.random.seed(42)
    
    for r in range(ROWS):
        y1 = r * (h // ROWS)
        y2 = (r + 1) * (h // ROWS) if r < ROWS - 1 else h
        for c in range(COLS):
            x1 = c * (w // COLS)
            x2 = (c + 1) * (w // COLS) if c < COLS - 1 else w
            
            sub = dot_matrix[y1:y2, x1:x2]
            sh, sw = sub.shape
            
            runs = []
            for ty in range(sh):
                in_run = False
                start_x = 0
                for tx in range(sw):
                    if sub[ty, tx]:
                        if not in_run:
                            in_run = True
                            start_x = tx
                    else:
                        if in_run:
                            runs.append((ty, start_x, tx - start_x))
                            in_run = False
                if in_run:
                    runs.append((ty, start_x, sw - start_x))
            
            if len(runs) == 0:
                continue
                
            # Path data for this tile
            path_runs = []
            for ty, start_x, length in runs:
                abs_x = x1 + start_x
                abs_y = y1 + ty
                px = ox + abs_x * scale
                py = oy + abs_y * scale
                pw = length * scale
                ph = scale
                path_runs.append(f'M {px:.1f} {py:.1f} h {pw:.1f} v {ph:.1f} h -{pw:.1f} Z')
            
            d_str = " ".join(path_runs)
            
            # Center of this tile
            tile_cx = ox + ((x1 + x2) / 2.0) * scale
            tile_cy = oy + ((y1 + y2) / 2.0) * scale
            
            # Progressive decode timing: 0.1s to 8.8s start + 1.1s decode time
            # By 9.9s (< 10.0s), 100% of all tiles across the face are completely locked!
            row_frac = r / float(ROWS - 1)
            col_frac = c / float(COLS - 1)
            jitter = np.random.uniform(-0.10, 0.10)
            prog = np.clip(row_frac * 0.86 + col_frac * 0.08 + jitter, 0.0, 1.0)
            t_start = 0.1 + prog * 8.6
            t_mid1 = t_start + 0.35
            t_mid2 = t_start + 0.70
            t_loaded = t_start + 1.05
            
            # Micro-jitter for encode/decode holographic flicker
            jx = np.random.uniform(-5.0, 5.0)
            jy = np.random.uniform(-4.0, 4.0)
            
            # Shatter vector at 25s (explode outward in small pieces)
            vx = tile_cx - cx_center
            vy = tile_cy - cy_center
            base_dist = math.sqrt(vx * vx + vy * vy) + 1e-4
            base_angle = math.atan2(vy, vx)
            spread = np.random.uniform(-0.40, 0.40)
            final_angle = base_angle + spread
            
            disp_dist = np.random.uniform(90.0, 240.0)
            dx = disp_dist * math.cos(final_angle)
            dy = disp_dist * math.sin(final_angle)
            rot = np.random.uniform(-120.0, 120.0)
            
            tiles_data.append({
                'id': tile_idx,
                'r': r,
                'c': c,
                'cx': tile_cx,
                'cy': tile_cy,
                'd': d_str,
                't_start': t_start,
                't_mid1': t_mid1,
                't_mid2': t_mid2,
                't_loaded': t_loaded,
                'jx': jx,
                'jy': jy,
                'dx': dx,
                'dy': dy,
                'rot': rot
            })
            tile_idx += 1
            
    return tiles_data

tiles_dark = extract_tile_runs(dots_dark)
tiles_light = extract_tile_runs(dots_light)
print(f"Dark active tiles: {len(tiles_dark)}, Light active tiles: {len(tiles_light)}")

# 3. Ambient Floating Particles for Tech Atmosphere
NUM_PARTICLES = 140
np.random.seed(42)
particles = []
for i in range(NUM_PARTICLES):
    angle = np.random.uniform(0, 2 * math.pi)
    dist = np.random.uniform(120, 260)
    px = cx_center + dist * math.cos(angle)
    py = cy_center + (dist * 0.75) * math.sin(angle)
    r = np.random.uniform(1.0, 2.2)
    dx = np.random.uniform(-18, 18)
    dy = np.random.uniform(-18, 18)
    particles.append((px, py, r, dx, dy))

# 4. Build SVG Generator
def build_banner_svg(theme="dark"):
    is_dark = (theme == "dark")
    chrome_col = "#22D3EE" if is_dark else "#0891B2"
    border_col = "#1E293B" if is_dark else "#CBD5E1"
    portrait_col = "#A78BFA" if is_dark else "#7C3AED"
    
    tiles = tiles_dark if is_dark else tiles_light
    
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 430" width="100%" height="100%">')
    svg.append('<defs>')
    
    svg.append('''
      <linearGradient id="scanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>
        <stop offset="50%" stop-color="#22D3EE" stop-opacity="0.55"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </linearGradient>
      <radialGradient id="haloGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.24"/>
        <stop offset="60%" stop-color="#A78BFA" stop-opacity="0.08"/>
        <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
      </radialGradient>
    ''')
    
    # CSS Keyframes for Laser Scanner & All Tiles
    css_rules = []
    css_rules.append('''
      /* Laser Scanner: 0-10s sweeps down with decode wave, 10-25s sweeps across assembled face, 25s fades at shatter */
      @keyframes laserScan30s {
        0% { transform: translateY(20px); opacity: 0.9; }
        33.33% { transform: translateY(380px); opacity: 0.9; }
        58.0% { transform: translateY(140px); opacity: 0.65; }
        83.33% { transform: translateY(340px); opacity: 0.85; }
        85.0% { transform: translateY(360px); opacity: 0.95; }
        88.0% { transform: translateY(370px); opacity: 0; }
        98.0% { transform: translateY(20px); opacity: 0; }
        100% { transform: translateY(20px); opacity: 0.9; }
      }
      .scanner-beam {
        animation: laserScan30s 30s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      }
    ''')
    
    # Keyframe for each tile:
    # 0s - 10s: Encode/decode pixel-by-pixel load (10 seconds)
    # 10s - 25s: 15 FULL SECONDS STABLE & FULLY ASSEMBLED (100% solid and clear)
    # 25s - 27.8s: Shatters into small pieces ("choote pieces mai tut jaye")
    # 27.8s - 30s: Dissolves to 0 opacity and resets for next cycle
    for t in tiles:
        tid = t['id']
        p_start = (t['t_start'] / CYCLE_DUR) * 100.0
        p_mid1 = (t['t_mid1'] / CYCLE_DUR) * 100.0
        p_mid2 = (t['t_mid2'] / CYCLE_DUR) * 100.0
        p_loaded = (t['t_loaded'] / CYCLE_DUR) * 100.0
        p_shatter_start = (25.0 / CYCLE_DUR) * 100.0 # Exactly 25.0s (15s after 10s load)
        p_shattered = (27.8 / CYCLE_DUR) * 100.0     # 27.8s fully dispersed
        
        jx = t['jx']
        jy = t['jy']
        dx = t['dx']
        dy = t['dy']
        rot = t['rot']
        
        css_rules.append(f'''
          @keyframes kf_tile_{tid} {{
            0% {{
              opacity: 0;
              transform: scale(0.6);
            }}
            {p_start:.2f}% {{
              opacity: 0;
              transform: scale(0.6);
            }}
            {p_mid1:.2f}% {{
              opacity: 0.55;
              transform: translate({jx:.1f}px, {jy:.1f}px) scale(1.1);
            }}
            {p_mid2:.2f}% {{
              opacity: 0.85;
              transform: translate({-jx*0.4:.1f}px, {-jy*0.4:.1f}px) scale(0.96);
            }}
            {p_loaded:.2f}% {{
              opacity: 1;
              transform: translate(0px, 0px) scale(1) rotate(0deg);
            }}
            {p_shatter_start:.2f}% {{
              opacity: 1;
              transform: translate(0px, 0px) scale(1) rotate(0deg);
            }}
            {p_shattered:.2f}% {{
              opacity: 0;
              transform: translate({dx:.1f}px, {dy:.1f}px) scale(0.18) rotate({rot:.1f}deg);
            }}
            100% {{
              opacity: 0;
              transform: scale(0.6);
            }}
          }}
          .tile-{tid} {{
            transform-origin: {t['cx']:.1f}px {t['cy']:.1f}px;
            animation: kf_tile_{tid} 30s cubic-bezier(0.2, 0.8, 0.2, 1) infinite;
          }}
        ''')
    
    svg.append('<style>')
    svg.append("".join(css_rules))
    svg.append('</style>')
    svg.append('</defs>')
    
    # Transparent Canvas (No box, zero borders)
    svg.append('<rect width="1180" height="430" fill="none"/>')
    
    # Ambient Halos & Concentric Reticles (Pulsing background)
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
    
    # Clip-path to frame outer boundary cleanly
    svg.append(f'<clipPath id="portraitClip"><rect x="{cx_center - 185}" y="20" width="370" height="390" rx="14"/></clipPath>')
    svg.append('<g clip-path="url(#portraitClip)">')
    
    # Render all small tile paths (Pixel-by-pixel decode, 15s stable, and shatter into pieces)
    for t in tiles:
        tid = t['id']
        d_str = t['d']
        svg.append(f'<path fill="{portrait_col}" d="{d_str}" class="tile-{tid}" shape-rendering="crispEdges"/>')
    
    # Scanning Cyber Laser Beam (Synchronized with 30s cycle)
    svg.append(f'''
      <rect x="{cx_center - 175}" y="0" width="350" height="28" fill="url(#scanGrad)" class="scanner-beam"/>
    ''')
    svg.append('</g>') # End portraitClip
    
    svg.append('</svg>')
    return "\n".join(svg)

print("Compiling dark and light decode, 15s stable & shatter SVGs...")
dark_svg_code = build_banner_svg("dark")
light_svg_code = build_banner_svg("light")

# Validate XML syntax with ElementTree
ET.fromstring(dark_svg_code)
ET.fromstring(light_svg_code)
print("XML validation PASSED for both decode & shatter SVGs!")

dark_path = os.path.join(output_dir, "dark.svg")
light_path = os.path.join(output_dir, "light.svg")

with open(dark_path, "w", encoding="utf-8") as f:
    f.write(dark_svg_code)
with open(light_path, "w", encoding="utf-8") as f:
    f.write(light_svg_code)

print(f"dark.svg successfully written: {len(dark_svg_code)/1024:.1f} KB")
print(f"light.svg successfully written: {len(light_svg_code)/1024:.1f} KB")
