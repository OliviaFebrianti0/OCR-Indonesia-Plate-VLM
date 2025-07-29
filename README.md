# OCR_Project – License Plate Recognition using VLM (LMStudio)
Proyek ini bertujuan untuk melakukan Optical Character Recognition (OCR) pada gambar plat nomor kendaraan menggunakan Visual Language Model (VLM) seperti llava-phi-3-mini, yang dijalankan melalui LMStudio dan diintegrasikan dengan Python.

Hasil prediksi dievaluasi menggunakan metrik Character Error Rate (CER) dan disimpan dalam file CSV untuk keperluan analisis lebih lanjut.

# Struktur Folder

OCR_Project/
├── ocr_predict.py                # Script pembuat ground_truth.csv dari file .txt (YOLO format)

├── generate_ground_truth.csv     # (Opsional) Output dari ocr_predict.py

├── results.csv                   # Hasil prediksi + nilai CER

├── test/

│   ├── test001_1.jpg             # Gambar input

│   ├── test001_1.txt             # File label YOLO (class_id dan x_center)

│   ├── ...

│   └── ground_truth.csv          # Hasil dari ocr_predict.py

# Instalasi & Persiapan
1. Install LM Studio
- Unduh dan install dari: https://lmstudio.ai/
- Setelah itu, load model multimodal seperti llava-phi-3-mini-gguf dan pastikan model yang digunakan mendukung input gambar dan prompt teks.

2. Jalankan Server LM Studio
Buka terminal (Command Prompt) dan jalankan 'cmd /c %USERPROFILE%/.lmstudio/bin/lms.exe bootstrap' dan 'lms server start'. Jika berhasil, akan muncul "Success! Server is now running on port 1234"
* Pastikan LMStudio berjalan di background selama eksekusi program Python.

4. Install Library Python
Masuk ke folder OCR_Project/ dan jalankan 'pip install requests pillow python-Levenshtein pandas'.

# Eksekusi Program
1. Persiapan Dataset
Letakkan file gambar .jpg dan label .txt (YOLO-style: class_id x_center ...) ke dalam folder test/.

2. Generate Ground Truth
Gunakan generate_ground_truth_csv.py untuk membuat file ground_truth.csv secara otomatis dari file .txt.  Hasil akan disimpan sebagai 'test/ground_truth.csv'.
* Contoh isi ground_truth.csv:
  image,ground_truth
  test001_1.jpg,B9140BCD
  test001_2.jpg,B2407UZO

2. Buat dan Jalankan Program Utama
Buatlah program 'ocr_predict.py' kemudian jalankan program tersebut. Program akan melakukan encode gambar ke Base64, mengirim ke LM Studio + prompt, menerima hasil prediksi, menghitung CER berdasarkan ground truth dan menyimpan hasil ke 'results.csv'.
File results.csv dengan format 'image,ground_truth,prediction,CER_score'.
* Contoh isi results.csv:
  test001_1.jpg,B9140BCD,B914OBCD,0.125
  test001_2.jpg,B2407UZO,B2407UZO,0.0

3. Kirim Gambar ke LMStudio untuk Prediksi
- Lakukan pengujian OCR dengan mengirim gambar satu per satu ke LMStudio menggunakan prompt berikut: "What is the license plate number shown in this image? Respond only with the plate number."
- Gunakan API http://localhost:1234/v1/chat/completions jika ingin otomatisasi via Python (gunakan Base64 image).

# Evaluasi: Character Error Rate (CER)
Rumus: CER = (S + D + I) / N
S: Substitusi karakter
D: Karakter yang dihapus (deletion)
I: Karakter yang disisipkan (insertion)
N: Total karakter pada ground truth
* Nilai CER menunjukkan seberapa jauh prediksi model dibandingkan label asli dan perhitungan CER dilakukan untuk setiap baris.
