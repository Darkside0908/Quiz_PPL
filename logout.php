<?php
/**
 * STUB: logout.php — pendamping stub index.php,
 * dipakai test untuk mereset sesi antar test case.
 */
session_start();
session_destroy();
header('Location: login.php');
exit;
