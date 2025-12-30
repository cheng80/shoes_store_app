# 소셜 로그인 최종 설계안 (별도 테이블 방식) ⭐ 추천

## 🎯 문제점 분석

### 현재 설계의 문제 (단일 테이블)

```sql
user 테이블:
- 로컬 사용자: u_password는 값, u_google_sub/u_kakao_id는 NULL
- 소셜 사용자: u_password는 NULL, u_google_sub 또는 u_kakao_id는 값
```

**문제점:**
- ❌ NULL 값이 많아짐
- ❌ 정규화 위반
- ❌ 확장성 낮음 (새 소셜 로그인 추가 시 컬럼 증가)
- ❌ 사용자 타입 구분이 복잡함

---

## 💡 해결책: 별도 테이블 방식 (원안)

### 데이터베이스 구조

#### 1. `user` 테이블 (기본 사용자 정보)

```sql
CREATE TABLE user (
  u_seq INT AUTO_INCREMENT PRIMARY KEY COMMENT '고객 고유 ID(PK)',
  u_email VARCHAR(255) NOT NULL COMMENT '이메일 (로컬/소셜 모두 필수, UNIQUE)',
  u_name VARCHAR(255) NOT NULL COMMENT '고객 이름',
  u_phone VARCHAR(30) NULL COMMENT '전화번호 (선택 사항)',
  u_address VARCHAR(255) NULL COMMENT '고객 주소',
  u_image MEDIUMBLOB NULL COMMENT '고객 프로필 이미지',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '고객 가입일자',
  u_quit_date DATETIME NULL COMMENT '고객 탈퇴일자',
  registration_completed BOOLEAN NOT NULL DEFAULT TRUE COMMENT '회원가입 완료 여부',
  
  UNIQUE INDEX idx_user_email (u_email),
  UNIQUE INDEX idx_user_phone (u_phone),
  INDEX idx_user_created_at (created_at),
  INDEX idx_user_quit_date (u_quit_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='고객 계정 정보';
```

**특징:**
- ✅ NULL 값 최소화 (기본 사용자 정보만)
- ✅ 로그인 관련 정보 없음 (깔끔함)

---

#### 2. `user_auth_identities` 테이블 (로그인 수단별 인증 정보)

```sql
CREATE TABLE user_auth_identities (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '인증 수단 고유 ID(PK)',
  u_seq INT NOT NULL COMMENT '고객 번호(FK)',
  provider VARCHAR(50) NOT NULL COMMENT '로그인 제공자(local, google, kakao)',
  provider_subject VARCHAR(255) NOT NULL COMMENT '제공자 고유 식별자(로컬: 이메일, 구글: sub, 카카오: id)',
  password VARCHAR(255) NULL COMMENT '로컬 로그인 비밀번호 (로컬만)',
  provider_issuer VARCHAR(255) NULL COMMENT '제공자 발급자(구글 iss 등)',
  email_at_provider VARCHAR(255) NULL COMMENT '제공자에서 받은 이메일',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일자',
  last_login_at DATETIME NULL COMMENT '마지막 로그인 일시',
  
  CONSTRAINT fk_user_auth_user
    FOREIGN KEY (u_seq) REFERENCES user(u_seq)
    ON DELETE CASCADE ON UPDATE CASCADE,
  
  UNIQUE INDEX idx_provider_subject (provider, provider_subject),
  INDEX idx_user_auth_u_seq (u_seq),
  INDEX idx_user_auth_provider (provider)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='사용자 로그인 수단 매핑';
```

**특징:**
- ✅ 로그인 수단별 정보 분리
- ✅ NULL 값 최소화 (로컬은 password, 소셜은 provider_subject)
- ✅ 확장성: 새 소셜 로그인 추가 시 테이블 구조 변경 불필요

---

## 🔐 로그인 로직

### 로컬 로그인 (이메일 + 비밀번호)

```python
POST /api/auth/local/login
{
  "email": "user@example.com",
  "password": "hashed_password"
}

처리 로직:
1. user_auth_identities에서 조회:
   WHERE provider='local' AND provider_subject=email
2. password와 입력 비밀번호 비교
3. 일치하면 user_id로 user 테이블 조회
```

