<?php
require_once 'auth_check.php';
verify_access('Administrator');
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Administrator Management Console</title>
    <style>
        body { font-family: sans-serif; background-color: #faf5ff; margin: 0; padding: 30px; }
        .nav { display: flex; justify-content: space-between; align-items: center; background: white; padding: 15px 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .container { margin-top: 30px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .badge { background-color: #f3e8ff; color: #6b21a8; padding: 6px 12px; border-radius: 20px; font-weight: bold; }
        .logout-btn { background-color: #dc2626; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; }
    </style>
</head>
<body>
    <div class="nav">
        <h2>🛠️ Enterprise Infrastructure Command Console</h2>
        <div>
            <span class="badge">System Root Admin</span>
            <a href="logout.php" class="logout-btn">Terminate Session</a>
        </div>
    </div>
    <div class="container">
        <h1>Administrator Node Access: <?php echo htmlspecialchars($_SESSION["full_name"]); ?></h1>
        <h3>Root Core Administrative Commands</h3>
        <ul>
            <li>User Allocation Security Adjustments</li>
            <li>System Auditing Relational Database File Backups</li>
            <li>Ecosystem Operational Traffic Tracking Metrics</li>
        </ul>
    </div>
</body>
</html>