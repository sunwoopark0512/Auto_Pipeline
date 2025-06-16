#!/usr/bin/env python3
"""
automation_report.py
자동 성과 리포트 생성 및 Notion 전송
- 주간/월간 성과 리포트 자동 생성 (PDF/HTML)
- 성과 데이터 기반으로 리포트 작성 후 Notion에 자동 기록
"""

import os
import logging
from datetime import datetime
import requests
from dotenv import load_dotenv
from fpdf import FPDF
from jinja2 import Template

# ---------------------- 환경 변수 로딩 ----------------------
load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

NOTION_API_URL = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ---------------------- Notion 데이터 조회 ----------------------
def fetch_notion_data():
    """Notion DB에서 콘텐츠 데이터를 가져옵니다."""
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
    }

    try:
        response = requests.post(NOTION_API_URL, headers=headers)
        response.raise_for_status()
        logging.info("✅ Notion 데이터 로드 완료")
        return response.json().get("results", [])
    except Exception as e:
        logging.error(f"❌ Notion 데이터 로드 실패: {e}")
        return []

# ---------------------- PDF 리포트 생성 ----------------------
def generate_pdf_report(data, report_type="weekly"):
    """주간/월간 성과 리포트 PDF 생성"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"{report_type.capitalize()} Performance Report", ln=True, align="C")
    pdf.set_font("Arial", "", 12)

    for item in data:
        try:
            title = item['properties']['Title']['title'][0]['text']['content']
            views = item['properties']['Views']['number']
            post_date = item['properties']['Post Date']['date']['start']
        except Exception:
            continue

        pdf.ln(10)
        pdf.cell(200, 10, f"Title: {title}", ln=True)
        pdf.cell(200, 10, f"Views: {views}", ln=True)
        pdf.cell(200, 10, f"Post Date: {post_date}", ln=True)

    filename = f"{report_type}_performance_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    logging.info(f"✅ PDF 리포트 생성 완료: {filename}")
    return filename

# ---------------------- HTML 리포트 생성 ----------------------
def generate_html_report(data, report_type="weekly"):
    """주간/월간 성과 리포트 HTML 생성"""
    try:
        with open("report_template.html", "r", encoding="utf-8") as f:
            template_content = f.read()
    except Exception as e:
        logging.error(f"❌ HTML 템플릿 읽기 실패: {e}")
        return None

    template = Template(template_content)
    html = template.render(report_type=report_type, data=data)

    filename = f"{report_type}_performance_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    logging.info(f"✅ HTML 리포트 생성 완료: {filename}")
    return filename

# ---------------------- 리포트 Notion 업로드 ----------------------
def send_report_to_notion(report_filename):
    """생성된 리포트를 Notion에 업로드"""
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
    }

    file_url = f"https://example.com/{report_filename}"
    post_data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": f"{report_filename} Report"}}]},
            "Report": {"rich_text": [{"text": {"content": file_url}}]},
            "Date": {"date": {"start": datetime.utcnow().date().isoformat()}},
        },
    }

    try:
        response = requests.post(url, headers=headers, json=post_data)
        response.raise_for_status()
        logging.info(f"✅ 리포트 Notion 업로드 완료: {report_filename}")
    except Exception as e:
        logging.error(f"❌ 리포트 업로드 실패: {e}")

# ---------------------- 메인 함수 ----------------------
def main(report_type="weekly"):
    data = fetch_notion_data()
    if not data:
        logging.error("❌ 리포트 생성 실패: 데이터 없음")
        return

    if report_type == "weekly":
        report_filename = generate_pdf_report(data, report_type)
    else:
        report_filename = generate_html_report(data, report_type)

    if report_filename:
        send_report_to_notion(report_filename)

if __name__ == "__main__":
    main(report_type="weekly")