**API 구현:**
```python
@router.post("/auth/local/login")
async def local_login(
    email: str = Form(...),
    password: str = Form(...)
):
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # user_auth_identities에서 로컬 로그인 정보 조회
        curs.execute("""
            SELECT uai.u_seq, uai.password, u.u_seq, u.u_name, u.u_email, u.u_phone, u.u_address
            FROM user_auth_identities uai
            JOIN user u ON uai.u_seq = u.u_seq
            WHERE uai.provider = 'local' AND uai.provider_subject = %s
        """, (email,))
        row = curs.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=401,
                detail="이메일 또는 비밀번호가 올바르지 않습니다"
            )
        
        # 비밀번호 확인
        if row[1] != password:
            raise HTTPException(
                status_code=401,
                detail="이메일 또는 비밀번호가 올바르지 않습니다"
            )
        
        # 마지막 로그인 시간 업데이트
        curs.execute("""
            UPDATE user_auth_identities 
            SET last_login_at = NOW() 
            WHERE u_seq = %s AND provider = 'local'
        """, (row[0],))
        conn.commit()
        
        return {
            "result": "OK",
            "user_seq": row[2],
            "u_name": row[3],
            "u_email": row[4],
            "u_phone": row[5],
            "u_address": row[6]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()
```

---

### 소셜 로그인 (구글/카카오)

```python
POST /api/auth/social/login
{
  "provider": "google",
  "provider_subject": "구글sub값",
  "email": "user@gmail.com",
  "name": "김철수"
}

처리 로직:
1. user_auth_identities에서 조회:
   WHERE provider='google' AND provider_subject=구글sub값
2. 없으면 신규 사용자 생성
   - user 테이블에 기본 정보 저장
   - user_auth_identities에 소셜 로그인 정보 저장
```

**API 구현:**
```python
@router.post("/auth/social/login")
async def social_login(
    provider: str = Form(...),
    provider_subject: str = Form(...),
    email: str = Form(...),
    name: str = Form(...),
    provider_issuer: Optional[str] = Form(None)
):
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 기존 사용자 확인
        curs.execute("""
            SELECT uai.u_seq, u.u_seq, u.u_name, u.u_email, u.u_phone, u.u_address
            FROM user_auth_identities uai
            JOIN user u ON uai.u_seq = u.u_seq
            WHERE uai.provider = %s AND uai.provider_subject = %s
        """, (provider, provider_subject))
        row = curs.fetchone()
        
        if row:
            # 기존 사용자
            # 마지막 로그인 시간 업데이트
            curs.execute("""
                UPDATE user_auth_identities 
                SET last_login_at = NOW() 
                WHERE provider = %s AND provider_subject = %s
            """, (provider, provider_subject))
            conn.commit()
            
            return {
                "result": "OK",
                "user_seq": row[1],
                "u_name": row[2],
                "u_email": row[3],
                "u_phone": row[4],
                "u_address": row[5],
                "registration_completed": True
            }
        
        # 신규 사용자 생성
        # 1. user 테이블에 기본 정보 저장
        curs.execute("""
            INSERT INTO user (u_email, u_name, registration_completed)
            VALUES (%s, %s, TRUE)
        """, (email, name))
        user_seq = curs.lastrowid
        
        # 2. user_auth_identities에 소셜 로그인 정보 저장
        curs.execute("""
            INSERT INTO user_auth_identities 
            (u_seq, provider, provider_subject, provider_issuer, email_at_provider)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_seq, provider, provider_subject, provider_issuer, email))
        
        conn.commit()
        
        return {
            "result": "OK",
            "user_seq": user_seq,
            "u_name": name,
            "u_email": email,
            "u_phone": None,
            "u_address": None,
            "registration_completed": True
        }
        
    except Exception as e:
        conn.rollback()
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()
```

---

## 🔍 사용자 타입 확인 API (UI 분기용)

```python
GET /api/users/{user_seq}/login_type

Response:
{
  "result": {
    "user_seq": 123,
    "login_types": ["local"],  // 또는 ["google"], ["local", "google"]
    "has_password": true,       // 비밀번호 변경 가능 여부
    "providers": ["local"]      // 사용 가능한 로그인 수단
  }
}
```

**API 구현:**
```python
@router.get("/users/{user_seq}/login_type")
async def get_user_login_type(user_seq: int):
    """
    사용자 타입 확인 (UI 분기 처리용)
    - 로컬 로그인 사용자: 비밀번호 변경 가능
    - 소셜 로그인 사용자: 비밀번호 변경 불가
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        curs.execute("""
            SELECT provider, password
            FROM user_auth_identities
            WHERE u_seq = %s
        """, (user_seq,))
        rows = curs.fetchall()
        
        if not rows:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        
        login_types = [row[0] for row in rows]
        has_password = any(row[1] is not None for row in rows)
        
        return {
            "result": {
                "user_seq": user_seq,
                "login_types": login_types,
                "has_password": has_password,
                "providers": login_types,
                "is_local_only": login_types == ["local"],
                "is_social_only": "local" not in login_types,
                "has_multiple": len(login_types) > 1
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()
```

