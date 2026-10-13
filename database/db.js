const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const DB_PATH = path.join(__dirname, 'database.sqlite');

const db = new sqlite3.Database(DB_PATH, (err) => {
  if (err) {
    console.error('❌ Lỗi kết nối CSDL SQLite:', err.message);
  } else {
    console.log('✅ Đã kết nối cơ sở dữ liệu SQLite thành công tại:', DB_PATH);
  }
});

// Bật hỗ trợ ràng buộc khóa ngoại (Foreign Keys) trong SQLite
db.run('PRAGMA foreign_keys = ON');

// Các hàm tiện ích Wrapper Promise giúp viết code Controller async/await cực kỳ gọn gàng và dễ giải thích
const query = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
};

const get = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) reject(err);
      else resolve(row);
    });
  });
};

const run = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.run(sql, params, function (err) {
      if (err) reject(err);
      else resolve({ lastID: this.lastID, changes: this.changes });
    });
  });
};

const exec = (sql) => {
  return new Promise((resolve, reject) => {
    db.exec(sql, (err) => {
      if (err) reject(err);
      else resolve();
    });
  });
};

module.exports = {
  db,
  query,
  get,
  run,
  exec,
  DB_PATH
};
