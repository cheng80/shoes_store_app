"""
PurchaseItem 복합 쿼리 API
- PurchaseItem 중심의 JOIN 쿼리들
- PurchaseItem + User + Product + Branch + 모든 카테고리
- b_tnum으로 주문 그룹화 지원

개별 실행: python purchase_item_join.py
"""

from fastapi import FastAPI, Query
from typing import Optional
from database.connection import connect_db

app = FastAPI(title="PurchaseItem JOIN API")
ipAddress = "127.0.0.1"
port = 8000


# ============================================
# PurchaseItem + User + Product + Branch (4테이블 JOIN)
# ============================================
@app.get("/purchase_items/{purchase_item_seq}/with_details")
async def get_purchase_item_with_details(purchase_item_seq: int):
    """
    특정 PurchaseItem + User + Product + Branch 정보
    JOIN: PurchaseItem + User + Product + Branch
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pi.b_seq,
            pi.b_price,
            pi.b_quantity,
            pi.b_date,
            pi.b_tnum,
            u.u_seq,
            u.u_id,
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
        FROM purchase_item pi
        JOIN user u ON pi.u_seq = u.u_seq
        JOIN product p ON pi.p_seq = p.p_seq
        JOIN branch br ON pi.br_seq = br.br_seq
        WHERE pi.b_seq = %s
        """
        curs.execute(sql, (purchase_item_seq,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "PurchaseItem not found"}
        
        result = {
            'b_seq': row[0],
            'b_price': row[1],
            'b_quantity': row[2],
            'b_date': row[3].isoformat() if row[3] else None,
            'b_tnum': row[4],
            'user': {
                'u_seq': row[5],
                'u_id': row[6],
                'u_name': row[7],
                'u_phone': row[8]
            },
            'product': {
                'p_seq': row[9],
                'p_name': row[10],
                'p_price': row[11],
                'p_image': row[12]
            },
            'branch': {
                'br_seq': row[13],
                'br_name': row[14],
                'br_address': row[15],
                'br_phone': row[16]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# PurchaseItem 전체 상세 (Product의 모든 카테고리 포함)
# ============================================
@app.get("/purchase_items/{purchase_item_seq}/full_detail")
async def get_purchase_item_full_detail(purchase_item_seq: int):
    """
    특정 PurchaseItem의 전체 상세 정보
    JOIN: PurchaseItem + User + Product + Branch + 모든 카테고리 + Maker (9테이블)
    용도: 주문 상세 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pi.b_seq,
            pi.b_price,
            pi.b_quantity,
            pi.b_date,
            pi.b_tnum,
            u.u_seq,
            u.u_id,
            u.u_name,
            u.u_phone,
            p.p_seq,
            p.p_name,
            p.p_price,
            p.p_stock,
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
        FROM purchase_item pi
        JOIN user u ON pi.u_seq = u.u_seq
        JOIN product p ON pi.p_seq = p.p_seq
        JOIN kind_category kc ON p.kc_seq = kc.kc_seq
        JOIN color_category cc ON p.cc_seq = cc.cc_seq
        JOIN size_category sc ON p.sc_seq = sc.sc_seq
        JOIN gender_category gc ON p.gc_seq = gc.gc_seq
        JOIN maker m ON p.m_seq = m.m_seq
        JOIN branch br ON pi.br_seq = br.br_seq
        WHERE pi.b_seq = %s
        """
        curs.execute(sql, (purchase_item_seq,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "PurchaseItem not found"}
        
        result = {
            'b_seq': row[0],
            'b_price': row[1],
            'b_quantity': row[2],
            'b_date': row[3].isoformat() if row[3] else None,
            'b_tnum': row[4],
            'user': {
                'u_seq': row[5],
                'u_id': row[6],
                'u_name': row[7],
                'u_phone': row[8]
            },
            'product': {
                'p_seq': row[9],
                'p_name': row[10],
                'p_price': row[11],
                'p_stock': row[12],
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
# 고객별 PurchaseItem 목록 + 상세 정보
# ============================================
@app.get("/purchase_items/by_user/{user_seq}/with_details")
async def get_purchase_items_by_user_with_details(user_seq: int):
    """
    특정 고객의 모든 PurchaseItem + Product + Branch 정보
    JOIN: PurchaseItem + User + Product + Branch
    용도: 고객 주문 내역 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pi.b_seq,
            pi.b_price,
            pi.b_quantity,
            pi.b_date,
            pi.b_tnum,
            p.p_seq,
            p.p_name,
            p.p_price,
            p.p_image,
            br.br_name
        FROM purchase_item pi
        JOIN product p ON pi.p_seq = p.p_seq
        JOIN branch br ON pi.br_seq = br.br_seq
        WHERE pi.u_seq = %s
        ORDER BY pi.b_date DESC, pi.b_seq DESC
        """
        curs.execute(sql, (user_seq,))
        rows = curs.fetchall()
        
        result = [{
            'b_seq': row[0],
            'b_price': row[1],
            'b_quantity': row[2],
            'b_date': row[3].isoformat() if row[3] else None,
            'b_tnum': row[4],
            'product': {
                'p_seq': row[5],
                'p_name': row[6],
                'p_price': row[7],
                'p_image': row[8]
            },
            'branch_name': row[9]
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 주문번호(b_tnum)로 그룹화된 PurchaseItem 목록
# ============================================
@app.get("/purchase_items/by_tnum/{b_tnum}/with_details")
async def get_purchase_items_by_tnum_with_details(b_tnum: str):
    """
    특정 주문번호(b_tnum)의 모든 PurchaseItem + 상세 정보
    JOIN: PurchaseItem + User + Product + Branch + 모든 카테고리
    용도: 주문 상세 화면 (여러 항목을 하나의 주문으로 표시)
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
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
            br.br_name,
            br.br_address
        FROM purchase_item pi
        JOIN user u ON pi.u_seq = u.u_seq
        JOIN product p ON pi.p_seq = p.p_seq
        JOIN kind_category kc ON p.kc_seq = kc.kc_seq
        JOIN color_category cc ON p.cc_seq = cc.cc_seq
        JOIN size_category sc ON p.sc_seq = sc.sc_seq
        JOIN gender_category gc ON p.gc_seq = gc.gc_seq
        JOIN maker m ON p.m_seq = m.m_seq
        JOIN branch br ON pi.br_seq = br.br_seq
        WHERE pi.b_tnum = %s
        ORDER BY pi.b_seq
        """
        curs.execute(sql, (b_tnum,))
        rows = curs.fetchall()
        
        if not rows:
            return {"result": "Error", "message": "No purchase items found for this transaction number"}
        
        # 첫 번째 행에서 공통 정보 추출
        first_row = rows[0]
        order_info = {
            'b_tnum': first_row[4],
            'b_date': first_row[3].isoformat() if first_row[3] else None,
            'user': {
                'u_seq': first_row[5],
                'u_name': first_row[6],
                'u_phone': first_row[7]
            },
            'branch_name': first_row[18],
            'branch_address': first_row[19],
            'items': []
        }
        
        # 각 항목 추가
        total_amount = 0
        for row in rows:
            item = {
                'b_seq': row[0],
                'b_price': row[1],
                'b_quantity': row[2],
                'product': {
                    'p_seq': row[8],
                    'p_name': row[9],
                    'p_price': row[10],
                    'p_image': row[11],
                    'kind_name': row[12],
                    'color_name': row[13],
                    'size_name': row[14],
                    'gender_name': row[15],
                    'maker_name': row[16]
                }
            }
            order_info['items'].append(item)
            total_amount += row[1] * row[2]
        
        order_info['total_amount'] = total_amount
        order_info['item_count'] = len(rows)
        
        return {"result": order_info}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객별 주문 목록 (b_tnum 그룹화)
# ============================================
@app.get("/purchase_items/by_user/{user_seq}/orders")
async def get_user_orders(user_seq: int):
    """
    특정 고객의 주문 목록 (b_tnum으로 그룹화)
    JOIN: PurchaseItem + User + Product + Branch
    용도: 고객 주문 목록 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 고유한 b_tnum 목록 조회
        sql_tnums = """
        SELECT DISTINCT b_tnum, MIN(b_date) as order_date
        FROM purchase_item
        WHERE u_seq = %s AND b_tnum IS NOT NULL
        GROUP BY b_tnum
        ORDER BY order_date DESC
        """
        curs.execute(sql_tnums, (user_seq,))
        tnum_rows = curs.fetchall()
        
        result = []
        for tnum_row in tnum_rows:
            b_tnum = tnum_row[0]
            order_date = tnum_row[1]
            
            # 각 주문의 항목들 조회
            sql_items = """
            SELECT 
                pi.b_seq,
                pi.b_price,
                pi.b_quantity,
                p.p_name,
                br.br_name
            FROM purchase_item pi
            JOIN product p ON pi.p_seq = p.p_seq
            JOIN branch br ON pi.br_seq = br.br_seq
            WHERE pi.b_tnum = %s
            ORDER BY pi.b_seq
            """
            curs.execute(sql_items, (b_tnum,))
            item_rows = curs.fetchall()
            
            total_amount = sum(row[1] * row[2] for row in item_rows)
            
            order = {
                'b_tnum': b_tnum,
                'order_date': order_date.isoformat() if order_date else None,
                'item_count': len(item_rows),
                'total_amount': total_amount,
                'items': [{
                    'b_seq': row[0],
                    'b_price': row[1],
                    'b_quantity': row[2],
                    'product_name': row[3],
                    'branch_name': row[4]
                } for row in item_rows]
            }
            result.append(order)
        
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
    print(f"🚀 PurchaseItem JOIN API 서버 시작")
    print(f"   서버 주소: http://{ipAddress}:{port}")
    print(f"   Swagger UI: http://{ipAddress}:{port}/docs")
    print(f"")
    print(f"   엔드포인트:")
    print(f"   - GET /purchase_items/{{purchase_item_seq}}/with_details")
    print(f"   - GET /purchase_items/{{purchase_item_seq}}/full_detail")
    print(f"   - GET /purchase_items/by_user/{{user_seq}}/with_details")
    print(f"   - GET /purchase_items/by_tnum/{{b_tnum}}/with_details")
    print(f"   - GET /purchase_items/by_user/{{user_seq}}/orders")
    uvicorn.run(app, host=ipAddress, port=port)

