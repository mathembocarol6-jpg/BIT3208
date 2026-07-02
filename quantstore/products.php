<?php
session_start();

if (!isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit();
}

$host = 'localhost';
$db   = 'quantstore_db';
$user = 'root';
$pass = '';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$db;charset=utf8", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $stmt = $pdo->query("SELECT * FROM products");
    $products = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Products - QuantStore</title>
    <link rel="stylesheet" href="style.css?v=<?php echo time(); ?>">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; display: flex; flex-direction: column; min-height: 100vh; }
        .dashboard-wrapper { display: flex; flex-direction: column; flex: 1; }
        .main-content { flex: 1; padding: 30px; }
        .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 2px solid #e0e7ff; padding-bottom: 10px; }
        .add-product-btn { background: linear-gradient(135deg, #4f46e5, #06b6d4); color: white; padding: 10px 20px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; text-decoration: none; }
        .product-grid { display: grid; grid-template-columns: 1fr; gap: 25px; }
        .product-card { background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); overflow: hidden; display: flex; flex-direction: column; border: 1px solid #e2e8f0; max-width: 350px; }
        .product-img-container { width: 100%; height: 200px; background-color: #f8fafc; display: flex; justify-content: center; align-items: center; overflow: hidden; }
        .product-img-container img { max-width: 100%; max-height: 100%; object-fit: contain; }
        .product-details { padding: 20px; display: flex; flex-direction: column; flex-grow: 1; }
        .product-title { font-size: 1.2rem; color: #1e1b4b; margin-bottom: 8px; }
        .product-desc { font-size: 0.95rem; color: #64748b; margin-bottom: 15px; flex-grow: 1; }
        .product-meta { display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 15px; border-top: 1px solid #f1f5f9; }
        .product-price { font-size: 1.25rem; font-weight: 700; color: #06b6d4; }
        .action-btns a { text-decoration: none; font-size: 0.9rem; font-weight: 600; margin-left: 10px; color: #4f46e5; }
        .action-btns a.delete { color: #ef4444; }
        @media (min-width: 600px) { .product-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (min-width: 992px) { .dashboard-wrapper { flex-direction: row; } .main-content { margin-left: 260px; padding: 40px; } }
    </style>
</head>
<body>

    <div class="dashboard-wrapper">
        <?php require_once 'header.php'; ?>

        <main class="main-content">
            <div class="page-header">
                <h1>Manage Products</h1>
                <button class="add-product-btn">+ Add New Product</button>
            </div>

            <div class="product-grid">
                <?php foreach ($products as $product): ?>
                <article class="product-card">
                    <div class="product-img-container">
                        <img src="<?php echo htmlspecialchars($product['image_path']); ?>" alt="<?php echo htmlspecialchars($product['title']); ?>">
                    </div>
                    <div class="product-details">
                        <h2 class="product-title"><?php echo htmlspecialchars($product['title']); ?></h2>
                        <p class="product-desc"><?php echo htmlspecialchars($product['description']); ?></p>
                        <div class="product-meta">
                            <span class="product-price">KES <?php echo number_format($product['price']); ?></span>
                            <div class="action-btns">
                                <a href="#">Edit</a>
                                <a href="#" class="delete">Delete</a>
                            </div>
                        </div>
                    </div>
                </article>
                <?php endforeach; ?>
            </div>
        </main>
    </div>

</body>
</html>