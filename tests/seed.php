<?php
/**
 * DRIVER: seed.php
 * Test driver untuk menyiapkan data uji (test fixture).
 * Menggunakan koneksi.php ASLI (tidak dimodifikasi) — environment
 * pengujian (lokal maupun CI) dikonfigurasi agar cocok dengan
 * kredensial hardcode di koneksi.php (host=localhost, user=root,
 * password kosong, db=quiz_pengupil), bukan sebaliknya.
 *
 * Membuat user 'testuser' dengan password yang diketahui, karena
 * password user bawaan database dump tidak diketahui (hash bcrypt).
 *
 * Jalankan: php tests/seed.php
 */
require(__DIR__ . '/../koneksi.php');

$username = 'testuser';
$name     = 'Test User';
$email    = 'testuser@example.com';
$plain    = 'Password123!';

$cek = mysqli_query($con, "SELECT id FROM users WHERE username = '$username'");
if (mysqli_num_rows($cek) > 0) {
    echo "Seed: user '$username' sudah ada, skip.\n";
    exit(0);
}

$hash  = password_hash($plain, PASSWORD_DEFAULT);
$query = "INSERT INTO users (username, name, email, password)
          VALUES ('$username', '$name', '$email', '$hash')";

if (mysqli_query($con, $query)) {
    echo "Seed: user '$username' berhasil dibuat.\n";
} else {
    echo "Seed GAGAL: " . mysqli_error($con) . "\n";
    exit(1);
}
