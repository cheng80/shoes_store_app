"""
api/ 폴더의 라우터 파일을 루트 디렉토리의 단독 실행 파일로 동기화
"""

import os
import shutil
import re

def sync_file(api_file_path, root_file_path):
    """api/ 폴더의 파일을 루트 디렉토리로 동기화 (FastAPI 앱으로 변환)"""
    with open(api_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # APIRouter → FastAPI 앱으로 변환
    content = content.replace('from fastapi import APIRouter', 'from fastapi import FastAPI')
    content = content.replace('from app_new_form.database.connection import connect_db', 
                             'from database.connection import connect_db')
    content = content.replace('router = APIRouter()', 
                             'app = FastAPI()\nipAddress = "127.0.0.1"')
    content = content.replace('@router.', '@app.')
    
    # 엔드포인트 경로 조정 (라우터는 빈 문자열, 단독 실행은 /select_xxx 형식)
    # 이 부분은 파일별로 다를 수 있으므로 수동 확인 필요
    
    # main 블록 추가
    if 'if __name__ == "__main__":' not in content:
        content += '\n\n# ============================================\n'
        content += 'if __name__ == "__main__":\n'
        content += '    import uvicorn\n'
        content += '    uvicorn.run(app, host=ipAddress, port=8000)\n'
    
    with open(root_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {os.path.basename(root_file_path)} 동기화 완료")

def main():
    api_dir = 'api'
    root_dir = '.'
    
    # 동기화할 파일 목록
    files_to_sync = [
        'staff.py',
        'pickup.py',
        # 나머지 파일들도 필요시 추가
    ]
    
    for filename in files_to_sync:
        api_path = os.path.join(api_dir, filename)
        root_path = os.path.join(root_dir, filename)
        
        if os.path.exists(api_path):
            sync_file(api_path, root_path)
        else:
            print(f"⚠️  {api_path} 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()

