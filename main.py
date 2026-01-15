"""
航班记录与可视化系统 (MVP)
使用 Streamlit + Folium 实现航班路线可视化
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import pandas as pd
from datetime import datetime
import database_utils
import ui

# 页面配置
st.set_page_config(
    page_title="SkyLink私人航班管家",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 加载自定义CSS样式
ui.load_custom_css()

# 初始化数据库
database_utils.init_database()

# 初始化session_state用于存储航班记录（从数据库加载）
if 'flights' not in st.session_state:
    st.session_state.flights = database_utils.load_flights_from_db()

# 初始化编辑状态
if 'editing_flight_id' not in st.session_state:
    st.session_state.editing_flight_id = None

# 初始化删除确认状态
if 'deleting_flight_id' not in st.session_state:
    st.session_state.deleting_flight_id = None

def reload_flights():
    """从数据库重新加载航班记录到session_state"""
    st.session_state.flights = database_utils.load_flights_from_db()

# 初始化地理编码器
@st.cache_resource
def get_geocoder():
    """初始化并缓存地理编码器"""
    return Nominatim(user_agent="flight_tracker_app")

geolocator = get_geocoder()

def geocode_city(city_name):
    """
    根据城市名称获取经纬度坐标
    返回: (latitude, longitude) 或 None（如果未找到）
    """
    try:
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        return None
    except Exception as e:
        st.error(f"地理编码错误 ({city_name}): {str(e)}")
        return None

def calculate_distance(point1, point2):
    """
    计算两点间的大圆距离（公里）
    使用geopy的great_circle函数
    """
    try:
        distance = great_circle(point1, point2).kilometers
        return round(distance, 2)
    except Exception as e:
        st.error(f"距离计算错误: {str(e)}")
        return None

def format_flight_time(minutes):
    """
    格式化飞行时间（分钟）为可读字符串
    例如: 90 -> "1小时30分钟", 120 -> "2小时"
    """
    if minutes is None or minutes == 0:
        return "未设置"
    # 确保minutes是整数类型
    try:
        minutes = int(minutes)
    except (ValueError, TypeError):
        return "未设置"
    
    if minutes <= 0:
        return "未设置"
    
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0 and mins > 0:
        return f"{hours}小时{mins}分钟"
    elif hours > 0:
        return f"{hours}小时"
    else:
        return f"{mins}分钟"

def minutes_to_hours_minutes(minutes):
    """
    将分钟数转换为(小时, 分钟)元组
    例如: 90 -> (1, 30), 120 -> (2, 0)
    """
    if minutes is None or minutes == 0:
        return (0, 0)
    try:
        minutes = int(minutes)
        if minutes <= 0:
            return (0, 0)
        return (minutes // 60, minutes % 60)
    except (ValueError, TypeError):
        return (0, 0)

def hours_minutes_to_minutes(hours, minutes):
    """
    将小时和分钟转换为总分钟数
    例如: (1, 30) -> 90, (2, 0) -> 120
    """
    try:
        hours = int(hours) if hours else 0
        minutes = int(minutes) if minutes else 0
        return hours * 60 + minutes
    except (ValueError, TypeError):
        return 0

def format_total_flight_time(total_minutes):
    """
    格式化总飞行时间为可读字符串（用于统计显示）
    例如: 390 -> "6小时30分钟"
    """
    if total_minutes is None or total_minutes == 0:
        return "0小时"
    try:
        total_minutes = int(total_minutes)
        if total_minutes <= 0:
            return "0小时"
        hours = total_minutes // 60
        mins = total_minutes % 60
        if hours > 0 and mins > 0:
            return f"{hours}小时{mins}分钟"
        elif hours > 0:
            return f"{hours}小时"
        else:
            return f"{mins}分钟"
    except (ValueError, TypeError):
        return "0小时"

def is_in_china(lat, lon):
    """
    判断坐标是否在中国范围内
    中国大致范围：纬度 18-54，经度 73-135
    """
    return 18 <= lat <= 54 and 73 <= lon <= 135

def create_flight_map(flights_data):
    """
    创建并返回包含所有航班路线的folium地图对象
    """
    if not flights_data:
        # 如果没有航班数据，显示世界地图中心（北京）
        m = folium.Map(location=[39.9042, 116.4074], zoom_start=2)
        return m
    
    # 计算地图中心（所有坐标的平均值）
    all_coords = []
    for flight in flights_data:
        if flight.get('departure_coords') and flight.get('arrival_coords'):
            all_coords.append(flight['departure_coords'])
            all_coords.append(flight['arrival_coords'])
    
    if all_coords:
        center_lat = sum(coord[0] for coord in all_coords) / len(all_coords)
        center_lon = sum(coord[1] for coord in all_coords) / len(all_coords)
        m = folium.Map(location=[center_lat, center_lon], zoom_start=3)
    else:
        m = folium.Map(location=[39.9042, 116.4074], zoom_start=2)
    
    # 绘制每条航线
    colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a']
    for idx, flight in enumerate(flights_data):
        dep_coords = flight.get('departure_coords')
        arr_coords = flight.get('arrival_coords')
        
        if dep_coords and arr_coords:
            color = colors[idx % len(colors)]
            
            # 添加出发地marker（使用更美观的图标）
            folium.Marker(
                location=dep_coords,
                popup=f"""
                <div style="font-family: Arial; min-width: 150px;">
                    <h4 style="margin: 5px 0; color: #667eea;">✈️ 出发地</h4>
                    <p style="margin: 5px 0;"><strong>{flight['departure_city']}</strong></p>
                    <p style="margin: 5px 0; font-size: 0.9em; color: #666;">日期: {flight['date']}</p>
                </div>
                """,
                tooltip=f"出发: {flight['departure_city']}",
                icon=folium.Icon(color='green', icon='plane', prefix='fa', icon_color='white')
            ).add_to(m)
            
            # 添加到达地marker
            folium.Marker(
                location=arr_coords,
                popup=f"""
                <div style="font-family: Arial; min-width: 150px;">
                    <h4 style="margin: 5px 0; color: #764ba2;">✈️ 到达地</h4>
                    <p style="margin: 5px 0;"><strong>{flight['arrival_city']}</strong></p>
                    <p style="margin: 5px 0; font-size: 0.9em; color: #666;">日期: {flight['date']}</p>
                </div>
                """,
                tooltip=f"到达: {flight['arrival_city']}",
                icon=folium.Icon(color='red', icon='plane', prefix='fa', icon_color='white')
            ).add_to(m)
            
            # 绘制飞行路线（使用更美观的样式）
            flight_time_str = format_flight_time(flight.get('flight_time'))
            folium.PolyLine(
                locations=[dep_coords, arr_coords],
                popup=f"""
                <div style="font-family: Arial; min-width: 200px;">
                    <h4 style="margin: 5px 0; color: {color};">
                        {flight['departure_city']} → {flight['arrival_city']}
                    </h4>
                    <p style="margin: 5px 0;"><strong>日期:</strong> {flight['date']}</p>
                    <p style="margin: 5px 0;"><strong>距离:</strong> {flight.get('distance', 'N/A'):.0f} 公里</p>
                    <p style="margin: 5px 0;"><strong>飞行时间:</strong> {flight_time_str}</p>
                </div>
                """,
                color=color,
                weight=3,
                opacity=0.8,
                dashArray='10, 5'
            ).add_to(m)
    
    return m

# 主界面
ui.render_main_title()

# 侧边栏：输入表单
with st.sidebar:
    st.markdown("### ✈️ 添加航班记录")
    st.markdown("")
    
    departure_city = st.text_input("出发城市", placeholder="例如: Beijing")
    arrival_city = st.text_input("到达城市", placeholder="例如: San Francisco")
    flight_date = st.date_input("出行日期", value=datetime.now().date())
    flight_distance = st.number_input(
        "飞行距离（公里，可选）", 
        min_value=0.0, 
        value=0.0,
        help="如果留空（0），系统将自动计算"
    )
    st.write("**飞行时间（可选）**")
    flight_time_col1, flight_time_col2 = st.columns(2)
    with flight_time_col1:
        flight_time_hours = st.number_input("小时", min_value=0, value=0, step=1, key="flight_time_hours")
    with flight_time_col2:
        flight_time_minutes = st.number_input("分钟", min_value=0, max_value=59, value=0, step=1, key="flight_time_minutes", help="如果留空，则时间默认为0")
    
    if st.button("添加航班", type="primary", use_container_width=True):
        if not departure_city or not arrival_city:
            st.error("⚠️ 请填写出发城市和到达城市")
        else:
            # 设置显示确认对话框
            st.session_state.show_add_confirm = True
            st.session_state.pending_flight_data = {
                'departure_city': departure_city,
                'arrival_city': arrival_city,
                'date': flight_date,
                'distance': flight_distance,
                'flight_time_hours': flight_time_hours,
                'flight_time_minutes': flight_time_minutes
            }
            st.rerun()
    
    # 显示确认对话框
    if st.session_state.get('show_add_confirm', False):
        pending_data = st.session_state.get('pending_flight_data', {})
        
        # 地理编码
        with st.spinner("正在解析城市坐标..."):
            dep_coords = geocode_city(pending_data['departure_city'])
            arr_coords = geocode_city(pending_data['arrival_city'])
        
        if dep_coords and arr_coords:
            # 计算距离（如果未提供）
            if pending_data['distance'] == 0:
                distance = calculate_distance(dep_coords, arr_coords)
            else:
                distance = pending_data['distance']
            
            if distance:
                # 将小时和分钟转换为总分钟数
                total_flight_time = hours_minutes_to_minutes(
                    pending_data['flight_time_hours'],
                    pending_data['flight_time_minutes']
                )
                
                # 显示确认对话框
                st.markdown("")
                st.info("📋 **请确认航班信息**")
                st.markdown("")
                
                flight_time_str = format_flight_time(total_flight_time if total_flight_time > 0 else None)
                ui.render_confirmation_info(pending_data, distance, flight_time_str, dep_coords, arr_coords)
                
                st.markdown("")
                
                col_confirm1, col_confirm2 = st.columns(2)
                with col_confirm1:
                    if st.button("✅ 确认添加", type="primary", use_container_width=True):
                        # 添加航班记录
                        flight_record = {
                            'departure_city': pending_data['departure_city'],
                            'arrival_city': pending_data['arrival_city'],
                            'date': pending_data['date'].strftime('%Y-%m-%d'),
                            'distance': distance,
                            'departure_coords': dep_coords,
                            'arrival_coords': arr_coords,
                            'flight_time': total_flight_time if total_flight_time > 0 else None
                        }
                        # 保存到数据库
                        flight_id = database_utils.save_flight_to_db(flight_record)
                        flight_record['id'] = flight_id
                        # 更新session_state
                        st.session_state.flights.append(flight_record)
                        # 清除确认对话框状态
                        st.session_state.show_add_confirm = False
                        st.session_state.pending_flight_data = {}
                        st.success(f"已添加航班: {pending_data['departure_city']} → {pending_data['arrival_city']}")
                        st.rerun()
                
                with col_confirm2:
                    if st.button("❌ 取消", use_container_width=True):
                        # 清除确认对话框状态
                        st.session_state.show_add_confirm = False
                        st.session_state.pending_flight_data = {}
                        st.rerun()
        else:
            st.error("无法解析城市坐标，请检查城市名称是否正确")
            if st.button("关闭", key="close_error"):
                st.session_state.show_add_confirm = False
                st.session_state.pending_flight_data = {}
                st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 航班数据管理")
    st.markdown("")
    
    # 一键导入外部软件数据按钮
    if st.button("📥 一键导入外部软件数据（如航旅纵横）", use_container_width=True, type="secondary"):
        st.info("功能开发中，敬请期待（可能调API难度较大🧐）...")
    
    st.markdown("")
    
    # 显示航班记录列表（按日期排序）
    if st.session_state.flights:
        st.markdown("#### 航班记录列表")
        # 按日期排序（从晚到早，最新的在最上面）
        sorted_flights = sorted(st.session_state.flights, key=lambda x: x['date'], reverse=True)
        for idx, flight in enumerate(sorted_flights):
            with st.container():
                # 使用卡片样式显示航班记录
                flight_time_str = format_flight_time(flight.get('flight_time'))
                ui.render_flight_card(
                    flight['departure_city'],
                    flight['arrival_city'],
                    flight['date'],
                    flight['distance'],
                    flight_time_str
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    edit_key = f"edit_{flight['id']}"
                    if st.button("✏️ 编辑", key=edit_key, use_container_width=True):
                        st.session_state.editing_flight_id = flight['id']
                        st.rerun()
                
                with col2:
                    delete_key = f"delete_{flight['id']}"
                    if st.button("🗑️ 删除", key=delete_key, use_container_width=True):
                        st.session_state.deleting_flight_id = flight['id']
                        st.rerun()
                
                # 删除确认对话框
                if st.session_state.deleting_flight_id == flight['id']:
                    st.markdown("")
                    st.warning(f"⚠️ **确定要删除航班记录吗？**\n\n**{flight['departure_city']} → {flight['arrival_city']}**\n\n此操作不可恢复！")
                    st.markdown("")
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("✅ 确认删除", key=f"confirm_delete_{flight['id']}", type="primary", use_container_width=True):
                            database_utils.delete_flight_from_db(flight['id'])
                            reload_flights()
                            st.session_state.deleting_flight_id = None
                            st.success(f"✅ 已删除航班: {flight['departure_city']} → {flight['arrival_city']}")
                            st.rerun()
                    with confirm_col2:
                        if st.button("❌ 取消", key=f"cancel_delete_{flight['id']}", use_container_width=True):
                            st.session_state.deleting_flight_id = None
                            st.rerun()
                
                # 编辑表单
                if st.session_state.editing_flight_id == flight['id']:
                    st.markdown("")
                    st.markdown("#### ✏️ 编辑航班记录")
                    st.markdown("")
                    
                    edit_col1, edit_col2 = st.columns(2)
                    with edit_col1:
                        edit_departure = st.text_input("出发城市", value=flight['departure_city'], key=f"edit_dep_{flight['id']}")
                        edit_date = st.date_input("出行日期", value=datetime.strptime(flight['date'], '%Y-%m-%d').date(), key=f"edit_date_{flight['id']}")
                    with edit_col2:
                        edit_arrival = st.text_input("到达城市", value=flight['arrival_city'], key=f"edit_arr_{flight['id']}")
                        edit_distance = st.number_input("飞行距离（公里）", value=float(flight['distance']), min_value=0.0, key=f"edit_dist_{flight['id']}")
                    
                    # 将分钟数转换为小时和分钟
                    flight_time_hours_edit, flight_time_mins_edit = minutes_to_hours_minutes(flight.get('flight_time'))
                    edit_col3, edit_col4 = st.columns(2)
                    with edit_col3:
                        st.write("**飞行时间（可选）**")
                    with edit_col4:
                        st.write("")  # 占位符，保持对齐
                    edit_col5, edit_col6 = st.columns(2)
                    with edit_col5:
                        edit_flight_time_hours = st.number_input(
                            "小时", 
                            value=flight_time_hours_edit,
                            min_value=0, 
                            step=1,
                            key=f"edit_time_hours_{flight['id']}"
                        )
                    with edit_col6:
                        edit_flight_time_minutes = st.number_input(
                            "分钟", 
                            value=flight_time_mins_edit,
                            min_value=0,
                            max_value=59,
                            step=1,
                            key=f"edit_time_mins_{flight['id']}"
                        )
                    
                    edit_col7, edit_col8 = st.columns(2)
                    with edit_col7:
                        if st.button("✅ 保存", key=f"save_{flight['id']}", type="primary", use_container_width=True):
                            if not edit_departure or not edit_arrival:
                                st.error("⚠️ 请填写出发城市和到达城市")
                            else:
                                with st.spinner("正在更新..."):
                                    # 在按钮点击时从session_state重新读取输入框值（因为使用了key参数）
                                    # 这样可以确保获取到用户修改后的最新值
                                    flight_time_hours_key = f"edit_time_hours_{flight['id']}"
                                    flight_time_mins_key = f"edit_time_mins_{flight['id']}"
                                    edit_flight_time_hours_val = st.session_state.get(flight_time_hours_key, edit_flight_time_hours)
                                    edit_flight_time_minutes_val = st.session_state.get(flight_time_mins_key, edit_flight_time_minutes)
                                    
                                    # 将小时和分钟转换为总分钟数
                                    total_edit_flight_time = hours_minutes_to_minutes(edit_flight_time_hours_val, edit_flight_time_minutes_val)
                                    
                                    # 如果城市名称改变，需要重新地理编码
                                    if edit_departure != flight['departure_city'] or edit_arrival != flight['arrival_city']:
                                        dep_coords = geocode_city(edit_departure)
                                        arr_coords = geocode_city(edit_arrival)
                                        
                                        if not dep_coords or not arr_coords:
                                            st.error("无法解析城市坐标，请检查城市名称是否正确")
                                        else:
                                            # 如果距离未手动修改，重新计算
                                            if edit_distance == flight['distance']:
                                                edit_distance = calculate_distance(dep_coords, arr_coords)
                                            
                                            updated_record = {
                                                'departure_city': edit_departure,
                                                'arrival_city': edit_arrival,
                                                'date': edit_date.strftime('%Y-%m-%d'),
                                                'distance': edit_distance,
                                                'departure_coords': dep_coords,
                                                'arrival_coords': arr_coords,
                                                'flight_time': total_edit_flight_time if total_edit_flight_time > 0 else None
                                            }
                                            database_utils.update_flight_in_db(flight['id'], updated_record)
                                            st.session_state.editing_flight_id = None
                                            reload_flights()
                                            st.success("航班记录已更新")
                                            st.rerun()
                                    else:
                                        # 城市名称未改变，只需更新日期、距离和飞行时间
                                        updated_record = {
                                            'departure_city': edit_departure,
                                            'arrival_city': edit_arrival,
                                            'date': edit_date.strftime('%Y-%m-%d'),
                                            'distance': edit_distance,
                                            'departure_coords': flight['departure_coords'],
                                            'arrival_coords': flight['arrival_coords'],
                                            'flight_time': total_edit_flight_time if total_edit_flight_time > 0 else None
                                        }
                                        database_utils.update_flight_in_db(flight['id'], updated_record)
                                        st.session_state.editing_flight_id = None
                                        reload_flights()
                                        st.success("航班记录已更新")
                                        st.rerun()
                    
                    with edit_col8:
                        if st.button("❌ 取消", key=f"cancel_{flight['id']}", use_container_width=True):
                            st.session_state.editing_flight_id = None
                            st.rerun()
    else:
        st.info("暂无航班记录")
    
    st.markdown("---")
    st.markdown("")
    if st.button("🗑️ 清空所有记录", type="secondary", use_container_width=True):
        if st.session_state.flights:
            database_utils.clear_all_flights_from_db()
            reload_flights()
            st.success("✅ 已清空所有航班记录")
            st.rerun()
        else:
            st.info("💡 没有可清空的记录")

# 主内容区：统计信息和地图
st.markdown("### 📊 飞行统计概览")

col1, col2, col3 = st.columns(3)

with col1:
    total_flights = len(st.session_state.flights)
    # 统计国内和国外航班数
    domestic_count = 0
    international_count = 0
    for flight in st.session_state.flights:
        dep_coords = flight.get('departure_coords')
        arr_coords = flight.get('arrival_coords')
        if dep_coords and arr_coords:
            if is_in_china(dep_coords[0], dep_coords[1]) and is_in_china(arr_coords[0], arr_coords[1]):
                domestic_count += 1
            else:
                international_count += 1
        else:
            # 如果没有坐标信息，无法判断，暂时计入国际
            international_count += 1
    
    # 使用自定义样式显示总航班次数
    ui.render_metric_card(
        "✈️ 总航班次数",
        str(total_flights),
        f"国内 {domestic_count} | 国际 {international_count}",
        card_type="blue"
    )

with col2:
    total_distance = sum(flight.get('distance', 0) for flight in st.session_state.flights)
    distance_km = f"{total_distance:,.0f}"
    ui.render_metric_card(
        "🌍 累计飞行里程",
        distance_km,
        "公里",
        card_type="green"
    )

with col3:
    total_flight_time_minutes = sum(
        flight.get('flight_time', 0) or 0 
        for flight in st.session_state.flights
    )
    total_flight_time_str = format_total_flight_time(total_flight_time_minutes)
    ui.render_metric_card(
        "⏱️ 累计飞行时间",
        total_flight_time_str,
        "总时长",
        card_type="orange"
    )

# 第二排：去过的城市（长条框）
st.markdown("")
# 提取所有去过的城市（包括出发和到达城市）
all_cities = set()
for flight in st.session_state.flights:
    all_cities.add(flight['departure_city'])
    all_cities.add(flight['arrival_city'])

# 渲染横向长条城市列表卡片
ui.render_cities_card_horizontal(all_cities, card_type="purple")

# 显示地图
st.markdown("")
st.markdown("### 🌍 飞行路线地图")

if st.session_state.flights:
    flight_map = create_flight_map(st.session_state.flights)
    # 使用streamlit-folium渲染地图，添加容器样式
    ui.render_map_container()
    st_folium(flight_map, width=1200, height=600, returned_objects=[])
    ui.close_map_container()
    
    st.markdown("")
    # 显示航班列表（可选）
    with st.expander("📋 查看所有航班记录", expanded=True):
        df = pd.DataFrame([
            {
                '出发城市': flight['departure_city'],
                '到达城市': flight['arrival_city'],
                '日期': flight['date'],
                '距离（公里）': f"{flight.get('distance', 0):,.0f}",
                '飞行时间': format_flight_time(flight.get('flight_time'))
            }
            for flight in sorted(st.session_state.flights, key=lambda x: x['date'], reverse=True)
        ])
        # 使用样式化的表格
        st.dataframe(
            df, 
            use_container_width=True,
            hide_index=True
        )
else:
    st.info("💡 暂无航班记录，请在左侧添加第一条航班记录")
    # 显示空白地图
    ui.render_map_container()
    empty_map = folium.Map(location=[39.9042, 116.4074], zoom_start=2)
    st_folium(empty_map, width=1200, height=600, returned_objects=[])
    ui.close_map_container()
