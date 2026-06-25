<?php
require_once 'db.php';
session_start();

if(isset($_SESSION["loggedin"]) && $_SESSION["loggedin"] === true){
    header("location: " . strtolower($_SESSION["role"]) . "_dashboard.php");
    exit;
}

$username = $password = $role = $email = $full_name = "";
$login_username = $login_password = "";
$error = $success = "";

if($_SERVER["REQUEST_METHOD"] == "POST"){
    if(isset($_POST['register'])){
        $username = trim($_POST["username"]);
        $password = trim($_POST["password"]);
        $email = trim($_POST["email"]);
        $role = trim($_POST["role"]);
        $full_name = trim($_POST["full_name"]);
        
        if(empty($username) || empty($password) || empty($email) || empty($role) || empty($full_name)){
            $error = "Please fill in all registration fields.";
        } else {
            $sql = "SELECT id FROM users WHERE username = :username OR email = :email";
            if($stmt = $pdo->prepare($sql)){
                $stmt->bindParam(":username", $username, PDO::PARAM_STR);
                $stmt->bindParam(":email", $email, PDO::PARAM_STR);
                if($stmt->execute()){
                    if($stmt->rowCount() > 0){
                        $error = "This username or email is already taken.";
                    } else {
                        $sql = "INSERT INTO users (username, password, email, role, full_name) VALUES (:username, :password, :email, :role, :full_name)";
                        if($stmt = $pdo->prepare($sql)){
                            $param_password = password_hash($password, PASSWORD_DEFAULT);
                            $stmt->bindParam(":username", $username, PDO::PARAM_STR);
                            $stmt->bindParam(":password", $param_password, PDO::PARAM_STR);
                            $stmt->bindParam(":email", $email, PDO::PARAM_STR);
                            $stmt->bindParam(":role", $role, PDO::PARAM_STR);
                            $stmt->bindParam(":full_name", $full_name, PDO::PARAM_STR);
                            
                            if($stmt->execute()){
                                $success = "Account created successfully. You can now log in.";
                            } else {
                                $error = "Something went wrong. Please try again.";
                            }
                        }
                    }
                }
                unset($stmt);
            }
        }
    } elseif(isset($_POST['login'])) {
        $login_username = trim($_POST["username"]);
        $login_password = trim($_POST["password"]);
        
        if(empty($login_username) || empty($login_password)){
            $error = "Please enter both username and password.";
        } else {
            $sql = "SELECT id, username, password, role, full_name FROM users WHERE username = :username";
            if($stmt = $pdo->prepare($sql)){
                $stmt->bindParam(":username", $login_username, PDO::PARAM_STR);
                if($stmt->execute()){
                    if($stmt->rowCount() == 1){
                        if($row = $stmt->fetch()){
                            $id = $row["id"];
                            $username = $row["username"];
                            $hashed_password = $row["password"];
                            $role = $row["role"];
                            $full_name = $row["full_name"];
                            
                            if(password_verify($login_password, $hashed_password)){
                                session_start();
                                $_SESSION["loggedin"] = true;
                                $_SESSION["id"] = $id;
                                $_SESSION["username"] = $username;
                                $_SESSION["role"] = $role;
                                $_SESSION["full_name"] = $full_name;
                                
                                header("location: " . strtolower($role) . "_dashboard.php");
                                exit;
                            } else {
                                $error = "Invalid password entered.";
                            }
                        }
                    } else {
                        $error = "No account found with that username.";
                    }
                } else {
                    $error = "Oops! Something went wrong. Please try again.";
                }
                unset($stmt);
            }
        }
    }
}
unset($pdo);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Academic Portal Gateway</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f1f5f9; color: #334155; margin: 0; padding: 20px; }
        .wrapper { max-width: 900px; margin: 40px auto; background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
        h2 { color: #1e3a8a; margin-top: 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
        .form-group { margin-bottom: 18px; }
        label { display: block; margin-bottom: 6px; font-weight: 600; font-size: 14px; }
        input[type="text"], input[type="password"], input[type="email"], select { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; font-size: 14px; }
        input:focus, select:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }
        .btn { background-color: #2563eb; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-weight: 600; width: 100%; font-size: 15px; }
        .btn:hover { background-color: #1d4ed8; }
        .alert { padding: 12px; border-radius: 6px; margin-bottom: 20px; font-size: 14px; grid-column: span 2; }
        .alert-danger { background-color: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
        .alert-success { background-color: #dcfce7; color: #166534; border: 1px solid #86efac; }
        @media (max-width: 768px) { .wrapper { grid-template-columns: 1fr; } .alert { grid-column: span 1; } }
    </style>
</head>
<body>
    <div class="wrapper">
        <?php 
        if(!empty($error)){ echo '<div class="alert alert-danger">' . $error . '</div>'; }
        if(!empty($success)){ echo '<div class="alert alert-success">' . $success . '</div>'; }
        ?>
        <div>
            <h2>Sign In</h2>
            <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" value="<?php echo htmlspecialchars($login_username); ?>">
                </div>    
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password">
                </div>
                <div class="form-group">
                    <input type="submit" name="login" class="btn" value="Login">
                </div>
            </form>
        </div>
        <div>
            <h2>Create Account</h2>
            <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" name="full_name" value="<?php echo htmlspecialchars($full_name); ?>">
                </div>
                <div class="form-group">
                    <label>Email Address</label>
                    <input type="email" name="email" value="<?php echo htmlspecialchars($email); ?>">
                </div>
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" value="<?php echo htmlspecialchars($username); ?>">
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password">
                </div>
                <div class="form-group">
                    <label>Portal Access Role</label>
                    <select name="role">
                        <option value="Student">Student</option>
                        <option value="Lecturer">Lecturer</option>
                        <option value="Administrator">Administrator</option>
                    </select>
                </div>
                <div class="form-group">
                    <input type="submit" name="register" class="btn" value="Register System Profile">
                </div>
            </form>
        </div>
    </div>
</body>
</html>