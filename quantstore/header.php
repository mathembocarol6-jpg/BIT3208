<?php
$current_page = basename($_SERVER['PHP_SELF']);
?>
<div class="sidebar">
    <div class="logo-box">
        <video width="100%" autoplay loop muted playsinline>
            <source src="logo.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    <ul class="nav-links">
        <li><a href="dashboard.php" class="<?php echo ($current_page == 'dashboard.php') ? 'active' : ''; ?>">Dashboard</a></li>
        <li><a href="products.php" class="<?php echo ($current_page == 'products.php') ? 'active' : ''; ?>">Products</a></li>
        <li><a href="about.php" class="<?php echo ($current_page == 'about.php') ? 'active' : ''; ?>">About</a></li>
        <li><a href="profile.php" class="<?php echo ($current_page == 'profile.php') ? 'active' : ''; ?>">Profile</a></li>
        <li><a href="logout.php" style="color: #ef4444;">Logout</a></li>
    </ul>
</div>