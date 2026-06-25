import sqlite3
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_NAME = "employee_management.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            department TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            salary REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Management Hub</title>
    <style>
        body { font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; padding: 0; background-color: #f4f6f9; color: #333; }
        .auth-container, .dashboard-container { max-width: 1000px; margin: 40px auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .auth-container { max-width: 400px; margin-top: 100px; text-align: center; }
        h1, h2 { color: #1e293b; margin-top: 0; }
        .form-group { margin-bottom: 15px; text-align: left; }
        label { display: block; margin-bottom: 5px; font-weight: 600; font-size: 14px; }
        input[type="text"], input[type="number"], input[type="password"], input[type="email"], select { 
            width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; font-size: 14px;
        }
        button { 
            background-color: #2563eb; color: white; border: none; padding: 10px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; width: 100%; font-size: 14px; transition: background 0.2s;
        }
        button:hover { background-color: #1d4ed8; }
        .secondary-btn { background-color: #64748b; margin-top: 10px; }
        .secondary-btn:hover { background-color: #475569; }
        .danger-btn { background-color: #dc2626; }
        .danger-btn:hover { background-color: #b91c1c; }
        .nav-tabs { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
        .tab-link { cursor: pointer; padding: 8px 16px; font-weight: 600; color: #64748b; border-radius: 6px; }
        .tab-link.active { color: #2563eb; background-color: #eff6ff; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; }
        th { background-color: #f8fafc; font-weight: 600; color: #475569; }
        .flex-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
        .action-btns { display: flex; gap: 5px; }
        .action-btns button { padding: 6px 10px; font-size: 12px; width: auto; }
        .alert { padding: 12px; border-radius: 6px; margin-bottom: 15px; font-size: 14px; display: none; }
        .alert-success { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
        .alert-error { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
        .search-bar { margin-bottom: 20px; display: flex; gap: 10px; }
    </style>
</head>
<body>

    <div id="authPanel" class="auth-container">
        <h1 id="authTitle">💼 Portal Sign In</h1>
        <div class="alert alert-success" id="authSuccess"></div>
        <div class="alert alert-error" id="authError"></div>
        
        <div class="form-group">
            <label>Username</label>
            <input type="text" id="authUsername">
        </div>
        <div class="form-group">
            <label>Password</label>
            <input type="password" id="authPassword">
        </div>
        <button id="mainAuthBtn" onclick="handleAuth()">Log In</button>
        <button class="secondary-btn" id="toggleAuthBtn" onclick="toggleAuthMode()">Register New Account</button>
    </div>

    <div id="dashboardPanel" class="dashboard-container" style="display: none;">
        <div class="flex-header">
            <h2>Internal Employee Management System</h2>
            <div>
                <span id="welcomeUser" style="margin-right: 15px; font-weight:600;"></span>
                <button onclick="logout()" class="secondary-btn" style="width: auto; margin:0;">Logout</button>
            </div>
        </div>

        <div class="nav-tabs">
            <div class="tab-link active" id="tabView" onclick="switchTab('view')">📊 View Records</div>
            <div class="tab-link" id="tabAdd" onclick="switchTab('add')">➕ Register Employee</div>
        </div>

        <div class="alert alert-success" id="dashSuccess"></div>
        <div class="alert alert-error" id="dashError"></div>

        <div id="viewSection">
            <div class="search-bar">
                <input type="text" id="searchQuery" placeholder="Search by Name or Department..." oninput="loadEmployees()">
            </div>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Full Name</th>
                        <th>Age</th>
                        <th>Department</th>
                        <th>Email Address</th>
                        <th>Salary</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="employeeTableBody"></tbody>
            </table>
        </div>

        <div id="formSection" style="display: none;">
            <h3 id="formTitle">Register New Employee Record</h3>
            <input type="hidden" id="empId">
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" id="empName">
            </div>
            <div class="form-group">
                <label>Age</label>
                <input type="number" id="empAge" value="25">
            </div>
            <div class="form-group">
                <label>Department</label>
                <input type="text" id="empDept">
            </div>
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" id="empEmail">
            </div>
            <div class="form-group">
                <label>Salary ($)</label>
                <input type="number" id="empSalary" value="0">
            </div>
            <button id="saveEmpBtn" onclick="saveEmployee()">Submit Registration</button>
            <button class="secondary-btn" id="cancelEditBtn" style="display: none;" onclick="resetEmpForm()">Cancel Edit</button>
        </div>
    </div>

    <script>
        let isLoginMode = true;
        let currentUser = "";

        function showAlert(id, message, isSuccess) {
            const el = document.getElementById(id);
            el.innerText = message;
            el.className = isSuccess ? "alert alert-success" : "alert alert-error";
            el.style.display = "block";
            setTimeout(() => { el.style.display = "none"; }, 4000);
        }

        function toggleAuthMode() {
            isLoginMode = !isLoginMode;
            document.getElementById("authTitle").innerText = isLoginMode ? "💼 Portal Sign In" : "📝 Register Account";
            document.getElementById("mainAuthBtn").innerText = isLoginMode ? "Log In" : "Register Account";
            document.getElementById("toggleAuthBtn").innerText = isLoginMode ? "Register New Account" : "Back to Sign In";
        }

        async function handleAuth() {
            const username = document.getElementById("authUsername").value.trim();
            const password = document.getElementById("authPassword").value.trim();
            
            if (!username || !password) {
                showAlert("authError", "All fields are required.", false);
                return;
            }

            const endpoint = isLoginMode ? "/api/login" : "/api/register_user";
            const res = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();

            if (res.ok) {
                if (isLoginMode) {
                    currentUser = username;
                    document.getElementById("welcomeUser").innerText = "Welcome, " + username + "! 👋";
                    document.getElementById("authPanel").style.display = "none";
                    document.getElementById("dashboardPanel").style.display = "block";
                    loadEmployees();
                } else {
                    showAlert("authSuccess", "Account created successfully! You can now log in.", true);
                    toggleAuthMode();
                }
            } else {
                showAlert("authError", data.error, false);
            }
        }

        function logout() {
            currentUser = "";
            document.getElementById("authUsername").value = "";
            document.getElementById("authPassword").value = "";
            document.getElementById("dashboardPanel").style.display = "none";
            document.getElementById("authPanel").style.display = "block";
        }

        function switchTab(type) {
            document.getElementById("tabView").className = type === 'view' ? "tab-link active" : "tab-link";
            document.getElementById("tabAdd").className = type === 'add' ? "tab-link active" : "tab-link";
            document.getElementById("viewSection").style.display = type === 'view' ? "block" : "none";
            document.getElementById("formSection").style.display = type === 'add' ? "block" : "none";
            if(type === 'view') loadEmployees();
        }

        async function loadEmployees() {
            const query = document.getElementById("searchQuery").value.trim();
            const url = query ? `/api/employees?search=${encodeURIComponent(query)}` : '/api/employees';
            const res = await fetch(url);
            const employees = await res.json();
            
            const tbody = document.getElementById("employeeTableBody");
            tbody.innerHTML = "";
            
            employees.forEach(emp => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>\${emp.id}</td>
                    <td>\${emp.name}</td>
                    <td>\${emp.age}</td>
                    <td>\${emp.department}</td>
                    <td>\${emp.email}</td>
                    <td>\$\${Number(emp.salary).toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                    <td class="action-btns">
                        <button onclick="editEmployee(\${emp.id}, '\${emp.name}', \${emp.age}, '\${emp.department}', '\${emp.email}', \${emp.salary})">Edit</button>
                        <button class="danger-btn" onclick="deleteEmployee(\${emp.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function editEmployee(id, name, age, dept, email, salary) {
            document.getElementById("empId").value = id;
            document.getElementById("empName").value = name;
            document.getElementById("empAge").value = age;
            document.getElementById("empDept").value = dept;
            document.getElementById("empEmail").value = email;
            document.getElementById("empSalary").value = salary;
            
            document.getElementById("formTitle").innerText = "Update Existing Details Log";
            document.getElementById("saveEmpBtn").innerText = "Save Changes";
            document.getElementById("cancelEditBtn").style.display = "block";
            switchTab('add');
        }

        function resetEmpForm() {
            document.getElementById("empId").value = "";
            document.getElementById("empName").value = "";
            document.getElementById("empAge").value = "25";
            document.getElementById("empDept").value = "";
            document.getElementById("empEmail").value = "";
            document.getElementById("empSalary").value = "0";
            
            document.getElementById("formTitle").innerText = "Register New Employee Record";
            document.getElementById("saveEmpBtn").innerText = "Submit Registration";
            document.getElementById("cancelEditBtn").style.display = "none";
        }

        async function saveEmployee() {
            const id = document.getElementById("empId").value;
            const name = document.getElementById("empName").value.trim();
            const age = parseInt(document.getElementById("empAge").value);
            const department = document.getElementById("empDept").value.trim();
            const email = document.getElementById("empEmail").value.trim();
            const salary = parseFloat(document.getElementById("empSalary").value);

            if(!name || !department || !email) {
                showAlert("dashError", "Form Validation Error: All tracking elements fields are mandatory.", false);
                return;
            }
            if(age < 18 || age > 65) {
                showAlert("dashError", "Form Validation Error: Age parameters must sit between 18 and 65.", false);
                return;
            }
            if(salary <= 0) {
                showAlert("dashError", "Form Validation Error: Salary must calculate as a positive dynamic.", false);
                return;
            }

            const payload = { name, age, department, email, salary };
            let url = "/api/employees";
            let method = "POST";

            if (id) {
                url = `/api/employees?id=\${id}`;
                method = "PUT";
            }

            const res = await fetch(url, {
                method: method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            if(res.ok) {
                showAlert("dashSuccess", id ? "Profile logs securely modified!" : "Employee registered successfully!", true);
                resetEmpForm();
                switchTab('view');
            } else {
                showAlert("dashError", data.error, false);
            }
        }

        async function deleteEmployee(id) {
            if(!confirm("Are you sure you want to completely erase this record profile?")) return;
            const res = await fetch(`/api/employees?id=\${id}`, { method: "DELETE" });
            if(res.ok) {
                showAlert("dashSuccess", "Internal profile dataset cleared completely.", true);
                loadEmployees();
            } else {
                const data = await res.json();
                showAlert("dashError", data.error, false);
            }
        }
    </script>
</body>
</html>
"""

class WebServerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_INTERFACE.encode("utf-8"))
        elif self.path.startswith("/api/employees"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            if "search=" in self.path:
                query_param = self.path.split("search=")[1]
                decoded_query = urllib.parse.unquote(query_param) if 'urllib' in globals() else query_param.replace("%20", " ")
                cursor.execute("SELECT * FROM employees WHERE name LIKE ? OR department LIKE ?", (f"%{decoded_query}%", f"%{decoded_query}%"))
            else:
                cursor.execute("SELECT * FROM employees")
                
            rows = cursor.fetchall()
            conn.close()
            
            employees = [{"id": r[0], "name": r[1], "age": r[2], "department": r[3], "email": r[4], "salary": r[5]} for r in rows]
            self.wfile.write(json.dumps(employees).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if self.path == "/api/register_user":
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
                self.wfile.write(json.dumps({"error": "That username is already taken."}).encode("utf-8"))
            finally:
                conn.close()

        elif self.path == "/api/login":
            username = data.get("username", "").strip()
            password = data.get("password", "").strip()
            
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid Username or Password."}).encode("utf-8"))

        elif self.path == "/api/employees":
            name = data.get("name", "").strip()
            age = int(data.get("age", 25))
            department = data.get("department", "").strip()
            email = data.get("email", "").strip()
            salary = float(data.get("salary", 0))

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO employees (name, age, department, email, salary) VALUES (?, ?, ?, ?, ?)",
                               (name, age, department, email, salary))
                conn.commit()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            except sqlite3.IntegrityError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "An employee with this email already exists."}).encode("utf-8"))
            finally:
                conn.close()

    def do_PUT(self):
        if self.path.startswith("/api/employees"):
            emp_id = self.path.split("id=")[1]
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            name = data.get("name")
            age = data.get("age")
            department = data.get("department")
            email = data.get("email")
            salary = data.get("salary")

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            try:
                cursor.execute('''UPDATE employees SET name=?, age=?, department=?, email=?, salary=? WHERE id=?''',
                               (name, age, department, email, salary, emp_id))
                conn.commit()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            except sqlite3.IntegrityError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Email address is assigned elsewhere."}).encode("utf-8"))
            finally:
                conn.close()

    def do_DELETE(self):
        if self.path.startswith("/api/employees"):
            emp_id = self.path.split("id=")[1]
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
            conn.commit()
            conn.close()
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, WebServerHandler)
    print("\n" + "="*50)
    print(" 🚀 WEBSITE SERVER STARTED SUCCESSFULLY!")
    print(" 👉 Open your browser and go to: http://localhost:8080")
    print("=" * 50 + "\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping web server. Goodbye!")
        httpd.server_close()

if __name__ == "__main__":
    run()