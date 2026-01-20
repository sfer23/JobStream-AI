import argparse
import os
import sys

# Add the parent directory to sys.path to resolve imports if run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generator import generate_pdf

def main():
    parser = argparse.ArgumentParser(description="PDF Generator Service CLI")
    parser.add_argument("--input", required=True, help="Path to input Markdown CV")
    parser.add_argument("--output", required=True, help="Path to output PDF")
    parser.add_argument("--photo", help="Path to candidate photo")
    parser.add_argument("--assets", default="assets/icons", help="Directory for assets (icons, etc.)")
    parser.add_argument("--hidden-prompt", help="Text to inject as invisible white text for AI parsers")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
        
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
            
        print(f"Generating PDF from {args.input}...")
        generate_pdf(content, args.output, photo_path=args.photo, assets_dir=args.assets, hidden_prompt=args.hidden_prompt)
        print(f"PDF successfully saved to {args.output}")
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
