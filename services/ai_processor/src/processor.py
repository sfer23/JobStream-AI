import json
import os
from .client import OpenRouterClient

class CVProcessor:
    def __init__(self, client: OpenRouterClient = None, log_dir: str = None):
        self.client = client or OpenRouterClient(log_dir=log_dir)

    def _read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def analyze_match(self, job_json_path, cv_md_path, prefs_md_path):
        job_data = self._read_file(job_json_path)
        cv_content = self._read_file(cv_md_path)
        prefs_content = self._read_file(prefs_md_path)

        prompt = f"""
Analyze the match between the following Job Description (JSON), the Candidate's CV (Markdown), and the Candidate's Preferences (Markdown).

Job Description:
{job_data}

Candidate's CV:
{cv_content}

Candidate's Preferences:
{prefs_content}

Tasks:
1. Evaluate how well the candidate fits the job requirements.
2. Evaluate how well the job fits the candidate's preferences (Salary, roles, etc.).
3. Provide a match score between 0 and 1 (where 1 is a perfect match).

Response Format:
Return ONLY a JSON object with two fields: "score" (float) and "reasoning" (string).
Example: {{"score": 0.85, "reasoning": "Fits all technical requirements, but salary is slightly below target."}}
"""
        response = self.client.complete(prompt, system_prompt="You are an expert HR recruiter and career coach.")
        try:
            # Clean response if LLM adds markdown blocks
            clean_res = response.strip()
            if clean_res.startswith("```json"):
                clean_res = clean_res[7:-3].strip()
            elif clean_res.startswith("```"):
                clean_res = clean_res[3:-3].strip()
            return json.loads(clean_res)
        except Exception as e:
            return {"score": 0.0, "reasoning": f"Error parsing response: {str(e)}. Raw response: {response}"}

    def optimize_cv(self, job_json_path, cv_md_path, prefs_md_path):
        job_data = self._read_file(job_json_path)
        cv_content = self._read_file(cv_md_path)
        prefs_content = self._read_file(prefs_md_path)

        prompt = f"""
Optimize the following Candidate's CV for the given Job Description and Candidate's Preferences.

Job Description:
{job_data}

Original CV:
{cv_content}

Candidate's Preferences:
{prefs_content}

Tasks:
1. Rewrite the CV to highlight experience relevant to the job description.
2. Maintain all factual information (do not invent experience).
3. Ensure the CV is concise (aim for 1-2 pages in Markdown format).
4. Organize content in a professional, readable Markdown format.

Response Format:
Return ONLY the optimized Markdown content for the CV. Do not include any intro or outro text.
"""
        return self.client.complete(prompt, system_prompt="You are an expert CV writer and recruiter.")

    def create_cover_letter(self, job_json_path, cv_md_path, prefs_md_path):
        job_data = self._read_file(job_json_path)
        cv_content = self._read_file(cv_md_path)
        prefs_content = self._read_file(prefs_md_path)

        prompt = f"""
Create a professional cover letter for the following Job Description and Candidate's CV.

Job Description:
{job_data}

Candidate's CV:
{cv_content}

Candidate's Preferences:
{prefs_content}

Tasks:
1. Write a compelling cover letter that bridges the gap between the candidate's experience and the job's needs.
2. Align the tone with the job description.
3. Keep it to one page.

Response Format:
Return ONLY the cover letter content in Markdown format.
"""
        return self.client.complete(prompt, system_prompt="You are an expert career advisor.")
