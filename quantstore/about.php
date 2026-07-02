<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About QuantStore</title>
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
            margin-bottom: 15px;
            border-bottom: 2px solid #e0e7ff;
            padding-bottom: 10px;
        }

        .container p {
            line-height: 1.7;
            color: #475569;
            margin-bottom: 25px;
            font-size: 1.1rem;
        }

        .container h3 {
            font-size: 1.3rem;
            color: #4f46e5;
            margin-bottom: 15px;
        }

        .container ul {
            list-style: none;
        }

        .container ul li {
            position: relative;
            padding-left: 25px;
            margin-bottom: 12px;
            color: #475569;
            line-height: 1.6;
        }

        .container ul li::before {
            content: "✦";
            position: absolute;
            left: 0;
            color: #06b6d4;
            font-weight: bold;
        }

        .container ul li strong {
            color: #1e1b4b;
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
                <h1>About QuantStore</h1>
                <p>QuantStore is your premier destination for high-quality equipment tailored for all major ball games.</p>

                <h3>Our Equipment Range</h3>
                <ul>
                    <li><strong>Volleyball:</strong> Professional-grade balls, knee pads, and nets.</li>
                    <li><strong>Netball:</strong> Match-ready netballs and bibs.</li>
                    <li><strong>Handball:</strong> High-grip balls for indoor and outdoor play.</li>
                    <li><strong>Football:</strong> Durable match balls, training equipment, and goalkeeping gloves.</li>
                </ul>
            </div>
        </main>

    </div>

</body>
</html>