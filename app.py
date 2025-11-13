from arima_api import app
import mysql.connector
import os

# ==========================================================
# 🔹 Ambil konfigurasi database dari file config.py (atau dari environment variable)
# ==========================================================
try:
    from config import DB_CONFIG
except ImportError:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "u611918462_keuangan_pmds"),
        "password": os.getenv("DB_PASSWORD", "Darussalamsukaraja_2021"),
        "database": os.getenv("u611918462_keuangan"),
    }

# ==========================================================
# 🔹 Tes koneksi ke database Hostinger
# ==========================================================
print("🔄 Menguji koneksi ke database...")
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    if conn.is_connected():
        print("✅ Koneksi berhasil ke database Hostinger!")
    conn.close()
except Exception as e:
    print("❌ Gagal konek ke database Hostinger:", e)

# ==========================================================
# 🔹 Menjalankan Flask App
# ==========================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Menjalankan Flask di port {port} ...")
    app.run(host="0.0.0.0", port=port, debug=True)
