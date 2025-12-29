"""
Pickup 복합 쿼리 API
- Pickup 중심의 JOIN 쿼리들
- Pickup + PurchaseItem + User + Product + Branch

개별 실행: python pickup_join.py
"""

from fastapi import FastAPI, Query
from typing import Optional
from database.connection import connect_db

app = FastAPI(title="Pickup JOIN API")
ipAddress = "127.0.0.1"
port = 8000


# ============================================
# Pickup + PurchaseItem + User + Product + Branch
# ============================================
@app.get("/pickups/{pickup_seq}/with_details")
async def get_pickup_with_details(pickup_seq: int):
    """
    특정 Pickup + PurchaseItem + User + Product + Branch 정보
    JOIN: Pickup + PurchaseItem + User + Product + Branch (5테이블)
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pic.pic_seq,
            pic.pic_date,
            pi.b_seq,
            pi.b_price,
            pi.b_quantity,
            pi.b_date,
            pi.b_tnum,
            u.u_seq,
            u.u_name,
            u.u_phone,
            p.p_seq,
            p.p_name,
            p.p_price,
            p.p_image,
            br.br_seq,
            br.br_name,
            br.br_address,
            br.br_phone
        FROM pickup pic
        JOIN purchase_item pi ON pic.b_seq = pi.b_seq
        JOIN user u ON pi.u_seq = u.u_seq
        JOIN product p ON pi.p_seq = p.p_seq
        JOIN branch br ON pi.br_seq = br.br_seq
        WHERE pic.pic_seq = %s
        """
        curs.execute(sql, (pickup_seq,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Pickup not found"}
        
        result = {
            'pic_seq': row[0],
            'pic_date': row[1].isoformat() if row[1] else None,
            'purchase_item': {
                'b_seq': row[2],
                'b_price': row[3],
                'b_quantity': row[4],
                'b_date': row[5].isoformat() if row[5] else None,
                'b_tnum': row[6]
            },
            'user': {
                'u_seq': row[7],
                'u_name': row[8],
                'u_phone': row[9]
            },
            'product': {
                'p_seq': row[10],
                'p_name': row[11],
                'p_price': row[12],
                'p_image': row[13]
            },
            'branch': {
                'br_seq': row[14],
                'br_name': row[15],
                'br_address': row[16],
                'br_phone': row[17]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# Pickup 전체 상세 (Product의 모든 카테고리 포함)
# ============================================
@app.get("/pickups/{pickup_seq}/full_detail")
async def get_pickup_full_detail(pickup_seq: int):
    """
    특정 Pickup의 전체 상세 정보
    JOIN: Pickup + PurchaseItem + User + Product + Branch + 모든 카테고리 + Maker (10테이블)
    용도: 수령 상세 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pic.pic_seq,
            pic.pic_date,
            pi.b_seq,
            pi.b_price,
            pi.b_quantity,
            pi.b_date,
            pi.b_tnum,
            u.u_seq,
            u.u_name,
            u.u_phone,
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
            br.br_address,
            br.br_phone
        FROM pickup pic
        JOIN purchase_item pi ON pic.b_seq = pi.b_seq
        JOIN user u ON pi.u_seq = u.u_seq
        JOIN product p ON pi.p_seq = p.p_seq
        JOIN kind_category kc ON p.kc_seq = kc.kc_seq
        JOIN color_category cc ON p.cc_seq = cc.cc_seq
        JOIN size_category sc ON p.sc_seq = sc.sc_seq
        JOIN gender_category gc ON p.gc_seq = gc.gc_seq
        JOIN maker m ON p.m_seq = m.m_seq
        JOIN branch br ON pi.br_seq = br.br_seq
        WHERE pic.pic_seq = %s
        """
        curs.execute(sql, (pickup_seq,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Pickup not found"}
        
        result = {
            'pic_seq': row[0],
            'pic_date': row[1].isoformat() if row[1] else None,
            'purchase_item': {
                'b_seq': row[2],
                'b_price': row[3],
                'b_quantity': row[4],
                'b_date': row[5].isoformat() if row[5] else None,
                'b_tnum': row[6]
            },
            'user': {
                'u_seq': row[7],
                'u_name': row[8],
                'u_phone': row[9]
            },
            'product': {
                'p_seq': row[10],
                'p_name': row[11],
                'p_price': row[12],
                'p_image': row[13],
                'kind_name': row[14],
                'color_name': row[15],
                'size_name': row[16],
                'gender_name': row[17],
                'maker_name': row[18]
            },
            'branch': {
                'br_seq': row[19],
                'br_name': row[20],
                'br_address': row[21],
                'br_phone': row[22]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객별 Pickup 목록
# ============================================
@app.get("/pickups/by_user/{user_seq}/with_details")
async def get_pickups_by_user_with_details(user_seq: int):
    """
    특정 고객의 모든 Pickup + 상세 정보
    JOIN: Pickup + PurchaseItem + User + Product + Branch
    용도: 고객 수령 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pic.pic_seq,
            pic.pic_date,
            pi.b_seq,
            pi.b_price,
            pi.b_quantity,
            pi.b_date,
            p.p_name,
            p.p_image,
            br.br_name
        FROM pickup pic
        JOIN purchase_item pi ON pic.b_seq = pi.b_seq
        JOIN product p ON pi.p_seq = p.p_seq
        JOIN branch br ON pi.br_seq = br.br_seq
        WHERE pi.u_seq = %s
        ORDER BY pic.pic_date DESC, pic.pic_seq DESC
        """
        curs.execute(sql, (user_seq,))
        rows = curs.fetchall()
        
        result = [{
            'pic_seq': row[0],
            'pic_date': row[1].isoformat() if row[1] else None,
            'purchase_item': {
                'b_seq': row[2],
                'b_price': row[3],
                'b_quantity': row[4],
                'b_date': row[5].isoformat() if row[5] else None
            },
            'product': {
                'p_name': row[6],
                'p_image': row[7]
            },
            'branch_name': row[8]
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 지점별 Pickup 목록
# ============================================
@app.get("/pickups/by_branch/{branch_seq}/with_details")
async def get_pickups_by_branch_with_details(branch_seq: int):
    """
    특정 지점의 모든 Pickup + 상세 정보
    JOIN: Pickup + PurchaseItem + User + Product + Branch
    용도: 지점별 수령 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pic.pic_seq,
            pic.pic_date,
            pi.b_seq,
            pi.b_price,
            pi.b_quantity,
            u.u_name,
            u.u_phone,
            p.p_name,
            p.p_image
        FROM pickup pic
        JOIN purchase_item pi ON pic.b_seq = pi.b_seq
        JOIN user u ON pi.u_seq = u.u_seq
        JOIN product p ON pi.p_seq = p.p_seq
        WHERE pi.br_seq = %s
        ORDER BY pic.pic_date DESC, pic.pic_seq DESC
        """
        curs.execute(sql, (branch_seq,))
        rows = curs.fetchall()
        
        result = [{
            'pic_seq': row[0],
            'pic_date': row[1].isoformat() if row[1] else None,
            'purchase_item': {
                'b_seq': row[2],
                'b_price': row[3],
                'b_quantity': row[4]
            },
            'user': {
                'u_name': row[5],
                'u_phone': row[6]
            },
            'product': {
                'p_name': row[7],
                'p_image': row[8]
            }
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# ============================================
if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Pickup JOIN API 서버 시작")
    print(f"   서버 주소: http://{ipAddress}:{port}")
    print(f"   Swagger UI: http://{ipAddress}:{port}/docs")
    print(f"")
    print(f"   엔드포인트:")
    print(f"   - GET /pickups/{{pickup_seq}}/with_details")
    print(f"   - GET /pickups/{{pickup_seq}}/full_detail")
    print(f"   - GET /pickups/by_user/{{user_seq}}/with_details")
    print(f"   - GET /pickups/by_branch/{{branch_seq}}/with_details")
    uvicorn.run(app, host=ipAddress, port=port)

