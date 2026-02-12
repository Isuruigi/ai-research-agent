"""
Test script to verify the AI Research Agent works locally
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_research_simple():
    """Test simple research query"""
    print("\n🔍 Testing /research endpoint with simple query...")
    
    payload = {
        "query": "What is artificial intelligence?",
        "max_results": 3
    }
    
    print(f"Sending query: {payload['query']}")
    start = time.time()
    
    response = requests.post(
        f"{BASE_URL}/research",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    elapsed = time.time() - start
    
    print(f"Status: {response.status_code}")
    print(f"Time taken: {elapsed:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Query: {data.get('query')}")
        print(f"Report length: {len(data.get('report', ''))} characters")
        print(f"Sources found: {len(data.get('sources', []))}")
        print(f"\nFirst 200 chars of report:")
        print(data.get('report', '')[:200] + "...")
        return True
    else:
        print(f"❌ FAILED: {response.text}")
        return False

def test_docs():
    """Test if docs are accessible"""
    print("\n🔍 Testing /docs endpoint...")
    response = requests.get(f"{BASE_URL}/docs")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Swagger docs are accessible!")
        return True
    return False

def test_metrics():
    """Test metrics endpoint"""
    print("\n🔍 Testing /metrics endpoint...")
    response = requests.get(f"{BASE_URL}/metrics")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        lines = response.text.split('\n')
        print(f"✅ Metrics available! ({len(lines)} metrics)")
        return True
    return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 AI Research Agent - Local Testing")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("API Documentation", test_docs),
        ("Prometheus Metrics", test_metrics),
        ("Research Query", test_research_simple),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your agent is working perfectly!")
        print(f"\n👉 Visit http://localhost:8000/docs to try it interactively")
    else:
        print("\n⚠️ Some tests failed. Check the output above.")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("Make sure the server is running:")
        print("  cd ai-research-agent")
        print("  venv\\Scripts\\activate")
        print("  uvicorn src.api.main:app --reload")
