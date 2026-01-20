import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    def __init__(self, log_dir=None):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "tngtech/deepseek-r1t2-chimera:free")
        self.log_dir = log_dir
        
        if self.log_dir:
            os.makedirs(self.log_dir, exist_ok=True)
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is not set in environment variables")
            
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

    def complete(self, prompt, system_prompt="You are a helpful assistant specialized in career coaching and CV optimization."):
        if self.log_dir:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            req_file = os.path.join(self.log_dir, f"request_{timestamp}.txt")
            with open(req_file, "w", encoding="utf-8") as f:
                f.write(f"SYSTEM: {system_prompt}\n\nUSER: {prompt}")

        response = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://github.com/google/cv_helper",
                "X-Title": "CV Helper AI Processor",
            },
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        content = response.choices[0].message.content

        if self.log_dir:
            res_file = os.path.join(self.log_dir, f"response_{timestamp}.txt")
            with open(res_file, "w", encoding="utf-8") as f:
                f.write(content)

        return content
