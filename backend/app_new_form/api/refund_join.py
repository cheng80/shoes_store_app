"""
Refund 복합 쿼리 API
- Refund 중심의 JOIN 쿼리들
- Refund + User + Staff + Pickup + PurchaseItem + Product + Branch

개별 실행: python refund_join.py
"""

from fastapi import APIRouter, Query
from typing import Optional
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# Refund + User + Staff + Pickup + PurchaseItem + Product + Branch
# ============================================
@router.get("/refunds/{refund_seq}/with_details")
async def get_refund_with_details(refund_seq: int):
    """
    특정 Refund + User + Staff + Pickup + PurchaseItem + Product + Branch 정보
    JOIN: Refund + User + Staff + Pickup + PurchaseItem + Product + Branch (7테이블)
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            ref.ref_seq,
            ref.ref_date,
            ref.ref_reason,
            u.u_seq,
            u.u_name,
            u.u_phone,
            s.s_seq,
            s.s_rank,
            s.s_phone,
            pic.pic_seq,
            pic.created_at,
            pi.b_seq,
            pi.b_price,
            pi.b_quantity,
            pi.b_date,
            p.p_seq,
            p.p_name,
            p.p_price,
            p.p_image,
            br.br_seq,
            br.br_name
        FROM refund ref
        JOIN user u ON ref.u_seq = u.u_seq
        JOIN staff s ON ref.s_seq = s.s_seq
        JOIN pickup pic ON ref.pic_seq = pic.pic_seq
        JOIN purchase_item pi ON pic.b_seq = pi.b_seq
        JOIN product p ON pi.p_seq = p.p_seq
        JOIN branch br ON pi.br_seq = br.br_seq
        WHERE ref.ref_seq = %s
        """
        curs.execute(sql, (refund_seq,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Refund not found"}
        
        result = {
            'ref_seq': row[0],
            'ref_date': row[1].isoformat() if row[1] else None,
            'ref_reason': row[2],
            'user': {
                'u_seq': row[3],
                'u_name': row[4],
                'u_phone': row[5]
            },
            'staff': {
                's_seq': row[6],
                's_rank': row[7],
                's_phone': row[8]
            },
            'pickup': {
                'pic_seq': row[9],
                'created_at': row[10].isoformat() if row[10] else None
            },
            'purchase_item': {
                'b_seq': row[11],
                'b_price': row[12],
                'b_quantity': row[13],
                'b_date': row[14].isoformat() if row[14] else None
            },
            'product': {
                'p_seq': row[15],
                'p_name': row[16],
                'p_price': row[17],
                'p_image': row[18]
            },
            'branch': {
                'br_seq': row[19],
                'br_name': row[20]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# Refund 전체 상세 (Product의 모든 카테고리 포함)
# ============================================
@router.get("/refunds/{refund_seq}/full_detail")
async def get_refund_full_detail(refund_seq: int):
    """
    특정 Refund의 전체 상세 정보
    JOIN: Refund + User + Staff + Pickup + PurchaseItem + Product + Branch + 모든 카테고리 + Maker (12테이블)
    용도: 반품 상세 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            ref.ref_seq,
            ref.ref_date,
            ref.ref_reason,
            u.u_seq,
            u.u_name,
            u.u_phone,
            s.s_seq,
            s.s_rank,
            s.s_phone,
            pic.pic_seq,
            pic.created_at,
            pi.b_seq,
            pi.b_price,
            pi.b_quantity,
            pi.b_date,
            p.p_seq,
            p.p_name,
            p.p_price,
            p.p_image,
            kc.kc_name,
            cc.cc_name,
            sc.sc_name,
            gc.gc_name,
            m.m_name,
            br.br_seq,
            br.br_name,
            br.br_address
        FROM refund ref
        JOIN user u ON ref.u_seq = u.u_seq
        JOIN staff s ON ref.s_seq = s.s_seq
        JOIN pickup pic ON ref.pic_seq = pic.pic_seq
        JOIN purchase_item pi ON pic.b_seq = pi.b_seq
        JOIN product p ON pi.p_seq = p.p_seq
        JOIN kind_category kc ON p.kc_seq = kc.kc_seq
        JOIN color_category cc ON p.cc_seq = cc.cc_seq
        JOIN size_category sc ON p.sc_seq = sc.sc_seq
        JOIN gender_category gc ON p.gc_seq = gc.gc_seq
        JOIN maker m ON p.m_seq = m.m_seq
        JOIN branch br ON pi.br_seq = br.br_seq
        WHERE ref.ref_seq = %s
        """
        curs.execute(sql, (refund_seq,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Refund not found"}
        
        result = {
            'ref_seq': row[0],
            'ref_date': row[1].isoformat() if row[1] else None,
            'ref_reason': row[2],
            'user': {
                'u_seq': row[3],
                'u_name': row[4],
                'u_phone': row[5]
            },
            'staff': {
                's_seq': row[6],
                's_rank': row[7],
                's_phone': row[8]
            },
            'pickup': {
                'pic_seq': row[9],
                'created_at': row[10].isoformat() if row[10] else None
            },
            'purchase_item': {
                'b_seq': row[11],
                'b_price': row[12],
                'b_quantity': row[13],
                'b_date': row[14].isoformat() if row[14] else None
            },
            'product': {
                'p_seq': row[15],
                'p_name': row[16],
                'p_price': row[17],
                'p_image': row[18],
                'kind_name': row[19],
                'color_name': row[20],
                'size_name': row[21],
                'gender_name': row[22],
                'maker_name': row[23]
            },
            'branch': {
                'br_seq': row[24],
                'br_name': row[25],
                'br_address': row[26]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객별 Refund 목록
# ============================================
@router.get("/refunds/by_user/{user_seq}/with_details")
async def get_refunds_by_user_with_details(user_seq: int):
    """
    특정 고객의 모든 Refund + 상세 정보
    JOIN: Refund + User + Staff + Pickup + PurchaseItem + Product
    용도: 고객 반품 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            ref.ref_seq,
            ref.ref_date,
            ref.ref_reason,
            s.s_rank,
            s.s_phone,
            p.p_name,
            p.p_image,
            pi.b_price,
            pi.b_quantity
        FROM refund ref
        JOIN staff s ON ref.s_seq = s.s_seq
        JOIN pickup pic ON ref.pic_seq = pic.pic_seq
        JOIN purchase_item pi ON pic.b_seq = pi.b_seq
        JOIN product p ON pi.p_seq = p.p_seq
        WHERE ref.u_seq = %s
        ORDER BY ref.ref_date DESC, ref.ref_seq DESC
        """
        curs.execute(sql, (user_seq,))
        rows = curs.fetchall()
        
        result = [{
            'ref_seq': row[0],
            'ref_date': row[1].isoformat() if row[1] else None,
            'ref_reason': row[2],
            'staff': {
                's_rank': row[3],
                's_phone': row[4]
            },
            'product': {
                'p_name': row[5],
                'p_image': row[6]
            },
            'purchase_item': {
                'b_price': row[7],
                'b_quantity': row[8]
            }
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 직원별 처리한 Refund 목록
# ============================================
@router.get("/refunds/by_staff/{staff_seq}/with_details")
async def get_refunds_by_staff_with_details(staff_seq: int):
    """
    특정 직원이 처리한 모든 Refund + 상세 정보
    JOIN: Refund + User + Staff + Pickup + PurchaseItem + Product
    용도: 직원별 반품 처리 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            ref.ref_seq,
            ref.ref_date,
            ref.ref_reason,
            u.u_name,
            u.u_phone,
            p.p_name,
            p.p_image,
            pi.b_price,
            pi.b_quantity
        FROM refund ref
        JOIN user u ON ref.u_seq = u.u_seq
        JOIN pickup pic ON ref.pic_seq = pic.pic_seq
        JOIN purchase_item pi ON pic.b_seq = pi.b_seq
        JOIN product p ON pi.p_seq = p.p_seq
        WHERE ref.s_seq = %s
        ORDER BY ref.ref_date DESC, ref.ref_seq DESC
        """
        curs.execute(sql, (staff_seq,))
        rows = curs.fetchall()
        
        result = [{
            'ref_seq': row[0],
            'ref_date': row[1].isoformat() if row[1] else None,
            'ref_reason': row[2],
            'user': {
                'u_name': row[3],
                'u_phone': row[4]
            },
            'product': {
                'p_name': row[5],
                'p_image': row[6]
            },
            'purchase_item': {
                'b_price': row[7],
                'b_quantity': row[8]
            }
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)