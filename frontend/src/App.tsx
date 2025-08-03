import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Community from './pages/Community';
import Cooperation from './pages/Cooperation';
import Literature from './pages/Literature';
import Login from './pages/Login';
import Register from './pages/Register';
import NotFound from './pages/NotFound';
import UserProfile from './pages/UserProfile';
import Statistics from './pages/Statistics';
import ResearchTools from './pages/ResearchTools';
import PlagiarismCheck from './pages/PlagiarismCheck';
import JournalImpact from './pages/JournalImpact';
import PrivateRoute from './components/PrivateRoute';
import './App.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        {/* 导航栏 */}
        <nav className="bg-white shadow-lg border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <span className="text-2xl font-bold gradient-text">科研协作平台</span>
              </div>
              <div className="flex space-x-8">
                <Link to="/" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
                  首页
                </Link>
                <Link to="/community" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
                  科研社区
                </Link>
                <Link to="/cooperation" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
                  课题互助
                </Link>
                <Link to="/literature" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
                  文献管理
                </Link>
                <Link to="/profile" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
                  个人中心
                </Link>
                <Link to="/statistics" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
                  统计分析
                </Link>
                <Link to="/research-tools" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
                  科研工具
                </Link>
                <Link to="/plagiarism-check" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
                  查重服务
                </Link>
                <Link to="/journal-impact" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
                  期刊查询
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* 主内容区域 */}
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/community" element={<Community />} />
            <Route path="/cooperation" element={<Cooperation />} />
            <Route path="/literature" element={<Literature />} />
            <Route path="/profile" element={<PrivateRoute><UserProfile /></PrivateRoute>} />
            <Route path="/statistics" element={<PrivateRoute><Statistics /></PrivateRoute>} />
            <Route path="/research-tools" element={<PrivateRoute><ResearchTools /></PrivateRoute>} />
            <Route path="/plagiarism-check" element={<PrivateRoute><PlagiarismCheck /></PrivateRoute>} />
            <Route path="/journal-impact" element={<PrivateRoute><JournalImpact /></PrivateRoute>} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>

        {/* 页脚 */}
        <footer className="bg-white border-t border-gray-200 mt-auto">
          <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <p className="text-lg font-semibold gradient-text">科研协作平台</p>
              <p className="mt-2 text-sm text-gray-600">
                © 2024 科研团队 - 让科研更高效，让合作更简单
              </p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
};

export default App;