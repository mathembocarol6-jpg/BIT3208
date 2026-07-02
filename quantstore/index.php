<?php
session_start();

if (isset($_SESSION['user_id'])) {
    header("Location: dashboard.php");
    exit();
}

$error_message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);
    
    $conn = new mysqli("localhost", "root", "", "quantstore_db");

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $stmt = $conn->prepare("SELECT id, username, password_hash FROM users WHERE username = ? LIMIT 1");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if (password_verify($password, $row['password_hash'])) {
            $_SESSION['user_id'] = $row['id'];
            $_SESSION['username'] = $row['username'];
            header("Location: dashboard.php");
            exit();
        } else {
            $error_message = "Invalid system credentials.";
        }
    } else {
        $error_message = "Invalid system credentials.";
    }

    $stmt->close();
    $conn->close();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - QuantStore</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: linear-gradient(135deg, #1e1b4b, #0f172a); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .login-card { background: #ffffff; border-radius: 12px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2); width: 100%; max-width: 400px; overflow: hidden; }
        .login-header { background: linear-gradient(135deg, #4f46e5, #06b6d4); padding: 30px 20px; text-align: center; color: white; }
        .login-body { padding: 30px 20px; }
        .error-banner { background-color: #fee2e2; color: #b91c1c; padding: 10px; border-radius: 6px; margin-bottom: 20px; font-size: 0.9rem; text-align: center; }
        .form-group { margin-bottom: 20px; }
        .form-label { display: block; margin-bottom: 6px; color: #475569; font-size: 0.9rem; font-weight: 600; }
        .form-input { width: 100%; padding: 10px 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 1rem; }
        .login-btn { width: 100%; background: #4f46e5; color: white; border: none; padding: 12px; border-radius: 6px; font-weight: 600; cursor: pointer; }
        .login-btn:hover { background: #1e1b4b; }
        .register-link { text-align: center; margin-top: 15px; font-size: 0.9rem; }
        .register-link a { color: #4f46e5; text-decoration: none; font-weight: 600; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="login-header">
            <h1>QuantStore</h1>
            <p>Inventory Control Portal Access</p>
        </div>
        <div class="login-body">
            <?php if (!empty($error_message)): ?>
                <div class="error-banner"><?php echo htmlspecialchars($error_message); ?></div>
            <?php endif; ?>
            <form action="index.php" method="POST">
                <div class="form-group">
                    <label class="form-label" for="username">Username</label>
                    <input class="form-input" type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label class="form-label" for="password">Password</label>
                    <input class="form-input" type="password" id="password" name="password" required>
                </div>
                <button class="login-btn" type="submit">Sign In</button>
            </form>
            <div class="register-link">
                Don't have an account? <a href="register.php">Register here</a>
            </div>
        </div>
    </div>
</body>
</html>