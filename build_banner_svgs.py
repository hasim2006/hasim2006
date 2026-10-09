import os
import math
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageEnhance

# Input paths
img_path = r"c:\Users\hasim\OneDrive\Desktop\github'\WhatsApp Image 2026-10-09 at 8.49.45 PM.jpeg"
output_dir = r"c:\Users\hasim\OneDrive\Desktop\github'\hasim2006"
os.makedirs(output_dir, exist_ok=True)

# 1. Load and Crop
img_rgb = Image.open(img_path).convert("RGB")
crop_box = (80, 20, 672, 690)
cropped = img_rgb.crop(crop_box)
cropped = cropped.resize((300, 340), Image.Resampling.LANCZOS)

enhancer = ImageEnhance.Contrast(cropped)
img_contrast = enhancer.enhance(1.3)
img_auto = ImageOps.autocontrast(img_contrast, cutoff=1)
img_sharp = img_auto.filter(ImageFilter.UnsharpMask(radius=3, percent=140))

gray = img_sharp.convert("L")
arr_gray = np.array(gray, dtype=np.float32)
h, w = arr_gray.shape # 340, 300

# 2. Subject Polygon Mask
poly_points = [
    # Top hair contour
    (108, 55), (118, 38), (130, 26), (150, 24), (165, 30), (178, 42), (186, 58), (188, 75), (188, 95),
    # Right ear / jaw
    (191, 108), (192, 128), (188, 148), (182, 170), (176, 185),
    # Right shoulder / jacket
    (195, 192), (220, 202), (250, 215), (280, 228), (300, 240), (300, 340),
    # Bottom
    (0, 340),
    # Left shoulder / jacket
    (0, 240), (25, 222), (55, 205), (80, 195),
    # Left neck / ear / hair
    (92, 185), (88, 168), (86, 148), (87, 128), (88, 108), (92, 90), (96, 70)
]
mask_img = Image.new("L", (w, h), 0)
draw = ImageDraw.Draw(mask_img)
draw.polygon(poly_points, fill=255)
mask = np.array(mask_img) > 0

# 3. Floyd-Steinberg Dithering
def dither_dark_mode(gray_arr, mask_arr):
    mat = gray_arr.copy()
    mat[~mask_arr] = 0.0
    dots = np.zeros((h, w), dtype=bool)
    for y in range(h):
        xs = range(w) if y % 2 == 0 else range(w - 1, -1, -1)
        step = 1 if y % 2 == 0 else -1
        for x in xs:
            if not mask_arr[y, x]:
                mat[y, x] = 0.0
                continue
            old_val = mat[y, x]
            new_val = 255.0 if old_val >= 128.0 else 0.0
            dots[y, x] = (new_val == 255.0)
            err = old_val - new_val
            if step == 1:
                if x + 1 < w and mask_arr[y, x + 1]:
                    mat[y, x + 1] += err * (7.0 / 16.0)
                if y + 1 < h:
                    if x - 1 >= 0 and mask_arr[y + 1, x - 1]:
                        mat[y + 1, x - 1] += err * (3.0 / 16.0)
                    if mask_arr[y + 1, x]:
                        mat[y + 1, x] += err * (5.0 / 16.0)
                    if x + 1 < w and mask_arr[y + 1, x + 1]:
                        mat[y + 1, x + 1] += err * (1.0 / 16.0)
            else:
                if x - 1 >= 0 and mask_arr[y, x - 1]:
                    mat[y, x - 1] += err * (7.0 / 16.0)
                if y + 1 < h:
                    if x + 1 < w and mask_arr[y + 1, x + 1]:
                        mat[y + 1, x + 1] += err * (3.0 / 16.0)
                    if mask_arr[y + 1, x]:
                        mat[y + 1, x] += err * (5.0 / 16.0)
                    if x - 1 >= 0 and mask_arr[y + 1, x - 1]:
                        mat[y + 1, x - 1] += err * (1.0 / 16.0)
    return dots

