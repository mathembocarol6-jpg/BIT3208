<?php
session_start();

function verify_access($allowed_role) {
    if(!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true){
        header("location: index.php");
        exit;
    }
    if($_SESSION["role"] !== $allowed_role){
        header("location: unauthorized.php");
        exit;
    }
}
?>