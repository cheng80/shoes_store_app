# SQLite 로그인 히스토리 스키마 설계

**목적**: 
- 사용자가 다음 로그인 시 이전 접속 정보를 확인하여 본인 접속 기록인지 확인
- 사용자가 자신의 접속 이력을 조회할 수 있도록 함

**데이터베이스**: SQLite (별도 파일로 관리)

---

## 📋 설계 원칙

1. **개인정보 제외**: 사용자 ID, 이메일, 전화번호, 이름 등 직접적인 개인정보 저장 안 함
2. **로그인 시간 기록**: 로그인 시각 필수 기록
3. **본인 확인용 정보**: 사용자가 자신의 접속 기록을 식별할 수 있는 최소한의 정보만 저장
4. **단순화**: 복잡한 보안 감사 기능 제외, 사용자 이력 조회에 집중

---

## 🗄️ 테이블 구조 (단순화 버전)

### 최종 권장 스키마 ⭐

```sql
CREATE TABLE login_history (
  -- 기본 정보
  lh_seq INTEGER PRIMARY KEY AUTOINCREMENT,
  lh_time DATETIME NOT NULL,                    -- 로그인 시각 (필수)
  lh_user_type VARCHAR(20) NOT NULL,            -- 사용자 타입 (user, staff)
  
  -- 사용자 식별 (개인정보 제외, 해시값 사용)
  lh_user_hash VARCHAR(64) NOT NULL,            -- 사용자 식별자 해시 (SHA-256)
  
  -- 본인 확인용 정보 (사용자가 자신의 접속 기록을 식별할 수 있는 정보)
  lh_device VARCHAR(100),                        -- 디바이스/브라우저 (예: "iPhone 12", "Chrome")
  lh_location VARCHAR(50),                       -- 대략적 위치 (예: "서울", "부산")
  
  -- 인덱스
  CREATE INDEX idx_lh_user_hash ON login_history(lh_user_hash);
  CREATE INDEX idx_lh_time ON login_history(lh_time DESC);
);
```

**컬럼 설명:**

| 컬럼명 | 타입 | 필수 | 앱에서 획득 가능 여부 | 설명 |
|--------|------|------|---------------------|------|
| `lh_seq` | INTEGER | ✅ | ❌ (DB 자동 생성) | 자동 증가 기본키 |
| `lh_time` | DATETIME | ✅ | ✅ (DateTime.now()) | 로그인 시각 |
| `lh_user_type` | VARCHAR(20) | ✅ | ✅ (로그인 시 구분) | 사용자 타입: `user` (고객), `staff` (직원) |
| `lh_user_hash` | VARCHAR(64) | ✅ | ✅ (user_seq 해시화) | 사용자 식별자 해시 |
| `lh_device` | VARCHAR(100) | ❌ | ⚠️ (패키지 필요) | 디바이스 정보 (예: "iPhone 12", "Samsung Galaxy") |
| `lh_location` | VARCHAR(50) | ❌ | ⚠️ (권한 필요) | 대략적 위치 (예: "서울", "부산") |

**앱에서 획득 가능 여부:**

### ✅ 앱에서 쉽게 획득 가능
- **`lh_time`**: `DateTime.now()` 또는 `DateTime.now().toIso8601String()`
- **`lh_user_type`**: 로그인 시 사용자 타입 정보 (앱에서 알고 있음)
- **`lh_user_hash`**: `user_seq`를 SHA-256 해시화 (Dart의 `dart:convert` 사용)

### ⚠️ 패키지 추가 필요
- **`lh_device`**: `device_info_plus` 패키지 필요
  ```yaml
  dependencies:
    device_info_plus: ^9.1.0
  ```
  ```dart
  import 'package:device_info_plus/device_info_plus.dart';
  
  DeviceInfoPlugin deviceInfo = DeviceInfoPlugin();
  if (Platform.isAndroid) {
    AndroidDeviceInfo androidInfo = await deviceInfo.androidInfo;
    device = "${androidInfo.brand} ${androidInfo.model}";
  } else if (Platform.isIOS) {
    IosDeviceInfo iosInfo = await deviceInfo.iosInfo;
    device = iosInfo.model;
  }
  ```

### ⚠️ 권한 및 패키지 필요
- **`lh_location`**: `geolocator` 패키지 + 위치 권한 필요
  ```yaml
  dependencies:
    geolocator: ^10.1.0
  ```
  - Android: `ACCESS_FINE_LOCATION` 권한 필요
  - iOS: `NSLocationWhenInUseUsageDescription` 필요
  - IP 기반 위치는 백엔드에서 획득 가능 (권한 불필요)

**설계 이유:**
- ✅ **`lh_time`**: 언제 로그인했는지 확인 (필수, 앱에서 쉽게 획득 가능)
- ✅ **`lh_user_hash`**: 본인의 이력만 조회하기 위한 식별자 (필수, 앱에서 획득 가능)
- ⚠️ **`lh_device`**: "이 디바이스로 로그인한 적이 있나?" 확인용 (패키지 필요)
- ⚠️ **`lh_location`**: "이 지역에서 로그인한 적이 있나?" 확인용 (권한 필요 또는 백엔드에서 IP 기반 획득)

