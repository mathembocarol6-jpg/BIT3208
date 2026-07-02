<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contact Us | Mikadocake</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <?php include 'header.php'; ?>

    <div class="full-bg">
        <div style="max-width: 600px; margin: 0 auto; background: rgba(0, 0, 0, 0.7); padding: 30px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.2);">
            <h1 style="text-align: center;">Contact Us</h1>
            <form action="process_contact.php" method="POST">
                <input type="text" name="name" placeholder="Your Name" style="width: 100%; padding: 10px; margin-bottom: 10px;" required>
                <input type="email" name="email" placeholder="Your Email" style="width: 100%; padding: 10px; margin-bottom: 10px;" required>
                <textarea name="message" placeholder="Your Message" style="width: 100%; padding: 10px; margin-bottom: 10px; height: 100px;" required></textarea>
                <button type="submit" style="width: 100%; padding: 10px; background: #d63384; color: white; border: none; cursor: pointer;">Send Message</button>
            </form>
        </div>
    </div>

</body>
</html>