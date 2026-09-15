"""
6000'e tamamlamak icin eklenecek 10 yeni ornek icin annotation yardimcisi.

Kullanim: asagidaki NEW_SAMPLES listesine gercek, siz/annotator ekibinizin
topladigi cumleleri + aspect terimlerini + polarity + category'yi girin.
Script tokenization (NLTK word_tokenize, paper'daki yontemle ayni) ve BIOS
etiket dizisini otomatik uretir, GitHub datasetiyle ayni semada bir CSV
satirina donusturur.

Aspect terimleri metinde GECTIGI GIBI (case-sensitive, boslukla) yazilmali;
script bunlari tokenize edilmis metin icinde bulup B/I/S/O atar.
"""
import ast
import csv
import sys

import nltk
for pkg in ("punkt", "punkt_tab"):
    try:
        nltk.data.find(f"tokenizers/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)
from nltk.tokenize import word_tokenize


def tokenize_tr(text):
    return word_tokenize(text, language="turkish")


def build_bios_labels(tokens, aspect_terms):
    """aspect_terms: orijinal metinde gectigi sirada aspect frazlari (str listesi).
    Her biri kendi ici tokenize edilip `tokens` icinde ardışık bir alt-dizi
    olarak aranir; bulunamazsa hata firlatir (yaziminizi kontrol edin)."""
    labels = ["O"] * len(tokens)
    lowered_tokens = [t.lower() for t in tokens]

    for phrase in aspect_terms:
        phrase_tokens = [t.lower() for t in tokenize_tr(phrase)]
        n = len(phrase_tokens)
        found = False
        for i in range(len(tokens) - n + 1):
            if lowered_tokens[i:i + n] == phrase_tokens:
                if n == 1:
                    labels[i] = "S"
                else:
                    labels[i] = "B"
                    for j in range(i + 1, i + n):
                        labels[j] = "I"
                found = True
                break
        if not found:
            raise ValueError(
                f"Aspect frazi bulunamadi: {phrase!r} -- metindeki yaziminla "
                f"birebir (bosluk/noktalama) eslesmiyor olabilir. Tokens: {tokens}"
            )
    return labels


def make_row(text, aspects, polarities, category, source):
    assert len(aspects) == len(polarities), "aspects ve polarities ayni uzunlukta olmali"
    tokens = tokenize_tr(text)
    labels = build_bios_labels(tokens, aspects)
    return {
        "text": text,
        "target": str(aspects),
        "polarity": str(polarities),
        "category": category,
        "tokens": str(tokens),
        "labels": str(labels),
        "source": source,
    }


# ============================================================
# BURAYA GERCEK, TOPLANMIS 10 ORNEGI GIRIN
# Her sozluk: text, aspects (metinde gectigi gibi), polarities, category, source
# ============================================================
NEW_SAMPLES = [
    {
        "text": "Üniversitenin kütüphane olanakları ve sessiz çalışma alanları harika ancak yemekhane menüleri çok yetersiz.",
        "aspects": ["kütüphane olanakları", "sessiz çalışma alanları", "yemekhane menüleri"],
        "polarities": ["positive", "positive", "negative"],
        "category": "education",
        "source": "LLM-generated",
    },
    {
        "text": "Hazırlık sınıfının yabancı dil eğitimi çok kaliteli fakat yerleşkenin şehir merkezine ulaşımı oldukça zor.",
        "aspects": ["yabancı dil eğitimi", "şehir merkezine ulaşımı"],
        "polarities": ["positive", "negative"],
        "category": "education",
        "source": "LLM-generated",
    },
    {
        "text": "Fizyoterapi merkezindeki tedavi ekipmanları yenilenmiş ancak personelin güler yüzü eksikti.",
        "aspects": ["tedavi ekipmanları", "personelin güler yüzü"],
        "polarities": ["positive", "negative"],
        "category": "health",
        "source": "LLM-generated",
    },
    {
        "text": "Poliklinikteki doktorların ilgi ve uzmanlığı harika ama online tahlil sonuç sistemi çok yavaş çalışıyor.",
        "aspects": ["doktorların ilgi ve uzmanlığı", "online tahlil sonuç sistemi"],
        "polarities": ["positive", "negative"],
        "category": "health",
        "source": "LLM-generated",
    },
    {
        "text": "Diyetisyenin sunduğu tarif çeşitliliği motivasyonu artırıyor fakat seans ücretleri öğrenci bütçesini zorluyor.",
        "aspects": ["tarif çeşitliliği", "seans ücretleri"],
        "polarities": ["positive", "negative"],
        "category": "health",
        "source": "LLM-generated",
    },
    {
        "text": "Online diyet danışmanlığının iletişim hızı harikaydı fakat kişiye özel listeler biraz tekrara düşüyordu.",
        "aspects": ["iletişim hızı", "kişiye özel listeler"],
        "polarities": ["positive", "negative"],
        "category": "health",
        "source": "LLM-generated",
    },
    {
        "text": "Fırının simit ve poğaça tazeliği gayet iyi ama ambalajlama ve hijyen konusunda biraz özen gösterilmeli.",
        "aspects": ["simit ve poğaça tazeliği", "ambalajlama ve hijyen"],
        "polarities": ["positive", "negative"],
        "category": "daily_life",
        "source": "LLM-generated",
    },
    {
        "text": "Mahalle fırınının tam buğday ekmeği lezzeti harika fakat park yeri sıkıntısı yüzünden durup almak zor oluyor.",
        "aspects": ["tam buğday ekmeği lezzeti", "park yeri sıkıntısı"],
        "polarities": ["positive", "negative"],
        "category": "daily_life",
        "source": "LLM-generated",
    },
    {
        "text": "Üniversitenin kulüp faaliyetleri ve sosyal ortamı canlı ama yurt kontenjanları çok kısıtlı.",
        "aspects": ["kulüp faaliyetleri", "sosyal ortamı", "yurt kontenjanları"],
        "polarities": ["positive", "positive", "negative"],
        "category": "education",
        "source": "LLM-generated",
    },
    {
        "text": "Diş sağlığı merkezinin sterilizasyonu ve hijyeni mükemmeldi fakat randevu saatinde çok bekleniyor.",
        "aspects": ["sterilizasyonu", "hijyeni", "randevu saatinde"],
        "polarities": ["positive", "positive", "negative"],
        "category": "health",
        "source": "LLM-generated",
    },
]


def main():
    if not NEW_SAMPLES:
        print("NEW_SAMPLES bos -- once gercek 10 ornegi bu dosyaya girin.")
        sys.exit(1)

    rows = []
    for i, s in enumerate(NEW_SAMPLES):
        try:
            row = make_row(s["text"], s["aspects"], s["polarities"], s["category"], s.get("source", ""))
            rows.append(row)
            print(f"[{i+1}] OK: {s['text'][:60]}...")
            print(f"     tokens: {row['tokens']}")
            print(f"     labels: {row['labels']}")
        except ValueError as e:
            print(f"[{i+1}] HATA: {e}")
            sys.exit(1)

    out_path = "new_10_samples.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "target", "polarity", "category", "tokens", "labels", "source"])
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r[k] for k in writer.fieldnames})

    print(f"\n{len(rows)} satir yazildi: {out_path}")
    print("Bu dosyayi Drive'daki 6k_Turkish_ABSA_Dataset klasorune yukleyip")
    print("clean_experiments.ipynb Section 2'de full_df birlestirmesine ekleyin.")


if __name__ == "__main__":
    main()
