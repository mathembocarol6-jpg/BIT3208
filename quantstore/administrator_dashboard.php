<?php
session_start();

if (!isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - QuantStore</title>
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

        .container {
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            padding: 30px;
            max-width: 800px;
            margin: 0 auto;
        }

        .container h1 {
            color: #1e1b4b;
            margin-bottom: 10px;
        }

        .container p {
            color: #64748b;
            font-size: 1.05rem;
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
            <div class="container">
                <h1>Welcome, <?php echo htmlspecialchars($_SESSION['username']); ?></h1>
                <p>This is your QuantStore Administrator Portal.</p>
            </div>
        </main>
    </div>

</body>
</html>