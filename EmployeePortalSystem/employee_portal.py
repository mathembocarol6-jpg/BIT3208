import sqlite3
import json
import uuid
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_NAME = "employee_portal.db"
ACTIVE_SESSIONS = {}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Employee'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            username TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

init_db()

HTML_INTERFACE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Employee Portal</title>
    <style>
        body { font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; background-color: #f8fafc; color: #1e293b; }
        .container { max-width: 95%; width: 1000px; margin: 40px auto; box-sizing: border-box; }
        .auth-card { max-width: 400px; margin: 100px auto; background: white; padding: 35px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); text-align: center; }
        .dashboard { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); display: none; }
        h1, h2, h3 { color: #0f172a; margin-top: 0; }
        .form-group { margin-bottom: 16px; text-align: left; }
        label { display: block; margin-bottom: 6px; font-weight: 600; font-size: 13px; color: #475569; }
        input, select { width: 100%; padding: 11px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; font-size: 14px; transition: all 0.2s; }
        input:focus, select:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
        button { background-color: #2563eb; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: 600; width: 100%; font-size: 14px; margin-top: 10px; transition: background 0.15s; }
        button:hover { background-color: #1d4ed8; }
        .secondary-btn { background-color: #64748b; margin-top: 12px; }
        .secondary-btn:hover { background-color: #475569; }
        .header-bar { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 20px; margin-bottom: 30px; gap: 15px; flex-wrap: wrap; }
        .portal-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 30px; }
        .panel { background: #f8fafc; border: 1px solid #e2e8f0; padding: 25px; border-radius: 8px; }
        .alert { padding: 12px 16px; border-radius: 6px; margin-bottom: 20px; font-size: 14px; display: none; font-weight: 500; text-align: left; }
        .alert-success { background-color: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
        .alert-error { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
        .profile-badge { background: white; border: 1px solid #cbd5e1; padding: 15px; border-radius: 6px; margin-bottom: 12px; }
        .profile-badge p { margin: 6px 0; font-size: 14px; }
        @media (max-width: 768px) {
            .portal-grid { grid-template-columns: 1fr; }
            .header-bar { flex-direction: column; text-align: center; }
        }
    </style>
</head>
<body>

    <div class="container">
        <div id="authPanel" class="auth-card">
            <h2 id="authTitle">🔒 Corporate Gateway</h2>
            <div class="alert alert-success" id="authSuccess"></div>
            <div class="alert alert-error" id="authError"></div>
            
            <div class="form-group">
                <label>System Username</label>
                <input type="text" id="authUsername" autocomplete="off">
            </div>
            <div class="form-group">
                <label>Security Password</label>
                <input type="password" id="authPassword">
            </div>
            
            <div id="registrationFields" style="display: none;">
                <div class="form-group"><label>Full Name</label><input type="text" id="regName"></div>
                <div class="form-group"><label>Corporate Email</label><input type="email" id="regEmail"></div>
                <div class="form-group"><label>Department</label><input type="text" id="regDept"></div>
                <div class="form-group"><label>Job Title / Position</label><input type="text" id="regPosition"></div>
            </div>
            
            <button id="authMainBtn" onclick="handleAuth()">Authenticate Log In</button>
            <button class="secondary-btn" id="authToggleBtn" onclick="toggleAuthMode()">Register New Employee</button>
        </div>

        <div id="dashboardPanel" class="dashboard">
            <div class="header-bar">
                <div>
                    <h1>💼 Employee Headquarters</h1>
                    <span id="userGreeting" style="font-weight: 600; color: #2563eb;"></span>
                </div>
                <button onclick="logout()" class="secondary-btn" style="width: auto; padding: 10px 20px; margin: 0;">Secure Logout</button>
            </div>

            <div class="alert alert-success" id="dashSuccess"></div>
            <div class="alert alert-error" id="dashError"></div>

            <div class="portal-grid">
                <div class="panel">
                    <h3>My Profile Matrix</h3>
                    <p style="font-size:13px; color:#64748b; margin-top:-10px;">Keep your centralized enterprise resource profile metrics updated.</p>
                    <div class="form-group"><label>Full Name</label><input type="text" id="dashName"></div>
                    <div class="form-group"><label>Corporate Email</label><input type="email" id="dashEmail"></div>
                    <div class="form-group"><label>Department Area</label><input type="text" id="dashDept"></div>
                    <div class="form-group"><label>Current Position</label><input type="text" id="dashPosition"></div>
                    <button onclick="saveProfileChanges()">Commit Sync Changes</button>
                </div>

                <div class="panel">
                    <h3>Verified Active Record View</h3>
                    <div id="profileDisplayContainer" style="margin-top: 15px;"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isLoginMode = true;

        function showAlert(elemId, msg, isSuccess) {
            const el = document.getElementById(elemId);
            el.innerText = msg;
            el.className = isSuccess ? "alert alert-success" : "alert alert-error";
            el.style.display = "block";
            setTimeout(() => { el.style.display = "none"; }, 4000);
        }

        function toggleAuthMode() {
            isLoginMode = !isLoginMode;
            document.getElementById("authTitle").innerText = isLoginMode ? "🔒 Corporate Gateway" : "📝 Register Account Record";
            document.getElementById("authMainBtn").innerText = isLoginMode ? "Authenticate Log In" : "Register Worker Credentials";
            document.getElementById("authToggleBtn").innerText = isLoginMode ? "Register New Employee" : "Back to Security Sign In";
            document.getElementById("registrationFields").style.display = isLoginMode ? "none" : "block";
        }

        window.onload = async function() {
            const res = await fetch("/api/session-check");
            if (res.ok) {
                const data = await res.json();
                loadProtectedDashboard(data.username);
            }
        }

        async function handleAuth() {
            const username = document.getElementById("authUsername").value.trim();
            const password = document.getElementById("authPassword").value.trim();

            if (!username || !password) {
                showAlert("authError", "Validation Error: Complete key identity credentials fields.", false);
                return;
            }

            if (isLoginMode) {
                const res = await fetch("/api/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });
                const data = await res.json();
                if (res.ok) {
                    loadProtectedDashboard(username);
                } else {
                    showAlert("authError", data.error, false);
                }
            } else {
                const full_name = document.getElementById("regName").value.trim();
                const email = document.getElementById("regEmail").value.trim();
                const department = document.getElementById("regDept").value.trim();
                const position = document.getElementById("regPosition").value.trim();

                if (!full_name || !email || !department || !position) {
                    showAlert("authError", "Validation Error: All profile telemetry blocks are mandatory.", false);
                    return;
                }
                if (!/^[\w\.-]+@[\w\.-]+\.\w+$/.test(email)) {
                    showAlert("authError", "Validation Error: Invalid format constraint parsed for Email address.", false);
                    return;
                }

                const res = await fetch("/api/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password, full_name, email, department, position })
                });
                const data = await res.json();
                if (res.ok) {
                    showAlert("authSuccess", "Account established! Sign in below using authenticated vectors.", true);
                    toggleAuthMode();
                } else {
                    showAlert("authError", data.error, false);
                }
            }
        }

        function loadProtectedDashboard(user) {
            document.getElementById("userGreeting").innerText = "Operator Account Identity: " + user;
            document.getElementById("authPanel").style.display = "none";
            document.getElementById("dashboardPanel").style.display = "block";
            fetchEmployeeProfileData();
        }

        async function fetchEmployeeProfileData() {
            const res = await fetch("/api/protected/profile");
            if (!res.ok) {
                logout();
                return;
            }
            const profile = await res.json();
            if (profile && profile.full_name) {
                document.getElementById("dashName").value = profile.full_name;
                document.getElementById("dashEmail").value = profile.email;
                document.getElementById("dashDept").value = profile.department;
                document.getElementById("dashPosition").value = profile.position;

                document.getElementById("profileDisplayContainer").innerHTML = `
                    <div class="profile-badge">
                        <p><strong>Legal Identity Name:</strong> ${profile.full_name}</p>
                        <p><strong>Corporate Core Email:</strong> ${profile.email}</p>
                        <p><strong>Department Matrix Assignment:</strong> ${profile.department}</p>
                        <p><strong>Assigned Strategic Title:</strong> ${profile.position}</p>
                    </div>
                `;
            } else {
                document.getElementById("profileDisplayContainer").innerHTML = `<p style="color:#64748b;">Profile data stream is currently empty.</p>`;
            }
        }

        async function saveProfileChanges() {
            const full_name = document.getElementById("dashName").value.trim();
            const email = document.getElementById("dashEmail").value.trim();
            const department = document.getElementById("dashDept").value.trim();
            const position = document.getElementById("dashPosition").value.trim();

            if (!full_name || !email || !department || !position) {
                showAlert("dashError", "Validation Check Failed: Profile synchronization points cannot be blank.", false);
                return;
            }

            const res = await fetch("/api/protected/profile", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ full_name, email, department, position })
            });

            if (res.ok) {
                showAlert("dashSuccess", "Enterprise resources synced securely down to DB storage file.", true);
                fetchEmployeeProfileData();
            } else {
                const data = await res.json();
                showAlert("dashError", data.error, false);
            }
        }

        async function logout() {
            await fetch("/api/logout", { method: "POST" });
            document.getElementById("authUsername").value = "";
            document.getElementById("authPassword").value = "";
            document.getElementById("dashboardPanel").style.display = "none";
            document.getElementById("authPanel").style.display = "block";
        }
    </script>
</body>
</html>
"""

class PortalServerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def get_session_user(self):
        cookie_header = self.headers.get('Cookie', '')
        if "Session-ID=" in cookie_header:
            try:
                session_id = cookie_header.split("Session-ID=")[1].split(";")[0].strip()
                return ACTIVE_SESSIONS.get(session_id)
            except Exception:
                return None
        return None

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_INTERFACE.encode("utf-8"))
            return
        elif self.path == "/api/session-check":
            user = self.get_session_user()
            if user:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"username": user}).encode("utf-8"))
            else:
                self.send_response(401)
                self.end_headers()
            return
        elif self.path == "/api/protected/profile":
            user = self.get_session_user()
            if not user:
                self.send_response(403)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Access Revoked: Session validation breakdown."}).encode("utf-8"))
                return
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT full_name, email, department, position FROM profiles WHERE username = ?", (user,))
            row = cursor.fetchone()
            conn.close()
            
            profile_data = {}
            if row:
                profile_data = {"full_name": row[0], "email": row[1], "department": row[2], "position": row[3]}
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(profile_data).encode("utf-8"))
            return
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload = json.loads(self.rfile.read(content_length).decode('utf-8'))

        if self.path == "/api/register":
            username = payload.get("username", "").strip()
            password = payload.get("password", "").strip()
            full_name = payload.get("full_name", "").strip()
            email = payload.get("email", "").strip()
            department = payload.get("department", "").strip()
            position = payload.get("position", "").strip()

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                cursor.execute("INSERT INTO profiles (username, full_name, email, department, position) VALUES (?, ?, ?, ?, ?)",
                               (username, full_name, email, department, position))
                conn.commit()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            except sqlite3.IntegrityError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Unique constraint failure: Username or Email is already taken."}).encode("utf-8"))
            finally:
                conn.close()
            return
        elif self.path == "/api/login":
            username = payload.get("username", "").strip()
            password = payload.get("password", "").strip()

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            valid_user = cursor.fetchone()
            conn.close()

            if valid_user:
                session_token = str(uuid.uuid4())
                ACTIVE_SESSIONS[session_token] = username
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Set-Cookie", f"Session-ID={session_token}; Path=/; HttpOnly; SameSite=Strict")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            else:
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Access Denied: Invalid Username or Password Credentials."}).encode("utf-8"))
            return
        elif self.path == "/api/protected/profile":
            user = self.get_session_user()
            if not user:
                self.send_response(403)
                self.end_headers()
                return

            full_name = payload.get("full_name", "").strip()
            email = payload.get("email", "").strip()
            department = payload.get("department", "").strip()
            position = payload.get("position", "").strip()

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            try:
                cursor.execute('''UPDATE profiles SET full_name=?, email=?, department=?, position=? WHERE username=?''',
                               (full_name, email, department, position, user))
                conn.commit()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            except sqlite3.IntegrityError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Collision error: Email address allocated elsewhere."}).encode("utf-8"))
            finally:
                conn.close()
            return
        elif self.path == "/api/logout":
            cookie_header = self.headers.get('Cookie', '')
            if "Session-ID=" in cookie_header:
                session_id = cookie_header.split("Session-ID=")[1].split(";")[0].strip()
                if session_id in ACTIVE_SESSIONS:
                    del ACTIVE_SESSIONS[session_id]
            
            self.send_response(200)
            self.send_header("Set-Cookie", "Session-ID=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            return

def start_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, PortalServerHandler)
    print("\n" + "="*60)
    print(" 🚀 EMPLOYEE PORTAL APP SCRIPT ONLINE!")
    print(" 👉 Connection Link: http://localhost:8080")
    print("=" * 60 + "\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

if __name__ == "__main__":
    start_server()