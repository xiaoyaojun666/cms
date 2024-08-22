import os
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup

from cms.models import Paper


class Command(BaseCommand):
    help = 'Fetches daily papers from arXiv for the given keyword and saves them into the database'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str, help='Keyword to search for papers')

    def handle(self, *args, **options):
        keyword = options['keyword']

        # 目标URL（这里是查询最近100篇关于给定关键词的论文）
        search_query = f'ti:{keyword}'
        url = f"https://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending"

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            entries = soup.find_all('entry')
            self.stdout.write(f'共检索到：{len(entries)}条论文')
            for entry in entries:
                published_date_text = entry.published.text
                published_date = datetime.strptime(published_date_text, '%Y-%m-%dT%H:%M:%SZ')

                title = entry.title.text.replace('\n', ' ').strip()
                summary = entry.summary.text.replace('\n', ' ').strip()
                authors = ', '.join(author.find('name').text for author in entry.find_all('author'))
                paper_url = entry.id.text

                # 检查去重
                if Paper.objects.filter(paper_url=paper_url).exists():
                    self.stdout.write(f"论文已存在：{paper_url}\n")
                    continue

                pdf_url = paper_url.replace('abs', 'pdf')
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # 下载PDF文件并保存到本地
                pdf_response = requests.get(pdf_url)
                pdf_index = pdf_url.find("pdf")
                pdf_filename = pdf_url[pdf_index + 4:] + '.pdf'
                pdf_path = os.path.join('pdfs', pdf_filename)

                # 创建目录如果不存在
                os.makedirs('pdfs', exist_ok=True)

                with open(pdf_path, 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)

                # 将信息插入数据库，包括PDF路径
                Paper.objects.create(
                    key_words=keyword,
                    title=title,
                    summary=summary,
                    published_date=published_date_text,
                    authors=authors,
                    paper_url=paper_url,
                    pdf_path=pdf_path,
                    create_time=create_time
                )

                self.stdout.write(
                    f"Title: {title}\nSummary: {summary}\nPublished Date: {published_date_text}\nAuthors: {authors}\nPaper URL: {paper_url}\nPDF Path: {pdf_path}\nCreate Time: {create_time}\n"
                )
                self.stdout.write("-" * 80)
        else:
            self.stderr.write("Failed to retrieve data")