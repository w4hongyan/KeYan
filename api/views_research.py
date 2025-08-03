from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import User, Literature, LiteratureUser
from .serializers import UserSerializer
import json

class ResearchToolsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """获取用户保存的图表列表"""
        charts = request.user.saved_charts or []
        return Response({
            'success': True,
            'data': charts
        })

    def create(self, request):
        """保存新图表"""
        try:
            title = request.data.get('title')
            chart_data = request.data.get('data')
            chart_type = request.data.get('chart_type')
            config = request.data.get('config', {})

            if not title or not chart_data or not chart_type:
                return Response({
                    'success': False,
                    'message': '缺少必要参数'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 获取用户现有图表
            saved_charts = request.user.saved_charts or []
            
            # 创建新图表
            new_chart = {
                'id': len(saved_charts) + 1,
                'title': title,
                'data': chart_data,
                'chart_type': chart_type,
                'config': config,
                'created_at': str(models.DateTimeField().value_from_object(request.user))
            }
            
            saved_charts.append(new_chart)
            request.user.saved_charts = saved_charts
            request.user.save()

            return Response({
                'success': True,
                'message': '图表保存成功',
                'data': new_chart
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """获取单个图表详情"""
        try:
            charts = request.user.saved_charts or []
            chart = next((c for c in charts if c['id'] == int(pk)), None)
            
            if not chart:
                return Response({
                    'success': False,
                    'message': '图表不存在'
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'success': True,
                'data': chart
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """删除图表"""
        try:
            charts = request.user.saved_charts or []
            chart_index = next((i for i, c in enumerate(charts) if c['id'] == int(pk)), None)
            
            if chart_index is None:
                return Response({
                    'success': False,
                    'message': '图表不存在'
                }, status=status.HTTP_404_NOT_FOUND)

            deleted_chart = charts.pop(chart_index)
            request.user.saved_charts = charts
            request.user.save()

            return Response({
                'success': True,
                'message': '图表删除成功'
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def templates(self, request):
        """获取图表模板"""
        templates = [
            {
                'name': '年度发表趋势',
                'type': 'line',
                'description': '展示年度文献发表数量变化',
                'sample_data': [
                    {'x': '2019', 'y': 45},
                    {'x': '2020', 'y': 52},
                    {'x': '2021', 'y': 61},
                    {'x': '2022', 'y': 58},
                    {'x': '2023', 'y': 73},
                    {'x': '2024', 'y': 89}
                ]
            },
            {
                'name': '研究领域分布',
                'type': 'pie',
                'description': '展示不同研究领域的占比',
                'sample_data': [
                    {'x': '机器学习', 'y': 35},
                    {'x': '生物信息', 'y': 28},
                    {'x': '化学', 'y': 15},
                    {'x': '物理', 'y': 12},
                    {'x': '医学', 'y': 10}
                ]
            },
            {
                'name': '期刊影响因子对比',
                'type': 'bar',
                'description': '对比不同期刊的影响因子',
                'sample_data': [
                    {'x': 'Nature', 'y': 64.8},
                    {'x': 'Science', 'y': 56.9},
                    {'x': 'Cell', 'y': 64.5},
                    {'x': 'NEJM', 'y': 91.2},
                    {'x': 'Lancet', 'y': 79.3}
                ]
            },
            {
                'name': '用户活跃度',
                'type': 'area',
                'description': '展示平台用户活跃度变化',
                'sample_data': [
                    {'x': '周一', 'y': 120},
                    {'x': '周二', 'y': 132},
                    {'x': '周三', 'y': 101},
                    {'x': '周四', 'y': 134},
                    {'x': '周五', 'y': 190},
                    {'x': '周六', 'y': 230},
                    {'x': '周日', 'y': 210}
                ]
            }
        ]
        
        return Response({
            'success': True,
            'data': templates
        })

    @action(detail=False, methods=['post'])
    def generate_sample_data(self, request):
        """生成示例数据"""
        try:
            chart_type = request.data.get('type', 'bar')
            count = request.data.get('count', 10)
            
            if chart_type == 'pie':
                categories = ['机器学习', '生物信息', '化学', '物理', '医学', '工程', '数学']
                data = [
                    {'x': cat, 'y': np.random.randint(10, 100)}
                    for cat in categories[:count]
                ]
            else:
                labels = [f'数据{i+1}' for i in range(count)]
                data = [
                    {'x': label, 'y': np.random.randint(20, 200)}
                    for label in labels
                ]
            
            return Response({
                'success': True,
                'data': data
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def statistics_data(self, request):
        """获取科研统计数据"""
        try:
            # 获取用户文献统计
            user_literatures = LiteratureUser.objects.filter(user=request.user)
            
            # 按年份统计
            yearly_stats = (
                user_literatures
                .annotate(year=models.ExtractYear('created_at'))
                .values('year')
                .annotate(count=models.Count('id'))
                .order_by('year')
            )
            
            # 按领域统计
            field_stats = (
                user_literatures
                .values('literature__category')
                .annotate(count=models.Count('id'))
                .order_by('-count')
            )
            
            # 按期刊统计
            journal_stats = (
                user_literatures
                .values('literature__journal__name')
                .annotate(count=models.Count('id'))
                .order_by('-count')[:10]
            )
            
            data = {
                'yearly_data': [
                    {'x': str(stat['year']), 'y': stat['count']}
                    for stat in yearly_stats if stat['year']
                ],
                'field_data': [
                    {'x': stat['literature__category'] or '未分类', 'y': stat['count']}
                    for stat in field_stats
                ],
                'journal_data': [
                    {'x': stat['literature__journal__name'], 'y': stat['count']}
                    for stat in journal_stats
                ]
            }
            
            return Response({
                'success': True,
                'data': data
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)