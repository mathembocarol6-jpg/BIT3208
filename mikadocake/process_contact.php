<?php
$conn = new mysqli("localhost", "root", "", "mikadocake_db");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $conn->real_escape_string($_POST['name']);
    $email = $conn->real_escape_string($_POST['email']);
    $message = $conn->real_escape_string($_POST['message']);

    $sql = "INSERT INTO contacts (name, email, message) VALUES ('$name', '$email', '$message')";

    if ($conn->query($sql) === TRUE) {
        echo "<h1>Message Received!</h1>";
        echo "<p>Thank you, $name. We will get back to you soon.</p>";
        echo "<a href='products.php'>Back to Products</a>";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
} else {
    header("Location: contact.php");
}
$conn->close();
?>