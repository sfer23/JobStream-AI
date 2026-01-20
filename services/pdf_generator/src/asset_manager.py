import os
from PIL import Image, ImageDraw, ImageFont

def extract_emoji(emoji_char, font_path, output_dir="assets/icons", size=256):
    """Renders a single emoji character with its natural padding."""
    hex_code = "u_" + "_".join(f"{ord(c):x}" for c in emoji_char)
    output_path = os.path.join(output_dir, f"{hex_code}.png")
    
    if os.path.exists(output_path):
        return True

    image = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype(font_path, int(size * 0.8))
        bbox = draw.textbbox((0, 0), emoji_char, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (size - w) // 2 - bbox[0]
        y = (size - h) // 2 - bbox[1]
        
        draw.text((x, y), emoji_char, font=font, embedded_color=True)
        image.save(output_path)
        return True
    except Exception as e:
        # print(f"Failed to extract {emoji_char}: {e}")
        return False

DEFAULT_EMOJI_LIST = [
    "🎓", "🏫", "📜", "📚", "📖", "📝", "✍️", "✏️", "🧠", "💡",
    "💼", "🏢", "🏗️", "📈", "📉", "📊", "🚀", "🎯", "👔", "🤝",
    "🔧", "🔨", "⚒️", "🛠️", "⛏️", "🔩", "⚙️", "🧱", "⛓️",
    "💻", "🖥️", "⌨️", "🖱️", "🕹️", "💾", "💿", "📀", "📷", "🎥", "🎬",
    "📱", "🔋", "🔌", "📡", "🛰️", "🔬", "🔭", "🧪", "🌡️", "🧬",
    "🏆", "🥇", "🥈", "🥉", "🏅", "🌟", "✨", "💎", "👤", "👥", "👑",
    "📍", "🏠", "📞", "☎️", "✉️", "📧", "🌐", "🔗", "💬", "🗨️",
    "🔍", "📅", "📆", "🗓️", "🗒️", "📋", "📌", "📎", "🖇️", "📏", "📐",
    "⚛️", "🐍", "☕", "🐘", "🦀", "🕸️", "🎨", "🎭", "🎼", "🎹", "🎸", "🎻",
    "🌍", "🌎", "🌏", "🗺️", "🗣️", "🛡️", "🔑", "🗝️", "🔓", "🔒", "🩹", "🩺",
    "🔥", "⚡", "🌈", "⚓", "🏁", "🚩", "🚦", "🚥", "🚧", "🛑"
]

def ensure_assets(icons_dir="assets/icons"):
    os.makedirs(icons_dir, exist_ok=True)
    
    # Try different common font paths for Windows
    font_paths = [
        "C:\\Windows\\Fonts\\seguiemj.ttf",
        "C:\\Windows\\Fonts\\segoeui.ttf"
    ]
    
    font_path = None
    for fp in font_paths:
        if os.path.exists(fp):
            font_path = fp
            break
            
    if not font_path:
        print("Warning: Emoji font not found. Icons may not be generated.")
        return

    count = 0
    unique_emojis = list(set(DEFAULT_EMOJI_LIST))
    for char in unique_emojis:
        if extract_emoji(char, font_path, output_dir=icons_dir):
            count += 1
            
    # print(f"Assets check complete. {count} icons available.")

def get_emoji_path(char, icons_dir="assets/icons"):
    hex_code = "u_" + "_".join(f"{ord(c):x}" for c in char)
    path = os.path.join(icons_dir, f"{hex_code}.png")
    if os.path.exists(path):
        return path
    return None
