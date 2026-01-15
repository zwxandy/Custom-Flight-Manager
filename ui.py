"""
UI样式和组件模块
包含所有前端样式定义和UI组件函数
"""

import streamlit as st


def load_custom_css():
    """加载自定义CSS样式"""
    st.markdown("""
    <style>
        /* 主标题样式 - 炫酷渐变色 */
        .main-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.8rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            animation: gradient-shift 4s ease infinite;
            letter-spacing: 1px;
            position: relative;
            display: inline-block;
        }
        
        /* 渐变动画效果 - 让颜色流动起来 */
        @keyframes gradient-shift {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        /* 标题容器添加光晕效果 */
        .main-title-wrapper {
            position: relative;
            display: inline-block;
            filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.4));
        }
        
        /* 统计卡片样式 - 扁平化设计 */
        .metric-card {
            background: white;
            padding: 0.8rem 1.2rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
        }
        
        /* 不同主题的统计卡片 */
        .metric-card.card-blue {
            border-left-color: #667eea;
        }
        
        .metric-card.card-green {
            border-left-color: #10b981;
        }
        
        .metric-card.card-orange {
            border-left-color: #f59e0b;
        }
        
        /* 整体页面背景 */
        .stApp {
            background: #f5f5f5;
        }
        
        /* 侧边栏样式 - 米黄色 */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #fef9e7 0%, #faf5e6 100%);
        }
        
        /* 按钮样式增强 */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
            border: none;
            padding: 0.5rem 1rem;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        
        /* 侧边栏按钮样式 */
        .sidebar .stButton > button {
            font-size: 0.95rem;
        }
        
        /* 输入框样式 */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            transition: border-color 0.3s;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stDateInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* 航班记录卡片 */
        .flight-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 0.6rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 3px solid #667eea;
            transition: all 0.3s;
        }
        
        .flight-card:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            transform: translateX(5px);
        }
        
        /* 地图容器样式 */
        .map-container {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 0.3rem 0 1rem 0;
        }
        
        /* 表格样式 */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* 分隔线样式 */
        hr {
            margin: 0.8rem 0;
            border: none;
            border-top: 2px solid #e0e0e0;
        }
        
        /* 信息框样式 */
        .stInfo {
            border-radius: 10px;
            border-left: 4px solid #17a2b8;
        }
        
        .stSuccess {
            border-radius: 10px;
            border-left: 4px solid #28a745;
        }
        
        .stError {
            border-radius: 10px;
            border-left: 4px solid #dc3545;
        }
        
        .stWarning {
            border-radius: 10px;
            border-left: 4px solid #ffc107;
        }
        
        /* 侧边栏标题样式 */
        .sidebar h1, .sidebar h2, .sidebar h3 {
            color: #667eea;
            font-weight: 700;
        }
        
        /* 主内容区样式 */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
        
        /* 主内容区背景 - 浅灰色 */
        .main {
            background: #f5f5f5;
        }
        
        /* 减少标题和内容之间的间距 */
        h3 {
            margin-top: 0.5rem;
            margin-bottom: 0.2rem;
        }
        
        /* 减少markdown元素之间的间距 */
        .element-container {
            margin-bottom: 0.5rem;
        }
        
        /* 展开器样式 */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 10px;
            font-weight: 600;
        }
        
        /* 城市标签样式 */
        .city-tag {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            margin: 0.3rem 0.3rem 0.3rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .city-tag:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        /* 城市列表容器 */
        .cities-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.3rem;
            margin-top: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)


def render_main_title():
    """渲染主标题 - 炫酷渐变色效果"""
    st.markdown('<div class="main-title-wrapper"><h1 class="main-title">✈️ SkyLink航班管家</h1></div>', unsafe_allow_html=True)


def render_metric_card(title, value, subtitle="", card_type="blue"):
    """
    渲染统计卡片
    
    参数:
        title: 卡片标题（包含图标）
        value: 主要数值
        subtitle: 副标题/说明文字
        card_type: 卡片类型 ("blue", "green", "orange")
    """
    # 根据类型选择颜色
    color_map = {
        "blue": "#667eea",
        "green": "#10b981",
        "orange": "#f59e0b"
    }
    card_color = color_map.get(card_type, "#667eea")
    
    st.markdown(f"""
    <div class="metric-card card-{card_type}">
        <h3 style="color: {card_color}; margin: 0 0 0.2rem 0; font-size: 1.0rem; font-weight: 600; letter-spacing: 0.3px;">{title}</h3>
        <h2 style="color: #1a202c; margin: 0.1rem 0; font-size: 2.0rem; font-weight: 700; line-height: 1.1;">{value}</h2>
        <p style="color: #64748b; margin: 0.2rem 0 0 0; font-size: 0.8rem; font-weight: 500;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_flight_card(departure_city, arrival_city, date, distance, flight_time_str):
    """
    渲染航班记录卡片
    
    参数:
        departure_city: 出发城市
        arrival_city: 到达城市
        date: 日期
        distance: 距离
        flight_time_str: 飞行时间字符串
    """
    st.markdown(f"""
    <div class="flight-card">
        <div style="margin-bottom: 0.8rem;">
            <h4 style="color: #1a202c; margin: 0; font-size: 1.1rem; font-weight: 600;">
                <span style="color: #667eea; font-weight: 700;">{departure_city}</span> 
                <span style="color: #94a3b8; margin: 0 0.5rem;">→</span>
                <span style="color: #ff6b35; font-weight: 700;">{arrival_city}</span>
            </h4>
        </div>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.3rem;">
                <span style="font-size: 0.9rem;">📅</span>
                <span style="color: #475569; font-size: 0.85rem; font-weight: 500;">{date}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.3rem;">
                <span style="font-size: 0.9rem;">📏</span>
                <span style="color: #475569; font-size: 0.85rem; font-weight: 500;">{distance:.0f} km</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.3rem;">
                <span style="font-size: 0.9rem;">⏱️</span>
                <span style="color: #475569; font-size: 0.85rem; font-weight: 500;">{flight_time_str}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_confirmation_info(pending_data, distance, flight_time_str, dep_coords, arr_coords):
    """
    渲染确认对话框的信息展示
    
    参数:
        pending_data: 待确认的航班数据字典
        distance: 飞行距离
        flight_time_str: 飞行时间字符串
        dep_coords: 出发地坐标
        arr_coords: 到达地坐标
    """
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
            <p style="margin: 0.3rem 0;"><strong>出发城市：</strong> {pending_data['departure_city']}</p>
            <p style="margin: 0.3rem 0;"><strong>到达城市：</strong> {pending_data['arrival_city']}</p>
            <p style="margin: 0.3rem 0;"><strong>出行日期：</strong> {pending_data['date'].strftime('%Y-%m-%d')}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_info2:
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
            <p style="margin: 0.3rem 0;"><strong>飞行距离：</strong> {distance:.0f} 公里</p>
            <p style="margin: 0.3rem 0;"><strong>飞行时间：</strong> {flight_time_str}</p>
            <p style="margin: 0.3rem 0; font-size: 0.85rem; color: #718096;"><strong>坐标：</strong> ({dep_coords[0]:.4f}, {dep_coords[1]:.4f}) → ({arr_coords[0]:.4f}, {arr_coords[1]:.4f})</p>
        </div>
        """, unsafe_allow_html=True)


def render_map_container():
    """渲染地图容器的开始标签"""
    st.markdown('<div class="map-container">', unsafe_allow_html=True)


def close_map_container():
    """关闭地图容器的结束标签"""
    st.markdown('</div>', unsafe_allow_html=True)


def render_cities_card(cities, card_type="purple"):
    """
    渲染城市列表卡片（垂直布局）
    
    参数:
        cities: 城市列表（已去重）
        card_type: 卡片类型，用于设置边框颜色
    """
    # 根据类型选择颜色
    color_map = {
        "blue": "#667eea",
        "green": "#10b981",
        "orange": "#f59e0b",
        "purple": "#764ba2"
    }
    card_color = color_map.get(card_type, "#764ba2")
    
    # 生成城市标签HTML
    if cities:
        city_tags_html = '<div class="cities-container">'
        for city in sorted(cities):  # 按字母顺序排序
            city_tags_html += f'<span class="city-tag">{city}</span>'
        city_tags_html += '</div>'
        cities_count = len(cities)
    else:
        city_tags_html = '<p style="color: #94a3b8; margin: 0.5rem 0; font-size: 0.9rem;">暂无城市记录</p>'
        cities_count = 0
    
    st.markdown(f"""
    <div class="metric-card card-{card_type}">
        <h3 style="color: {card_color}; margin: 0 0 0.4rem 0; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.3px;">🌆 去过的城市</h3>
        <h2 style="color: #1a202c; margin: 0.3rem 0; font-size: 2rem; font-weight: 700; line-height: 1.2;">{cities_count}</h2>
        <p style="color: #64748b; margin: 0.4rem 0 0 0; font-size: 0.8rem; font-weight: 500;">共 {cities_count} 个城市</p>
        {city_tags_html}
    </div>
    """, unsafe_allow_html=True)


def render_cities_card_horizontal(city_counts, card_type="purple"):
    """
    渲染横向长条城市列表卡片
    
    参数:
        city_counts: 城市和次数的字典，格式为 {城市名: 次数}
        card_type: 卡片类型，用于设置边框颜色
    """
    # 根据类型选择颜色
    color_map = {
        "blue": "#667eea",
        "green": "#10b981",
        "orange": "#f59e0b",
        "purple": "#764ba2"
    }
    card_color = color_map.get(card_type, "#764ba2")
    
    # 生成城市标签HTML，按次数降序排列
    if city_counts:
        # 按次数降序排序，如果次数相同则按城市名排序
        sorted_cities = sorted(city_counts.items(), key=lambda x: (-x[1], x[0]))
        city_tags_html = '<div class="cities-container">'
        for city, count in sorted_cities:
            city_tags_html += f'<span class="city-tag">{city} <span style="opacity: 0.8; font-weight: 600;">({count})</span></span>'
        city_tags_html += '</div>'
        cities_count = len(city_counts)
    else:
        city_tags_html = '<p style="color: #94a3b8; margin: 0.5rem 0; font-size: 0.9rem;">暂无城市记录</p>'
        cities_count = 0
    
    st.markdown(f"""
    <div class="metric-card card-{card_type}" style="padding: 1rem 1.4rem;">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
            <h3 style="color: {card_color}; margin: 0; font-size: 1.0rem; font-weight: 600; letter-spacing: 0.3px; white-space: nowrap;">🌆 去过的城市</h3>
            <span style="color: #64748b; font-size: 0.85rem; font-weight: 500;">共 {cities_count} 个城市</span>
        </div>
        {city_tags_html}
    </div>
    """, unsafe_allow_html=True)

