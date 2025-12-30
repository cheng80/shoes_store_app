-- staff 테이블에 s_id와 s_quit_date 컬럼 추가
-- 실행: mysql -u root -p shoes_shop_db < alter_staff_add_columns.sql

USE shoes_shop_db;

-- s_id 컬럼 추가 (s_seq 다음에)
ALTER TABLE staff 
ADD COLUMN s_id VARCHAR(50) NOT NULL COMMENT '직원 로그인 ID' AFTER s_seq;

-- s_quit_date 컬럼 추가 (created_at 다음에)
ALTER TABLE staff 
ADD COLUMN s_quit_date DATETIME NULL COMMENT '직원 탈퇴 일자' AFTER created_at;

-- s_id에 UNIQUE 인덱스 추가
ALTER TABLE staff 
ADD UNIQUE INDEX idx_staff_id (s_id);

-- s_quit_date에 인덱스 추가
ALTER TABLE staff 
ADD INDEX idx_staff_quit_date (s_quit_date);

-- 기존 데이터에 임시 s_id 값 설정 (s_seq 기반)
UPDATE staff SET s_id = CONCAT('staff', LPAD(s_seq, 3, '0')) WHERE s_id IS NULL OR s_id = '';

SELECT 'staff 테이블 컬럼 추가 완료!' AS result;

