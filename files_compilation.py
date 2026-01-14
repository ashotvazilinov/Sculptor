from bs4 import BeautifulSoup
from pathlib import Path

input_dir = Path("D:/downloads/ксения")   # папка с 251 html
output_file = "ksen_chat_all.html"

html_files = sorted(input_dir.glob("*.html"))

all_messages = []
head_html = None

for i, file in enumerate(html_files):
    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

        if i == 0:
            head_html = soup.head

        body = soup.body
        if body:
            all_messages.append(body.decode_contents())

# собираем финальный html
final_html = f"""
<!DOCTYPE html>
<html>
{head_html}
<body>
{''.join(all_messages)}
</body>
</html>
"""

with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Готово! Создан файл {output_file}")
