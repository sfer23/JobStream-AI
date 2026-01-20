import os
from PIL import Image, ImageDraw, ImageFont

def extract_emoji(emoji_char, font_path, size=256):
    """Renders a single emoji character with its natural padding."""
    hex_code = "u_" + "_".join(f"{ord(c):x}" for c in emoji_char)
    output_path = f"assets/icons/{hex_code}.png"
    
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
    except Exception:
        return False

if __name__ == "__main__":
    icons_dir = "assets/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    font_path = "C:\\Windows\\Fonts\\seguiemj.ttf"
    
    emoji_list = [
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
    
    unique_emojis = list(set(emoji_list))
    count = 0
    for char in unique_emojis:
        if extract_emoji(char, font_path):
            count += 1
            
    print(f"Successfully restored {count} ORIGINAL emoji icons.")
