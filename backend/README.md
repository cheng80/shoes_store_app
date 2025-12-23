# Backend API (FastAPI)

FastAPI 백엔드 서버입니다. RESTful 방식의 기본 CRUD와 복합 쿼리(JOIN)를 제공합니다.

## 폴더 구조

```
backend/
├── app/
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── models/
│   │   └── all_models.py       # 모든 모델 통합 (9개)
│   ├── api/                     # API 라우터 (9개 파일)
│   └── database/
│       └── connection.py       # DB 연결
├── requirements.txt
├── API.md                      # API 문서
└── README.md                    # 이 파일
```

## 시작하기

### 1. 가상환경 생성 및 활성화 (선택사항)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 설정

`app/database/connection.py`에서 데이터베이스 정보를 수정하세요:

```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'your_password',
    'database': 'shoes_store_db',
    'charset': 'utf8mb4'
}
```

데이터베이스 초기화는 `database/init.sql` 파일을 MySQL Workbench에서 실행하세요.

### 4. 서버 실행

**방법 1: uvicorn 직접 실행 (권장)**
```bash
cd backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**방법 2: python 모듈로 실행**
```bash
cd backend
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**방법 3: main.py 직접 실행**
```bash
cd backend
python3 app/main.py
```

### 5. 서버 접속

서버가 시작되면 다음 주소로 접속할 수 있습니다:

- **API 문서 (Swagger UI)**: http://127.0.0.1:8000/docs
- **API 문서 (ReDoc)**: http://127.0.0.1:8000/redoc
- **루트 엔드포인트**: http://127.0.0.1:8000/
- **헬스 체크**: http://127.0.0.1:8000/health

### 서버 중지

터미널에서 `Ctrl + C`를 누르면 서버가 중지됩니다.

### 명령어 옵션 설명

- `app.main:app`: `app` 폴더의 `main.py` 파일에서 `app` 객체를 가져옴
- `--host 127.0.0.1`: 로컬호스트에서만 접근 가능
- `--port 8000`: 포트 번호 (기본값: 8000)
- `--reload`: 코드 변경 시 자동 재시작 (개발용, 프로덕션에서는 제거)

## API 구조

- **기본 CRUD**: RESTful 방식 (GET, POST, PUT, DELETE)
- **필터링**: 쿼리 파라미터로 처리
- **복합 쿼리**: JOIN은 별도 엔드포인트로 제공

## API 문서

자세한 API 문서는 [API.md](API.md)를 참고하세요.

## 지원 모델

1. Customer, Employee, Manufacturer
2. ProductBase, ProductImage, Product
3. Purchase, PurchaseItem, LoginHistory

