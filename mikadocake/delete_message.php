<?php
$conn = new mysqli("localhost", "root", "", "mikadocake_db");

if (isset($_GET['id'])) {
    $id = (int)$_GET['id'];
    $conn->query("DELETE FROM contacts WHERE id = $id");
}

header("Location: admin_messages.php");
?>