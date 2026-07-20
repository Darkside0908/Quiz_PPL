"""
Test case modul REGISTER (register.php) — file register.php TIDAK diubah.

TC-R01  Register valid                    -> redirect ke index.php, user masuk DB
TC-R02  Password != Re-Password           -> pesan 'Password tidak sama !!'
TC-R03  Username sudah terdaftar          -> pesan 'Username sudah terdaftar !!'
TC-R04  Field kosong                      -> pesan 'Data tidak boleh kosong !!'
TC-R05  End-to-end: register lalu login   -> akun baru bisa dipakai login
TC-R06  Kolom name tersimpan benar        -> XFAIL (bug asli: variabel $nama,
                                              didokumentasikan, TIDAK diperbaiki)
"""
import pytest
from selenium.webdriver.common.by import By

from conftest import BASE_URL, SEED_USERNAME


def do_register(driver, name, email, username, password, repassword):
    driver.get(f"{BASE_URL}/register.php")
    driver.find_element(By.ID, "name").send_keys(name)
    driver.find_element(By.ID, "InputEmail").send_keys(email)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "InputPassword").send_keys(password)
    driver.find_element(By.ID, "InputRePassword").send_keys(repassword)
    driver.find_element(By.NAME, "submit").click()


def get_alert_text(driver):
    alerts = driver.find_elements(By.CSS_SELECTOR, ".alert-danger")
    return alerts[0].text if alerts else ""


def get_validate_text(driver):
    msgs = driver.find_elements(By.CSS_SELECTOR, "p.text-danger")
    return " ".join(m.text for m in msgs)


def cleanup_user(db, username):
    with db.cursor() as cur:
        cur.execute("DELETE FROM users WHERE username = %s", (username,))
    db.commit()


class TestRegister:

    def test_tc_r01_register_valid(self, driver, db, unique_user):
        """TC-R01: semua field valid -> redirect index.php & user ada di DB."""
        u = unique_user
        try:
            do_register(driver, u["name"], u["email"], u["username"],
                        u["password"], u["password"])
            assert driver.current_url.endswith("index.php"), \
                f"Harusnya redirect ke index.php, sekarang di {driver.current_url}"
            with db.cursor() as cur:
                cur.execute("SELECT username FROM users WHERE username = %s",
                            (u["username"],))
                assert cur.fetchone() is not None, "User tidak tersimpan di DB"
        finally:
            cleanup_user(db, u["username"])

    def test_tc_r02_password_tidak_sama(self, driver, unique_user):
        """TC-R02: password & re-password beda -> pesan validasi."""
        u = unique_user
        do_register(driver, u["name"], u["email"], u["username"],
                    u["password"], u["password"] + "beda")
        assert "index.php" not in driver.current_url
        assert "Password tidak sama" in get_validate_text(driver)

    def test_tc_r03_username_sudah_terdaftar(self, driver, unique_user):
        """TC-R03: pakai username seed yang sudah ada -> ditolak."""
        u = unique_user
        do_register(driver, u["name"], u["email"], SEED_USERNAME,
                    u["password"], u["password"])
        assert "index.php" not in driver.current_url
        assert "Username sudah terdaftar" in get_alert_text(driver)

    def test_tc_r04_field_kosong(self, driver):
        """TC-R04: submit form kosong -> validasi field kosong."""
        driver.get(f"{BASE_URL}/register.php")
        driver.find_element(By.NAME, "submit").click()
        assert "Data tidak boleh kosong" in get_alert_text(driver)

    def test_tc_r05_register_lalu_login(self, driver, db, unique_user):
        """TC-R05 (end-to-end): akun hasil register harus bisa login."""
        u = unique_user
        try:
            do_register(driver, u["name"], u["email"], u["username"],
                        u["password"], u["password"])
            driver.delete_all_cookies()
            driver.get(f"{BASE_URL}/login.php")
            driver.find_element(By.ID, "username").send_keys(u["username"])
            driver.find_element(By.ID, "InputPassword").send_keys(u["password"])
            driver.find_element(By.NAME, "submit").click()
            assert driver.current_url.endswith("index.php"), \
                "Akun hasil register tidak bisa dipakai login"
        finally:
            cleanup_user(db, u["username"])

    @pytest.mark.xfail(reason="Bug asli di register.php: INSERT memakai variabel "
                              "$nama yang tidak terdefinisi (harusnya $name), "
                              "sehingga kolom name selalu kosong. Sesuai instruksi, "
                              "source code TIDAK diperbaiki — hanya didokumentasikan.")
    def test_tc_r06_kolom_name_tersimpan(self, driver, db, unique_user):
        """TC-R06: nama yang diinput harus tersimpan di kolom name."""
        u = unique_user
        try:
            do_register(driver, u["name"], u["email"], u["username"],
                        u["password"], u["password"])
            with db.cursor() as cur:
                cur.execute("SELECT name FROM users WHERE username = %s",
                            (u["username"],))
                row = cur.fetchone()
                assert row is not None
                assert row[0] == u["name"], \
                    f"Kolom name berisi '{row[0]}', harusnya '{u['name']}'"
        finally:
            cleanup_user(db, u["username"])
