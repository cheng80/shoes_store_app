/* =========================================================
   소셜 로그인 지원을 위한 데이터베이스 마이그레이션 스크립트
   
   변경 사항:
   1. user_auth_identities 테이블 생성 (로그인 수단 매핑)
   2. user 테이블 구조 변경 (u_id, u_password 제거, u_phone nullable)
   3. 기존 데이터 마이그레이션
   
   실행 순서:
   1. 이 스크립트 실행 전 백업 필수!
   2. 기존 데이터 마이그레이션
   3. user 테이블 구조 변경
   4. user_auth_identities 테이블 생성
========================================================= */

USE shoes_shop_db;

-- =========================================================
-- 1단계: user_auth_identities 테이블 생성
-- =========================================================
DROP TABLE IF EXISTS user_auth_identities;
CREATE TABLE user_auth_identities (
  id                INT AUTO_INCREMENT PRIMARY KEY COMMENT '인증 수단 고유 ID(PK)',
  u_seq             INT NOT NULL COMMENT '고객 번호(FK)',
  provider          VARCHAR(50) NOT NULL COMMENT '로그인 제공자(local, google, kakao)',
  provider_subject  VARCHAR(255) NOT NULL COMMENT '제공자 고유 식별자(로컬: 이메일, 구글: sub, 카카오: id)',
  provider_issuer   VARCHAR(255) NULL COMMENT '제공자 발급자(구글 iss 등)',
  email_at_provider VARCHAR(255) NULL COMMENT '제공자에서 받은 이메일',
  password          VARCHAR(255) NULL COMMENT '로컬 로그인 비밀번호 (로컬만)',
  created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일자',
  last_login_at     DATETIME NULL COMMENT '마지막 로그인 일시',
  
  CONSTRAINT fk_user_auth_user
    FOREIGN KEY (u_seq) REFERENCES user(u_seq)
    ON DELETE CASCADE ON UPDATE CASCADE,
  
  UNIQUE INDEX idx_provider_subject (provider, provider_subject),
  INDEX idx_user_auth_u_seq (u_seq),
  INDEX idx_user_auth_provider (provider)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='사용자 로그인 수단 매핑';

-- =========================================================
-- 2단계: 기존 데이터 마이그레이션 (u_id, u_password → user_auth_identities)
-- =========================================================
-- 기존 로컬 로그인 사용자들을 user_auth_identities로 이동
-- u_id를 이메일로 간주하여 마이그레이션 (u_id가 이메일 형식이면 그대로, 아니면 u_email로 업데이트 필요)
INSERT INTO user_auth_identities (u_seq, provider, provider_subject, password, created_at)
SELECT 
  u_seq,
  'local',
  u_id,  -- u_id를 provider_subject로 사용 (이메일 또는 로그인 ID)
  u_password,
  created_at
FROM user
WHERE u_id IS NOT NULL AND u_password IS NOT NULL;

-- =========================================================
-- 3단계: user 테이블 구조 변경
-- =========================================================

-- 3-1. u_email 컬럼 추가 (NOT NULL, unique)
-- 기존 u_id가 이메일 형식이면 u_email로 복사, 아니면 NULL로 시작
ALTER TABLE user 
ADD COLUMN u_email VARCHAR(255) NULL COMMENT '고객 이메일' AFTER u_seq;

-- u_id가 이메일 형식인 경우 u_email로 복사
UPDATE user 
SET u_email = u_id 
WHERE u_id LIKE '%@%' AND u_email IS NULL;

-- u_email에 UNIQUE 인덱스 추가 (NULL 허용)
ALTER TABLE user 
ADD UNIQUE INDEX idx_user_email (u_email);

-- u_email을 NOT NULL로 변경 (기존 데이터가 있으면 먼저 처리 필요)
-- 주의: u_email이 NULL인 레코드가 있으면 실패할 수 있음
-- ALTER TABLE user MODIFY COLUMN u_email VARCHAR(255) NOT NULL COMMENT '고객 이메일';

-- 3-2. u_phone을 NULL 허용으로 변경
ALTER TABLE user 
MODIFY COLUMN u_phone VARCHAR(30) NULL COMMENT '고객 전화번호';

-- 3-3. u_id 컬럼 제거 (user_auth_identities로 이동)
ALTER TABLE user 
DROP INDEX idx_user_id,
DROP COLUMN u_id;

-- 3-4. u_password 컬럼 제거 (user_auth_identities로 이동)
ALTER TABLE user 
DROP COLUMN u_password;

-- =========================================================
-- 4단계: 검증 쿼리
-- =========================================================
-- 마이그레이션 결과 확인
SELECT 
  'user 테이블 구조 확인' AS check_type,
  COUNT(*) AS total_users,
  COUNT(u_email) AS users_with_email,
  COUNT(u_phone) AS users_with_phone
FROM user;

SELECT 
  'user_auth_identities 테이블 확인' AS check_type,
  provider,
  COUNT(*) AS count
FROM user_auth_identities
GROUP BY provider;

-- =========================================================
-- 완료 메시지
-- =========================================================
SELECT '마이그레이션 완료!' AS status;

