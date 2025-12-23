import xml.etree.ElementTree as ET
import feedparser
import os

def asistan_tara():
    # 1. XML dosyasını oku (Dosya adının blogs.xml olduğunu varsayıyoruz)
    if not os.path.exists('blogs.xml'):
        print("Hata: blogs.xml dosyası bulunamadı!")
        return

    tree = ET.parse('blogs.xml')
    root = tree.getroot()
    
    # XML yapınızda linkler hangi etiketteyse burayı ona göre güncelleyin (örn: 'url')
    # Genelde <url><loc>link</loc></url> yapısı olur.
    urls = [elem.text for elem in root.findall('.//url')]
    
    found_posts = []
    print(f"Toplam {len(urls)} blog kontrol ediliyor...\n")

    for url in urls:
        # RSS beslemesini bulmaya çalış (WordPress, Blogspot vb. uyumlu)
        feed_url = url.rstrip('/') + '/feed'
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries:
            # Başlıkta "yansıtıcı" kelimesini ara
            if "yansıtıcı" in entry.title.lower():
                yazi_bilgisi = f"- **Başlık:** {entry.title}  \n  **Link:** {entry.link}  \n  **Blog:** {url}\n"
                found_posts.append(yazi_bilgisi)
                print(f"Bulundu: {entry.title}")

    # 2. Sonuçları bir markdown dosyasına kaydet
    with open("sonuclar.md", "w", encoding="utf-8") as f:
        f.write("# 🔍 Tarama Sonuçları\n\n")
        if found_posts:
            f.writelines(found_posts)
        else:
            f.write("Maalesef kriterlere uygun yeni bir yazı bulunamadı.")
    
    print("\nİşlem tamamlandı. 'sonuclar.md' dosyası güncellendi.")

if __name__ == "__main__":
    asistan_tara()
