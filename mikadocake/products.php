<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Premium Collections</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <?php include 'header.php'; ?>

    <div class="full-bg">
        <h1 style="text-align:center;">Our Premium Collection</h1>
        
        <div class="product-grid">
            <?php
            $conn = new mysqli("localhost", "root", "", "mikadocake_db");
            
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }

            $result = $conn->query("SELECT * FROM products");
            
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    echo "<div class='product-card'>
                            <img src='uploads/".$row['image_path']."'>
                            <h3>".htmlspecialchars($row['title'])."</h3>
                            <p>".htmlspecialchars($row['description'])."</p>
                            <p><strong>KES ".number_format($row['price'], 2)."</strong></p>
                          </div>";
                }
            } else {
                echo "<p>No products found.</p>";
            }
            $conn->close();
            ?>
        </div>
    </div>

</body>
</html>