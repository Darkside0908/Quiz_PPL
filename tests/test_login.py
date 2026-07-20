"""
Test case modul LOGIN (login.php) — file login.php TIDAK diubah.

TC-L01  Login valid                      -> redirect ke index.php
TC-L02  Password salah                   -> tetap di login.php
TC-L03  Username tidak terdaftar         -> muncul pesan error
TC-L04  Field kosong                     -> pesan 'Data tidak boleh kosong !!'
TC-L05  SQL injection                    -> login harus GAGAL
TC-L06  Input hanya spasi                -> dianggap kosong
"""
import pytest
from selenium.webdriver.common.by import By

from conftest import BASE_URL, SEED_USERNAME, SEED_PASSWORD


def do_login(driver, username, password):
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "InputPassword").send_keys(password)
    driver.find_element(By.NAME, "submit").click()


def get_alert_text(driver):
    alerts = driver.find_elements(By.CSS_SELECTOR, ".alert-danger")
    return alerts[0].text if alerts else ""


class TestLogin:

    def test_tc_l01_login_valid(self, driver):
        """TC-L01: username & password benar -> masuk dashboard."""
        do_login(driver, SEED_USERNAME, SEED_PASSWORD)
        assert driver.current_url.endswith("index.php"), \
            f"Harusnya redirect ke index.php, sekarang di {driver.current_url}"
        welcome = driver.find_element(By.ID, "welcome").text
        assert SEED_USERNAME in welcome

    def test_tc_l02_password_salah(self, driver):
        """TC-L02: password salah -> tidak boleh masuk dashboard.
        Catatan: aplikasi tidak menampilkan pesan error pada kasus ini
        (silent failure) — perilaku asli login.php, tidak diubah."""
        do_login(driver, SEED_USERNAME, "password_ngawur_999")
        assert "index.php" not in driver.current_url
        assert "login.php" in driver.current_url

    def test_tc_l03_username_tidak_terdaftar(self, driver):
        """TC-L03: username tak terdaftar -> muncul pesan error.
        Catatan: teks error aslinya 'Register User Gagal !!' (perilaku
        asli login.php, tidak diubah)."""
        do_login(driver, "user_tidak_ada_xyz", "apapun123")
        assert "index.php" not in driver.current_url
        assert get_alert_text(driver) != "", "Pesan error harus tampil"

    def test_tc_l04_field_kosong(self, driver):
        """TC-L04: submit tanpa isi apa pun -> validasi field kosong."""
        driver.get(f"{BASE_URL}/login.php")
        driver.find_element(By.NAME, "submit").click()
        assert "Data tidak boleh kosong" in get_alert_text(driver)

    def test_tc_l05_sql_injection(self, driver):
        """TC-L05: payload SQL injection tidak boleh bisa login."""
        do_login(driver, "' OR '1'='1' -- ", "' OR '1'='1")
        assert "index.php" not in driver.current_url, \
            "CELAH KEAMANAN: SQL injection berhasil login!"

    def test_tc_l06_input_hanya_spasi(self, driver):
        """TC-L06: input spasi saja harus dianggap kosong."""
        do_login(driver, "   ", "   ")
        assert "index.php" not in driver.current_url
        assert "Data tidak boleh kosong" in get_alert_text(driver)
