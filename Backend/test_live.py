import json
import urllib.request

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("Testing local FastAPI server on", BASE_URL)

    # 1. Health check
    with urllib.request.urlopen(f"{BASE_URL}/health") as response:
        health = json.loads(response.read())
        print(f"[PASSED] /health -> Status: {health['status']}, Platform: {health['platform']}")

    # 2. Login with seeded test account
    login_body = json.dumps({
        "email": "test@primecloud.io",
        "password": "password123"
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/login",
        data=login_body,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        login_data = json.loads(response.read())
        token = login_data["access_token"]
        print(f"[PASSED] /auth/login -> Logged in as: {login_data['user']['email']}")
        print(f"         Token: {token}")

    # 3. Authenticated /auth/me check
    req = urllib.request.Request(
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as response:
        me = json.loads(response.read())
        print(f"[PASSED] /auth/me -> Authenticated: {me['name']} (Role: {me['role']})")

    # 4. Signup a new user
    signup_body = json.dumps({
        "name": "Prime New User",
        "email": "newbie@primecloud.io",
        "password": "mypassword123"
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/signup",
        data=signup_body,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        new_user = json.loads(response.read())
        print(f"[PASSED] /auth/signup -> Registered: {new_user['email']} (ID: {new_user['id']})")

    # 5. Password reset
    reset_body = json.dumps({
        "email": "test@primecloud.io",
        "new_password": "brandnewpassword456"
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/reset-password",
        data=reset_body,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        reset_res = json.loads(response.read())
        print(f"[PASSED] /auth/reset-password -> {reset_res['message']}")

    # 6. Verify login with the new password
    login_body2 = json.dumps({
        "email": "test@primecloud.io",
        "password": "brandnewpassword456"
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/login",
        data=login_body2,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as response:
        login_data2 = json.loads(response.read())
        print(f"[PASSED] /auth/login (with new password) -> Token: {login_data2['access_token']}")

    # 7. Logout
    req = urllib.request.Request(
        f"{BASE_URL}/auth/logout",
        data=b"",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as response:
        logout_res = json.loads(response.read())
        print(f"[PASSED] /auth/logout -> {logout_res['message']}")

    print("\nAll endpoints tested and working 100% locally!")

if __name__ == "__main__":
    run_tests()
