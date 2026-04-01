import urllib.request, json, urllib.error, time

# Wake up Render
print("Waking up Render...")
try:
    req = urllib.request.Request('https://academia-ci0l.onrender.com/')
    urllib.request.urlopen(req, timeout=120)
except: pass
print("Awake!\n")

# Test creating a student profile
print("Testing student profile creation...")
start = time.time()
data = json.dumps({
    "name": "Test Student",
    "register_no": "999999999999",
    "roll_no": "99",
    "mobile_no": "9999999999",
    "gender": "Male",
    "email_personal": "test@test.com"
}).encode()

# Use user_id from a real user - try user_id=1
req = urllib.request.Request(
    'https://academia-ci0l.onrender.com/student/profile?user_id=1',
    data=data,
    headers={'Content-Type': 'application/json'}
)

try:
    resp = urllib.request.urlopen(req, timeout=120)
    elapsed = time.time() - start
    body = resp.read().decode()
    print(f"SUCCESS in {elapsed:.1f}s!")
    print(f"Response: {body[:500]}")
except urllib.error.HTTPError as e:
    elapsed = time.time() - start
    body = e.read().decode()
    print(f"FAILED in {elapsed:.1f}s (status {e.code})")
    print(f"Error: {body}")
except Exception as e:
    elapsed = time.time() - start
    print(f"ERROR after {elapsed:.1f}s: {e}")