def dither_light_mode(gray_arr, mask_arr):
    mat = gray_arr.copy()
    mat[~mask_arr] = 255.0
    mat = 255.0 - mat # Invert: dark parts high
    mat[~mask_arr] = 0.0
    dots = np.zeros((h, w), dtype=bool)
    for y in range(h):
        xs = range(w) if y % 2 == 0 else range(w - 1, -1, -1)
        step = 1 if y % 2 == 0 else -1
        for x in xs:
            if not mask_arr[y, x]:
                mat[y, x] = 0.0
                continue
            old_val = mat[y, x]
            new_val = 255.0 if old_val >= 128.0 else 0.0
            dots[y, x] = (new_val == 255.0)
            err = old_val - new_val
            if step == 1:
                if x + 1 < w and mask_arr[y, x + 1]:
                    mat[y, x + 1] += err * (7.0 / 16.0)
                if y + 1 < h:
                    if x - 1 >= 0 and mask_arr[y + 1, x - 1]:
                        mat[y + 1, x - 1] += err * (3.0 / 16.0)
                    if mask_arr[y + 1, x]:
                        mat[y + 1, x] += err * (5.0 / 16.0)
                    if x + 1 < w and mask_arr[y + 1, x + 1]:
                        mat[y + 1, x + 1] += err * (1.0 / 16.0)
            else:
                if x - 1 >= 0 and mask_arr[y, x - 1]:
                    mat[y, x - 1] += err * (7.0 / 16.0)
                if y + 1 < h:
                    if x + 1 < w and mask_arr[y + 1, x + 1]:
                        mat[y + 1, x + 1] += err * (3.0 / 16.0)
                    if mask_arr[y + 1, x]:
                        mat[y + 1, x] += err * (5.0 / 16.0)
                    if x - 1 >= 0 and mask_arr[y + 1, x - 1]:
                        mat[y + 1, x - 1] += err * (1.0 / 16.0)
    return dots

dots_dark = dither_dark_mode(arr_gray, mask)
dots_light = dither_light_mode(arr_gray, mask)

print(f"Dark mode dots: {np.sum(dots_dark)}")
print(f"Light mode dots: {np.sum(dots_light)}")

# Convert dots into runs M x y h L v 1 h -L Z
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

# 4. Group runs into 94 drift bands with organic noise
NUM_BANDS = 94
cx_grid, cy_grid = 150.0, 170.0

def assign_bands(runs):
    np.random.seed(42)
    keys = []
    for y, sx, length in runs:
        mx = sx + length / 2.0
        r = math.sqrt((mx - cx_grid)**2 + (y - cy_grid)**2)
        angle = math.atan2(y - cy_grid, mx - cx_grid)
        noise = np.random.normal(0, 4.0)
        key = r + 15.0 * math.sin(3.0 * angle) + noise
        keys.append(key)
    
    order = np.argsort(keys)
    band_assignment = np.zeros(len(runs), dtype=int)
    chunk_size = len(runs) / NUM_BANDS
    for rank, orig_idx in enumerate(order):
        band = min(NUM_BANDS - 1, int(rank / chunk_size))
        band_assignment[orig_idx] = band
        
    return band_assignment

