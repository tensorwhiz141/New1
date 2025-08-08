#!/usr/bin/env python3
"""
Test script for the HackRx webhook endpoint
Usage: python test_webhook.py <your-deployed-url>
"""

import requests
import json
import sys

def test_webhook(base_url):
    """Test the webhook endpoint with sample data"""
    
    # Remove trailing slash if present
    base_url = base_url.rstrip('/')
    
    webhook_url = f"{base_url}/api/v1/hackrx/run"
    health_url = f"{base_url}/api/v1/hackrx/health"
    
    print(f"🧪 Testing webhook endpoints for: {base_url}")
    print("=" * 50)
    
    # Test 1: Health check
    print("1️⃣ Testing health check endpoint...")
    try:
        response = requests.get(health_url, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print("   ✅ Health check passed!")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False
    
    print()
    
    # Test 2: Webhook with sample question
    print("2️⃣ Testing webhook endpoint...")
    test_data = {
        "question": "What are the main policies mentioned in the documents?"
    }
    
    try:
        response = requests.post(
            webhook_url, 
            json=test_data, 
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Question: {result.get('question', 'N/A')}")
            print(f"   Answer: {result.get('answer', 'N/A')[:100]}...")
            print("   ✅ Webhook test passed!")
            return True
        else:
            print(f"   ❌ Webhook failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Webhook test failed: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_webhook.py <your-deployed-url>")
        print("Example: python test_webhook.py https://your-app.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1]
    success = test_webhook(base_url)
    
    if success:
        webhook_url = f"{base_url.rstrip('/')}/api/v1/hackrx/run"
        print()
        print("🎉 All tests passed!")
        print(f"📝 Your webhook URL for submission: {webhook_url}")
        print()
        print("You can now submit this URL to the HackRx platform!")
    else:
        print()
        print("❌ Tests failed. Please check your deployment.")

if __name__ == "__main__":
    main()
