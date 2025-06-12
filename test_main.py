from fastapi.testclient import TestClient
from main import app
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import app


client = TestClient(app)

def test_read_root():
    """루트 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello FastAPI!"}

def test_health_check():
    """헬스체크 엔드포인트 테스트"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_items():
    """모든 아이템 조회 테스트"""
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 2
    assert items[0]["name"] == "노트북"

def test_get_item():
    """특정 아이템 조회 테스트"""
    response = client.get("/items/1")
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    assert item["name"] == "노트북"

def test_get_nonexistent_item():
    """존재하지 않는 아이템 조회 테스트"""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_create_item():
    """아이템 생성 테스트"""
    new_item = {
        "name": "키보드",
        "price": 100000,
        "description": "기계식 키보드"
    }
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    created_item = response.json()
    assert created_item["name"] == "키보드"
    assert created_item["price"] == 100000
    assert "id" in created_item

def test_update_item():
    """아이템 수정 테스트"""
    update_data = {
        "name": "업데이트된 노트북",
        "price": 1500000,
        "description": "성능 업그레이드"
    }
    response = client.put("/items/1", json=update_data)
    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["name"] == "업데이트된 노트북"
    assert updated_item["price"] == 1500000

def test_delete_item():
    """아이템 삭제 테스트"""
    response = client.delete("/items/2")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted"
    
    # 삭제된 아이템 조회시 404 확인
    response = client.get("/items/2")
    assert response.status_code == 404

def test_invalid_json():
    """잘못된 JSON 데이터 테스트"""
    response = client.post("/items", json={"name": "test"})  # price 누락
    assert response.status_code == 422  # Validation Error

# 성능 테스트 예시
def test_concurrent_requests():
    """동시 요청 테스트"""
    import concurrent.futures
    
    def make_request():
        return client.get("/")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        responses = [f.result() for f in futures]
        
    assert all(r.status_code == 200 for r in responses)