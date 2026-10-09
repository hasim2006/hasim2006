import os

output_dir = r"c:\Users\hasim\OneDrive\Desktop\github'\hasim2006"
os.makedirs(output_dir, exist_ok=True)

def build_header_svg(theme="dark"):
    is_dark = (theme == "dark")
    text_val = "#F8FAFC" if is_dark else "#0F172A"
    text_muted = "#94A3B8" if is_dark else "#475569"
    chrome_col = "#22D3EE" if is_dark else "#0891B2"
    
    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 90" width="100%" height="100%">')
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

      <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>
        <stop offset="25%" stop-color="#22D3EE" stop-opacity="0.8"/>
        <stop offset="50%" stop-color="#A78BFA" stop-opacity="0.8"/>
        <stop offset="75%" stop-color="#10B981" stop-opacity="0.8"/>
        <stop offset="100%" stop-color="#10B981" stop-opacity="0"/>
      </linearGradient>
    ''')
    
    svg.append('<style>')
    svg.append(f'''
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&amp;display=swap');
      text {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}
      
      /* Slow Transparent-to-Full-Loaded Fade In Animation */
      @keyframes slowFadeLoad {{
        0% {{
          opacity: 0;
          transform: translateY(12px);
        }}
        25% {{
          opacity: 0.25;
        }}
        55% {{
          opacity: 0.65;
        }}
        100% {{
          opacity: 1;
          transform: translateY(0px);
        }}
      }}
      
      .greeting-container {{
        animation: slowFadeLoad 2.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
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
        transform-origin: 182px 50px;
        animation: wave-hand 2.2s infinite ease-in-out;
      }}
    ''')
    svg.append('</style>')
    svg.append('</defs>')
    
    # Transparent background (merges seamlessly into page outside the box)
    svg.append('<rect width="1180" height="90" fill="none"/>')
    
    # Entire Greeting wrapped in slow fade-in load-in animation container
    svg.append('<g class="greeting-container">')
    
    # Left CLI Prompt & Greeting
    svg.append(f'''
    <g>
      <!-- Green CLI prompt symbol -->
      <text x="24" y="52" font-size="28" font-weight="700" fill="#10B981">&gt;</text>
      <!-- Greeting text -->
      <text x="50" y="52" font-size="26" font-weight="700" fill="{text_val}">Hi there </text>
      
      <!-- Animated Waving Hand Emoji -->
      <text x="182" y="52" font-size="28" class="wave-hand">👋</text>
      
      <text x="226" y="52" font-size="26" font-weight="500" fill="{text_muted}"> I&apos;m </text>
      
      <!-- Mohammad Hasim with Dynamic Glowing Gradient Transition -->
      <text x="290" y="52" font-size="28" font-weight="800" fill="url(#nameGrad)" letter-spacing="0.5">
        Mohammad Hasim
        <animate attributeName="opacity" values="0.88; 1; 0.88" dur="2.5s" repeatCount="indefinite"/>
      </text>
    </g>
    
    <!-- Top Right Status Badge -->
    <g>
      <rect x="888" y="28" width="268" height="34" rx="8" fill="{chrome_col}18" stroke="{chrome_col}55" stroke-width="1.2"/>
      <circle cx="908" cy="45" r="4.5" fill="#10B981">
        <animate attributeName="opacity" values="1; 0.3; 1" dur="2s" repeatCount="indefinite"/>
      </circle>
      <text x="924" y="50" fill="{chrome_col}" font-size="12.5" font-weight="700" letter-spacing="1.2">FULL-STACK &amp; AI DEVELOPER</text>
    </g>
    
    <!-- Subtle cyber accent line below greeting -->
    <line x1="24" y1="80" x2="1156" y2="80" stroke="url(#lineGrad)" stroke-width="1.5"/>
    ''')
    
    svg.append('</g>') # End greeting-container
    svg.append('</svg>')
    return "\n".join(svg)

header_dark = build_header_svg("dark")
header_light = build_header_svg("light")

with open(os.path.join(output_dir, "header_dark.svg"), "w", encoding="utf-8") as f:
    f.write(header_dark)
with open(os.path.join(output_dir, "header_light.svg"), "w", encoding="utf-8") as f:
    f.write(header_light)

print("header_dark.svg and header_light.svg with slowFadeLoad animation generated successfully!")
