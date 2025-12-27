# Manufacturer API 개발 체크리스트

## 📋 기본 정보

| 항목 | 내용 |
|------|------|
| **파일명** | `manufacturers.py` |
| **테이블** | `Manufacturer` |
| **담당자** | (이름 작성) |
| **작성일** | (날짜 작성) |
| **완료일** | (날짜 작성) |

---

## 📊 테이블 스키마

```sql
CREATE TABLE Manufacturer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mName VARCHAR(255) NOT NULL,
    UNIQUE INDEX idx_manufacturer_name (mName)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 컬럼 설명

| 컬럼명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| `id` | INT | ✅ | 자동 증가 기본키 |
| `mName` | VARCHAR(255) | ✅ | 제조사 이름 (UNIQUE) |

---

## 🎯 구현해야 할 API 목록

### 1. 전체 조회 (Read All)
- [ ] **완료**

| 항목 | 내용 |
|------|------|
| **엔드포인트** | `GET /select_manufacturers` |
| **파라미터** | 없음 |
| **응답 형식** | `{"results": [{"id": 1, "mName": "Nike"}, ...]}` |

**구현 요구사항:**
- [ ] 모든 제조사 목록 반환
- [ ] id 순으로 정렬 (ORDER BY id)
- [ ] 빈 결과시 빈 배열 반환 `{"results": []}`

---

### 2. 단일 조회 (Read One)
- [ ] **완료**

| 항목 | 내용 |
|------|------|
| **엔드포인트** | `GET /select_manufacturer/{manufacturer_id}` |
| **파라미터** | `manufacturer_id` (path, int) |
| **응답 형식** | `{"result": {"id": 1, "mName": "Nike"}}` |

**구현 요구사항:**
- [ ] ID로 제조사 조회
- [ ] 존재하지 않는 ID 처리: `{"result": "Error", "message": "..."}`

---

### 3. 추가 (Create)
- [ ] **완료**

| 항목 | 내용 |
|------|------|
| **엔드포인트** | `POST /insert_manufacturer` |
| **파라미터** | `mName` (Form, 필수) |
| **응답 형식** | `{"result": "OK", "id": 3}` |

**구현 요구사항:**
- [ ] Form 데이터로 제조사명 받기
- [ ] 성공 시 생성된 ID 반환
- [ ] 에러 시: `{"result": "Error", "errorMsg": "..."}`
- [ ] 중복 제조사명 처리 (UNIQUE 제약조건)

---

### 4. 수정 (Update)
- [ ] **완료**

| 항목 | 내용 |
|------|------|
| **엔드포인트** | `POST /update_manufacturer` |
| **파라미터** | `manufacturer_id` (Form), `mName` (Form) |
| **응답 형식** | `{"result": "OK"}` |

**구현 요구사항:**
- [ ] Form 데이터로 ID와 새 이름 받기
- [ ] 해당 ID의 제조사명 업데이트
- [ ] 에러 시: `{"result": "Error", "errorMsg": "..."}`

---

### 5. 삭제 (Delete)
- [ ] **완료**

| 항목 | 내용 |
|------|------|
| **엔드포인트** | `DELETE /delete_manufacturer/{manufacturer_id}` |
| **파라미터** | `manufacturer_id` (path, int) |
| **응답 형식** | `{"result": "OK"}` |

**구현 요구사항:**
- [ ] ID로 제조사 삭제
- [ ] 에러 시: `{"result": "Error", "errorMsg": "..."}`
- [ ] ⚠️ FK 참조 시 삭제 실패 가능 (Product 테이블에서 참조)

---

## ✅ 기능 테스트 체크리스트

### 사전 준비
- [ ] 데이터베이스 연결 확인
- [ ] `python manufacturers.py` 실행 (http://127.0.0.1:8000)
- [ ] Swagger UI 접속 확인 (http://127.0.0.1:8000/docs)

### 테스트 시나리오

#### 시나리오 1: 전체 조회
```bash
curl -X GET http://127.0.0.1:8000/select_manufacturers
```
- [ ] 기존 데이터 목록 반환 확인
- [ ] 응답 형식: `{"results": [...]}`

#### 시나리오 2: 추가 → 조회 → 수정 → 삭제 (CRUD 사이클)

**Step 1: 추가**
```bash
curl -X POST http://127.0.0.1:8000/insert_manufacturer \
  -d "mName=TestBrand"
