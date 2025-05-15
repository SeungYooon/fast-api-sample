# 기존과 동일
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 앱의 루트로 워킹 디렉토리 지정
WORKDIR /app

# 필요한 파일들만 정확하게 복사
COPY requirements.txt start.sh ./
COPY app ./app  

RUN pip install --upgrade pip && pip install -r requirements.txt

# start.sh는 그대로 app.main:app 기준 사용 가능
CMD ["./start.sh"]

RUN pip install python-dotenv