---

## 📝 회원가입 로직

### 로컬 로그인 회원가입

```python
POST /api/users
{
  "u_email": "user@example.com",
  "u_password": "hashed_password",
  "u_name": "홍길동",
  "u_phone": "010-1234-5678",  // 선택
  "u_address": "서울시 강남구..." // 선택
}

처리 로직:
1. user 테이블에 기본 정보 저장
2. user_auth_identities에 로컬 로그인 정보 저장
   - provider='local'
   - provider_subject=u_email
   - password=u_password
```

**API 구현:**
```python
@router.post("/users")
async def insert_user(
    u_email: str = Form(...),
    u_password: str = Form(...),
    u_name: str = Form(...),
    u_phone: Optional[str] = Form(None),
    u_address: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 이메일 중복 확인
        curs.execute("SELECT u_seq FROM user WHERE u_email = %s", (u_email,))
        if curs.fetchone():
            raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다")
        
        # 전화번호 중복 확인 (있는 경우만)
        if u_phone:
            curs.execute("SELECT u_seq FROM user WHERE u_phone = %s", (u_phone,))
            if curs.fetchone():
                raise HTTPException(status_code=400, detail="이미 사용 중인 전화번호입니다")
        
        # 이미지 처리
        image_data = None
        if file:
            image_data = await file.read()
        
        # 1. user 테이블에 기본 정보 저장
        curs.execute("""
            INSERT INTO user (u_email, u_name, u_phone, u_address, u_image, registration_completed)
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """, (u_email, u_name, u_phone, u_address, image_data))
        user_seq = curs.lastrowid
        
        # 2. user_auth_identities에 로컬 로그인 정보 저장
        curs.execute("""
            INSERT INTO user_auth_identities 
            (u_seq, provider, provider_subject, password)
            VALUES (%s, 'local', %s, %s)
        """, (user_seq, u_email, u_password))
        
        conn.commit()
        return {"result": "OK", "u_seq": user_seq}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()
```

---

## 🔄 회원 정보 수정 로직

### 회원 정보 수정 (이메일 읽기 전용)

```python
POST /api/users/{user_seq}
{
  "u_name": "홍길동",
  "u_phone": "010-1234-5678",
  "u_address": "서울시 강남구..."
}

// 이메일은 수정 불가 (읽기 전용)
```

**API 구현:**
```python
@router.post("/users/{user_seq}")
async def update_user(
    user_seq: int,
    u_name: Optional[str] = Form(None),
    u_phone: Optional[str] = Form(None),
    u_address: Optional[str] = Form(None)
):
    """
    회원 정보 수정
    - 이메일은 읽기 전용 (수정 불가)
    - 비밀번호는 별도 API로 처리
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 사용자 존재 확인
        curs.execute("SELECT u_seq FROM user WHERE u_seq = %s", (user_seq,))
        if not curs.fetchone():
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        
        # 업데이트할 필드 수집
        updates = []
        params = []
        
        if u_name:
            updates.append("u_name = %s")
            params.append(u_name)
        
        if u_phone is not None:
            if u_phone:
                # 전화번호 중복 확인
                curs.execute("""
                    SELECT u_seq FROM user 
                    WHERE u_phone = %s AND u_seq != %s
                """, (u_phone, user_seq))
                if curs.fetchone():
                    raise HTTPException(status_code=400, detail="이미 사용 중인 전화번호입니다")
            updates.append("u_phone = %s")
            params.append(u_phone if u_phone else None)
        
        if u_address is not None:
            updates.append("u_address = %s")
            params.append(u_address)
        
        if updates:
            sql = f"UPDATE user SET {', '.join(updates)} WHERE u_seq = %s"
            params.append(user_seq)
            curs.execute(sql, params)
            conn.commit()
        
        return {"result": "OK", "message": "회원 정보가 수정되었습니다"}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()
```

---

### 비밀번호 변경 (로컬 로그인만)

```python
POST /api/users/{user_seq}/password
{
  "current_password": "old_password",
  "new_password": "new_password"
}

// 소셜 로그인 사용자는 비밀번호 변경 불가
```

