import sqlite3
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_NAME = "student_portal.db"

def init_db():
    """Ensures the database and required tables always exist safely."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            username TEXT PRIMARY KEY,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            course TEXT NOT NULL,
            gpa REAL NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

# Automatically initialize database structures right before the website spins up
init_db()

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academic Student Portal</title>
    <style>
        body { font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; background-color: #f1f5f9; color: #1e293b; }
        .auth-card, .portal-container { max-width: 95%; width: 900px; margin: 40px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); box-sizing: border-box; }
        .auth-card { max-width: 380px; margin-top: 80px; text-align: center; }
        h1, h2, h3 { color: #0f172a; margin-top: 0; }
        .input-group { margin-bottom: 16px; text-align: left; }
        label { display: block; margin-bottom: 6px; font-weight: 600; font-size: 13px; color: #475569; }
        input, select { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; font-size: 14px; }
        input:focus, select:focus { outline: 2px solid #3b82f6; border-color: transparent; }
        button { background-color: #3b82f6; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: 600; width: 100%; font-size: 14px; margin-top: 10px; transition: background 0.15s; }
        button:hover { background-color: #2563eb; }
        .secondary-btn { background-color: #64748b; }
        .secondary-btn:hover { background-color: #475569; }
        .header-bar { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 25px; gap: 15px; flex-wrap: wrap; }
        .grid-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
        .data-card { background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; height: fit-content; }
        .alert { padding: 12px; border-radius: 6px; margin-bottom: 16px; font-size: 14px; display: none; font-weight: 500; text-align: left; }
        .alert-success { background-color: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
        .alert-error { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
        
        @media (max-width: 768px) {
            .grid-layout { grid-template-columns: 1fr; }
            .header-bar { flex-direction: column; text-align: center; }
            button { width: 100%; }
        }
    </style>
</head>
<body>

    <div id="authContainer" class="auth-card">
        <h1 id="authHeader">🎓 Student Portal</h1>
        <div class="alert alert-success" id="authSuccessMsg"></div>
        <div class="alert alert-error" id="authErrorMsg"></div>
        
        <div class="input-group">
            <label>Username</label>
            <input type="text" id="usernameInput" autocomplete="off">
        </div>
        <div class="input-group">
            <label>Password</label>
            <input type="password" id="passwordInput">
        </div>
        
        <button id="authActionButton" onclick="submitAuthForm()">Log In</button>
        <button class="secondary-btn" id="authToggleServerButton" onclick="toggleAuthMode()">Create Portal Account</button>
    </div>

    <div id="portalDashboard" class="portal-container" style="display: none;">
        <div class="header-bar">
            <h2>🏫 Academic Management Center</h2>
            <div>
                <span id="activeUserGreeting" style="font-weight: 600; margin-right: 15px;"></span>
                <button onclick="executeLogout()" class="secondary-btn" style="width: auto; padding: 8px 16px; margin: 0;">Logout</button>
            </div>
        </div>

        <div class="alert alert-success" id="dashSuccessMsg"></div>
        <div class="alert alert-error" id="dashErrorMsg"></div>

        <div class="grid-layout">
            <div class="data-card">
                <h3>Submit Academic Profile</h3>
                <div class="input-group">
                    <label>Student ID Number</label>
                    <input type="text" id="studentId" placeholder="e.g. STU101">
                </div>
                <div class="input-group">
                    <label>Full Legal Name</label>
                    <input type="text" id="studentName">
                </div>
                <div class="input-group">
                    <label>Primary Email Address</label>
                    <input type="email" id="studentEmail">
                </div>
                <div class="input-group">
                    <label>Degree Major Course</label>
                    <input type="text" id="studentCourse">
                </div>
                <div class="input-group">
                    <label>Current Cumulative GPA</label>
                    <input type="number" id="studentGpa" step="0.01" min="0" max="4" value="4.00">
                </div>
                <button onclick="saveStudentProfile()">Update Information Logs</button>
            </div>

            <div class="data-card">
                <h3>Your Academic Records Overview</h3>
                <div id="recordDisplayPlaceholder" style="margin-top: 15px; line-height: 1.6;">
                    <p style="color: #64748b;">No profile metrics synchronized to this user terminal file.</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isLoginView = true;
        let loggedInSessionUser = "";

        function showNotification(targetId, text, isSuccess) {
            const container = document.getElementById(targetId);
            container.innerText = text;
            container.className = isSuccess ? "alert alert-success" : "alert alert-error";
            container.style.display = "block";
            setTimeout(() => { container.style.display = "none"; }, 4000);
        }

        function toggleAuthMode() {
            isLoginView = !isLoginView;
            document.getElementById("authHeader").innerText = isLoginView ? "🎓 Student Portal" : "📝 Register Account";
            document.getElementById("authActionButton").innerText = isLoginView ? "Log In" : "Register Account";
            document.getElementById("authToggleServerButton").innerText = isLoginView ? "Create Portal Account" : "Back to Sign In";
        }

        async function submitAuthForm() {
            const username = document.getElementById("usernameInput").value.trim();
            const password = document.getElementById("passwordInput").value.trim();

            if (!username || !password) {
                showNotification("authErrorMsg", "Validation Error: Credentials fields are mandatory.", false);
                return;
            }

            const targetApiUrl = isLoginView ? "/api/login" : "/api/register";
            const response = await fetch(targetApiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });
            const result = await response.json();

            if (response.ok) {
                if (isLoginView) {
                    loggedInSessionUser = username;
                    document.getElementById("activeUserGreeting").innerText = "Logged in: " + username;
                    document.getElementById("authContainer").style.display = "none";
                    document.getElementById("portalDashboard").style.display = "block";
                    fetchStudentProfile();
                } else {
                    showNotification("authSuccessMsg", "Registration Complete! Access parameters initialized successfully.", true);
                    toggleAuthMode();
                }
            } else {
                showNotification("authErrorMsg", result.error, false);
            }
        }

        function executeLogout() {
            loggedInSessionUser = "";
            document.getElementById("usernameInput").value = "";
            document.getElementById("passwordInput").value = "";
            document.getElementById("portalDashboard").style.display = "none";
            document.getElementById("authContainer").style.display = "block";
        }

        async function fetchStudentProfile() {
            const response = await fetch(`/api/student?username=${encodeURIComponent(loggedInSessionUser)}`);
            const profile = await response.json();
            const viewer = document.getElementById("recordDisplayPlaceholder");

            if (profile && profile.student_id) {
                document.getElementById("studentId").value = profile.student_id;
                document.getElementById("studentName").value = profile.name;
                document.getElementById("studentEmail").value = profile.email;
                document.getElementById("studentCourse").value = profile.course;
                document.getElementById("studentGpa").value = profile.gpa;

                viewer.innerHTML = `
                    <div style="background: white; padding: 15px; border-radius: 6px; border: 1px solid #cbd5e1;">
                        <p><strong>Student ID:</strong> \${profile.student_id}</p>
                        <p><strong>Name:</strong> \${profile.name}</p>
                        <p><strong>Email Address:</strong> \${profile.email}</p>
                        <p><strong>Enrolled Major:</strong> \${profile.course}</p>
                        <p><strong>Cumulative GPA:</strong> <span style="color: #2563eb; font-weight: bold;">\${Number(profile.gpa).toFixed(2)} / 4.00</span></p>
                    </div>
                `;
            } else {
                document.getElementById("studentId").value = "";
                document.getElementById("studentName").value = "";
                document.getElementById("studentEmail").value = "";
                document.getElementById("studentCourse").value = "";
                document.getElementById("studentGpa").value = "4.00";
                viewer.innerHTML = '<p style="color: #64748b;">No profile configurations linked to this portal space yet. Complete the form to establish logs.</p>';
            }
        }

        async function saveStudentProfile() {
            const id = document.getElementById("studentId").value.trim();
            const name = document.getElementById("studentName").value.trim();
            const email = document.getElementById("studentEmail").value.trim();
            const course = document.getElementById("studentCourse").value.trim();
            const gpa = parseFloat(document.getElementById("studentGpa").value);

            if (!id || !name || !email || !course || isNaN(gpa)) {
                showNotification("dashErrorMsg", "Form Validation Error: Complete all registration entries.", false);
                return;
            }
            if (gpa < 0.0 || gpa > 4.0) {
                showNotification("dashErrorMsg", "Form Validation Error: Academic scale bounds limit GPA from 0.00 to 4.00.", false);
                return;
            }
            if (!/^[\w\.-]+@[\w\.-]+\.\w+$/.test(email)) {
                showNotification("dashErrorMsg", "Form Validation Error: Email structure format constraint breakdown.", false);
                return;
            }

            const response = await fetch("/api/student", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: loggedInSessionUser, student_id: id, name, email, course, gpa })
            });

            const result = await response.json();
            if (response.ok) {
                showNotification("dashSuccessMsg", "Academic profile metrics saved and synchronized successfully.", true);
                fetchStudentProfile();
            } else {
                showNotification("dashErrorMsg", result.error, false);
            }
        }
    </script>
</body>
</html>
"""

class StudentPortalHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_INTERFACE.encode("utf-8"))
        elif self.path.startswith("/api/student"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            user_param = ""
            if "username=" in self.path:
                user_param = self.path.split("username=")[1]
                user_param = urllib.parse.unquote(user_param)
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT student_id, name, email, course, gpa 
                FROM students 
                WHERE username = ?
            ''', (user_param,))
            row = cursor.fetchone()
            conn.close()
            
            student_data = {}
            if row:
                student_data = {"student_id": row[0], "name": row[1], "email": row[2], "course": row[3], "gpa": row[4]}
            self.wfile.write(json.dumps(student_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload_bytes = self.rfile.read(content_length)
        data = json.loads(payload_bytes.decode('utf-8'))

        if self.path == "/api/register":
            username = data.get("username", "").strip()
            password = data.get("password", "").strip()
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            except sqlite3.IntegrityError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "That username identifier is already registered."}).encode("utf-8"))
            finally:
                conn.close()

        elif self.path == "/api/login":
            username = data.get("username", "").strip()
            password = data.get("password", "").strip()
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            matched_user = cursor.fetchone()
            conn.close()
            
            if matched_user:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid Portal Username or Password Verification."}).encode("utf-8"))

        elif self.path == "/api/student":
            username = data.get("username", "").strip()
            student_id = data.get("student_id", "").strip()
            name = data.get("name", "").strip()
            email = data.get("email", "").strip()
            course = data.get("course", "").strip()
            gpa = float(data.get("gpa", 0.0))

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO students (username, student_id, name, email, course, gpa) 
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(username) DO UPDATE SET student_id=excluded.student_id, name=excluded.name, email=excluded.email, course=excluded.course, gpa=excluded.gpa
                ''', (username, student_id, name, email, course, gpa))
                conn.commit()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            except sqlite3.IntegrityError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Unique constraint error: Student ID or Email assigned elsewhere."}).encode("utf-8"))
            finally:
                conn.close()

def execute_server():
    address_configuration = ('', 8080)
    server_daemon = HTTPServer(address_configuration, StudentPortalHandler)
    print("\n" + "="*60)
    print(" 🚀 STUDENT PORTAL WEB RUNTIME INITIALIZED SUCCESSFULLY!")
    print(" 👉 View Portal Page via Local Interface: http://localhost:8080")
    print("=" * 60 + "\n")
    try:
        server_daemon.serve_forever()
    except KeyboardInterrupt:
        print("\nHalting Web Server Session.")
        server_daemon.server_close()

if __name__ == "__main__":
    execute_server()