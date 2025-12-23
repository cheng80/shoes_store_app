-- ============================================
-- MySQL Database Reset Script
-- 기존 데이터 및 테이블 삭제 (초기화)
-- ============================================
-- 
-- 사용 방법 (MySQL Workbench):
--   1. MySQL Workbench 실행
--   2. File > Open SQL Script... 선택
--   3. 이 파일(reset.sql) 선택
--   4. 실행할 데이터베이스 선택 (shoes_store_db)
--   5. 번개 아이콘(Execute) 클릭 또는 Ctrl+Shift+Enter
--
-- 주의: 이 스크립트는 모든 데이터를 삭제합니다!
-- ============================================

USE shoes_store_db;

SET FOREIGN_KEY_CHECKS = 0;

-- 모든 테이블 삭제 (외래키 관계 순서 고려)
DROP TABLE IF EXISTS LoginHistory;
DROP TABLE IF EXISTS PurchaseItem;
DROP TABLE IF EXISTS Purchase;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS ProductImage;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS ProductBase;
DROP TABLE IF EXISTS Manufacturer;

SET FOREIGN_KEY_CHECKS = 1;

SELECT 'All tables have been dropped successfully!' AS Status;

