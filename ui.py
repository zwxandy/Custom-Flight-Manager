"""
UI样式和组件模块
包含所有前端样式定义和UI组件函数
"""

import streamlit as st


def load_custom_css():
    """加载自定义CSS样式"""
    st.markdown("""
    <style>
        /* 主标题样式 */
        .main-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }
        
        /* 统计卡片样式 */
        .metric-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 0.8rem 1rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
            transition: transform 0.2s;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* 侧边栏样式 */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* 按钮样式增强 */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s;
            border: none;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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
            margin-bottom: 1rem;
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
    </style>
    """, unsafe_allow_html=True)


def render_main_title():
    """渲染主标题"""
    st.markdown('<h1 class="main-title">✈️ Xuan的私人航班管家</h1>', unsafe_allow_html=True)


def render_metric_card(title, value, subtitle=""):
    """
    渲染统计卡片
    
    参数:
        title: 卡片标题（包含图标）
        value: 主要数值
        subtitle: 副标题/说明文字
    """
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #667eea; margin: 0 0 0.3rem 0; font-size: 0.9rem; font-weight: 600;">{title}</h3>
        <h2 style="color: #2d3748; margin: 0.2rem 0; font-size: 1.8rem; font-weight: 700;">{value}</h2>
        <p style="color: #718096; margin: 0.3rem 0 0 0; font-size: 0.75rem;">{subtitle}</p>
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
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <h4 style="color: #2d3748; margin: 0;">
                <span style="color: #667eea;">{departure_city}</span> 
                → 
                <span style="color: #764ba2;">{arrival_city}</span>
            </h4>
        </div>
        <p style="color: #718096; font-size: 0.85rem; margin: 0.5rem 0;">
            📅 {date} | 📏 {distance:.0f} km | ⏱️ {flight_time_str}
        </p>
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

