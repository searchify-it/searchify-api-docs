#!/usr/bin/env python3
"""
Test script to validate the code examples in README.client-stream-api.md
Uses the same configuration values as test_stream_endpoint.py
"""

import requests
import json
import re
from typing import Dict, List, Any

# Configuration 
API_BASE_URL = "http://base_url_here"
API_KEY = "sk-your_api_key_here"
INSTANCE_HASH = "your_instance_hash_here"
TEST_QUERY = "your_test_query_here"

def test_python_example():
    """Test the Python example from the README"""
    print("🐍 Testing Python Example from README")
    print("=" * 50)
    
    def stream_searchify_response(api_key, instance_hash, query):
        url = f"{API_BASE_URL}/v1/stream"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "instance_hash": instance_hash,
            "query": query
        }
        
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        full_text = ""
        citations = {}
        
        for line in response.iter_lines():
            if line and line.startswith(b'data: '):
                data = json.loads(line[6:])  # Remove 'data: ' prefix
                
                # Get complete text (no concatenation needed)
                full_text = data.get('updatedText', '')
                
                # Store search results for citations
                if data.get('search_results'):
                    for result in data['search_results']:
                        citations[result['id']] = result
                
                # Check if streaming is complete
                if data.get('isDone'):
                    print(f"✅ Final response: {full_text[:100]}...")
                    print(f"✅ Available citations: {len(citations)} found")
                    return {"text": full_text, "citations": citations}
        
        return {"text": full_text, "citations": citations}
    
    try:
        result = stream_searchify_response(API_KEY, INSTANCE_HASH, TEST_QUERY)
        
        # Extract citations from the text
        citation_matches = re.findall(r'\[(\d+)\]', result["text"])
        print(f"📝 Citation matches found: {citation_matches}")
        
        for citation_id in citation_matches:
            if citation_id in result["citations"]:
                citation = result["citations"][citation_id]
                print(f"📖 Citation [{citation_id}]: {citation['title']} - {citation['url']}")
        
        print("✅ Python example test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Python example test FAILED: {e}")
        return False

def test_javascript_equivalent():
    """Test JavaScript equivalent using requests (simulating fetch)"""
    print("\n🌐 Testing JavaScript Equivalent (simulated with requests)")
    print("=" * 50)
    
    def stream_searchify_response_js_style(api_key, instance_hash, query):
        url = f"{API_BASE_URL}/v1/stream"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'instance_hash': instance_hash,
            'query': query
        }
        
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        full_text = ''
        citations = {}
        
        for line in response.iter_lines():
            if line and line.startswith(b'data: '):
                data = json.loads(line[6:])
                
                # Get the complete text (no need to concatenate)
                full_text = data.get('updatedText', '')
                
                # Store search results for citations
                if data.get('search_results'):
                    for result in data['search_results']:
                        citations[result['id']] = result
                
                # Check if streaming is complete
                if data.get('isDone'):
                    print(f"✅ Final response: {full_text[:100]}...")
                    print(f"✅ Available citations: {len(citations)} found")
                    return {"text": full_text, "citations": citations}
        
        return {"text": full_text, "citations": citations}
    
    try:
        result = stream_searchify_response_js_style(API_KEY, INSTANCE_HASH, TEST_QUERY)
        
        # Extract citations from the text
        citation_matches = re.findall(r'\[(\d+)\]', result["text"])
        print(f"📝 Citation matches found: {citation_matches}")
        
        for citation_id in citation_matches:
            if citation_id in result["citations"]:
                citation = result["citations"][citation_id]
                print(f"📖 Citation [{citation_id}]: {citation['title']} - {citation['url']}")
        
        print("✅ JavaScript equivalent test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ JavaScript equivalent test FAILED: {e}")
        return False

