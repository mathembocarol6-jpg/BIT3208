<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Contact Us</title>
</head>
<body>
    <?php require_once 'header.php'; ?>
    <div class="container">
        <h2>Contact Us</h2>
        <form action="mailto:info@quantstore.com" method="POST" enctype="text/plain">
            <input type="text" name="name" placeholder="Your Name" required>
            <input type="email" name="email" placeholder="Your Email" required>
            <textarea name="message" placeholder="Your Message" rows="5" required style="width:100%; margin:8px 0;"></textarea>
            <button type="submit">Send Message</button>
        </form>
    </div>
</body>
</html>