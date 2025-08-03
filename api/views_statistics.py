from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from .models import Literature, User, UserProfile
from .serializers import LiteratureSerializer
from .utils import ApiResponse


class StatisticsView(APIView):
    """
    统计分析API
    
    POST /api/statistics/ - 获取统计数据
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """获取统计数据"""
        try:
            start_date_str = request.data.get('start_date')
            end_date_str = request.data.get('end_date')
            selected_field = request.data.get('field', 'all')

            # 解析日期范围
            if start_date_str and end_date_str:
                start_date = parse_date(start_date_str)
                end_date = parse_date(end_date_str)
                # 如果日期解析失败，使用默认值
                if not start_date or not end_date:
                    end_date = datetime.now().date()
                    start_date = end_date - timedelta(days=30)
            else:
                end_date = datetime.now().date()
                start_date = end_date - timedelta(days=30)

            # 基础统计数据
            total_literature = Literature.objects.filter(
                created_at__date__range=[start_date, end_date]
            ).count()

            total_views = Literature.objects.filter(
                created_at__date__range=[start_date, end_date]
            ).aggregate(total_views=Sum('view_count'))['total_views'] or 0

            total_downloads = Literature.objects.filter(
                created_at__date__range=[start_date, end_date]
            ).aggregate(total_downloads=Sum('download_count'))['total_downloads'] or 0

            total_users = User.objects.filter(
                date_joined__date__range=[start_date, end_date]
            ).count()

            # 每日上传趋势
            weekly_uploads = []
            current_date = start_date
            while current_date <= end_date:
                count = Literature.objects.filter(
                    created_at__date=current_date
                ).count()
                weekly_uploads.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'count': count
                })
                current_date += timedelta(days=1)

            # 领域分布
            field_queryset = Literature.objects.filter(
                created_at__date__range=[start_date, end_date]
            )
            
            if selected_field != 'all':
                field_queryset = field_queryset.filter(category__icontains=selected_field)

            field_distribution = list(field_queryset.values('category').annotate(
                count=Count('id')
            ).order_by('-count')[:10])
            
            # 将字段名转换为前端期望的格式，处理空值
            field_distribution = [
                {'field': item['category'] or '未分类', 'count': item['count']}
                for item in field_distribution
                if item['category'] is not None
            ]
            
            # 如果没有数据，添加一个默认项
            if not field_distribution:
                field_distribution = [{'field': '暂无数据', 'count': 0}]

            # 热门论文
            top_papers = Literature.objects.filter(
                created_at__date__range=[start_date, end_date]
            ).order_by('-view_count')[:10]

            top_papers_data = []
            for paper in top_papers:
                top_papers_data.append({
                    'id': paper.id,
                    'title': paper.title or '无标题',
                    'views': paper.view_count or 0,
                    'downloads': paper.download_count or 0,
                    'authors': [author.strip() for author in (paper.authors or '').split(',') if author.strip()]
                })

            # 用户活跃度
            user_activity = []
            current_date = start_date
            while current_date <= end_date:
                active_users = User.objects.filter(
                    last_login__date=current_date
                ).count()
                
                new_users = User.objects.filter(
                    date_joined__date=current_date
                ).count()

                user_activity.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'activeUsers': active_users,
                    'newUsers': new_users
                })
                current_date += timedelta(days=1)

            data = {
                'totalLiterature': total_literature,
                'totalViews': total_views,
                'totalDownloads': total_downloads,
                'totalUsers': total_users,
                'weeklyUploads': weekly_uploads,
                'fieldDistribution': field_distribution,
                'topPapers': top_papers_data,
                'userActivity': user_activity
            }

            return ApiResponse.success(data, "获取统计数据成功")

        except Exception as e:
            return ApiResponse.error(str(e))