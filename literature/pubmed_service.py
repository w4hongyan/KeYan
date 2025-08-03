import requests
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import re
import asyncio
import aiohttp
from datetime import datetime
from Bio import Entrez
from Bio.Entrez import Parser

class PubMedService:
    """PubMed API服务类"""
    
    def __init__(self, email: str = "research@example.com"):
        """初始化PubMed服务"""
        Entrez.email = email
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.session = None
        
    def search_literatures(self, query: str, max_results: int = 20) -> List[str]:
        """搜索文献并返回PMID列表"""
        try:
            handle = Entrez.esearch(
                db="pubmed",
                term=query,
                retmax=max_results,
                retmode="json"
            )
            result = Entrez.read(handle)
            handle.close()
            return result["IdList"]
        except Exception as e:
            print(f"搜索文献失败: {e}")
            return []
    
    def fetch_literature_details(self, pmid: str) -> Optional[Dict]:
        """获取单篇文献详细信息"""
        try:
            handle = Entrez.efetch(
                db="pubmed",
                id=pmid,
                retmode="xml",
                rettype="abstract"
            )
            xml_data = handle.read()
            handle.close()
            
            return self.parse_pubmed_xml(xml_data)
        except Exception as e:
            print(f"获取文献详情失败: {e}")
            return None
    
    def fetch_literatures_batch(self, pmids: List[str]) -> List[Dict]:
        """批量获取文献详情"""
        if not pmids:
            return []
            
        try:
            handle = Entrez.efetch(
                db="pubmed",
                id=",".join(pmids),
                retmode="xml",
                rettype="abstract"
            )
            xml_data = handle.read()
            handle.close()
            
            return self.parse_batch_pubmed_xml(xml_data)
        except Exception as e:
            print(f"批量获取文献失败: {e}")
            return []
    
    def parse_pubmed_xml(self, xml_data: str) -> Optional[Dict]:
        """解析PubMed XML数据"""
        try:
            root = ET.fromstring(xml_data)
            article = root.find('.//PubmedArticle')
            if article is None:
                return None
                
            medline_citation = article.find('.//MedlineCitation')
            if medline_citation is None:
                return None
                
            article_data = medline_citation.find('.//Article')
            if article_data is None:
                return None
            
            # 解析标题
            title = ""
            title_elem = article_data.find('.//ArticleTitle')
            if title_elem is not None and title_elem.text:
                title = title_elem.text
            
            # 解析作者
            authors = []
            author_list = article_data.find('.//AuthorList')
            if author_list is not None:
                for author in author_list.findall('.//Author'):
                    last_name = author.find('.//LastName')
                    first_name = author.find('.//ForeName')
                    if last_name is not None and last_name.text:
                        author_name = last_name.text
                        if first_name is not None and first_name.text:
                            author_name = f"{first_name.text} {author_name}"
                        authors.append(author_name)
            
            # 解析摘要
            abstract = ""
            abstract_elem = article_data.find('.//Abstract/AbstractText')
            if abstract_elem is not None and abstract_elem.text:
                abstract = abstract_elem.text
            
            # 解析期刊
            journal = ""
            journal_elem = article_data.find('.//Journal/Title')
            if journal_elem is not None and journal_elem.text:
                journal = journal_elem.text
            
            # 解析发表年份
            pub_year = None
            pub_date = article_data.find('.//Journal/JournalIssue/PubDate/Year')
            if pub_date is not None and pub_date.text:
                pub_year = int(pub_date.text)
            
            # 解析DOI
            doi = ""
            for elocation_id in article_data.findall('.//ELocationID'):
                if elocation_id.get('EIdType') == 'doi':
                    doi = elocation_id.text or ""
                    break
            
            # 解析关键词
            keywords = []
            keyword_list = medline_citation.find('.//KeywordList')
            if keyword_list is not None:
                for keyword in keyword_list.findall('.//Keyword'):
                    if keyword.text:
                        keywords.append(keyword.text)
            
            return {
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'journal': journal,
                'pub_year': pub_year,
                'doi': doi,
                'keywords': keywords,
                'pmid': medline_citation.find('.//PMID').text if medline_citation.find('.//PMID') is not None else ""
            }
            
        except Exception as e:
            print(f"解析PubMed XML失败: {e}")
            return None
    
    def parse_batch_pubmed_xml(self, xml_data: str) -> List[Dict]:
        """批量解析PubMed XML数据"""
        try:
            root = ET.fromstring(xml_data)
            articles = root.findall('.//PubmedArticle')
            
            results = []
            for article in articles:
                medline_citation = article.find('.//MedlineCitation')
                if medline_citation is None:
                    continue
                    
                article_data = medline_citation.find('.//Article')
                if article_data is None:
                    continue
                
                # 使用与单个解析相同的方法
                pmid = medline_citation.find('.//PMID').text if medline_citation.find('.//PMID') is not None else ""
                literature_data = self.parse_pubmed_xml(ET.tostring(article).decode())
                
                if literature_data:
                    results.append(literature_data)
            
            return results
            
        except Exception as e:
            print(f"批量解析PubMed XML失败: {e}")
            return []
    
    def get_full_text_url(self, doi: str) -> Optional[str]:
        """获取全文链接"""
        if not doi:
            return None
            
        # 尝试获取OA全文链接
        try:
            # 使用Unpaywall API获取OA链接
            url = f"https://api.unpaywall.org/v2/{doi}"
            params = {"email": Entrez.email}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'best_oa_location' in data and data['best_oa_location']:
                    return data['best_oa_location']['url']
                    
        except Exception as e:
            print(f"获取全文链接失败: {e}")
            
        return None

    def get_full_text_url_by_pmid(self, pmid: str) -> Optional[str]:
        """通过PMID获取全文链接"""
        try:
            handle = Entrez.elink(dbfrom="pubmed", db="pmc", id=pmid)
            records = Entrez.read(handle)
            handle.close()
            
            if records[0]["LinkSetDb"]:
                pmc_id = records[0]["LinkSetDb"][0]["Link"][0]["Id"]
                return f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/"
                
            return None
            
        except Exception:
            return None

    async def async_search_literatures(self, query: str, max_results: int = 20) -> List[str]:
        """异步搜索文献"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.search_literatures, query, max_results)

    async def async_fetch_literature_details(self, pmid: str) -> Optional[Dict]:
        """异步获取文献详情"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.fetch_literature_details, pmid)

    async def async_fetch_literatures_batch(self, pmids: List[str]) -> List[Dict]:
        """异步批量获取文献"""
        tasks = [self.async_fetch_literature_details(pmid) for pmid in pmids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results = []
        for result in results:
            if isinstance(result, dict) and result is not None:
                valid_results.append(result)
        
        return valid_results

    def search_with_filters(self, query: str, filters: Dict[str, str], max_results: int = 20) -> List[str]:
        """使用过滤器搜索文献"""
        search_query = query
        
        # 添加日期过滤器
        if 'date_from' in filters:
            search_query += f" AND {filters['date_from']}[Date - Publication]"
        if 'date_to' in filters:
            search_query += f" AND {filters['date_to']}[Date - Publication]"
            
        # 添加作者过滤器
        if 'author' in filters:
            search_query += f" AND {filters['author']}[Author]"
            
        # 添加期刊过滤器
        if 'journal' in filters:
            search_query += f" AND {filters['journal']}[Journal]"
            
        return self.search_literatures(search_query, max_results)

    def get_similar_articles(self, pmid: str, max_results: int = 10) -> List[str]:
        """获取相似文献"""
        try:
            handle = Entrez.elink(dbfrom="pubmed", db="pubmed", id=pmid, cmd="neighbor_score")
            records = Entrez.read(handle)
            handle.close()
            
            similar_pmids = []
            if records[0]["LinkSetDb"]:
                for link in records[0]["LinkSetDb"][0]["Link"][:max_results]:
                    similar_pmids.append(link["Id"])
                    
            return similar_pmids
            
        except Exception as e:
            print(f"Error getting similar articles: {e}")
            return []
    
    def search_by_doi(self, doi: str) -> Optional[Dict]:
        """通过DOI搜索文献"""
        pmids = self.search_literatures(f"{doi}[DOI]")
        if pmids:
            return self.fetch_literature_details(pmids[0])
        return None
    
    def search_by_author(self, author_name: str, max_results: int = 20) -> List[Dict]:
        """通过作者搜索文献"""
        pmids = self.search_literatures(f"{author_name}[Author]", max_results)
        return self.fetch_literatures_batch(pmids)
    
    def search_by_journal(self, journal_name: str, max_results: int = 20) -> List[Dict]:
        """通过期刊搜索文献"""
        pmids = self.search_literatures(f"{journal_name}[Journal]", max_results)
        return self.fetch_literatures_batch(pmids)

# 创建全局实例
pubmed_service = PubMedService()