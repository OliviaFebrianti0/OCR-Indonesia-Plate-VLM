import requests
import pandas as pd
import base64
import mimetypes
import os
from tqdm import tqdm
from Levenshtein import distance as levenshtein_distance

# === Konfigurasi LM Studio ===
LMSTUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "llava-phi-3-mini"  

# === Fungsi hitung CER ===
def calculate_cer(ground_truth, prediction):
    gt = ground_truth.strip().upper()
    pred = prediction.strip().upper()
    N = max(len(gt), 1)  # Hindari pembagian 0
    edit_distance = levenshtein_distance(gt, pred)
    cer = edit_distance / N
    return cer

# === Encode gambar ke base64 ===
def encode_image_to_base64(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "image/jpeg"  # default
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

# === Fungsi kirim permintaan ke LMStudio ===
def ocr_plate(image_path):
    image_b64 = encode_image_to_base64(image_path)
    prompt = "What is the license plate number shown in this image? Respond only with the plate number."

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_b64}},
                    {"type": "text", "text": prompt}
                ]
            }
        ],
        "temperature": 0.2,
        "stream": False
    }

    try:
        response = requests.post(LMSTUDIO_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip().replace(" ", "").upper()
    except Exception as e:
        print(f"❌ Gagal OCR untuk {image_path}: {e}")
        return "ERROR"

# === MAIN ===
def main():
    df = pd.read_csv("test/ground_truth.csv")  

    results = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Evaluasi Plat Nomor"):
        image_path = os.path.join("test", row["image"])
        ground_truth = row["ground_truth"]

        prediction = ocr_plate(image_path)
        cer = calculate_cer(ground_truth, prediction) if prediction != "ERROR" else 1.0

        results.append({
            "image": row["image"],
            "ground_truth": ground_truth,
            "prediction": prediction,
            "CER_score": round(cer, 4)
        })

    result_df = pd.DataFrame(results)
    result_df.to_csv("results.csv", index=False)
    print("\n✅ Selesai! Hasil disimpan ke 'results.csv'")

    avg_cer = result_df["CER_score"].mean()
    print(f"🎯 Rata-rata CER: {avg_cer:.4f}")

if __name__ == "__main__":
    main()
