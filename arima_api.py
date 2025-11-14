from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import mysql.connector
from pmdarima import auto_arima
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ⚙️ KONFIGURASI DATABASE (FIXED)
DB_CONFIG = {
    "host": "srv1416.hstgr.io",  
    "user": "u611918462_keuangan_pmds",
    "password": "Darussalamsukaraja_2021",
    "database": "u611918462_keuangan"
}

# --- tes koneksi ke database (FIXED) ---
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("✅ Koneksi berhasil ke database Hostinger")
    conn.close()
except Exception as e:
    print("❌ Gagal konek:", e)


# ==========================================================
# 🔹 Ambil data agregat dari DB (PONDOK)
# ==========================================================
def fetch_aggregates(filter_mode):
    cnx = mysql.connector.connect(**DB_CONFIG)
    cur = cnx.cursor(dictionary=True)

    if filter_mode == 'bulan':
        q_masuk = """
            SELECT DATE_FORMAT(tanggal_masuk, '%Y-%m') AS periode,
                   SUM(nominal_masuk_uang_pondok) AS total
            FROM rincian_uang_pondok
            GROUP BY periode ORDER BY periode
        """
        q_keluar = """
            SELECT DATE_FORMAT(tanggal_pengeluaran, '%Y-%m') AS periode,
                   SUM(nominal_keluar_uang_pondok) AS total
            FROM rincian_keluar_uang_pondok
            GROUP BY periode ORDER BY periode
        """
    elif filter_mode == 'tahun':
        q_masuk = """
            SELECT YEAR(tanggal_masuk) AS periode,
                   SUM(nominal_masuk_uang_pondok) AS total
            FROM rincian_uang_pondok
            GROUP BY periode ORDER BY periode
        """
        q_keluar = """
            SELECT YEAR(tanggal_pengeluaran) AS periode,
                   SUM(nominal_keluar_uang_pondok) AS total
            FROM rincian_keluar_uang_pondok
            GROUP BY periode ORDER BY periode
        """
    else:
        q_masuk = """
            SELECT DATE(tanggal_masuk) AS periode,
                   SUM(nominal_masuk_uang_pondok) AS total
            FROM rincian_uang_pondok
            GROUP BY periode ORDER BY periode
        """
        q_keluar = """
            SELECT DATE(tanggal_pengeluaran) AS periode,
                   SUM(nominal_keluar_uang_pondok) AS total
            FROM rincian_keluar_uang_pondok
            GROUP BY periode ORDER BY periode
        """

    cur.execute(q_masuk)
    rows_m = cur.fetchall()
    cur.execute(q_keluar)
    rows_k = cur.fetchall()
    cur.close()
    cnx.close()

    df_m = pd.DataFrame(rows_m)
    df_k = pd.DataFrame(rows_k)

    if df_m.empty and df_k.empty:
        return pd.DataFrame(columns=['periode', 'masuk', 'keluar'])

    df = pd.merge(df_m, df_k, on='periode', how='outer', suffixes=('_masuk', '_keluar')).fillna(0)
    if 'total_masuk' in df.columns:
        df = df.rename(columns={'total_masuk': 'masuk'})
    if 'total_keluar' in df.columns:
        df = df.rename(columns={'total_keluar': 'keluar'})

    return df[['periode', 'masuk', 'keluar']]


