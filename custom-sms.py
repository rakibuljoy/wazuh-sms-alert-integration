#!/usr/bin/env python3
import sys
import json
import requests
from datetime import datetime

# ১. Wazuh থেকে পাঠানো ডাটা পড়া
try:
    alert_file_path = sys.argv[1]
    
    with open(alert_file_path, 'r') as f:
        alert_json = json.loads(f.readline())

    # ২. আপনার অফিসের ডকুমেন্টেশন অনুযায়ী কনফিগারেশন (image_6a3c1f.jpg অনুযায়ী)
    sms_url = "https://api.rtcom.xyz/onetomany"
    
    # নিচের 'acode' এর জায়গায় আপনার পোর্টাল থেকে পাওয়া আসল কোডটি বসান
    payload = {
        "acode": "আপনার_ACODE_এখানে_দিন", # পোর্টাল থেকে পাওয়া Account Code
        "api_key": "57c3d28xxxxxxxxxxxxxxxxxxxxxxxx", 
        "senderid": "88096176xxxxx",   
        "type": "text",                
        "msg": "",                     # নিচে তৈরি করা হচ্ছে
        "contacts": "880178xxxxxxx",   
        "transactionType": "",        
        "contentID": ""                
    }

    # ৩. এলার্ট মেসেজ তৈরি করা
    alert_level = alert_json.get('rule', {}).get('level', '0')
    alert_desc = alert_json.get('rule', {}).get('description', 'No Description')
    payload["msg"] = f"Wazuh Alert! Lvl:{alert_level}, Desc:{alert_desc}"

    # ৪. JSON ফরম্যাটে ডাটা পাঠানো (ডকুমেন্টেশনের Request JSON বক্স অনুযায়ী)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(sms_url, json=payload, headers=headers, timeout=10)

    # ৫. ডিবাগিং এর জন্য লগ রাখা
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/tmp/sms_debug.log", "a") as f:
        f.write(f"[{now}] Status: {response.status_code} - Response: {response.text}\n")

except Exception as e:
    with open("/tmp/sms_error.log", "a") as f:
        f.write(f"Script Error: {str(e)}\n")
