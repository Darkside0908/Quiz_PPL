<?php
/**
 * STUB: index.php
 * ---------------------------------------------------------------
 * File ini adalah STUB yang dibuat untuk keperluan pengujian.
 * login.php dan register.php (TIDAK DIUBAH) melakukan redirect ke
 * index.php setelah berhasil, tetapi file ini tidak ada di
 * repository asli. Stub ini hanya menggantikan halaman dashboard
 * sesungguhnya agar alur login/register bisa diuji sampai selesai.
 * ---------------------------------------------------------------
 */
session_start();

if (!isset($_SESSION['username'])) {
    header('Location: login.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dashboard (Stub)</title>
</head>
<body>
    <h1 id="welcome">Selamat datang, <?= htmlspecialchars($_SESSION['username']); ?>!</h1>
    <p id="stub-info">Halaman ini adalah stub dashboard untuk pengujian.</p>
    <a id="logout" href="logout.php">Logout</a>
</body>
</html>
