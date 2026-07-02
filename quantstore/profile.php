<?php
session_start();

if (!isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit();
}

$servername = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "quantstore_db";

$conn = new mysqli($servername, $dbusername, $dbpassword, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$user_id = $_SESSION['user_id'];
$username = $_SESSION['username'];
$email = "Not Available";

$stmt = $conn->prepare("SELECT email FROM users WHERE id = ? LIMIT 1");
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $email = $row['email'];
}

$stmt->close();
$conn->close();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profile - QuantStore</title>
    <link rel="stylesheet" href="style.css?v=<?php echo time(); ?>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7f6;
            color: #333;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        .dashboard-wrapper {
            display: flex;
            flex-direction: column;
            flex: 1;
        }

        .main-content {
            flex: 1;
            padding: 30px;
        }

        .page-header {
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e7ff;
            padding-bottom: 10px;
        }

        .page-header h1 {
            color: #1e1b4b;
        }

        .profile-card {
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            max-width: 500px;
            margin: 0 auto;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }

        .profile-card-header {
            background: linear-gradient(135deg, #1e1b4b, #4f46e5);
            padding: 30px;
            text-align: center;
            color: white;
        }

        .user-avatar {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            border: 3px solid #06b6d4;
            object-fit: cover;
            margin-bottom: 15px;
        }

        .profile-card-header h2 {
            font-size: 1.5rem;
            margin-bottom: 5px;
        }

        .profile-card-header p {
            font-size: 0.9rem;
            color: #93c5fd;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .profile-card-body {
            padding: 30px;
        }

        .info-group {
            margin-bottom: 20px;
            border-bottom: 1px solid #f1f5f9;
            padding-bottom: 10px;
        }

        .info-label {
            font-size: 0.85rem;
            color: #64748b;
            text-transform: uppercase;
            margin-bottom: 4px;
            font-weight: 600;
        }

        .info-value {
            font-size: 1.05rem;
            color: #1e1b4b;
        }

        .edit-profile-btn {
            display: block;
            width: 100%;
            text-align: center;
            background-color: #4f46e5;
            color: white;
            padding: 12px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 10px;
            transition: background-color 0.2s;
        }

        .edit-profile-btn:hover {
            background-color: #1e1b4b;
        }

        @media (min-width: 992px) {
            .dashboard-wrapper {
                flex-direction: row;
            }

            .main-content {
                margin-left: 260px;
                padding: 40px;
            }
        }
    </style>
</head>
<body>

    <div class="dashboard-wrapper">
        
        <?php require_once 'header.php'; ?>

        <main class="main-content">
            <div class="page-header">
                <h1>My Profile</h1>
            </div>

            <div class="profile-card">
                <div class="profile-card-header">
                    <img src="IMG-20260302-WA0014.jpg" alt="User Profile Image" class="user-avatar">
                    <h2><?php echo htmlspecialchars($username); ?></h2>
                    <p>QuantStore Account</p>
                </div>
                
                <div class="profile-card-body">
                    <div class="info-group">
                        <div class="info-label">Account User Identifier</div>
                        <div class="info-value">#<?php echo htmlspecialchars($user_id); ?></div>
                    </div>

                    <div class="info-group">
                        <div class="info-label">Username Handle</div>
                        <div class="info-value"><?php echo htmlspecialchars($username); ?></div>
                    </div>

                    <div class="info-group">
                        <div class="info-label">Synchronized Email Address</div>
                        <div class="info-value"><?php echo htmlspecialchars($email); ?></div>
                    </div>

                    <a href="#" class="edit-profile-btn">Update Profile Details</a>
                </div>
            </div>
        </main>

    </div>

</body>
</html>