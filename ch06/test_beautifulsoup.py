from bs4 import BeautifulSoup

html_content = """
<html>
<body>
  <header><h1>우리 회사</h1></header>
  <nav><a href="/menu">메뉴</a></nav>
  <main>
    <h2>핵심 서비스 안내</h2>
    <p>우리의 핵심 서비스는 AI 기반의...</p>
  </main>
  <footer><p>Copyright 2025</p></footer>
</body>
</html>
"""

soup = BeautifulSoup(html_content, 'html.parser')

# 본문과 관계없는 레이아웃 요소(헤더, 내비게이션, 푸터 등) 제거
for tag in soup(['header', 'nav', 'footer', 'script', 'aside', 'style']):  # ➊
    tag.decompose()

# 정제된 텍스트 추출
cleaned_text = soup.get_text(separator='\n', strip=True)  # ➋

print(cleaned_text)