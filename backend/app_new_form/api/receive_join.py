"""
Receive 복합 쿼리 API
- Receive 중심의 JOIN 쿼리들
- Receive + Staff + Product + Maker + 모든 카테고리

개별 실행: python receive_join.py
"""

from fastapi import APIRouter, Query
from typing import Optional
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# Receive + Staff + Product + Maker
# ============================================
@router.get("/receives/{receive_seq}/with_details")
async def get_receive_with_details(receive_seq: int):
    """
    특정 Receive + Staff + Product + Maker 정보
    JOIN: Receive + Staff + Product + Maker (4테이블)
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            rec.rec_seq,
            rec.rec_quantity,
            rec.rec_date,
            s.s_seq,
            s.s_rank,
            s.s_phone,
            p.p_seq,
            p.p_name,
            p.p_price,
            p.p_stock,
            p.p_image,
            m.m_seq,
            m.m_name,
            m.m_phone,
            m.m_address
        FROM receive rec
        JOIN staff s ON rec.s_seq = s.s_seq
        JOIN product p ON rec.p_seq = p.p_seq
        JOIN maker m ON rec.m_seq = m.m_seq
        WHERE rec.rec_seq = %s
        """
        curs.execute(sql, (receive_seq,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Receive not found"}
        
        result = {
            'rec_seq': row[0],
            'rec_quantity': row[1],
            'rec_date': row[2].isoformat() if row[2] else None,
            'staff': {
                's_seq': row[3],
                's_rank': row[4],
                's_phone': row[5]
            },
            'product': {
                'p_seq': row[6],
                'p_name': row[7],
                'p_price': row[8],
                'p_stock': row[9],
                'p_image': row[10]
            },
            'maker': {
                'm_seq': row[11],
                'm_name': row[12],
                'm_phone': row[13],
                'm_address': row[14]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# Receive 전체 상세 (Product의 모든 카테고리 포함)
# ============================================
@router.get("/receives/{receive_seq}/full_detail")
async def get_receive_full_detail(receive_seq: int):
    """
    특정 Receive의 전체 상세 정보
    JOIN: Receive + Staff + Product + Maker + 모든 카테고리 (9테이블)
    용도: 입고 상세 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            rec.rec_seq,
            rec.rec_quantity,
            rec.rec_date,
            s.s_seq,
            s.s_rank,
            s.s_phone,
            p.p_seq,
            p.p_name,
            p.p_price,
            p.p_stock,
            p.p_image,
            kc.kc_name,
            cc.cc_name,
            sc.sc_name,
            gc.gc_name,
            m.m_seq,
            m.m_name,
            m.m_phone,
            m.m_address
        FROM receive rec
        JOIN staff s ON rec.s_seq = s.s_seq
        JOIN product p ON rec.p_seq = p.p_seq
        JOIN kind_category kc ON p.kc_seq = kc.kc_seq
        JOIN color_category cc ON p.cc_seq = cc.cc_seq
        JOIN size_category sc ON p.sc_seq = sc.sc_seq
        JOIN gender_category gc ON p.gc_seq = gc.gc_seq
        JOIN maker m ON rec.m_seq = m.m_seq
        WHERE rec.rec_seq = %s
        """
        curs.execute(sql, (receive_seq,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Receive not found"}
        
        result = {
            'rec_seq': row[0],
            'rec_quantity': row[1],
            'rec_date': row[2].isoformat() if row[2] else None,
            'staff': {
                's_seq': row[3],
                's_rank': row[4],
                's_phone': row[5]
            },
            'product': {
                'p_seq': row[6],
                'p_name': row[7],
                'p_price': row[8],
                'p_stock': row[9],
                'p_image': row[10],
                'kind_name': row[11],
                'color_name': row[12],
                'size_name': row[13],
                'gender_name': row[14]
            },
            'maker': {
                'm_seq': row[15],
                'm_name': row[16],
                'm_phone': row[17],
                'm_address': row[18]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 직원별 Receive 목록
# ============================================
@router.get("/receives/by_staff/{staff_seq}/with_details")
async def get_receives_by_staff_with_details(staff_seq: int):
    """
    특정 직원이 처리한 모든 Receive + 상세 정보
    JOIN: Receive + Staff + Product + Maker
    용도: 직원별 입고 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            rec.rec_seq,
            rec.rec_quantity,
            rec.rec_date,
            p.p_name,
            p.p_price,
            p.p_image,
            m.m_name
        FROM receive rec
        JOIN product p ON rec.p_seq = p.p_seq
        JOIN maker m ON rec.m_seq = m.m_seq
        WHERE rec.s_seq = %s
        ORDER BY rec.rec_date DESC, rec.rec_seq DESC
        """
        curs.execute(sql, (staff_seq,))
        rows = curs.fetchall()
        
        result = [{
            'rec_seq': row[0],
            'rec_quantity': row[1],
            'rec_date': row[2].isoformat() if row[2] else None,
            'product': {
                'p_name': row[3],
                'p_price': row[4],
                'p_image': row[5]
            },
            'maker_name': row[6]
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제품별 Receive 목록
# ============================================
@router.get("/receives/by_product/{product_seq}/with_details")
async def get_receives_by_product_with_details(product_seq: int):
    """
    특정 제품의 모든 Receive + 상세 정보
    JOIN: Receive + Staff + Product + Maker
    용도: 제품별 입고 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            rec.rec_seq,
            rec.rec_quantity,
            rec.rec_date,
            s.s_rank,
            s.s_phone,
            m.m_name,
            m.m_phone
        FROM receive rec
        JOIN staff s ON rec.s_seq = s.s_seq
        JOIN maker m ON rec.m_seq = m.m_seq
        WHERE rec.p_seq = %s
        ORDER BY rec.rec_date DESC, rec.rec_seq DESC
        """
        curs.execute(sql, (product_seq,))
        rows = curs.fetchall()
        
        result = [{
            'rec_seq': row[0],
            'rec_quantity': row[1],
            'rec_date': row[2].isoformat() if row[2] else None,
            'staff': {
                's_rank': row[3],
                's_phone': row[4]
            },
            'maker': {
                'm_name': row[5],
                'm_phone': row[6]
            }
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제조사별 Receive 목록
# ============================================
@router.get("/receives/by_maker/{maker_seq}/with_details")
async def get_receives_by_maker_with_details(maker_seq: int):
    """
    특정 제조사의 모든 Receive + 상세 정보
    JOIN: Receive + Staff + Product + Maker
    용도: 제조사별 입고 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            rec.rec_seq,
            rec.rec_quantity,
            rec.rec_date,
            s.s_rank,
            s.s_phone,
            p.p_name,
            p.p_price,
            p.p_image
        FROM receive rec
        JOIN staff s ON rec.s_seq = s.s_seq
        JOIN product p ON rec.p_seq = p.p_seq
        WHERE rec.m_seq = %s
        ORDER BY rec.rec_date DESC, rec.rec_seq DESC
        """
        curs.execute(sql, (maker_seq,))
        rows = curs.fetchall()
        
        result = [{
            'rec_seq': row[0],
            'rec_quantity': row[1],
            'rec_date': row[2].isoformat() if row[2] else None,
            'staff': {
                's_rank': row[3],
                's_phone': row[4]
            },
            'product': {
                'p_name': row[5],
                'p_price': row[6],
                'p_image': row[7]
            }
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)