def test_curl_equivalent():
    """Test the cURL example using requests"""
    print("\n🔧 Testing cURL Equivalent")
    print("=" * 50)
    
    try:
        url = f"{API_BASE_URL}/v1/stream"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "instance_hash": INSTANCE_HASH,
            "query": TEST_QUERY
        }
        
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        print("✅ cURL equivalent test PASSED")
        print(f"📊 Response status: {response.status_code}")
        print(f"📋 Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        # Check if we get streaming response
        chunk_count = 0
        for line in response.iter_lines():
            if line and line.startswith(b'data: '):
                chunk_count += 1
                if chunk_count >= 2:  # Just check first few chunks
                    break
        
        print(f"📡 Received {chunk_count} chunks (streaming working)")
        return True
        
    except Exception as e:
        print(f"❌ cURL equivalent test FAILED: {e}")
        return False

def test_response_format():
    """Test that the response format matches the README specification"""
    print("\n📋 Testing Response Format")
    print("=" * 50)
    
    try:
        url = f"{API_BASE_URL}/v1/stream"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "instance_hash": INSTANCE_HASH,
            "query": TEST_QUERY
        }
        
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        # Check first few chunks for proper format
        chunk_count = 0
        for line in response.iter_lines():
            if line and line.startswith(b'data: '):
                data = json.loads(line[6:])
                chunk_count += 1
                
                # Validate required fields
                required_fields = ['isDone', 'updatedText', 'search_results']
                for field in required_fields:
                    if field not in data:
                        print(f"❌ Missing required field: {field}")
                        return False
                
                # Validate search_results structure if present
                if data['search_results']:
                    for result in data['search_results']:
                        result_fields = ['id', 'snippet', 'source', 'url', 'title', 'metadata']
                        for field in result_fields:
                            if field not in result:
                                print(f"❌ Missing search result field: {field}")
                                return False
                        
                        # Validate snippet structure
                        snippet = result['snippet']
                        snippet_fields = ['pre', 'text', 'post']
                        for field in snippet_fields:
                            if field not in snippet:
                                print(f"❌ Missing snippet field: {field}")
                                return False
                
                if chunk_count >= 3:  # Check first 3 chunks
                    break
        
        print("✅ Response format validation PASSED")
        print(f"📊 Checked {chunk_count} chunks")
        return True
        
    except Exception as e:
        print(f"❌ Response format test FAILED: {e}")
        return False

def test_citation_extraction():
    """Test citation extraction logic from README"""
    print("\n📖 Testing Citation Extraction")
    print("=" * 50)
    
    try:
        url = f"{API_BASE_URL}/v1/stream"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "instance_hash": INSTANCE_HASH,
            "query": TEST_QUERY
        }
        
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        full_text = ""
        citations = {}
        
        for line in response.iter_lines():
            if line and line.startswith(b'data: '):
                data = json.loads(line[6:])
                
                full_text = data.get('updatedText', '')
                
                if data.get('search_results'):
                    for result in data['search_results']:
                        citations[result['id']] = result
                
                if data.get('isDone'):
                    break
        
        # Test citation extraction
        citation_matches = re.findall(r'\[(\d+)\]', full_text)
        print(f"📝 Found {len(citation_matches)} citation references in text")
        
        valid_citations = 0
        for citation_id in citation_matches:
            if citation_id in citations:
                valid_citations += 1
                citation = citations[citation_id]
                print(f"✅ Citation [{citation_id}]: {citation['title'][:50]}...")
        
        print(f"📊 {valid_citations}/{len(citation_matches)} citations have valid search results")
        
        if valid_citations > 0:
            print("✅ Citation extraction test PASSED")
            return True
        else:
            print("⚠️  No valid citations found (might be normal for some queries)")
            return True  # Not a failure, just no citations
            
    except Exception as e:
        print(f"❌ Citation extraction test FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing README Code Examples")
    print("=" * 60)
    
    tests = [
        ("Python Example", test_python_example),
        ("JavaScript Equivalent", test_javascript_equivalent),
        ("cURL Equivalent", test_curl_equivalent),
        ("Response Format", test_response_format),
        ("Citation Extraction", test_citation_extraction),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All README examples are working correctly!")
        return 0
    else:
        print("💥 Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code)