```
- [ ] `{"result": "OK", "id": N}` 응답 확인
- [ ] 반환된 ID 기록: ____

**Step 2: 단일 조회**
```bash
curl -X GET http://127.0.0.1:8000/select_manufacturer/{id}
```
- [ ] 추가한 데이터 조회 확인
- [ ] mName이 "TestBrand"인지 확인

**Step 3: 수정**
```bash
curl -X POST http://127.0.0.1:8000/update_manufacturer \
  -d "manufacturer_id={id}" \
  -d "mName=UpdatedBrand"
```
- [ ] `{"result": "OK"}` 응답 확인

**Step 4: 수정 확인**
```bash
curl -X GET http://127.0.0.1:8000/select_manufacturer/{id}
```
- [ ] mName이 "UpdatedBrand"로 변경되었는지 확인

**Step 5: 삭제**
```bash
curl -X DELETE http://127.0.0.1:8000/delete_manufacturer/{id}
```
- [ ] `{"result": "OK"}` 응답 확인

**Step 6: 삭제 확인**
```bash
curl -X GET http://127.0.0.1:8000/select_manufacturer/{id}
```
- [ ] `{"result": "Error", "message": "..."}` 응답 확인

#### 시나리오 3: 에러 케이스

**존재하지 않는 ID 조회**
```bash
curl -X GET http://127.0.0.1:8000/select_manufacturer/99999
```
- [ ] 에러 응답 확인

**중복 제조사명 추가 시도**
```bash
curl -X POST http://127.0.0.1:8000/insert_manufacturer \
  -d "mName=Nike"
```
- [ ] 에러 응답 확인 (이미 존재하는 제조사명)

---

## 📝 코드 구조 체크리스트

### 파일 상단
- [ ] docstring 작성 (파일 설명, 실행 방법)
- [ ] 필요한 import 문
  - [ ] `from fastapi import FastAPI, Form`
  - [ ] `from pydantic import BaseModel`
  - [ ] `from typing import Optional`
  - [ ] `from database.connection import connect_db`

### 모델 정의
- [ ] Pydantic BaseModel 클래스 정의
- [ ] 모든 컬럼에 대한 필드 정의
- [ ] `id`는 `Optional[int] = None`으로 정의

### API 함수
- [ ] 각 함수에 docstring 또는 주석 작성
- [ ] `async def` 사용
- [ ] DB 연결 후 반드시 `conn.close()` 호출
- [ ] 에러 처리 (try-except)

### 개별 실행 코드
- [ ] `if __name__ == "__main__":` 블록 작성
- [ ] `uvicorn.run(app, host=ipAddress, port=8000)`
- [ ] `ipAddress` 변수 정의 (`"127.0.0.1"`)

---

## 🔗 참고 자료

- **DB 스키마**: `database/schema.sql`
- **더미 데이터**: `database/dummy_data.sql`
- **DB 연결**: `app_basic_form/database/connection.py`
- **완성 예시**: `app_basic_form/manufacturers.py`

---

## 📌 메모

(개발 중 특이사항, 질문, 이슈 등 기록)

```
예시:
- 2025-12-27: FK 제약조건으로 Product에서 사용 중인 Manufacturer 삭제 불가 확인
```

---

## ✍️ 최종 확인

| 항목 | 확인 |
|------|------|
| 모든 API 구현 완료 | [ ] |
| 모든 테스트 통과 | [ ] |
| 코드 리뷰 완료 | [ ] |
| 담당자 서명 | _____________ |
| 검토자 서명 | _____________ |

