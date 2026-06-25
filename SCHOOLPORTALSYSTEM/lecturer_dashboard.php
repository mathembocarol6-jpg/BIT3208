<?php
require_once 'auth_check.php';
verify_access('Lecturer');
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Lecturer Terminal Workspace</title>
    <style>
        body { font-family: sans-serif; background-color: #f0f9ff; margin: 0; padding: 30px; }
        .nav { display: flex; justify-content: space-between; align-items: center; background: white; padding: 15px 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .container { margin-top: 30px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .badge { background-color: #e0f2fe; color: #0369a1; padding: 6px 12px; border-radius: 20px; font-weight: bold; }
        .logout-btn { background-color: #dc2626; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; }
    </style>
</head>
<body>
    <div class="nav">
        <h2>🔬 Faculty Lecturer Workspace</h2>
        <div>
            <span class="badge">Faculty Lecturer</span>
            <a href="logout.php" class="logout-btn">Terminate Session</a>
        </div>
    </div>
    <div class="container">
        <h1>Welcome back, Professor <?php echo htmlspecialchars($_SESSION["full_name"]); ?>!</h1>
        <h3>Assigned Classroom Operations</h3>
        <ul>
            <li>Student Roster Attendance Matrices</li>
            <li>Assignment Evaluation and Grading Matrix Logs</li>
            <li>Syllabus Course Content Upload Streams</li>
        </ul>
    </div>
</body>
</html>