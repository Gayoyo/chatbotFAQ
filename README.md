🤖 Chatbot FAQ dengan Flask

Chatbot FAQ sederhana berbasis Flask dan TF-IDF yang mampu menjawab pertanyaan dari pengguna berdasarkan data yang disediakan. Sistem ini juga menyimpan riwayat percakapan dan memungkinkan admin menambahkan/mengedit/menghapus FAQ melalui antarmuka web.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)


🛠️ Fitur

- Chatbot berbasis TF-IDF dan cosine similarity
- Upload FAQ via form atau file CSV
- Manajemen FAQ: Tambah, Edit, Hapus
- Riwayat percakapan user-bot
- Antarmuka admin dan user terpisah



🚀 Cara Menjalankan

1. Clone repositori

bash
-git clone https://github.com/username/chatbot-faq.git
cd chatbot-faq
-pip install -r requirements.txt
-python chatbot.py
-Buka aplikasi di browser http://127.0.0.1:5000 (halaman admin)
-halaman chatbotFAQ http://127.0.0.1:5000/chat_ui
