import os
import sys
import argparse
from dotenv import load_dotenv

# Add current directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.processor import CVProcessor
from src.pdf_gen import generate_pdf

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="AI CV Processor Debug Tool")
    parser.add_argument("--action", choices=["analyze", "optimize", "pdf", "cover_letter"], required=True, help="Action to perform")
    parser.add_argument("--job", help="Path to job JSON")
    parser.add_argument("--cv", help="Path to CV Markdown")
    parser.add_argument("--prefs", help="Path to preferences Markdown")
    parser.add_argument("--optimized-cv-path", help="Path to existing optimized CV Markdown (for direct PDF generation)")
    parser.add_argument("--photo", help="Path to candidate photo (for PDF generation)")
    parser.add_argument("--output-dir", default="debug/output", help="Directory for output files")
    parser.add_argument("--debug-dir", default="debug/logs", help="Directory for LLM request/reponse logs")
    
    args = parser.parse_args()
    
    # Defaults setting if not provided via CLI
    job_path = args.job or "debug/indeed/job_f835103115031a94/details.json"
    cv_path = args.cv or "debug/cv_mock/cv_full.md"
    prefs_path = args.prefs or "debug/cv_mock/preferences.md"
    
    os.makedirs(args.output_dir, exist_ok=True)
    if args.debug_dir:
        os.makedirs(args.debug_dir, exist_ok=True)
    
    processor = CVProcessor(log_dir=args.debug_dir)
    
    if args.action == "analyze":
        print(f"--- Action: Analyze Match ---")
        match_result = processor.analyze_match(job_path, cv_path, prefs_path)
        print(f"Match Score: {match_result.get('score')}")
        print(f"Reasoning: {match_result.get('reasoning')}")

    elif args.action == "optimize":
        print(f"--- Action: CV Optimization ---")
        optimized_cv = processor.optimize_cv(job_path, cv_path, prefs_path)
        opt_cv_full_path = os.path.join(args.output_dir, "cv_optimized.md")
        with open(opt_cv_full_path, "w", encoding="utf-8") as f:
            f.write(optimized_cv)
        print(f"Optimized CV saved to {opt_cv_full_path}")
    
    elif args.action == "pdf":
        print(f"--- Action: PDF Generation ---")
        optimized_cv = ""
        
        if args.optimized_cv_path:
            print(f"Loading existing optimized CV from: {args.optimized_cv_path}")
            with open(args.optimized_cv_path, "r", encoding="utf-8") as f:
                optimized_cv = f.read()
        else:
            print("Optimized CV path not provided. Generating from job, CV, and preferences...")
            optimized_cv = processor.optimize_cv(job_path, cv_path, prefs_path)
            # Optionally save the intermediate MD
            opt_cv_temp_path = os.path.join(args.output_dir, "cv_optimized.md")
            with open(opt_cv_temp_path, "w", encoding="utf-8") as f:
                f.write(optimized_cv)

        pdf_output_path = os.path.join(args.output_dir, "cv_optimized.pdf")
        generate_pdf(optimized_cv, pdf_output_path, photo_path=args.photo)
        print(f"PDF CV saved to {pdf_output_path}")
    
    elif args.action == "cover_letter":
        print(f"--- Action: Cover Letter Creation ---")
        cover_letter = processor.create_cover_letter(job_path, cv_path, prefs_path)
        cl_path = os.path.join(args.output_dir, "cover_letter.md")
        with open(cl_path, "w", encoding="utf-8") as f:
            f.write(cover_letter)
        print(f"Cover letter saved to {cl_path}")

if __name__ == "__main__":
    main()
