<?php
$conn = new mysqli("localhost", "root", "", "mikadocake_db");
$result = $conn->query("SELECT * FROM products ORDER BY id DESC");
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin | Manage Inventory</title>
    <style>
        table { width: 95%; margin: 40px auto; border-collapse: collapse; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #f4f4f4; }
        .del-btn { color: red; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1 style="text-align: center;">Inventory Management</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Price</th>
            <th>Image</th>
            <th>Action</th>
        </tr>
        <?php
        while($row = $result->fetch_assoc()) {
            echo "<tr>
                    <td>".$row['id']."</td>
                    <td>".htmlspecialchars($row['title'])."</td>
                    <td>KES ".number_format($row['price'])."</td>
                    <td>".htmlspecialchars($row['image_path'])."</td>
                    <td><a href='delete_product.php?id=".$row['id']."' class='del-btn'>Delete</a></td>
                  </tr>";
        }
        ?>
    </table>
</body>
</html>