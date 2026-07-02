<?php
$conn = new mysqli("localhost", "root", "", "mikadocake_db");
if ($conn->connect_error) { die("Connection failed: " . $conn->connect_error); }

$result = $conn->query("SELECT * FROM contacts ORDER BY created_at DESC");
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin | Manage Messages</title>
    <style>
        table { width: 95%; margin: 40px auto; border-collapse: collapse; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #f4f4f4; }
        .del-btn { color: red; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <h1 style="text-align: center;">Customer Messages</h1>
    <table>
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Message</th>
            <th>Received</th>
            <th>Action</th>
        </tr>
        <?php
        while($row = $result->fetch_assoc()) {
            echo "<tr>
                    <td>".htmlspecialchars($row['name'])."</td>
                    <td>".htmlspecialchars($row['email'])."</td>
                    <td>".htmlspecialchars($row['message'])."</td>
                    <td>".$row['created_at']."</td>
                    <td><a href='delete_message.php?id=".$row['id']."' class='del-btn'>Delete</a></td>
                  </tr>";
        }
        ?>
    </table>
</body>
</html>