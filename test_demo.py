"""
Interactive Demo Script for AI Research Agent
Tests the full functionality with a real research query
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def test_health():
    """Test health endpoint"""
    print_header("1. HEALTH CHECK")
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Server Status: {data['status']}")
    print(f"✅ Version: {data['version']}")
    print(f"✅ Timestamp: {data['timestamp']}")
    return response.status_code == 200

def test_docs():
    """Test docs endpoint"""
    print_header("2. API DOCUMENTATION")
    response = requests.get(f"{BASE_URL}/docs")
    
    if response.status_code == 200:
        print(f"✅ Swagger UI accessible at: {BASE_URL}/docs")
        print(f"✅ Interactive API documentation ready")
        print(f"   👉 Open {BASE_URL}/docs in your browser to explore!")
        return True
    return False

def test_research_query():
    """Test actual research query"""
    print_header("3. RESEARCH QUERY TEST")
    
    query = "What are the key features of LangGraph for building AI agents?"
    
    print(f"📝 Query: {query}")
    print(f"⏳ Processing (this may take 15-20 seconds)...\n")
    
    payload = {
        "query": query,
        "max_results": 3
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/research",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ SUCCESS! (took {elapsed:.1f}s)\n")
            print(f"📊 Response Details:")
            print(f"   - Session ID: {data.get('session_id', 'N/A')}")
            print(f"   - Confidence: {data.get('confidence', 0)*100:.0f}%")
            print(f"   - Sources Found: {len(data.get('sources', []))}")
            
            print(f"\n📚 Sources:")
            for i, source in enumerate(data.get('sources', [])[:5], 1):
                print(f"   {i}. {source}")
            
            print(f"\n📄 Research Report:")
            print("-" * 70)
            report = data.get('response', 'No response')
            # Print first 500 characters
            print(report[:500])
            if len(report) > 500:
                print(f"\n   ... (showing first 500 of {len(report)} characters)")
                print(f"   Full response available in API response")
            print("-" * 70)
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏱️ Request timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_metrics():
    """Test metrics endpoint"""
    print_header("4. METRICS ENDPOINT")
    response = requests.get(f"{BASE_URL}/metrics")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Metrics endpoint working")
        print(f"   Status: {data.get('status', 'N/A')}")
        return True
    return False

def run_demo():
    """Run complete demo"""
    print("\n" + "🚀 " * 35)
    print("  AI RESEARCH AGENT - LOCAL DEMO")
    print("🚀 " * 35)
    
    print(f"\n⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Server: {BASE_URL}")
    
    tests = [
        ("Health Check", test_health),
        ("API Documentation", test_docs),
        ("Metrics Endpoint", test_metrics),
        ("Research Query (Live Demo)", test_research_query),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            time.sleep(1)  # Small delay between tests
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
            results.append((name, False))
    
    # Final summary
    print_header("DEMO SUMMARY")
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "🎉 " * 35)
        print("  ALL TESTS PASSED! YOUR AGENT IS WORKING PERFECTLY!")
        print("🎉 " * 35)
        print(f"\n✨ Next Steps:")
        print(f"   1. Explore the API docs: {BASE_URL}/docs")
        print(f"   2. Try more queries via the /research endpoint")
        print(f"   3. Deploy to cloud when ready!")
    else:
        print(f"\n⚠️ Some tests failed. Check the output above for details.")
    
    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    try:
        run_demo()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("\nMake sure the server is running:")
        print("  cd ai-research-agent")
        print("  venv\\Scripts\\activate")
        print("  uvicorn src.api.main:app --reload")
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
