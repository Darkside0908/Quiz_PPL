"""
Konfigurasi & fixture pytest (berperan sebagai TEST DRIVER).

- Fixture `driver` menyiapkan Chrome headless via Selenium.
- Fixture `db` membuka koneksi langsung ke MySQL (untuk verifikasi
  data / back-door verification dan pembersihan data uji). Nilai
  default di sini SENGAJA disamakan dengan kredensial hardcode di
  koneksi.php (host=localhost/127.0.0.1, user=root, password kosong,
  db=quiz_pengupil) — koneksi.php tidak dimodifikasi sama sekali,
  environment pengujian yang menyesuaikan diri ke koneksi.php.
"""
import os
import uuid

import pymysql
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

# Kredensial user hasil seeding (tests/seed.php)
SEED_USERNAME = "testuser"
SEED_PASSWORD = "Password123!"

# Sama persis dengan yang di-hardcode koneksi.php
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "quiz_pengupil",
}


@pytest.fixture
def driver():
    """Selenium WebDriver: Chrome headless, fresh session per test."""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    drv = webdriver.Chrome(options=opts)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


@pytest.fixture
def db():
    """Koneksi DB langsung untuk verifikasi & cleanup data uji."""
    conn = pymysql.connect(**DB_CONFIG)
    yield conn
    conn.close()


@pytest.fixture
def unique_user():
    """Data user unik agar test register bisa diulang tanpa bentrok."""
    suffix = uuid.uuid4().hex[:8]
    return {
        "name": f"User Uji {suffix}",
        "email": f"uji_{suffix}@example.com",
        "username": f"uji_{suffix}",
        "password": "RahasiaUji123!",
    }
