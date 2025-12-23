import xml.etree.ElementTree as ET
import feedparser
import os
import re

def asistan_tara():
    if not os.path.exists('blogs.xml'):
        print("HATA: blogs.xml dosyası bulunamadı!")
        return

    try:
        # XML dosyasını aç
        tree = ET.parse('blogs.xml')
        root = tree.getroot()
        
        # Moodle Glossary yapısına göre <DEFINITION> içindeki linkleri topla
        urls = []
        for entry in root.findall('.//ENTRY'):
            definition = entry.find('DEFINITION')
            if definition is not None and definition.text:
                # Metin içindeki http ile başlayan linkleri ayıkla
                found_links = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', definition.text)
                for link in found_links:
                    # HTML etiketlerini temizle (p, br vb.)
                    clean_link = re.sub(r'<[^>]+>', '', link).strip()
                    if clean_link not in urls:
                        urls.append(clean_link)

        print(f"Sistemde {len(urls)} adet öğrenci blogu tespit edildi.")
        
        found_posts = []
        for url in urls:
            # Blogspot ve genel feed adreslerini dene
            # Blogger için genelde /feeds/posts/default kullanılır
            if "blogspot.com" in url:
                feed_url = url.split('?')[0].rstrip('/') + '/feeds/posts/default'
            else:
                feed_url = url.rstrip('/') + '/feed'
            
            print(f"Taranıyor: {url}")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries:
                # Başlıkta "yansıtıcı" kelimesini ara
                if "yansıtıcı" in entry.title.lower():
                    post_info = f"| {entry.title} | [Yazıyı Oku]({entry.link}) | {url} |"
                    found_posts.append(post_info)

        # Sonuçları Markdown tablosu olarak yaz
        with open("sonuclar.md", "w", encoding="utf-8") as f:
            f.write("# 📝 Yansıtıcı Yazı Tarama Sonuçları\n\n")
            if found_posts:
                f.write(f"Tarama zamanı: {len(found_posts)} yazı bulundu.\n\n")
                f.write("| Yazı Başlığı | Bağlantı | Öğrenci Blogu |\n")
                f.write("| :--- | :--- | :--- |\n")
                f.write("\n".join(found_posts))
            else:
                f.write("Tarama tamamlandı ancak başlığında 'yansıtıcı' geçen güncel bir yazı bulunamadı.")
        
        print("İşlem başarıyla tamamlandı. sonuclar.md güncellendi.")

    except Exception as e:
        print(f"Sistem çalışırken bir hata oluştu: {e}")

if __name__ == "__main__":
    asistan_tara()
