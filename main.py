import xml.etree.ElementTree as ET
import feedparser
import os

def get_yansitici_posts():
    # XML dosyasını oku
    tree = ET.parse('blogs.xml')
    root = tree.getroot()
    
    # XML yapınıza göre bu satırı özelleştirebiliriz (örneğin: 'url' etiketi)
    urls = [url_elem.text for url_elem in root.findall('.//url')]
    
    found_posts = []
    
    for url in urls:
        feed_url = url.rstrip('/') + '/feed'
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries:
            if "yansıtıcı" in entry.title.lower():
                found_posts.append(f"| {entry.title} | [Oku]({entry.link}) | {url} |")
    
    # README.md dosyasını güncelle
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# 📝 Öğrenci Yansıtıcı Yazıları\n\n")
        f.write("Otomatik olarak toplanan yansıtıcı başlıkları:\n\n")
        f.write("| Başlık | Link | Blog |\n")
        f.write("| :--- | :--- | :--- |\n")
        f.write("\n".join(found_posts))

if __name__ == "__main__":
    get_yansitici_posts()
