"""
Request 복합 쿼리 API
- Request 중심의 JOIN 쿼리들
- Request + Staff + Product + Maker + 모든 카테고리

개별 실행: python request_join.py
"""

from fastapi import APIRouter, Query
from typing import Optional
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# Request + Staff + Product + Maker
# ============================================
@router.get("/requests/{request_seq}/with_details")
async def get_request_with_details(request_seq: int):
    """
    특정 Request + Staff + Product + Maker 정보
    JOIN: Request + Staff + Product + Maker (4테이블)
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            req.req_seq,
            req.req_date,
            req.req_content,
            req.req_quantity,
            req.req_manappdate,
            req.req_dirappdate,
            req.s_superseq,
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
        FROM request req
        JOIN staff s ON req.s_seq = s.s_seq
        JOIN product p ON req.p_seq = p.p_seq
        JOIN maker m ON req.m_seq = m.m_seq
        WHERE req.req_seq = %s
        """
        curs.execute(sql, (request_seq,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Request not found"}
        
        result = {
            'req_seq': row[0],
            'req_date': row[1].isoformat() if row[1] else None,
            'req_content': row[2],
            'req_quantity': row[3],
            'req_manappdate': row[4].isoformat() if row[4] else None,
            'req_dirappdate': row[5].isoformat() if row[5] else None,
            's_superseq': row[6],
            'staff': {
                's_seq': row[7],
                's_rank': row[8],
                's_phone': row[9]
            },
            'product': {
                'p_seq': row[10],
                'p_name': row[11],
                'p_price': row[12],
                'p_stock': row[13],
                'p_image': row[14]
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
# Request 전체 상세 (Product의 모든 카테고리 포함)
# ============================================
@router.get("/requests/{request_seq}/full_detail")
async def get_request_full_detail(request_seq: int):
    """
    특정 Request의 전체 상세 정보
    JOIN: Request + Staff + Product + Maker + 모든 카테고리 (9테이블)
    용도: 발주 상세 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            req.req_seq,
            req.req_date,
            req.req_content,
            req.req_quantity,
            req.req_manappdate,
            req.req_dirappdate,
            req.s_superseq,
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
        FROM request req
        JOIN staff s ON req.s_seq = s.s_seq
        JOIN product p ON req.p_seq = p.p_seq
        JOIN kind_category kc ON p.kc_seq = kc.kc_seq
        JOIN color_category cc ON p.cc_seq = cc.cc_seq
        JOIN size_category sc ON p.sc_seq = sc.sc_seq
        JOIN gender_category gc ON p.gc_seq = gc.gc_seq
        JOIN maker m ON req.m_seq = m.m_seq
        WHERE req.req_seq = %s
        """
        curs.execute(sql, (request_seq,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Request not found"}
        
        result = {
            'req_seq': row[0],
            'req_date': row[1].isoformat() if row[1] else None,
            'req_content': row[2],
            'req_quantity': row[3],
            'req_manappdate': row[4].isoformat() if row[4] else None,
            'req_dirappdate': row[5].isoformat() if row[5] else None,
            's_superseq': row[6],
            'staff': {
                's_seq': row[7],
                's_rank': row[8],
                's_phone': row[9]
            },
            'product': {
                'p_seq': row[10],
                'p_name': row[11],
                'p_price': row[12],
                'p_stock': row[13],
                'p_image': row[14],
                'kind_name': row[15],
                'color_name': row[16],
                'size_name': row[17],
                'gender_name': row[18]
            },
            'maker': {
                'm_seq': row[19],
                'm_name': row[20],
                'm_phone': row[21],
                'm_address': row[22]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 직원별 Request 목록
# ============================================
@router.get("/requests/by_staff/{staff_seq}/with_details")
async def get_requests_by_staff_with_details(staff_seq: int):
    """
    특정 직원이 요청한 모든 Request + 상세 정보
    JOIN: Request + Staff + Product + Maker
    용도: 직원별 발주 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            req.req_seq,
            req.req_date,
            req.req_content,
            req.req_quantity,
            req.req_manappdate,
            req.req_dirappdate,
            p.p_name,
            p.p_price,
            p.p_image,
            m.m_name
        FROM request req
        JOIN product p ON req.p_seq = p.p_seq
        JOIN maker m ON req.m_seq = m.m_seq
        WHERE req.s_seq = %s
        ORDER BY req.req_date DESC, req.req_seq DESC
        """
        curs.execute(sql, (staff_seq,))
        rows = curs.fetchall()
        
        result = [{
            'req_seq': row[0],
            'req_date': row[1].isoformat() if row[1] else None,
            'req_content': row[2],
            'req_quantity': row[3],
            'req_manappdate': row[4].isoformat() if row[4] else None,
            'req_dirappdate': row[5].isoformat() if row[5] else None,
            'product': {
                'p_name': row[6],
                'p_price': row[7],
                'p_image': row[8]
            },
            'maker_name': row[9]
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 결재 상태별 Request 목록
# ============================================
@router.get("/requests/by_status")
async def get_requests_by_status(
    status: str = Query(..., description="결재 상태: pending(대기), manager_approved(팀장승인), director_approved(이사승인), all(전체)")
):
    """
    결재 상태별 Request 목록
    JOIN: Request + Staff + Product + Maker
    용도: 결재 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        if status == "pending":
            where_clause = "WHERE req.req_manappdate IS NULL AND req.req_dirappdate IS NULL"
        elif status == "manager_approved":
            where_clause = "WHERE req.req_manappdate IS NOT NULL AND req.req_dirappdate IS NULL"
        elif status == "director_approved":
            where_clause = "WHERE req.req_dirappdate IS NOT NULL"
        else:  # all
            where_clause = ""
        
        sql = f"""
        SELECT 
            req.req_seq,
            req.req_date,
            req.req_content,
            req.req_quantity,
            req.req_manappdate,
            req.req_dirappdate,
            s.s_rank,
            s.s_phone,
            p.p_name,
            p.p_price,
            m.m_name
        FROM request req
        JOIN staff s ON req.s_seq = s.s_seq
        JOIN product p ON req.p_seq = p.p_seq
        JOIN maker m ON req.m_seq = m.m_seq
        {where_clause}
        ORDER BY req.req_date DESC, req.req_seq DESC
        """
        curs.execute(sql)
        rows = curs.fetchall()
        
        result = [{
            'req_seq': row[0],
            'req_date': row[1].isoformat() if row[1] else None,
            'req_content': row[2],
            'req_quantity': row[3],
            'req_manappdate': row[4].isoformat() if row[4] else None,
            'req_dirappdate': row[5].isoformat() if row[5] else None,
            'staff': {
                's_rank': row[6],
                's_phone': row[7]
            },
            'product': {
                'p_name': row[8],
                'p_price': row[9]
            },
            'maker_name': row[10]
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제품별 Request 목록
# ============================================
@router.get("/requests/by_product/{product_seq}/with_details")
async def get_requests_by_product_with_details(product_seq: int):
    """
    특정 제품의 모든 Request + 상세 정보
    JOIN: Request + Staff + Product + Maker
    용도: 제품별 발주 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            req.req_seq,
            req.req_date,
            req.req_content,
            req.req_quantity,
            req.req_manappdate,
            req.req_dirappdate,
            s.s_rank,
            s.s_phone,
            m.m_name,
            m.m_phone
        FROM request req
        JOIN staff s ON req.s_seq = s.s_seq
        JOIN maker m ON req.m_seq = m.m_seq
        WHERE req.p_seq = %s
        ORDER BY req.req_date DESC, req.req_seq DESC
        """
        curs.execute(sql, (product_seq,))
        rows = curs.fetchall()
        
        result = [{
            'req_seq': row[0],
            'req_date': row[1].isoformat() if row[1] else None,
            'req_content': row[2],
            'req_quantity': row[3],
            'req_manappdate': row[4].isoformat() if row[4] else None,
            'req_dirappdate': row[5].isoformat() if row[5] else None,
            'staff': {
                's_rank': row[6],
                's_phone': row[7]
            },
            'maker': {
                'm_name': row[8],
                'm_phone': row[9]
            }
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제조사별 Request 목록
# ============================================
@router.get("/requests/by_maker/{maker_seq}/with_details")
async def get_requests_by_maker_with_details(maker_seq: int):
    """
    특정 제조사의 모든 Request + 상세 정보
    JOIN: Request + Staff + Product + Maker
    용도: 제조사별 발주 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            req.req_seq,
            req.req_date,
            req.req_content,
            req.req_quantity,
            req.req_manappdate,
            req.req_dirappdate,
            s.s_rank,
            s.s_phone,
            p.p_name,
            p.p_price,
            p.p_image
        FROM request req
        JOIN staff s ON req.s_seq = s.s_seq
        JOIN product p ON req.p_seq = p.p_seq
        WHERE req.m_seq = %s
        ORDER BY req.req_date DESC, req.req_seq DESC
        """
        curs.execute(sql, (maker_seq,))
        rows = curs.fetchall()
        
        result = [{
            'req_seq': row[0],
            'req_date': row[1].isoformat() if row[1] else None,
            'req_content': row[2],
            'req_quantity': row[3],
            'req_manappdate': row[4].isoformat() if row[4] else None,
            'req_dirappdate': row[5].isoformat() if row[5] else None,
            'staff': {
                's_rank': row[6],
                's_phone': row[7]
            },
            'product': {
                'p_name': row[8],
                'p_price': row[9],
                'p_image': row[10]
            }
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)