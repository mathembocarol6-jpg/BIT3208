<?php
$conn = new mysqli("localhost", "root", "", "mikadocake_db");

if (isset($_GET['id'])) {
    $id = (int)$_GET['id'];
    $conn->query("DELETE FROM products WHERE id = $id");
}

header("Location: manage_products.php");
?>