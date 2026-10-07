import streamlit as st
import pandas as pd

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Công Cụ Tính Lãi Gửi Tiết Kiệm", 
    page_icon="💎", 
    layout="centered"
)

# 2. TÙY CHỈNH GIAO DIỆN SANG TRỌNG (CUSTOM CSS)
st.markdown("""
    <style>
    /* Nền tổng thể dải màu tối sang trọng */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Thiết kế thẻ hiển thị metric */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(217, 119, 6, 0.3);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(8px);
    }
    
    /* Nhãn và giá trị metric */
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 500;
    }
    [data-testid="stMetricValue"] {
        color: #fbbf24 !important;
        font-weight: 700;
    }

    /* Tùy chỉnh các ô nhập liệu */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    
    /* Đường phân cách ánh vàng */
    hr {
        border-color: rgba(245, 158, 11, 0.2) !important;
    }

    /* Thiết kế khung thông tin Highlight */
    .stAlert {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #f59e0b !important;
        color: #f8fafc !important;
        border-radius: 10px;
    }

    /* Tab navigation sang trọng */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        background-color: rgba(15, 23, 42, 0.6);
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background-color: #f59e0b !important;
        color: #0f172a !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. HIỂN THỊ LOGO VÀ TIÊU ĐỀ
try:
    st.image("logo.jpg", width=120)
except Exception:
    pass

st.title("💎 Ứng Dụng Tính Lãi Gửi Tiết Kiệm")
st.caption("👨‍💻 Thực hiện bởi: **Lê Thái Thanh Hải** | Email: thailehai49@gmail.com")
st.caption("Công cụ quản lý & hoạch định tài chính cao cấp")

# 4. CÁC TAB TÍNH NĂNG
tab1, tab2 = st.tabs(["📊 Tính Tiền Lãi Tiết Kiệm", "🎯 Tính Ngược Mục Tiêu Gửi"])

# ==============================================================================
# TAB 1: TÍNH TIỀN LÃI TIẾT KIỆM
# ==============================================================================
with tab1:
    st.subheader("📋 Thông tin khách hàng & Khoản gửi")

    ten_nguoi_gui = st.text_input(
        "Họ và tên người gửi:", 
        value="Nguyễn Văn A", 
        placeholder="Nhập họ và tên...",
        key="ten_tab1"
    )

    col1, col2 = st.columns(2)

    with col1:
        so_tien_goc = st.number_input(
            "Số tiền gửi (VNĐ):", 
            min_value=1_000_000, 
            value=100_000_000, 
            step=5_000_000, 
            format="%d",
            key="goc_tab1"
        )
        st.caption(f"👉 **{so_tien_goc:,.0f} VNĐ**")

        ky_han_thang = st.number_input(
            "Kỳ hạn gửi (tháng):", 
            min_value=1, 
            value=12, 
            step=1,
            key="kyhan_tab1"
        )

    with col2:
        lai_suat_nam = st.number_input(
            "Lãi suất (%/năm):", 
            min_value=0.1, 
            max_value=30.0, 
            value=6.0, 
            step=0.1,
            format="%.1f",
            key="laisuat_tab1"
        )

        hinh_thuc_lanh = st.selectbox(
            "Hình thức lãnh lãi:",
            options=["Lãnh lãi theo tháng", "Lãnh lãi theo quý", "Lãnh lãi cuối kỳ"],
            key="hinhthuc_tab1"
        )

    loai_lai = st.radio(
        "Phương pháp tính lãi:",
        options=["Lãi đơn", "Lãi kép"],
        horizontal=True,
        key="loailai_tab1"
    )

    # TÍNH TOÁN
    if hinh_thuc_lanh == "Lãnh lãi theo tháng":
        thang_moi_ky = 1
    elif hinh_thuc_lanh == "Lãnh lãi theo quý":
        thang_moi_ky = 3
    else:
        thang_moi_ky = ky_han_thang

    r_ky = (lai_suat_nam / 100) * (thang_moi_ky / 12)
    tong_so_ky = ky_han_thang / thang_moi_ky

    if loai_lai == "Lãi đơn":
        tien_lai_dinh_ky = so_tien_goc * r_ky
        tong_tien_lai = tien_lai_dinh_ky * tong_so_ky
        tong_goc_va_lai = so_tien_goc + tong_tien_lai
    else:
        if hinh_thuc_lanh == "Lãnh lãi cuối kỳ":
            tong_goc_va_lai = so_tien_goc * ((1 + r_ky) ** tong_so_ky)
            tong_tien_lai = tong_goc_va_lai - so_tien_goc
            tien_lai_dinh_ky = tong_tien_lai
        else:
            tong_goc_va_lai = so_tien_goc * ((1 + r_ky) ** tong_so_ky)
            tong_tien_lai = tong_goc_va_lai - so_tien_goc
            tien_lai_dinh_ky = so_tien_goc * r_ky

    # HIỂN THỊ KẾT QUẢ
    st.divider()
    ten_hien_thi = ten_nguoi_gui if ten_nguoi_gui.strip() != "" else "Khách hàng"
    st.subheader(f"🏛️ Bảng kết quả dự tính — {ten_hien_thi}")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        if loai_lai == "Lãi kép" and hinh_thuc_lanh != "Lãnh lãi cuối kỳ":
            st.metric(
                label="Lãi kỳ đầu tiên", 
                value=f"{tien_lai_dinh_ky:,.0f} VNĐ"
            )
            st.caption("*(Lãi kép tăng dần từng kỳ)*")
        else:
            st.metric(
                label=f"Tiền lãi / {hinh_thuc_lanh.replace('Lãnh lãi theo ', '').replace('Lãnh lãi ', '')}", 
                value=f"{tien_lai_dinh_ky:,.0f} VNĐ"
            )

    with col_b:
        st.metric(
            label="Tổng tiền lãi nhận được", 
            value=f"{tong_tien_lai:,.0f} VNĐ"
        )

    with col_c:
        st.metric(
            label="Tổng số tiền gốc + lãi", 
            value=f"{tong_goc_va_lai:,.0f} VNĐ"
        )

    st.info(
        f"👤 **Khách hàng:** {ten_hien_thi}\n\n"
        f"💡 **Tóm tắt:** Gửi **{so_tien_goc:,.0f} VNĐ** trong **{ky_han_thang} tháng** "
        f"với lãi suất **{lai_suat_nam}%/năm** theo phương thức **{loai_lai}** ({hinh_thuc_lanh.lower()})."
    )

    # BIỂU ĐỒ VÀ BẢNG LỊCH TRÌNH
    st.divider()
    st.subheader("📈 Lịch trình tăng trưởng tài sản")

    data = []
    goc_don = so_tien_goc
    goc_kep = so_tien_goc

    for k in range(1, int(tong_so_ky) + 1):
        lai_don_ky = so_tien_goc * r_ky
        goc_don += lai_don_ky

        lai_kep_ky = goc_kep * r_ky
        goc_kep += lai_kep_ky

        data.append({
            "Khách hàng": ten_hien_thi,
            "Kỳ thứ": f"Kỳ {k}",
            "Lãi đơn (VNĐ)": round(goc_don),
            "Lãi kép (VNĐ)": round(goc_kep),
            "Lãi nhận kỳ này": round(lai_don_ky if loai_lai == "Lãi đơn" else lai_kep_ky)
        })

    df = pd.DataFrame(data)

    st.write("📊 **Biểu đồ so sánh tích lũy tài sản (Lãi đơn vs Lãi kép):**")
    st.line_chart(df.set_index("Kỳ thứ")[["Lãi đơn (VNĐ)", "Lãi kép (VNĐ)"]])

    with st.expander("🔍 Bấm để xem chi tiết bảng dòng tiền từng kỳ"):
        st.dataframe(df, use_container_width=True)

        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        file_name_save = f"bao_cao_tiet_kiem_{ten_hien_thi.replace(' ', '_')}.csv"
        
        st.download_button(
            label="📥 Tải báo cáo (.CSV)",
            data=csv_data,
            file_name=file_name_save,
            mime="text/csv"
        )

# ==============================================================================
# TAB 2: TÍNH NGƯỢC MỤC TIÊU TIẾT KIỆM
# ==============================================================================
with tab2:
    st.subheader("🎯 Thiết lập mục tiêu tài chính")
    
    ten_nguoi_gui_tab2 = st.text_input(
        "Họ và tên khách hàng:", 
        value="Nguyễn Văn A", 
        placeholder="Nhập họ và tên...",
        key="ten_tab2"
    )

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        muc_tieu = st.number_input(
            "Số tiền mục tiêu mong muốn (VNĐ):", 
            min_value=10_000_000, 
            value=500_000_000, 
            step=10_000_000, 
            format="%d"
        )
        st.caption(f"🎯 Mục tiêu: **{muc_tieu:,.0f} VNĐ**")

        ky_han_muon = st.number_input(
            "Thời gian gửi (tháng):", 
            min_value=1, 
            value=24, 
            step=1
        )

    with col_m2:
        lai_suat_muon = st.number_input(
            "Lãi suất dự kiến (%/năm):", 
            min_value=0.1, 
            max_value=30.0, 
            value=6.5, 
            step=0.1,
            format="%.1f"
        )

        loai_lai_muon = st.radio(
            "Phương thức áp dụng:",
            options=["Lãi kép (Khuyên dùng)", "Lãi đơn"]
        )

    r_thang = (lai_suat_muon / 100) / 12

    if "Lãi kép" in loai_lai_muon:
        goc_can_gui = muc_tieu / ((1 + r_thang) ** ky_han_muon)
    else:
        goc_can_gui = muc_tieu / (1 + (r_thang * ky_han_muon))

    tien_lai_nhan = muc_tieu - goc_can_gui

    st.divider()
    ten_hien_thi_2 = ten_nguoi_gui_tab2 if ten_nguoi_gui_tab2.strip() != "" else "Khách hàng"
    st.success(f"💎 Kế hoạch cho **{ten_hien_thi_2}**: Để đạt mục tiêu **{muc_tieu:,.0f} VNĐ** sau **{ky_han_muon} tháng**:")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.metric("Vốn gốc cần đầu tư ngay", f"{goc_can_gui:,.0f} VNĐ")
    with col_r2:
        st.metric("Tiền lãi tích lũy dự kiến", f"{tien_lai_nhan:,.0f} VNĐ")
