#!/usr/bin/env python3
"""
Test actual PSX endpoints to understand their structure
"""

import asyncio
import httpx
import json

async def test_psx_endpoints():
    """Test the actual PSX endpoints"""
    base_url = "https://dps.psx.com.pk"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test market watch endpoint
        print("Testing market-watch endpoint...")
        try:
            response = await client.get(f"{base_url}/market-watch")
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                content = response.text
                print(f"Content length: {len(content)}")
                print(f"First 500 chars: {content[:500]}")
                
                try:
                    data = response.json()
                    print(f"JSON data type: {type(data)}")
                    if isinstance(data, list):
                        print(f"Array length: {len(data)}")
                        if data:
                            print(f"First item: {data[0]}")
                except json.JSONDecodeError:
                    print("Response is not valid JSON")
            else:
                print(f"Error response: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Test intraday endpoint
        print("Testing intraday endpoint...")
        try:
            response = await client.get(f"{base_url}/timeseries/int/HBL")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"Content length: {len(content)}")
                print(f"First 500 chars: {content[:500]}")
                
                try:
                    data = response.json()
                    print(f"JSON data type: {type(data)}")
                    if isinstance(data, list):
                        print(f"Array length: {len(data)}")
                        if data:
                            print(f"First item: {data[0]}")
                except json.JSONDecodeError:
                    print("Response is not valid JSON")
            else:
                print(f"Error response: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Test EOD endpoint
        print("Testing EOD endpoint...")
        try:
            response = await client.get(f"{base_url}/timeseries/eod/HBL")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"Content length: {len(content)}")
                print(f"First 500 chars: {content[:500]}")
                
                try:
                    data = response.json()
                    print(f"JSON data type: {type(data)}")
                    if isinstance(data, list):
                        print(f"Array length: {len(data)}")
                        if data:
                            print(f"First item: {data[0]}")
                except json.JSONDecodeError:
                    print("Response is not valid JSON")
            else:
                print(f"Error response: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_psx_endpoints())