---

## 🔐 개인정보 보호 전략

### 사용자 식별자 해시화

```python
import hashlib

# 사용자 ID를 해시화하여 저장
def hash_user_id(user_seq: int, salt: str = "login_history_salt") -> str:
    """사용자 ID를 SHA-256 해시로 변환"""
    data = f"{user_seq}_{salt}".encode('utf-8')
    return hashlib.sha256(data).hexdigest()

# 예시
user_seq = 123
user_hash = hash_user_id(user_seq)  # "a1b2c3d4e5f6..."
```

**이유:**
- 개인정보 직접 저장 안 함
- 동일 사용자의 이력만 조회 가능 (같은 해시값)
- 역추적 어려움 (보안 강화)

---

## 📊 사용 예시

### 1. 로그인 성공 기록 (Flutter/Dart)

```dart
import 'dart:convert';
import 'package:crypto/crypto.dart';
import 'package:sqflite/sqflite.dart';

// 사용자 ID 해시화
String hashUserSeq(int userSeq, {String salt = 'login_history_salt'}) {
  final bytes = utf8.encode('$userSeq\_$salt');
  final digest = sha256.convert(bytes);
  return digest.toString();
}

// 로그인 성공 기록 (최소 버전 - 옵션 1)
Future<void> logLoginSuccess({
  required int userSeq,
  required String userType,
}) async {
  final db = await openDatabase('login_history.db');
  
  final userHash = hashUserSeq(userSeq);
  final loginTime = DateTime.now().toIso8601String();
  
  await db.insert('login_history', {
    'lh_time': loginTime,
    'lh_user_type': userType,
    'lh_user_hash': userHash,
  });
  
  await db.close();
}

// 로그인 성공 기록 (디바이스 정보 포함 - 옵션 2)
Future<void> logLoginSuccessWithDevice({
  required int userSeq,
  required String userType,
  String? device,
}) async {
  final db = await openDatabase('login_history.db');
  
  final userHash = hashUserSeq(userSeq);
  final loginTime = DateTime.now().toIso8601String();
  
  await db.insert('login_history', {
    'lh_time': loginTime,
    'lh_user_type': userType,
    'lh_user_hash': userHash,
    'lh_device': device,
  });
  
  await db.close();
}

// 디바이스 정보 획득 (device_info_plus 패키지 필요)
import 'package:device_info_plus/device_info_plus.dart';
import 'dart:io';

Future<String?> getDeviceInfo() async {
  final deviceInfo = DeviceInfoPlugin();
  
  if (Platform.isAndroid) {
    final androidInfo = await deviceInfo.androidInfo;
    return '${androidInfo.brand} ${androidInfo.model}';
  } else if (Platform.isIOS) {
    final iosInfo = await deviceInfo.iosInfo;
    return iosInfo.model;
  }
  return null;
}

// 사용 예시
await logLoginSuccess(
  userSeq: 123,
  userType: 'user',
);

// 디바이스 정보 포함
final device = await getDeviceInfo();
await logLoginSuccessWithDevice(
  userSeq: 123,
  userType: 'user',
  device: device,
);
```

### 2. 사용자 본인의 접속 이력 조회 (Flutter/Dart)

```dart
import 'package:sqflite/sqflite.dart';

Future<List<Map<String, dynamic>>> getUserLoginHistory({
  required int userSeq,
  int limit = 10,
}) async {
  final db = await openDatabase('login_history.db');
  
  final userHash = hashUserSeq(userSeq);
  
  final List<Map<String, dynamic>> rows = await db.query(
    'login_history',
    where: 'lh_user_hash = ?',
    whereArgs: [userHash],
    orderBy: 'lh_time DESC',
    limit: limit,
  );
  
  await db.close();
  
  return rows.map((row) => {
    'time': row['lh_time'],
    'device': row['lh_device'] ?? '알 수 없음',
    'location': row['lh_location'] ?? '알 수 없음',
  }).toList();
}

// 사용 예시
final history = await getUserLoginHistory(userSeq: 123);
// 결과 예시:
// [
//   {'time': '2025-01-15T10:30:00.000', 'device': 'iPhone 12', 'location': '알 수 없음'},
//   {'time': '2025-01-14T15:20:00.000', 'device': 'Samsung Galaxy S21', 'location': '알 수 없음'},
//   ...
// ]
```

### 3. 다음 로그인 시 이전 접속 정보 제시 (Flutter/Dart)

```dart
Future<Map<String, dynamic>?> getRecentLoginInfo(int userSeq) async {
  final db = await openDatabase('login_history.db');
  
  final userHash = hashUserSeq(userSeq);
  
  final List<Map<String, dynamic>> rows = await db.query(
    'login_history',
    where: 'lh_user_hash = ?',
    whereArgs: [userHash],
    orderBy: 'lh_time DESC',
    limit: 1,
  );
  
  await db.close();
  
  if (rows.isEmpty) {
    return null;
  }
  
  final row = rows.first;
  return {
    'last_login_time': row['lh_time'],
    'last_device': row['lh_device'] ?? '알 수 없음',
    'last_location': row['lh_location'] ?? '알 수 없음',
  };
}

// 사용 예시: 로그인 시 이전 접속 정보 제시
final previousInfo = await getRecentLoginInfo(123);
if (previousInfo != null) {
  print('이전 접속: ${previousInfo['last_login_time']}');
  print('디바이스: ${previousInfo['last_device']}');
  print('위치: ${previousInfo['last_location']}');
  print('이 접속 기록이 맞나요?');
}
```

