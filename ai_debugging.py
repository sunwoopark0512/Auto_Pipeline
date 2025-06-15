"""
AI-assisted Debugging 도구 DeepCode 사용하여 코드 최적화와 버그 자동화.
"""

from deepcode import DeepCodeClient
import os

# DeepCode AI 클라이언트 설정
client = DeepCodeClient(api_key=os.getenv('DEEP_CODE_API_KEY'))

def analyze_code(code_dir: str) -> dict:
    results = client.analyze_directory(code_dir)
    return results

def log_analysis_results(results: dict, log_file: str) -> None:
    with open(log_file, 'w') as file:
        file.write(str(results))
    print(f"🚨 Bugs found: {len(results)}")

if __name__ == '__main__':
    results = analyze_code('/path/to/your/project')
    log_analysis_results(results, '/path/to/bug_report.log')
