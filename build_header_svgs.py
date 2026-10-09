import os

output_dir = r"c:\Users\hasim\OneDrive\Desktop\github'\hasim2006"
os.makedirs(output_dir, exist_ok=True)

def build_header_svg(theme="dark"):
    is_dark = (theme == "dark")
    text_val = "#F8FAFC" if is_dark else "#0F172A"
    text_muted = "#94A3B8" if is_dark else "#475569"
    chrome_col = "#22D3EE" if is_dark else "#0891B2"
    
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 86" width="100%" height="100%">')
    svg.append('<defs>')
    svg.append('''
      <!-- Dynamic Transition Gradient for Name: Cycles smoothly between Cyan, Violet, Emerald, Gold -->
      <linearGradient id="nameGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#22D3EE">
          <animate attributeName="stop-color"
            values="#22D3EE; #A78BFA; #10B981; #FACC15; #22D3EE"
            dur="6s" repeatCount="indefinite"/>
        </stop>
        <stop offset="50%" stop-color="#A78BFA">
          <animate attributeName="stop-color"
            values="#A78BFA; #10B981; #FACC15; #22D3EE; #A78BFA"
            dur="6s" repeatCount="indefinite"/>
        </stop>
        <stop offset="100%" stop-color="#10B981">
          <animate attributeName="stop-color"
            values="#10B981; #FACC15; #22D3EE; #A78BFA; #10B981"
            dur="6s" repeatCount="indefinite"/>
        </stop>
      </linearGradient>

      <!-- Full-width edge-to-edge subtle line gradient touching container borders -->
      <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.9"/>
        <stop offset="25%" stop-color="#22D3EE" stop-opacity="0.5"/>
        <stop offset="50%" stop-color="#A78BFA" stop-opacity="0.5"/>
        <stop offset="75%" stop-color="#10B981" stop-opacity="0.5"/>
        <stop offset="100%" stop-color="#10B981" stop-opacity="0.9"/>
      </linearGradient>
    ''')
    
    svg.append('<style>')
    svg.append(f'''
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&amp;display=swap');
      text {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}
      
      /* Phase 1: Hi there appears immediately */
      @keyframes loadHiThere {{
        0% {{
          opacity: 0;
          transform: translateY(10px);
        }}
        100% {{
          opacity: 1;
          transform: translateY(0px);
        }}
      }}
      
      /* Phase 2: Rest of the line (I'm Mohammad Hasim) appears on the SAME line after 4.0 seconds */
      @keyframes loadSameLineAfter4s {{
        0% {{
          opacity: 0;
          transform: translateX(-12px);
        }}
        100% {{
          opacity: 1;
          transform: translateX(0px);
        }}
      }}
      
      .greeting-first {{
        animation: loadHiThere 1.0s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both;
      }}
      
      .name-after-4s {{
        opacity: 0;
        animation: loadSameLineAfter4s 1.2s cubic-bezier(0.16, 1, 0.3, 1) 4.0s forwards;
      }}
      
      .badge-after-4s {{
        opacity: 0;
        animation: loadSameLineAfter4s 1.2s cubic-bezier(0.16, 1, 0.3, 1) 4.0s forwards;
      }}
      
      @keyframes wave-hand {{
        0% {{ transform: rotate(0deg); }}
        15% {{ transform: rotate(24deg); }}
        30% {{ transform: rotate(-10deg); }}
        45% {{ transform: rotate(22deg); }}
        60% {{ transform: rotate(-6deg); }}
        75% {{ transform: rotate(12deg); }}
        100% {{ transform: rotate(0deg); }}
      }}
      
      .wave-hand {{
        transform-origin: 184px 48px;
        animation: wave-hand 2.2s infinite ease-in-out;
      }}
    ''')
    svg.append('</style>')
    svg.append('</defs>')
    
    # Transparent background (merges seamlessly into page outside the box)
    svg.append('<rect width="1180" height="86" fill="none"/>')
    
    # =========================================================================
    # SINGLE HORIZONTAL LINE:
    # 1. First (0s): "Hi there 👋" appears immediately
    # 2. Second (4s later): "I'm Mohammad Hasim" appears on the SAME LINE
    # =========================================================================
    
    # Part 1: "Hi there 👋" (Appears First)
    svg.append('<g class="greeting-first">')
    svg.append(f'''
      <!-- Green CLI prompt symbol -->
      <text x="24" y="48" font-size="28" font-weight="700" fill="#10B981">&gt;</text>
      <!-- Greeting text -->
      <text x="50" y="48" font-size="26" font-weight="700" fill="{text_val}">Hi there </text>
      <!-- Animated Waving Hand Emoji -->
      <text x="184" y="48" font-size="28" class="wave-hand">👋</text>
    ''')
    svg.append('</g>')
    
    # Part 2: "I'm Mohammad Hasim" (Appears on the SAME line after 4 seconds)
    svg.append('<g class="name-after-4s">')
    svg.append(f'''
      <text x="228" y="48" font-size="26" font-weight="500" fill="{text_muted}"> I&apos;m </text>
      <text x="294" y="48" font-size="28" font-weight="800" fill="url(#nameGrad)" letter-spacing="0.5">
        Mohammad Hasim
        <animate attributeName="opacity" values="0.88; 1; 0.88" dur="2.5s" repeatCount="indefinite"/>
      </text>
    ''')
    svg.append('</g>')
    
    # Top Right Status Badge (Also reveals alongside name after 4s)
    svg.append(f'''
    <g class="badge-after-4s">
      <rect x="888" y="24" width="268" height="34" rx="8" fill="{chrome_col}18" stroke="{chrome_col}55" stroke-width="1.2"/>
      <circle cx="908" cy="41" r="4.5" fill="#10B981">
        <animate attributeName="opacity" values="1; 0.3; 1" dur="2s" repeatCount="indefinite"/>
      </circle>
      <text x="924" y="46" fill="{chrome_col}" font-size="12.5" font-weight="700" letter-spacing="1.2">FULL-STACK &amp; AI DEVELOPER</text>
    </g>
    ''')
    
    # Bottom full-width border line (Touches and matches left and right side borders)
    svg.append(f'<line x1="0" y1="78" x2="1180" y2="78" stroke="url(#lineGrad)" stroke-width="1.5"/>')
    
    svg.append('</svg>')
    return "\n".join(svg)

header_dark = build_header_svg("dark")
header_light = build_header_svg("light")

with open(os.path.join(output_dir, "header_dark.svg"), "w", encoding="utf-8") as f:
    f.write(header_dark)
with open(os.path.join(output_dir, "header_light.svg"), "w", encoding="utf-8") as f:
    f.write(header_light)

print("header_dark.svg and header_light.svg generated: same line, Hi there first, and I'm Mohammad Hasim after 4 seconds!")