# 5. Generate 3 Logos for Travellers
NUM_TRAVELLERS = 900
def generate_logos():
    np.random.seed(42)
    # 1. Code bracket `</>`
    p1 = []
    n_part = NUM_TRAVELLERS // 3
    for i in range(n_part // 2):
        t = i / (n_part // 2)
        p1.append([122.0 - 32.0 * t, 125.0 + 45.0 * t])
    for i in range(n_part // 2):
        t = i / (n_part // 2)
        p1.append([90.0 + 32.0 * t, 170.0 + 45.0 * t])
    for i in range(n_part):
        t = i / n_part
        p1.append([138.0 + 24.0 * t, 220.0 - 100.0 * t])
    n_right = NUM_TRAVELLERS - len(p1)
    for i in range(n_right // 2):
        t = i / (n_right // 2)
        p1.append([178.0 + 32.0 * t, 125.0 + 45.0 * t])
    for i in range(n_right - n_right // 2):
        t = i / (n_right - n_right // 2)
        p1.append([210.0 - 32.0 * t, 170.0 + 45.0 * t])
    p1 = np.array(p1, dtype=np.float32)[:NUM_TRAVELLERS]
    p1 += np.random.normal(0, 0.7, p1.shape)

    # 2. React logo
    p2 = []
    n_nuc = int(NUM_TRAVELLERS * 0.16)
    for i in range(n_nuc):
        r = math.sqrt(np.random.uniform(0, 1)) * 14.0
        theta = np.random.uniform(0, 2 * math.pi)
        p2.append([cx_grid + r * math.cos(theta), cy_grid + r * math.sin(theta)])
    a, b = 72.0, 24.0
    n_orbit = (NUM_TRAVELLERS - n_nuc) // 3
    for angle_deg in [0, 60, 120]:
        rad = math.radians(angle_deg)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        for i in range(n_orbit):
            t = (i / n_orbit) * 2 * math.pi
            ex = a * math.cos(t)
            ey = b * math.sin(t)
            p2.append([cx_grid + ex * cos_a - ey * sin_a, cy_grid + ex * sin_a + ey * cos_a])
    while len(p2) < NUM_TRAVELLERS:
        p2.append(p2[-1])
    p2 = np.array(p2[:NUM_TRAVELLERS], dtype=np.float32)
    p2 += np.random.normal(0, 0.6, p2.shape)

    # 3. Python logo
    p3 = []
    n_half = NUM_TRAVELLERS // 2
    for i in range(n_half):
        t = (i / n_half) * 2 * math.pi
        if t < math.pi:
            x = cx_grid + 36.0 * math.cos(t) - 10.0
            y = cy_grid - 22.0 - 30.0 * math.sin(t)
        else:
            x = cx_grid - 10.0 + 24.0 * math.cos(t)
            y = cy_grid - 22.0 + 36.0 * math.sin(t) * 0.6
        p3.append([x, y])
    p3[0] = [cx_grid - 22.0, cy_grid - 38.0]
    p3[1] = [cx_grid - 21.0, cy_grid - 38.0]
    p3[2] = [cx_grid - 22.0, cy_grid - 37.0]
    for i in range(NUM_TRAVELLERS - n_half):
        px, py = p3[i]
        p3.append([2 * cx_grid - px, 2 * cy_grid - py])
    p3 = np.array(p3[:NUM_TRAVELLERS], dtype=np.float32)
    p3 += np.random.normal(0, 0.7, p3.shape)

    def match(src, tgt):
        n = len(src)
        matched = np.zeros_like(tgt)
        avail = np.ones(n, dtype=bool)
        angles = np.arctan2(src[:, 1] - cy_grid, src[:, 0] - cx_grid)
        order = np.argsort(angles)
        for idx in order:
            pt = src[idx]
            dists = np.sum((tgt - pt)**2, axis=1)
            dists[~avail] = 1e9
            best = np.argmin(dists)
            matched[idx] = tgt[best]
            avail[best] = False
        return matched

    p2_m = match(p1, p2)
    p3_m = match(p2_m, p3)
    return p1, p2_m, p3_m

p1_logo, p2_logo, p3_logo = generate_logos()

# 6. SVG Builder
def build_svg(theme="dark"):
    is_dark = (theme == "dark")
    bg_col = "#0A101F" if is_dark else "#F8FAFC"
    panel_bg = "#070c17" if is_dark else "#FFFFFF"
    chrome_col = "#22D3EE" if is_dark else "#0891B2"
    border_col = "#1E293B" if is_dark else "#E2E8F0"
    portrait_col = "#A78BFA" if is_dark else "#7C3AED"
    accent_col = "#10B981"
    text_muted = "#64748B"
    text_label = "#94A3B8" if is_dark else "#475569"
    text_val = "#F8FAFC" if is_dark else "#0F172A"
    leader_col = "#334155" if is_dark else "#CBD5E1"
    
    dots_arr = dots_dark if is_dark else dots_light
    runs = extract_runs(dots_arr)
    bands = assign_bands(runs)
    
    scale = 1.14
    ox = 52.0
    oy = 132.0
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" width="100%" height="100%">')
    svg.append('<defs>')
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
    svg.append('</defs>')
    
    # Terminal Window Background
    svg.append(f'<rect width="1180" height="610" rx="14" fill="{bg_col}" stroke="{border_col}" stroke-width="1.5"/>')
    
    # Window Top Header Bar (height 44)
    svg.append(f'<line x1="0" y1="44" x2="1180" y2="44" stroke="{border_col}" stroke-width="1"/>')
    svg.append('<circle cx="26" cy="22" r="5.5" class="traffic-red"/>')
    svg.append('<circle cx="44" cy="22" r="5.5" class="traffic-yellow"/>')
    svg.append('<circle cx="62" cy="22" r="5.5" class="traffic-green"/>')
    
    # Centered Title
    svg.append('<text x="590" y="27" text-anchor="middle" class="title">profile.sh --live</text>')
    
    # Pulsing LIVE Badge
    svg.append('<g>')
    svg.append('<circle cx="1004" cy="22" r="4.5" class="live-dot">')
    svg.append('<animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>')
    svg.append('</circle>')
    svg.append('<text x="1016" y="26" class="live-text">LIVE</text>')
    svg.append('</g>')
    
    # Coloured Handle Pill
    svg.append('<g>')
    svg.append('<rect x="1066" y="10" width="98" height="24" rx="12" class="pill-bg"/>')
    svg.append('<text x="1115" y="26" text-anchor="middle" class="pill-text">@hasim2006</text>')
    svg.append('</g>')
    
    # Left Panel: VISUAL.MAP
    svg.append(f'<text x="36" y="74" class="sec-hdr">VISUAL.MAP</text>')
    svg.append(f'<text x="150" y="74" fill="{text_muted}" font-size="11">· 300x340 Floyd-Steinberg Dither</text>')
    
    # Portrait Frame
    svg.append(f'<rect x="34" y="88" width="378" height="486" rx="10" fill="{panel_bg}" stroke="{border_col}" stroke-width="1"/>')
    svg.append(f'<path d="M 44 98 h 8 M 44 98 v 8 M 402 98 h -8 M 402 98 v 8 M 44 564 h 8 M 44 564 v -8 M 402 564 h -8 M 402 564 v -8" stroke="{chrome_col}44" stroke-width="1.5" fill="none"/>')
    svg.append(f'<text x="44" y="594" fill="{text_muted}" font-size="11">LOC: 12.9716°N 77.5946°E · LATENCY: 24ms</text>')
    
    # --- PORTRAIT LAYER (Full density dots grouped into 94 drift bands) ---
    svg.append(f'<g shape-rendering="crispEdges">')
    
    band_paths = [[] for _ in range(NUM_BANDS)]
    band_centroids = [[] for _ in range(NUM_BANDS)]
    
    for i, (y, sx, length) in enumerate(runs):
        b = bands[i]
        px = ox + sx * scale
        py = oy + y * scale
        pw = length * scale
        ph = scale
        band_paths[b].append(f'M {px:.1f} {py:.1f} h {pw:.1f} v {ph:.1f} h -{pw:.1f} Z')
        band_centroids[b].append((px, py))
        
    for b in range(NUM_BANDS):
        if not band_paths[b]:
            continue
        d_str = " ".join(band_paths[b])
        pts = band_centroids[b]
        b_cx = sum(p[0] for p in pts) / len(pts)
        b_cy = sum(p[1] for p in pts) / len(pts)
        
        logo_cx = ox + cx_grid * scale
        logo_cy = oy + cy_grid * scale
        dx = 0.42 * (logo_cx - b_cx)
        dy = 0.42 * (logo_cy - b_cy)
        
        svg.append(f'<path fill="{portrait_col}" d="{d_str}">')
        svg.append(f'''<animateTransform attributeName="transform" type="translate"
          values="0,0; 0,0; {dx:.1f},{dy:.1f}; {dx:.1f},{dy:.1f}; {dx:.1f},{dy:.1f}; {dx:.1f},{dy:.1f}; {dx:.1f},{dy:.1f}; {dx:.1f},{dy:.1f}; 0,0; 0,0"
          keyTimes="0; 0.211; 0.303; 0.444; 0.535; 0.676; 0.768; 0.908; 0.98; 1"
          dur="14.2s" repeatCount="indefinite"/>''')
        svg.append(f'''<animate attributeName="opacity"
          values="1; 1; 0; 0; 0; 0; 0; 0; 1; 1"
          keyTimes="0; 0.211; 0.303; 0.444; 0.535; 0.676; 0.768; 0.908; 0.98; 1"
          dur="14.2s" repeatCount="indefinite"/>''')
        svg.append('</path>')
        
    svg.append('</g>')
    
    # --- TRAVELLERS LAYER (~900 dots morphing between 3 logos) ---
    svg.append(f'<g fill="{portrait_col}">')
    for i in range(NUM_TRAVELLERS):
        x1 = ox + p1_logo[i, 0] * scale
        y1 = oy + p1_logo[i, 1] * scale
        x2 = ox + p2_logo[i, 0] * scale
        y2 = oy + p2_logo[i, 1] * scale
        x3 = ox + p3_logo[i, 0] * scale
        y3 = oy + p3_logo[i, 1] * scale
        
        disp_x = x1 + np.random.uniform(-35, 35)
        disp_y = y1 + np.random.uniform(-35, 35)
        
        svg.append(f'<circle r="1.4" cx="{disp_x:.1f}" cy="{disp_y:.1f}">')
        svg.append(f'''<animate attributeName="cx"
          values="{disp_x:.1f}; {disp_x:.1f}; {x1:.1f}; {x1:.1f}; {x2:.1f}; {x2:.1f}; {x3:.1f}; {x3:.1f}; {disp_x:.1f}; {disp_x:.1f}"
          keyTimes="0; 0.211; 0.303; 0.444; 0.535; 0.676; 0.768; 0.908; 0.98; 1"
          dur="14.2s" repeatCount="indefinite"/>''')
        svg.append(f'''<animate attributeName="cy"
          values="{disp_y:.1f}; {disp_y:.1f}; {y1:.1f}; {y1:.1f}; {y2:.1f}; {y2:.1f}; {y3:.1f}; {y3:.1f}; {disp_y:.1f}; {disp_y:.1f}"
          keyTimes="0; 0.211; 0.303; 0.444; 0.535; 0.676; 0.768; 0.908; 0.98; 1"
          dur="14.2s" repeatCount="indefinite"/>''')
        svg.append(f'''<animate attributeName="opacity"
          values="0; 0; 1; 1; 1; 1; 1; 1; 0; 0"
          keyTimes="0; 0.211; 0.303; 0.444; 0.535; 0.676; 0.768; 0.908; 0.98; 1"
          dur="14.2s" repeatCount="indefinite"/>''')
        svg.append('</circle>')
    svg.append('</g>')
    
    # --- RIGHT PANEL: SYSTEM.INFO ---
    svg.append(f'<text x="442" y="74" class="sec-hdr">SYSTEM.INFO</text>')
    svg.append(f'<text x="560" y="74" fill="{text_muted}" font-size="11">· ACTIVE SESSION ID #266045105</text>')
    
    rows = [
        ("Subject", "Mohammad Hasim", 140, text_val),
        ("Role", "Full-Stack Developer & IoT", 235, chrome_col),
        ("Origin", "India", 50, text_val),
        ("Education", "B.Tech CSE (IoT)", 150, text_val),
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
        ("Grid.LinkedIn", "in/mohammad-hasim-9992423a0", 240, text_val),
        ("Grid.GitHub", "github.com/hasim2006", 175, chrome_col),
        ("Grid.Portfolio", "hasim2006.github.io [WIP]", 210, accent_col)
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

dark_content = build_svg("dark")
light_content = build_svg("light")

dark_path = os.path.join(output_dir, "dark.svg")
light_path = os.path.join(output_dir, "light.svg")

with open(dark_path, "w", encoding="utf-8") as f:
    f.write(dark_content)
with open(light_path, "w", encoding="utf-8") as f:
    f.write(light_content)

print(f"dark.svg: {len(dark_content)/1024:.1f} KB")
print(f"light.svg: {len(light_content)/1024:.1f} KB")
