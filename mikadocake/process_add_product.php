<?php
$conn = new mysqli("localhost", "root", "", "mikadocake_db");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $title = $conn->real_escape_string($_POST['title']);
    $description = $conn->real_escape_string($_POST['description']);
    $price = (float)$_POST['price'];
    $image_path = $conn->real_escape_string($_POST['image_path']);

    $sql = "INSERT INTO products (title, description, price, image_path) 
            VALUES ('$title', '$description', '$price', '$image_path')";

    if ($conn->query($sql) === TRUE) {
        echo "Product added successfully! <a href='add_product.php'>Add another</a> or <a href='products.php'>View Store</a>";
    } else {
        echo "Error: " . $conn->error;
    }
}
$conn->close();
?>