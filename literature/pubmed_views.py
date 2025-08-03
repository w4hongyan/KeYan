from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .pubmed_service import pubmed_service
from .utils import ApiResponse

class PubMedSearchView(APIView):
    """PubMed文献搜索API"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """GET请求搜索文献"""
        query = request.query_params.get('query', '').strip()
        max_results = int(request.query_params.get('max_results', 20))
        search_type = request.query_params.get('type', 'general')
        
        if not query:
            return Response(
                ApiResponse.error("搜索关键词不能为空"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            results = []
            
            if search_type == 'doi':
                # DOI搜索
                result = pubmed_service.search_by_doi(query)
                if result:
                    results = [result]
            elif search_type == 'author':
                # 作者搜索
                results = pubmed_service.search_by_author(query, max_results)
            elif search_type == 'journal':
                # 期刊搜索
                results = pubmed_service.search_by_journal(query, max_results)
            else:
                # 通用搜索
                pmids = pubmed_service.search_literatures(query, max_results)
                results = pubmed_service.fetch_literatures_batch(pmids)
            
            # 添加全文链接
            for result in results:
                if result.get('doi'):
                    full_text_url = pubmed_service.get_full_text_url(result['doi'])
                    result['full_text_url'] = full_text_url
            
            return Response(
                ApiResponse.success({
                    'results': results,
                    'total': len(results),
                    'query': query,
                    'search_type': search_type
                }),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"搜索失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """POST请求批量搜索文献"""
        queries = request.data.get('queries', [])
        max_results = request.data.get('max_results', 10)
        
        if not queries:
            return Response(
                ApiResponse.error("搜索查询不能为空"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            all_results = {}
            
            for query in queries:
                pmids = pubmed_service.search_literatures(query, max_results)
                results = pubmed_service.fetch_literatures_batch(pmids)
                
                # 添加全文链接
                for result in results:
                    if result.get('doi'):
                        full_text_url = pubmed_service.get_full_text_url(result['doi'])
                        result['full_text_url'] = full_text_url
                
                all_results[query] = results
            
            return Response(
                ApiResponse.success({
                    'batch_results': all_results,
                    'queries_processed': len(queries)
                }),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"批量搜索失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PubMedDetailView(APIView):
    """PubMed文献详情API"""
    permission_classes = [AllowAny]
    
    def get(self, request, pmid):
        """根据PMID获取文献详情"""
        try:
            result = pubmed_service.fetch_literature_details(pmid)
            
            if not result:
                return Response(
                    ApiResponse.error("未找到该文献"),
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # 添加全文链接
            if result.get('doi'):
                full_text_url = pubmed_service.get_full_text_url(result['doi'])
                result['full_text_url'] = full_text_url
            
            return Response(
                ApiResponse.success(result),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"获取文献详情失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PubMedBatchView(APIView):
    """PubMed批量文献获取API"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """批量获取文献详情"""
        pmids = request.data.get('pmids', [])
        
        if not pmids:
            return Response(
                ApiResponse.error("PMID列表不能为空"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            results = pubmed_service.fetch_literatures_batch(pmids)
            
            # 添加全文链接
            for result in results:
                if result.get('doi'):
                    full_text_url = pubmed_service.get_full_text_url(result['doi'])
                    result['full_text_url'] = full_text_url
            
            return Response(
                ApiResponse.success({
                    'results': results,
                    'total': len(results),
                    'requested': len(pmids)
                }),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"批量获取文献失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PubMedStatsView(APIView):
    """PubMed搜索统计API"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """获取搜索统计信息"""
        query = request.query_params.get('query', '').strip()
        
        if not query:
            return Response(
                ApiResponse.error("查询词不能为空"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 获取搜索结果数量
            pmids = pubmed_service.search_literatures(query, 1000)  # 获取大量结果用于统计
            
            # 获取详细结果用于分析
            results = pubmed_service.fetch_literatures_batch(pmids[:50])  # 限制分析数量
            
            # 统计分析
            year_stats = {}
            journal_stats = {}
            author_stats = {}
            
            for result in results:
                # 年份统计
                year = result.get('pub_year')
                if year:
                    year_stats[year] = year_stats.get(year, 0) + 1
                
                # 期刊统计
                journal = result.get('journal')
                if journal:
                    journal_stats[journal] = journal_stats.get(journal, 0) + 1
                
                # 作者统计
                authors = result.get('authors', [])
                for author in authors:
                    author_stats[author] = author_stats.get(author, 0) + 1
            
            return Response(
                ApiResponse.success({
                    'total_results': len(pmids),
                    'analyzed_results': len(results),
                    'year_distribution': dict(sorted(year_stats.items(), key=lambda x: x[0], reverse=True)),
                    'top_journals': dict(sorted(journal_stats.items(), key=lambda x: x[1], reverse=True)[:10]),
                    'top_authors': dict(sorted(author_stats.items(), key=lambda x: x[1], reverse=True)[:10]),
                    'query': query
                }),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"获取统计信息失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )