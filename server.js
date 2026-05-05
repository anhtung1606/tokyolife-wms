const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());
// Phục vụ file tĩnh trong thư mục public
app.use(express.static(path.join(__dirname, 'public')));

// Cấu hình kết nối PostgreSQL
// Lấy DATABASE_URL từ biến môi trường (Render sẽ cung cấp)
// Nếu không có (chạy local), dùng URL mặc định
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgres://localhost:5432/tokyolife',
  ssl: process.env.DATABASE_URL ? { rejectUnauthorized: false } : false
});

// Các bảng dữ liệu (tương đương với các store trong IndexedDB)
const stores = ['users', 'suppliers', 'products', 'imports', 'exports'];

// API: Lấy tất cả dữ liệu của một bảng
app.get('/api/:store', async (req, res) => {
  const { store } = req.params;
  if (!stores.includes(store)) return res.status(400).send('Invalid store');
  try {
    const result = await pool.query(`SELECT data FROM ${store}`);
    res.json(result.rows.map(r => r.data));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// API: Lấy dữ liệu theo ID
app.get('/api/:store/:id', async (req, res) => {
  const { store, id } = req.params;
  if (!stores.includes(store)) return res.status(400).send('Invalid store');
  try {
    const result = await pool.query(`SELECT data FROM ${store} WHERE id = $1`, [id]);
    if (result.rows.length === 0) return res.json(null);
    res.json(result.rows[0].data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// API: Thêm hoặc Cập nhật dữ liệu
app.put('/api/:store', async (req, res) => {
  const { store } = req.params;
  if (!stores.includes(store)) return res.status(400).send('Invalid store');
  
  const obj = req.body;
  if (!obj.id) return res.status(400).send('Missing id');
  
  try {
    // Lưu dưới dạng JSONB để linh hoạt như IndexedDB
    await pool.query(
      `INSERT INTO ${store} (id, data) VALUES ($1, $2)
       ON CONFLICT (id) DO UPDATE SET data = $2`,
      [obj.id, obj]
    );
    res.json(obj);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// API: Xóa dữ liệu
app.delete('/api/:store/:id', async (req, res) => {
  const { store, id } = req.params;
  if (!stores.includes(store)) return res.status(400).send('Invalid store');
  try {
    await pool.query(`DELETE FROM ${store} WHERE id = $1`, [id]);
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