# ==========================================================
# 🔹 Ambil data agregat Unit Usaha
# ==========================================================
def fetch_aggregates_unit_usaha(filter_mode):
    cnx = mysql.connector.connect(**DB_CONFIG)
    cur = cnx.cursor(dictionary=True)

    if filter_mode == 'bulan':
        q_masuk = """
            SELECT DATE_FORMAT(tanggal_pemasukan, '%Y-%m') AS periode,
                   SUM(nominal_masuk_uang_unit_usaha) AS total
            FROM rincian_uang_unit_usaha
            GROUP BY periode ORDER BY periode
        """
        q_keluar = """
            SELECT DATE_FORMAT(tanggal_pengeluaran, '%Y-%m') AS periode,
                   SUM(nominal_keluar_uang_unit_usaha) AS total
            FROM rincian_keluar_uang_unit_usaha
            GROUP BY periode ORDER BY periode
        """
    elif filter_mode == 'tahun':
        q_masuk = """
            SELECT YEAR(tanggal_pemasukan) AS periode,
                   SUM(nominal_masuk_uang_unit_usaha) AS total
            FROM rincian_uang_unit_usaha
            GROUP BY periode ORDER BY periode
        """
        q_keluar = """
            SELECT YEAR(tanggal_pengeluaran) AS periode,
                   SUM(nominal_keluar_uang_unit_usaha) AS total
            FROM rincian_keluar_uang_unit_usaha
            GROUP BY periode ORDER BY periode
        """
    else:
        q_masuk = """
            SELECT DATE(tanggal_pemasukan) AS periode,
                   SUM(nominal_masuk_uang_unit_usaha) AS total
            FROM rincian_uang_unit_usaha
            GROUP BY periode ORDER BY periode
        """
        q_keluar = """
            SELECT DATE(tanggal_pengeluaran) AS periode,
                   SUM(nominal_keluar_uang_unit_usaha) AS total
            FROM rincian_keluar_uang_unit_usaha
            GROUP BY periode ORDER BY periode
        """

    cur.execute(q_masuk)
    rows_m = cur.fetchall()
    cur.execute(q_keluar)
    rows_k = cur.fetchall()
    cur.close()
    cnx.close()

    df_m = pd.DataFrame(rows_m)
    df_k = pd.DataFrame(rows_k)

    if df_m.empty and df_k.empty:
        return pd.DataFrame(columns=['periode', 'masuk', 'keluar'])

    df = pd.merge(df_m, df_k, on='periode', how='outer', suffixes=('_masuk', '_keluar')).fillna(0)
    if 'total_masuk' in df.columns:
        df = df.rename(columns={'total_masuk': 'masuk'})
    if 'total_keluar' in df.columns:
        df = df.rename(columns={'total_keluar': 'keluar'})

    return df[['periode', 'masuk', 'keluar']]


# ==========================================================
# 🔹 Ambil data agregat LAZISWAF
# ==========================================================
def fetch_aggregates_laziswaf(filter_mode):
    cnx = mysql.connector.connect(**DB_CONFIG)
    cur = cnx.cursor(dictionary=True)

    if filter_mode == 'bulan':
        q_masuk = """
            SELECT DATE_FORMAT(tanggal_pemasukan, '%Y-%m') AS periode,
                   SUM(nominal_masuk_uang_laziswaf) AS total
            FROM rincian_uang_laziswaf
            GROUP BY periode ORDER BY periode
        """
        q_keluar = """
            SELECT DATE_FORMAT(tanggal_pengeluaran, '%Y-%m') AS periode,
                   SUM(nominal_keluar_uang_laziswaf) AS total
            FROM rincian_keluar_uang_laziswaf
            GROUP BY periode ORDER BY periode
        """
    elif filter_mode == 'tahun':
        q_masuk = """
            SELECT YEAR(tanggal_pemasukan) AS periode,
                   SUM(nominal_masuk_uang_laziswaf) AS total
            FROM rincian_uang_laziswaf
            GROUP BY periode ORDER BY periode
        """
        q_keluar = """
            SELECT YEAR(tanggal_pengeluaran) AS periode,
                   SUM(nominal_keluar_uang_laziswaf) AS total
            FROM rincian_keluar_uang_laziswaf
            GROUP BY periode ORDER BY periode
        """
    else:
        q_masuk = """
            SELECT DATE(tanggal_pemasukan) AS periode,
                   SUM(nominal_masuk_uang_laziswaf) AS total
            FROM rincian_uang_laziswaf
            GROUP BY periode ORDER BY periode
        """
        q_keluar = """
            SELECT DATE(tanggal_pengeluaran) AS periode,
                   SUM(nominal_keluar_uang_laziswaf) AS total
            FROM rincian_keluar_uang_laziswaf
            GROUP BY periode ORDER BY periode
        """

    cur.execute(q_masuk)
    rows_m = cur.fetchall()
    cur.execute(q_keluar)
    rows_k = cur.fetchall()
    cur.close()
    cnx.close()

    df_m = pd.DataFrame(rows_m)
    df_k = pd.DataFrame(rows_k)

    if df_m.empty and df_k.empty:
        return pd.DataFrame(columns=['periode', 'masuk', 'keluar'])

    df = pd.merge(df_m, df_k, on='periode', how='outer', suffixes=('_masuk', '_keluar')).fillna(0)
    if 'total_masuk' in df.columns:
        df = df.rename(columns={'total_masuk': 'masuk'})
    if 'total_keluar' in df.columns:
        df = df.rename(columns={'total_keluar': 'keluar'})

    return df[['periode', 'masuk', 'keluar']]


