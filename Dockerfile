FROM python:3.11-slim

# 기본 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리
WORKDIR /app

# 복사 및 설치
COPY . /app
RUN pip install --no-cache-dir --upgrade pip
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# 기본 엔트리포인트 (파라미터별 실행 가능)
CMD ["python", "orchestrator.py"]