**API 구현:**
```python
@router.post("/users/{user_seq}/password")
async def update_password(
    user_seq: int,
    current_password: str = Form(...),
    new_password: str = Form(...)
):
    """
    비밀번호 변경 (로컬 로그인 사용자만)
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 로컬 로그인 정보 확인
        curs.execute("""
            SELECT u_seq, password 
            FROM user_auth_identities
            WHERE u_seq = %s AND provider = 'local'
        """, (user_seq,))
        row = curs.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=403,
                detail="로컬 로그인 계정이 아닙니다. 비밀번호를 변경할 수 없습니다"
            )
        
        # 현재 비밀번호 확인
        if row[1] != current_password:
            raise HTTPException(
                status_code=401,
                detail="현재 비밀번호가 올바르지 않습니다"
            )
        
        # 비밀번호 변경
        curs.execute("""
            UPDATE user_auth_identities 
            SET password = %s 
            WHERE u_seq = %s AND provider = 'local'
        """, (new_password, row[0]))
        conn.commit()
        
        return {"result": "OK", "message": "비밀번호가 변경되었습니다"}
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()
```

---

## 🎨 UI 분기 처리

### 프론트엔드 예시 (Flutter)

```dart
class UserProfileEditScreen extends StatefulWidget {
  final int userSeq;
  
  @override
  _UserProfileEditScreenState createState() => _UserProfileEditScreenState();
}

class _UserProfileEditScreenState extends State<UserProfileEditScreen> {
  bool _hasPassword = false;
  bool _isLoading = true;
  
  @override
  void initState() {
    super.initState();
    _loadUserLoginType();
  }
  
  Future<void> _loadUserLoginType() async {
    // 사용자 타입 확인
    final response = await api.get('/api/users/${widget.userSeq}/login_type');
    setState(() {
      _hasPassword = response['has_password'];
      _isLoading = false;
    });
  }
  
  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return CircularProgressIndicator();
    }
    
    return Scaffold(
      // ... UI 코드
      TextField(
        controller: _emailController,
        enabled: false,  // 이메일은 항상 읽기 전용
        decoration: InputDecoration(
          labelText: '이메일',
          hintText: '이메일은 수정할 수 없습니다',
        ),
      ),
      
      // 비밀번호 변경 버튼 (로컬 로그인만 표시)
      if (_hasPassword)
        ElevatedButton(
          onPressed: () {
            // 비밀번호 변경 화면으로 이동
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => ChangePasswordScreen(userSeq: widget.userSeq),
              ),
            );
          },
          child: Text('비밀번호 변경'),
        ),
      
      // ... 나머지 필드
    );
  }
}
```

---

## 📊 데이터 비교

### 단일 테이블 방식 (NULL 많음)

```
user 테이블:
u_seq=1, u_email="hong@example.com", u_password="hash...", 
         u_google_sub=NULL, u_kakao_id=NULL  (NULL 2개)

u_seq=2, u_email="kim@gmail.com", u_password=NULL,
         u_google_sub="구글sub", u_kakao_id=NULL  (NULL 2개)
```

### 별도 테이블 방식 (NULL 최소화) ⭐

```
user 테이블:
u_seq=1, u_email="hong@example.com", u_name="홍길동"  (NULL 없음)
u_seq=2, u_email="kim@gmail.com", u_name="김철수"  (NULL 없음)

user_auth_identities 테이블:
u_seq=1, provider="local", provider_subject="hong@example.com", password="password123"
u_seq=2, provider="google", provider_subject="구글sub", password=NULL  (NULL 1개만)
```

**장점:**
- ✅ NULL 값 최소화
- ✅ 정규화
- ✅ 확장성 (새 소셜 로그인 추가 용이)
- ✅ 사용자 타입 구분 쉬움

---

## ✅ 최종 요약

**핵심 변경사항:**

1. ✅ **별도 테이블 방식 채택**
   - `user` 테이블: 기본 사용자 정보만
   - `user_auth_identities` 테이블: 로그인 수단별 정보

2. ✅ **이메일 기반 로그인**
   - 로컬: 이메일 + 비밀번호
   - 소셜: 소셜 이메일 + 소셜 식별자

3. ✅ **사용자 타입 확인 API**
   - `/api/users/{user_seq}/login_type`
   - UI 분기 처리용

4. ✅ **회원 정보 수정: 이메일 읽기 전용**
   - 비밀번호는 로컬 로그인 사용자만 변경 가능

이 설계가 더 깔끔하고 확장 가능합니다!

