# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_connection, init_db

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_123'  # Diperlukan untuk fitur flash message

# 2.1 READ: Menampilkan Semua Barang
@app.route('/')
def index():
    conn = get_connection()
    produk = conn.execute('SELECT * FROM produk').fetchall()
    conn.close()
    return render_template('index.html', produk=produk)

# 2.2 CREATE: Tambah Barang Baru
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama  = request.form['nama']
        harga = float(request.form['harga'])
        stok  = int(request.form['stok'])
        conn = get_connection()
        try:
            conn.execute(
                'INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)',
                (nama, harga, stok)
            )
            conn.commit()
            flash('Produk berhasil ditambahkan!', 'success')
        except Exception as e:
            flash(f'Gagal: {e}', 'error')
        finally:
            conn.close()
        return redirect(url_for('index'))
    return render_template('tambah.html') 

# 2.3 UPDATE: Edit Data Barang
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_connection()
    if request.method == 'POST':
        nama  = request.form['nama']
        harga = float(request.form['harga'])
        stok  = int(request.form['stok'])
        conn.execute(
            'UPDATE produk SET nama=?, harga=?, stok=? WHERE id=?',
            (nama, harga, stok, id)
        )
        conn.commit()
        conn.close()
        flash('Data berhasil diperbarui!', 'success')
        return redirect(url_for('index'))
    
    produk = conn.execute('SELECT * FROM produk WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', produk=produk) 

# 2.4 DELETE: Hapus Barang
@app.route('/hapus/<int:id>')
def hapus(id):
    conn = get_connection()
    conn.execute('DELETE FROM produk WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash('Produk berhasil dihapus.', 'info')
    return redirect(url_for('index')) 

# 2.5 Entry Point Aplikasi
if __name__ == '__main__':
    init_db()  # Menjalankan fungsi inisialisasi database
    app.run(debug=True)
