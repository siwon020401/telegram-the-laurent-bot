# main.py
import os
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 텔레그램 봇 정보
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 지역별 더로랑 검색 링크 (예시 일부)
LINKS = [
   #강남구
    "https://www.daangn.com/kr/buy-sell/?in=%EC%97%AD%EC%82%BC%EB%8F%99-6035&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%B2%AD%EB%8B%B4%EB%8F%99-386&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%8C%80%EC%B9%98%EB%8F%99-6032&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%85%BC%ED%98%84%EB%8F%99-6031&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%97%AD%EC%82%BC1%EB%8F%99-392&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%95%95%EA%B5%AC%EC%A0%95%EB%8F%99-385&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%82%BC%EC%84%B1%EB%8F%99-6034&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%8B%A0%EC%82%AC%EB%8F%99-382&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%85%BC%ED%98%841%EB%8F%99-383&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%8F%84%EA%B3%A1%EB%8F%99-6033&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%9C%ED%8F%AC%EB%8F%99-6030&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%97%AD%EC%82%BC2%EB%8F%99-393&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%8C%80%EC%B9%981%EB%8F%99-389&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%9E%90%EA%B3%A1%EB%8F%99-6038&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%8C%80%EC%B9%984%EB%8F%99-391&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%82%BC%EC%84%B12%EB%8F%99-388&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%8C%80%EC%B9%982%EB%8F%99-390&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%82%BC%EC%84%B11%EB%8F%99-387&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%9D%BC%EC%9B%90%EB%8F%99-6037&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%85%BC%ED%98%842%EB%8F%99-384&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%9C%ED%8F%AC1%EB%8F%99-396&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%84%B8%EA%B3%A1%EB%8F%99-399&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%9C%ED%8F%AC4%EB%8F%99-398&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%8F%84%EA%B3%A11%EB%8F%99-394&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%9C%ED%8F%AC3%EB%8F%99-402&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%88%98%EC%84%9C%EB%8F%99-403&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%9C%ED%8F%AC2%EB%8F%99-397&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%8F%84%EA%B3%A12%EB%8F%99-395&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%9D%BC%EC%9B%90%EB%B3%B8%EB%8F%99-400&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%9D%BC%EC%9B%901%EB%8F%99-401&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%9C%A8%ED%98%84%EB%8F%99-6036&search=%EB%8D%94%EB%A1%9C%EB%9E%91"

    # 강서구
    "https://www.daangn.com/kr/buy-sell/?in=%ED%99%94%EA%B3%A1%EB%8F%99-6057&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%A7%88%EA%B3%A1%EB%8F%99-6052&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%97%BC%EC%B0%BD%EB%8F%99-258&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%93%B1%EC%B4%8C%EB%8F%99-6051&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%82%B4%EB%B0%9C%EC%82%B0%EB%8F%99-6050&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%B0%A9%ED%99%94%EB%8F%99-6053&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%9A%B0%EC%9E%A5%EC%82%B0%EB%8F%99-273&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%ED%99%94%EA%B3%A1%EC%A0%9C1%EB%8F%99-262&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%80%EC%96%91%EB%8F%99-6047&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%ED%99%94%EA%B3%A1%EB%B3%B8%EB%8F%99-266&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%93%B1%EC%B4%8C%EC%A0%9C3%EB%8F%99-261&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B3%B5%ED%95%AD%EB%8F%99-274&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%ED%99%94%EA%B3%A1%EC%A0%9C6%EB%8F%99-267&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%ED%99%94%EA%B3%A1%EC%A0%9C8%EB%8F%99-268&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%B0%A9%ED%99%94%EC%A0%9C1%EB%8F%99-275&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%ED%99%94%EA%B3%A1%EC%A0%9C3%EB%8F%99-264&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%B0%9C%EC%82%B0%EC%A0%9C1%EB%8F%99-272&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%ED%99%94%EA%B3%A1%EC%A0%9C4%EB%8F%99-265&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%93%B1%EC%B4%8C%EC%A0%9C1%EB%8F%99-259&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%ED%99%94%EA%B3%A1%EC%A0%9C2%EB%8F%99-263&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%80%EC%96%91%EC%A0%9C1%EB%8F%99-269&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%93%B1%EC%B4%8C%EC%A0%9C2%EB%8F%99-260&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%B0%A9%ED%99%94%EC%A0%9C2%EB%8F%99-276&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%B0%A9%ED%99%94%EC%A0%9C3%EB%8F%99-277&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%80%EC%96%91%EC%A0%9C3%EB%8F%99-271&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%80%EC%96%91%EC%A0%9C2%EB%8F%99-270&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%99%B8%EB%B0%9C%EC%82%B0%EB%8F%99-6056&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B0%9C%ED%99%94%EB%8F%99-6048&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EA%B3%BC%ED%95%B4%EB%8F%99-6049&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%98%A4%EA%B3%A1%EB%8F%99-6054&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%98%A4%EC%87%A0%EB%8F%99-6055&search=%EB%8D%94%EB%A1%9C%EB%9E%91"

    # 강북구
    "https://www.daangn.com/kr/buy-sell/?in=%EB%AF%B8%EC%95%84%EB%8F%99-142&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%88%98%EC%9C%A0%EB%8F%99-6046&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%82%BC%EA%B0%81%EC%82%B0%EB%8F%99-145&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%88%98%EC%9C%A03%EB%8F%99-151&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%88%98%EC%9C%A01%EB%8F%99-149&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%88%98%EC%9C%A02%EB%8F%99-150&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%82%BC%EC%96%91%EB%8F%99-141&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%B2%881%EB%8F%99-146&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%86%A1%EC%A4%91%EB%8F%99-143&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%9D%B8%EC%88%98%EB%8F%99-153&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%B2%88%EB%8F%99-6045&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%86%A1%EC%B2%9C%EB%8F%99-144&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EC%9A%B0%EC%9D%B4%EB%8F%99-152&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%B2%883%EB%8F%99-148&search=%EB%8D%94%EB%A1%9C%EB%9E%91",
    "https://www.daangn.com/kr/buy-sell/?in=%EB%B2%882%EB%8F%99-147&search=%EB%8D%94%EB%A1%9C%EB%9E%91"
]

SEEN_FILE = "seen_links.txt"
seen_links = set()

def load_seen_links():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())
    return set()

def save_seen_link(link):
    with open(SEEN_FILE, 'a', encoding='utf-8') as f:
        f.write(link + '\n')

def fetch_new_items():
    global seen_links
    new_items = []
    for url in LINKS:
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.select('article.flea-market-article')
            for item in items:
                title = item.select_one('span.article-title')
                price = item.select_one('span.article-price')
                href = item.find('a', href=True)
                if title and href:
                    link = 'https://www.daangn.com' + href['href']
                    if link not in seen_links:
                        seen_links.add(link)
                        save_seen_link(link)
                        new_items.append(f"🆕 {title.text.strip()} / {price.text.strip() if price else '가격 없음'}\n{link}")
        except Exception as e:
            print(f"[!] 에러: {e}")
    return new_items

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 더로랑 매물 검색 중...")
    new_items = fetch_new_items()
    if not new_items:
        await update.message.reply_text("😥 새 매물이 없습니다.")
    else:
        for msg in new_items:
            await update.message.reply_text(msg)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    seen_links = load_seen_links()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("더로랑", handle_query))
    print("🤖 클라우드 봇 실행 중...")
    app.run_polling()
