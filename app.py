import streamlit as st
st.image("logo.jpg", width=150)

st.set_page_config(page_title="Tính Lãi Gửi Tiết Kiệm", page_icon="💰", layout="centered")

st.title("💰 Ứng Dụng Tính Lãi Gửi Tiết Kiệm")
st.write("Nhập thông tin tiền gửi của bạn để tính toán tiền lãi theo lãi đơn và lãi kép.")

# --- NHẬP THÔNG TIN TỪ NGUỜI DÙNG ---
st.header("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien_goc = st.number_input(
        "Số tiền gửi (VNĐ):", 
        min_value=1_000_000, 
        value=100_000_000, 
        step=1_000_000, 
        format="%d"
    )
    st.caption(f"👉 **{so_tien_goc:,.0f} VNĐ**")

    ky_han_thang = st.number_input(
        "Kỳ hạn gửi (tháng):", 
        min_value=1, 
        value=12, 
        step=1
    )

with col2:
    lai_suat_nam = st.number_input(
        "Lãi suất (%/năm):", 
        min_value=0.1, 
        max_value=20.0, 
        value=6.0, 
        step=0.1,
        format="%.1f"
    )

    hinh_thuc_lanh = st.selectbox(
        "Hình thức lãnh lãi:",
        options=["Lãnh lãi theo tháng", "Lãnh lãi theo quý", "Lãnh lãi cuối kỳ"]
    )

loai_lai = st.radio(
    "Phương pháp tính lãi:",
    options=["Lãi đơn", "Lãi kép"],
    horizontal=True
)

# --- XỬ LÝ TÍNH TOÁN ---
# Xác định số kỳ nhập lãi/lãnh lãi trong 1 năm (m) và số tháng trong 1 kỳ (thang_moi_ky)
if hinh_thuc_lanh == "Lãnh lãi theo tháng":
    m = 12
    thang_moi_ky = 1
elif hinh_thuc_lanh == "Lãnh lãi theo quý":
    m = 4
    thang_moi_ky = 3
else:  # Lãnh lãi cuối kỳ
    m = 12 / ky_han_thang
    thang_moi_ky = ky_han_thang

# Tỷ lệ lãi suất trong 1 kỳ lãnh lãi
r_ky = (lai_suat_nam / 100) * (thang_moi_ky / 12)

# Tổng số kỳ lãnh lãi
tong_so_ky = ky_han_thang / thang_moi_ky

if loai_lai == "Lãi đơn":
    # Lãi đơn: Lãi định kỳ giữ nguyên, không cộng dồn vào gốc
    tien_lai_dinh_ky = so_tien_goc * r_ky
    tong_tien_lai = tien_lai_dinh_ky * tong_so_ky
    tong_goc_va_lai = so_tien_goc + tong_tien_lai
else:
    # Lãi kép: Lãi cộng dồn vào gốc sau mỗi kỳ
    if hinh_thuc_lanh == "Lãnh lãi cuối kỳ":
        # Cuối kỳ mới lãnh lãi 1 lần
        tong_goc_va_lai = so_tien_goc * ((1 + r_ky) ** tong_so_ky)
        tong_tien_lai = tong_goc_va_lai - so_tien_goc
        tien_lai_dinh_ky = tong_tien_lai
    else:
        # Nhập gốc định kỳ (tháng/quý)
        tong_goc_va_lai = so_tien_goc * ((1 + r_ky) ** tong_so_ky)
        tong_tien_lai = tong_goc_va_lai - so_tien_goc
        # Tiền lãi kỳ đầu tiên (để hiển thị tham khảo)
        tien_lai_dinh_ky = so_tien_goc * r_ky

# --- HIỂN THỊ KẾT QUẢ ---
st.divider()
st.header("📊 Kết quả tính toán")

# Hiển thị 3 chỉ số chính
col_a, col_b, col_c = st.columns(3)

with col_a:
    if loai_lai == "Lãi kép" and hinh_thuc_lanh != "Lãnh lãi cuối kỳ":
        st.metric(
            label="Lãi kỳ đầu tiên", 
            value=f"{tien_lai_dinh_ky:,.0f} VNĐ"
        )
        st.caption("*(Lãi kép tăng dần theo từng kỳ)*")
    else:
        st.metric(
            label=f"Tền lãi / {hinh_thuc_lanh.replace('Lãnh lãi theo ', '').replace('Lãnh lãi ', '')}", 
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

# Thông báo chi tiết bổ sung
st.info(
    f"💡 **Tóm tắt:** Gửi **{so_tien_goc:,.0f} VNĐ** trong **{ky_han_thang} tháng** "
    f"với lãi suất **{lai_suat_nam}%/năm** theo phương thức **{loai_lai}** ({hinh_thuc_lanh.lower()})."
)
