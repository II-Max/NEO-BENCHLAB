# 🚀 NEO BENCHLAB

**Nền Tảng Đánh Giá Hiệu Suất và Phân Tích Benchmarking Chuyên Nghiệp cho Hệ Thống Luyện Tập Lập Trình Online**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](README.md)

---

## 🎯 Giới Thiệu

**NEO BENCHLAB** là một nền tảng benchmarking và phân tích hiệu suất toàn diện, được thiết kế đặc biệt cho các hệ thống luyện tập lập trình online (Online Judge Systems). Nó cung cấp các công cụ mạnh mẽ để:

- ✅ **Đánh giá hiệu suất mã nguồn** với độ chính xác cao
- ✅ **Theo dõi tài nguyên hệ thống** (CPU, bộ nhớ) trong thời gian thực
- ✅ **Chạy kiểm tra tải** với cả triệu yêu cầu đồng thời
- ✅ **Hỗ trợ đa ngôn ngữ lập trình** (Python, C++, Java, Node.js)
- ✅ **Tạo báo cáo chi tiết** dưới các định dạng khác nhau
- ✅ **Cung cấp bảng điều khiển thời gian thực** với WebSocket

---

## 📋 Mục Lục

- [Giới Thiệu](#giới-thiệu)
- [Các Tính Năng](#các-tính-năng)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt-nhanh)
- [Khởi Động](#khởi-động)
- [Cấu Trúc Dự Án](#cấu-trúc-dự-án)

---

## ✨ Các Tính Năng

### 🔥 Tính Năng Cốt Lõi

- ✅ **Biên Dịch Đa Ngôn Ngữ**: Hỗ trợ tự động biên dịch cho C++, Java
- ✅ **Thực Thi Nhanh**: Hỗ trợ Python, Node.js không cần biên dịch
- ✅ **Giám Sát Tài Nguyên**: Theo dõi CPU & bộ nhớ trong thời gian thực
- ✅ **Kiểm Tra Tải**: Chạy benchmark với tải công việc đồng thời
- ✅ **Hộp Cát (Sandbox)**: Môi trường thực thi an toàn
- ✅ **Báo Cáo JSON/CSV**: Xuất kết quả dưới nhiều định dạng
- ✅ **WebSocket Real-time**: Cập nhật trực tiếp cho bảng điều khiển
- ✅ **Xử Lý Lỗi Toàn Diện**: Phân loại ngoại lệ tùy chỉnh

---

## 💻 Yêu Cầu Hệ Thống

### Tối Thiểu
- Python 3.10+
- RAM: 2GB
- Đĩa: 1GB

### Khuyến Nghị
- Python 3.11+
- RAM: 4GB+
- Ubuntu 20.04+ (hoặc macOS/Windows)

### Trình Biên Dịch Optional
```bash
# Để chạy C++
apt-get install build-essential

# Để chạy Java
apt-get install default-jdk

# Để chạy Node.js
apt-get install nodejs npm
```

---

## 🛠️ Cài Đặt Nhanh

### 1. Clone Repository
```bash
git clone https://github.com/II-Max/NEO-BENCHLAB.git
cd NEO-BENCHLAB
```

### 2. Tạo Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# hoặc
venv\Scripts\activate     # Windows
```

### 3. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### 4. Xác Minh Cài Đặt
```bash
python3 -c "from app.main import app; print('✓ Installation successful')"
```

---

## 🚀 Khởi Động

### Chế Độ Phát Triển
```bash
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Chế Độ Sản Xuất
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Với Docker
```bash
docker-compose up --build
```

### Truy Cập
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Endpoints

| Endpoint | Phương Thức | Mô Tả |
|----------|-----------|-------|
| `/system/health` | GET | Kiểm tra sức khỏe dịch vụ |
| `/stats` | GET | Thống kê hệ thống (CPU, RAM) |
| `/benchmarks` | GET | Danh sách benchmark khả dụng |
| `/benchmark/run` | POST | Chạy benchmark cho mã nguồn |
| `/reports` | GET | Danh sách báo cáo gần đây |
| `/dashboard/status` | GET | Trạng thái bảng điều khiển |

### Ví Dụ

```bash
# Chạy benchmark Python
curl -X POST http://localhost:8000/benchmark/run \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "source": "print(\"Hello\")\nprint(sum(range(1, 101)))"
  }'
```

---

## 📁 Cấu Trúc Dự Án

```
NEO-BENCHLAB/
├── app/
│   ├── benchmark/         # Động cơ benchmarking
│   │   ├── runner.py      # Logic điều phối
│   │   ├── monitor.py     # Giám sát tài nguyên
│   │   ├── compiler.py    # Biên dịch mã
│   │   ├── executor.py    # Thực thi mã
│   │   ├── stress.py      # Kiểm tra tải
│   │   └── ...
│   ├── judge/             # Hộp cát thực thi
│   │   ├── compiler.py    # Giao diện biên dịch
│   │   ├── executor.py    # Động cơ thực thi
│   │   ├── languages.py   # Cấu hình ngôn ngữ
│   │   └── ...
│   ├── dashboard/         # Bảng điều khiển
│   │   ├── api.py         # REST endpoints
│   │   └── websocket.py   # WebSocket
│   ├── utils/             # Tiện ích chung
│   │   ├── config.py      # Cấu hình
│   │   ├── logger.py      # Logging
│   │   └── ...
│   └── main.py            # Điểm vào
├── requirements.txt       # Dependencies
├── docker-compose.yml     # Docker config
├── QUICK_START.md         # Hướng dẫn nhanh
└── venv/                  # Môi trường ảo
```

---

## 📝 Các Ngôn Ngữ Hỗ Trợ

| Ngôn Ngữ | Trạng Thái | Biên Dịch |
|---------|-----------|----------|
| Python | ✅ | Không |
| C++ | ✅ | Có |
| Java | ✅ | Có |
| Node.js | ✅ | Không |

---

## ⚙️ Cấu Hình

Chỉnh sửa `app/utils/config.py`:

```python
@dataclass
class AppConfig:
    enable_stress_test: bool = True      # Bật kiểm tra tải
    threads: int = 4                     # Số luồng
    stress_requests: int = 50            # Số yêu cầu tải
    report_json: bool = True             # Xuất JSON
    report_csv: bool = True              # Xuất CSV
    timeout_seconds: int = 10            # Giới hạn thời gian
```

---

## 🤝 Đóng Góp

Chúng tôi rất hoan nghênh các đóng góp!

1. Fork repository
2. Tạo branch: `git checkout -b feature/YourFeature`
3. Commit: `git commit -m 'Add YourFeature'`
4. Push: `git push origin feature/YourFeature`
5. Mở Pull Request

---

## 📞 Hỗ Trợ

- **Issues**: [GitHub Issues](https://github.com/II-Max/NEO-BENCHLAB/issues)
- **Discussions**: [GitHub Discussions](https://github.com/II-Max/NEO-BENCHLAB/discussions)
- **Documentation**: [QUICK_START.md](QUICK_START.md)

---

## 📄 Giấy Phép

MIT License - Xem [LICENSE](LICENSE) để biết chi tiết

---

## 📊 Thống Kê

- **Modules**: 24 Python files
- **API Endpoints**: 7 endpoints
- **Ngôn Ngữ Hỗ Trợ**: 4 ngôn ngữ
- **Status**: ✅ Production Ready

---

**Version**: 1.0.0 | **Last Updated**: 2026-05-13

*Được phát triển bởi NEO Team* 🚀
