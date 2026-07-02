<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin | Add New Product</title>
    <style>
        .form-container { max-width: 400px; margin: 40px auto; padding: 20px; border: 1px solid #ddd; }
        input, textarea { width: 100%; margin-bottom: 15px; padding: 8px; }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>Add New Product</h1>
        <form action="process_add_product.php" method="POST">
            <input type="text" name="title" placeholder="Product Title" required>
            <textarea name="description" placeholder="Description"></textarea>
            <input type="number" step="0.01" name="price" placeholder="Price" required>
            <input type="text" name="image_path" placeholder="Image Filename (e.g. tool.jpg)" required>
            <button type="submit">Save Product</button>
        </form>
    </div>
</body>
</html>