---

## 🎯 최종 권장 스키마 (단순화)

**목적**: 사용자가 자신의 접속 이력을 조회하고, 다음 로그인 시 이전 접속 정보를 확인하기 위함

### 필수 컬럼 (4개)

1. **`lh_seq`** - 기본키 (자동 증가)
2. **`lh_time`** - 로그인 시각 (DATETIME, 필수) - "언제 로그인했는지"
3. **`lh_user_type`** - 사용자 타입 (VARCHAR, 필수) - "고객인지 직원인지"
4. **`lh_user_hash`** - 사용자 식별자 해시 (VARCHAR, 필수) - "누구의 이력인지"

### 선택 컬럼 (2개)

5. **`lh_device`** - 디바이스 정보 (VARCHAR) - "어떤 기기로 로그인했는지"
6. **`lh_location`** - 대략적 위치 (VARCHAR) - "어디서 로그인했는지"

---

## 📝 최종 권장 스키마 (단순화 버전)

```sql
CREATE TABLE login_history (
  -- 필수 컬럼
  lh_seq INTEGER PRIMARY KEY AUTOINCREMENT,
  lh_time DATETIME NOT NULL,
  lh_user_type VARCHAR(20) NOT NULL,
  lh_user_hash VARCHAR(64) NOT NULL,
  
  -- 본인 확인용 정보 (선택)
  lh_device VARCHAR(100),
  lh_location VARCHAR(50),
  
  -- 인덱스
  CREATE INDEX idx_lh_user_hash ON login_history(lh_user_hash);
  CREATE INDEX idx_lh_time ON login_history(lh_time DESC);
);
```

**총 6개 컬럼** (기본키 포함)

---

## 🔄 데이터 보관 정책

### 권장 보관 기간

- **활성 데이터**: 최근 90일
- **아카이빙**: 90일 이후 별도 아카이브 테이블로 이동
- **삭제**: 1년 이후 자동 삭제 (또는 법적 요구사항에 따라)

### 아카이빙 예시

```sql
-- 90일 이전 데이터를 아카이브 테이블로 이동
INSERT INTO login_history_archive
SELECT * FROM login_history
WHERE lh_time < datetime('now', '-90 days');

-- 원본 테이블에서 삭제
DELETE FROM login_history
WHERE lh_time < datetime('now', '-90 days');
```

---

## ✅ 체크리스트

- [x] 개인정보 직접 저장 안 함
- [x] 로그인 시각 기록 (필수, 앱에서 쉽게 획득 가능)
- [x] 사용자 타입 구분 (필수, 앱에서 알고 있음)
- [x] 사용자 식별자 해시화 (필수, 앱에서 해시화 가능)
- [ ] 디바이스 정보 기록 (선택, `device_info_plus` 패키지 필요)
- [ ] 위치 정보 기록 (선택, `geolocator` 패키지 + 권한 필요 또는 백엔드에서 IP 기반 획득)
- [x] 인덱스 설정 (조회 성능)
- [x] 단순화된 구조 (복잡한 보안 감사 기능 제외)

## 📦 필요한 패키지 (옵션에 따라)

### 최소 구현 (옵션 1)
```yaml
dependencies:
  sqflite: ^2.4.2  # 이미 있음
  crypto: ^3.0.3   # SHA-256 해시화용
```

### 디바이스 정보 추가 (옵션 2)
```yaml
dependencies:
  sqflite: ^2.4.2
  crypto: ^3.0.3
  device_info_plus: ^9.1.0  # 추가 필요
```

### 위치 정보 추가 (옵션 3)
```yaml
dependencies:
  sqflite: ^2.4.2
  crypto: ^3.0.3
  device_info_plus: ^9.1.0
  geolocator: ^10.1.0  # 추가 필요 (또는 백엔드에서 IP 기반 획득)
```

## 💡 사용 시나리오

### 시나리오 1: 다음 로그인 시 이전 접속 정보 제시

```
사용자가 로그인 성공 후:
"이전 접속: 2025-01-14 15:20:00"
"디바이스: iPhone 12"
"위치: 서울"
"이 접속 기록이 맞나요? [예/아니오]"
```

### 시나리오 2: 자신의 접속 이력 조회

```
사용자가 "내 접속 이력" 메뉴 클릭:
- 2025-01-15 10:30:00 | iPhone 12 | 서울
- 2025-01-14 15:20:00 | Chrome | 부산
- 2025-01-13 09:10:00 | Samsung Galaxy | 경기
...
```

이렇게 단순한 목적에 맞게 설계하면 됩니다!