# ==========================================================
# 🔹 Fungsi Prediksi ARIMA
# ==========================================================
def forecast_series(y_series, periods, seasonal=False, m=1):
    if len(y_series.dropna()) < 3 or y_series.sum() == 0:
        return [0.0] * periods
    try:
        model = auto_arima(
            y_series,
            seasonal=seasonal,
            m=m,
            suppress_warnings=True,
            error_action='ignore',
            stepwise=True
        )
        fc = model.predict(n_periods=periods)
        return [float(x) for x in fc]
    except Exception:
        avg = float(y_series.mean() if len(y_series) > 0 else 0)
        return [avg] * periods


# ==========================================================
# 🔹 Buat label periode berikutnya
# ==========================================================
def next_period_labels(last_label, count, mode):
    labels = []
    try:
        if mode == 'hari':
            base = datetime.strptime(str(last_label), '%Y-%m-%d')
            for i in range(1, count + 1):
                labels.append((base + pd.Timedelta(days=i)).strftime('%Y-%m-%d'))
        elif mode == 'bulan':
            base = datetime.strptime(str(last_label), '%Y-%m')
            for i in range(1, count + 1):
                labels.append((base + pd.DateOffset(months=i)).strftime('%Y-%m'))
        else:
            year = int(str(last_label)[:4])
            for i in range(1, count + 1):
                labels.append(str(year + i))
    except Exception as e:
        print("Error next_period_labels:", e, last_label, mode)
    return labels


# ==========================================================
# 🔹 Endpoint Grafik Pondok
# ==========================================================
@app.route('/api/grafik')
def api_grafik():
    return generate_response(fetch_aggregates)


# ==========================================================
# 🔹 Endpoint Grafik Unit Usaha
# ==========================================================
@app.route('/api/grafik_unit_usaha')
def api_grafik_unit_usaha():
    return generate_response(fetch_aggregates_unit_usaha)


# ==========================================================
# 🔹 Endpoint Grafik LAZISWAF
# ==========================================================
@app.route('/api/grafik_laziswaf')
def api_grafik_laziswaf():
    return generate_response(fetch_aggregates_laziswaf)


# ==========================================================
# 🔹 RESPON UTAMA (tidak diubah)
# ==========================================================
def generate_response(fetch_func):
    mode = request.args.get('filter', 'hari')
    predict_count = 7 if mode == 'hari' else (6 if mode == 'bulan' else 5)

    df = fetch_func(mode)

    if df.empty:
        return jsonify({
            'status': 'error',
            'message': 'Data tidak mencukupi untuk menampilkan grafik dan prediksi.',
            'label': [], 'masuk': [], 'keluar': [],
            'prediksi_label': [], 'prediksi_masuk': [], 'prediksi_keluar': []
        })

    df['masuk'] = pd.to_numeric(df['masuk'], errors='coerce').fillna(0)
    df['keluar'] = pd.to_numeric(df['keluar'], errors='coerce').fillna(0)

    if len(df) < 3:
        return jsonify({
            'status': 'error',
            'message': 'Data historis kurang dari 3 periode sehingga prediksi ARIMA tidak dapat dilakukan.',
            'label': df['periode'].astype(str).tolist(),
            'masuk': df['masuk'].astype(float).tolist(),
            'keluar': df['keluar'].astype(float).tolist(),
            'prediksi_label': [],
            'prediksi_masuk': [],
            'prediksi_keluar': []
        })

    seasonal = True if mode == 'bulan' else False
    m = 12 if mode == 'bulan' else 1

    fc_masuk = forecast_series(df['masuk'], predict_count, seasonal, m)
    fc_keluar = forecast_series(df['keluar'], predict_count, seasonal, m)

    last_label = df['periode'].iloc[-1]
    pred_labels = next_period_labels(last_label, predict_count, mode)

    return jsonify({
        'status': 'success',
        'label': df['periode'].astype(str).tolist(),
        'masuk': df['masuk'].astype(float).tolist(),
        'keluar': df['keluar'].astype(float).tolist(),
        'prediksi_label': pred_labels,
        'prediksi_masuk': fc_masuk,
        'prediksi_keluar': fc_keluar
    })


# ==========================================================
# 🔹 Jalankan server Flask
# ==========================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
