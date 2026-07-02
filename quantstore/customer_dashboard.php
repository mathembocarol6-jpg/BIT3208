<?php
session_start();
// Ensure the user is actually logged in
if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}
?>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css">
    <title>Customer Dashboard</title>
</head>
<body>
    <?php require_once 'header.php'; ?>
    <div class="container">
        <h1>Welcome, <?php echo htmlspecialchars($_SESSION['username']); ?></h1>
        <p>This is your QuantStore Customer Dashboard.</p>
        <div class="dashboard-content">
            <h3>Account Overview</h3>
            <p>Full Name: <?php echo htmlspecialchars($_SESSION['full_name'] ?? 'N/A'); ?></p>
        </div>
    </div>
</body>
</html>