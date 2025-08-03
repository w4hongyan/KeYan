import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Users, MessageCircle, TrendingUp, Search, ArrowRight, Star, Award, Zap } from 'lucide-react';

const Home: React.FC = () => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const features = [
    {
      icon: <BookOpen className="h-8 w-8" />,
      title: '智能文献管理',
      description: '支持PubMed搜索、自动导入、智能分类和翻译功能',
      link: '/literature',
      color: 'blue',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      icon: <Users className="h-8 w-8" />,
      title: '科研社区',
      description: '与同行交流经验，分享知识，解决科研难题',
      link: '/community',
      color: 'green',
      gradient: 'from-green-500 to-emerald-500'
    },
    {
      icon: <MessageCircle className="h-8 w-8" />,
      title: '课题互助',
      description: '发布合作需求，寻找科研伙伴，共同推进项目',
      link: '/cooperation',
      color: 'purple',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: <TrendingUp className="h-8 w-8" />,
      title: '数据分析',
      description: '文献统计分析，研究趋势可视化，科研洞察',
      link: '/analytics',
      color: 'orange',
      gradient: 'from-orange-500 to-red-500'
    }
  ];

  const stats = [
    { icon: <BookOpen className="h-6 w-6" />, value: '10,000+', label: '篇文献', color: 'text-blue-400' },
    { icon: <Users className="h-6 w-6" />, value: '500+', label: '活跃用户', color: 'text-green-400' },
    { icon: <Star className="h-6 w-6" />, value: '4.8', label: '用户评分', color: 'text-yellow-400' },
    { icon: <Award className="h-6 w-6" />, value: '200+', label: '合作案例', color: 'text-purple-400' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 via-purple-600/10 to-pink-600/10"></div>
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-300/20 rounded-full blur-3xl"></div>
        <div className="absolute top-1/2 right-1/4 w-96 h-96 bg-purple-300/20 rounded-full blur-3xl"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
          <div className="text-center lg:text-left lg:flex lg:items-center lg:justify-between">
            <div className="lg:w-1/2">
              <div className={`transition-all duration-1000 transform ${mounted ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
                <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-gray-900 leading-tight">
                  <span className="block">科研文献</span>
                  <span className="block bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                    智能管理平台
                  </span>
                </h1>
                <p className="mt-6 text-xl text-gray-600 max-w-2xl mx-auto lg:mx-0">
                  专为科研人员设计的全方位文献管理系统，集成PubMed搜索、智能翻译、社区交流、合作互助等功能，让科研更高效、更智能。
                </p>
                
                {/* 快速搜索栏 */}
                <div className="mt-8 max-w-md mx-auto lg:mx-0">
                  <div className="flex rounded-lg shadow-lg bg-white p-2">
                    <Search className="h-5 w-5 text-gray-400 mt-3 ml-3" />
                    <input
                      type="text"
                      placeholder="搜索文献、问题或合作..."
                      className="flex-1 px-3 py-2 text-gray-700 focus:outline-none"
                    />
                    <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-md hover:shadow-lg transition-shadow">
                      搜索
                    </button>
                  </div>
                </div>

                <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                  <Link
                    to="/literature"
                    className="group inline-flex items-center justify-center px-8 py-4 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                  >
                    立即开始
                    <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </Link>
                  <Link
                    to="/community"
                    className="inline-flex items-center justify-center px-8 py-4 border border-gray-300 text-base font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-50 hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                  >
                    探索社区
                  </Link>
                </div>
              </div>
            </div>

            {/* 右侧可视化区域 */}
            <div className="mt-12 lg:mt-0 lg:w-5/12">
              <div className={`relative transition-all duration-1000 transform ${mounted ? 'scale-100 opacity-100' : 'scale-95 opacity-0'}`}>
                <div className="relative bg-white/80 backdrop-blur-sm rounded-2xl shadow-2xl p-8">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg p-4 text-white">
                      <BookOpen className="h-8 w-8 mb-2" />
                      <p className="text-sm font-medium">文献管理</p>
                      <p className="text-2xl font-bold">10K+</p>
                    </div>
                    <div className="bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg p-4 text-white">
                      <Users className="h-8 w-8 mb-2" />
                      <p className="text-sm font-medium">活跃用户</p>
                      <p className="text-2xl font-bold">500+</p>
                    </div>
                    <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg p-4 text-white">
                      <MessageCircle className="h-8 w-8 mb-2" />
                      <p className="text-sm font-medium">合作案例</p>
                      <p className="text-2xl font-bold">200+</p>
                    </div>
                    <div className="bg-gradient-to-br from-orange-500 to-red-500 rounded-lg p-4 text-white">
                      <Zap className="h-8 w-8 mb-2" />
                      <p className="text-sm font-medium">问题解答</p>
                      <p className="text-2xl font-bold">1K+</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-base font-semibold text-indigo-600 tracking-wide uppercase">
              核心功能
            </h2>
            <p className="mt-2 text-3xl lg:text-4xl font-extrabold text-gray-900">
              一站式科研解决方案
            </p>
            <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
              从文献搜索到合作交流，为您的科研工作提供全方位支持
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2"
              >
                <div className={`absolute inset-0 bg-gradient-to-r ${feature.gradient} rounded-2xl opacity-0 group-hover:opacity-10 transition-opacity duration-300`}></div>
                <div className="relative p-8">
                  <div className={`inline-flex items-center justify-center p-4 bg-gradient-to-r ${feature.gradient} rounded-xl text-white shadow-lg`}>
                    {feature.icon}
                  </div>
                  <h3 className="mt-6 text-xl font-semibold text-gray-900">{feature.title}</h3>
                  <p className="mt-2 text-gray-600">{feature.description}</p>
                  <div className="mt-6">
                    <Link
                      to={feature.link}
                      className="text-sm font-medium text-indigo-600 hover:text-indigo-500 flex items-center"
                    >
                      了解更多
                      <ArrowRight className="ml-1 h-4 w-4" />
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600">
        <div className="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:py-20 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-white">
              平台数据一览
            </h2>
            <p className="mt-4 text-xl text-indigo-100">
              用数据说话，让科研更高效
            </p>
          </div>
          
          <div className="mt-12 grid grid-cols-2 gap-6 md:grid-cols-4">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className={`inline-flex items-center justify-center p-3 rounded-full bg-white/10 backdrop-blur-sm mb-4 ${stat.color}`}>
                  {stat.icon}
                </div>
                <div className="text-4xl font-extrabold text-white">{stat.value}</div>
                <div className="mt-2 text-sm font-medium text-indigo-100">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-white">
        <div className="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:py-20 lg:px-8">
          <div className="relative bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl shadow-xl overflow-hidden">
            <div className="absolute inset-0 bg-black/20"></div>
            <div className="relative px-6 py-12 sm:px-12 lg:px-16 lg:py-16">
              <div className="lg:flex lg:items-center lg:justify-between">
                <div className="lg:w-2/3">
                  <h2 className="text-3xl font-extrabold text-white">
                    开始您的科研之旅
                  </h2>
                  <p className="mt-4 text-xl text-indigo-100">
                    加入我们的科研社区，与全球科研人员一起成长，让每一次研究都更有价值。
                  </p>
                </div>
                <div className="mt-8 lg:mt-0 lg:flex-shrink-0">
                  <div className="inline-flex rounded-md shadow">
                    <Link
                      to="/register"
                      className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50"
                    >
                      免费注册
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;