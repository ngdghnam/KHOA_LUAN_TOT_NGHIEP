from src.config.search import SearchingGoogle 
from src.utils.crawl_util import CrawlUtils
from src.config.crawl import crawl_one, crawl_sync
from src.config.search import SearchingGoogle
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from src.config.logger import logger
from src.constants.index import NULL_QUERY
from .dto.request_dto import *

class SearchService:
    def __init__(self, search: SearchingGoogle, crawlUtils: CrawlUtils, session: AsyncSession):
        self.search = search
        self.crawlUtil = crawlUtils

    async def crawlFromSpecificURL(self, data: UrlDto):
        if data.url == "":
            return {"message": NULL_QUERY}

        res = await crawl_one(data.url)
        return res

    async def crawlData(self, request: RequestCrawlDto, skip_duplicates: bool = True):
        # Tạo set mới cho mỗi request thay vì dùng self.crawled_urls
        crawled_urls = set()

        if request.query == "":
            return {"message": NULL_QUERY}
        
        # Số lượng kết quả mong muốn
        target_count = request.number
        valid_results = []
        start_index = 1
        max_start = 91  # Google CSE giới hạn 100 kết quả tối đa

        while len(valid_results) < target_count and start_index <= max_start:
            remaining = target_count - len(valid_results)
            num_to_fetch = min(10, remaining)  # Google CSE max = 10
                    
            links = self.search.google_search(request.query, num_to_fetch, start=start_index)

            if not links:
                logger.warning(f"Không còn kết quả từ Google")
                break

            # Lấy danh sách URL và metadata từ dict
            urls_with_metadata = []
            for item in links:
                if item.get("link"):
                    urls_with_metadata.append({
                        "url": item["link"],
                        "title": item.get("title", ""),
                        "snippet": item.get("snippet", "")
                    })

            # Lọc URL hợp lệ
            valid_links_with_metadata = []

            for item in urls_with_metadata:
                url = item["url"]
                # Kiểm tra URL có hợp lệ không (không phải file download)
                if not self.crawlUtil.is_valid_url(url):
                    continue
                
                # Kiểm tra format cơ bản
                if isinstance(url, str) and url.strip() != "":
                    valid_links_with_metadata.append(item)

            # Lọc bỏ URLs đã crawl (nếu bật skip_duplicates)
            if skip_duplicates:
                new_links = [item for item in valid_links_with_metadata if item["url"] not in crawled_urls]
                logger.info(f"Tìm thấy {len(valid_links_with_metadata)} URLs, {len(new_links)} URLs mới")
                valid_links_with_metadata = new_links

            if not valid_links_with_metadata:
                logger.warning("Không có URL mới để crawl")
                start_index += 10
                continue
            
            # Lấy chỉ URLs để crawl
            urls_to_crawl = [item["url"] for item in valid_links_with_metadata]
            
            # Chạy crawl trong thread
            results = await asyncio.to_thread(crawl_sync, urls_to_crawl)
            crawled_urls.update(urls_to_crawl)

            # Kết hợp metadata với content
            for i, result in enumerate(results):
                content = result.get("content", "").strip()
                if content:  # Chỉ thêm kết quả có nội dung
                    # Tạo object hoàn chỉnh
                    article = {
                        "title": valid_links_with_metadata[i]["title"] or result.get("title", "Không có tiêu đề"),
                        "url": valid_links_with_metadata[i]["url"],
                        "content": content,
                        "snippet": valid_links_with_metadata[i]["snippet"],
                        "keyword": request.query  # Thêm keyword để biết từ query nào
                    }
                    valid_results.append(article)
                    
                    if len(valid_results) >= target_count:
                        break

            if len(valid_results) >= target_count:
                break
                
            start_index += 10
        
        if not valid_results:
            logger.warning("Không crawl được nội dung hợp lệ nào")
            return {"message": "Không crawl được nội dung hợp lệ", "data": []}

        # Trả về mảng các object
        return {"data": valid_results[:target_count]}

    async def crawlMultipleData(self, data: MultipleKeywordsDto):
        """
        Crawl dữ liệu cho nhiều keywords và gộp tất cả kết quả vào một mảng
        """
        if not data.keywords or len(data.keywords) == 0:
            logger.error("Danh sách keywords trống")
            return {"message": "Danh sách keywords không được để trống", "data": []}
        
        all_results = []
        successful_keywords = []
        failed_keywords = []

        tasks = [self.crawlData(RequestCrawlDto(query=k, number=5)) for k in data.keywords]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Xử lý kết quả từng keyword
        for keyword, result in zip(data.keywords, results):
            # Kiểm tra nếu có exception
            if isinstance(result, Exception):
                logger.error(f"Lỗi khi crawl keyword '{keyword}': {str(result)}")
                failed_keywords.append(keyword)
                continue
            
            # Kiểm tra nếu có data
            if result.get("data") and isinstance(result["data"], list):
                logger.info(f"Keyword '{keyword}': crawl thành công {len(result['data'])} bài viết")
                
                # Thêm các bài viết vào mảng tổng
                all_results.extend(result["data"])
                successful_keywords.append(keyword)
            else:
                logger.warning(f"Keyword '{keyword}': không có dữ liệu")
                failed_keywords.append(keyword)
        
        if not all_results:
            logger.warning("Không có dữ liệu nào được crawl thành công")
            return {
                "message": "Không tìm thấy dữ liệu cho các keywords",
                "successful_keywords": successful_keywords,
                "failed_keywords": failed_keywords,
                "data": []
            }

        return {
            "message": f"Đã crawl thành công {len(all_results)} bài viết từ {len(successful_keywords)}/{len(data.keywords)} keywords",
            "total_articles": len(all_results),
            "successful_keywords": successful_keywords,
            "failed_keywords": failed_keywords,
            "data": all_results  # Mảng object gồm title, url, content, snippet, keyword
        }
