
import streamlit as st
from datetime import datetime

# =========================
# CẤU HÌNH APP
# =========================
st.set_page_config(
    page_title="Quán Trà Sữa Lin Lin",
    page_icon="🧋",
    layout="centered"
)

st.title("🧋 QUÁN TRÀ SỮA LIN LIN")
st.write("Tính bill và xuất hóa đơn")

# =========================
# DỮ LIỆU MENU
# =========================

menu = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa socola": 35000,
    "Trà sữa matcha": 35000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000
}

toppings = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000
}

sugar_levels = ["100%", "70%", "0%"]

# =========================
# KHỞI TẠO GIỎ HÀNG
# =========================

if "cart" not in st.session_state:
    st.session_state.cart = []

# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================

st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)

# =========================
# CHỌN MÓN
# =========================

st.subheader("📝 Chọn món")

drink = st.selectbox(
    "🥤 Chọn loại thức uống",
    list(menu.keys())
)

size = st.radio(
    "📏 Chọn size",
    ["M", "L"],
    horizontal=True
)

size_price = 0

if size == "L":
    size_price = 5000

topping = st.selectbox(
    "🍮 Chọn topping",
    list(toppings.keys())
)

sugar = st.radio(
    "🍬 Mức độ đường",
    sugar_levels,
    horizontal=True
)

quantity = st.number_input(
    "🔢 Số lượng",
    min_value=1,
    max_value=20,
    value=1,
    step=1
)

# =========================
# TÍNH TIỀN
# =========================

unit_price = menu[drink] + size_price + toppings[topping]
total_item = unit_price * quantity

st.info(
    f"💰 Đơn giá: **{unit_price:,} VNĐ** | "
    f"Thành tiền: **{total_item:,} VNĐ**"
)

# =========================
# THÊM VÀO HÓA ĐƠN
# =========================

if st.button("➕ Thêm vào hóa đơn", use_container_width=True):

    item = {
        "drink": drink,
        "size": size,
        "topping": topping,
        "sugar": sugar,
        "quantity": quantity,
        "unit_price": unit_price,
        "total": total_item
    }

    st.session_state.cart.append(item)

    st.success("✅ Đã thêm món vào hóa đơn!")

# =========================
# HIỂN THỊ HÓA ĐƠN
# =========================

if st.session_state.cart:

    st.divider()
    st.subheader("🧾 HÓA ĐƠN")

    st.write(
        f"👤 **Khách hàng:** "
        f"{customer_name if customer_name else 'Khách lẻ'}"
    )

    grand_total = 0

    for i, item in enumerate(st.session_state.cart, start=1):

        st.write(
            f"**{i}. {item['drink']} - Size {item['size']}**"
        )

        st.write(
            f"Topping: {item['topping']} | "
            f"Đường: {item['sugar']} | "
            f"Số lượng: {item['quantity']}"
        )

        st.write(
            f"Đơn giá: {item['unit_price']:,} VNĐ | "
            f"Thành tiền: **{item['total']:,} VNĐ**"
        )

        grand_total += item["total"]

        st.divider()

    # =========================
    # TỔNG TIỀN
    # =========================

    st.subheader(
        f"💵 TỔNG THANH TOÁN: {grand_total:,} VNĐ"
    )

    col1, col2 = st.columns(2)

    # =========================
    # XÓA HÓA ĐƠN
    # =========================

    with col1:
        if st.button("🗑️ Xóa hóa đơn", use_container_width=True):
            st.session_state.cart = []
            st.rerun()

    # =========================
    # THANH TOÁN
    # =========================

    with col2:

        if st.button("💳 Thanh toán", use_container_width=True):

            now = datetime.now()
            invoice_code = now.strftime("%Y%m%d%H%M%S")

            invoice = ""

            invoice += "====================================\n"
            invoice += "       QUÁN TRÀ SỮA LIN LIN\n"
            invoice += "====================================\n"
            invoice += f"Mã hóa đơn: {invoice_code}\n"
            invoice += f"Thời gian: {now.strftime('%d/%m/%Y %H:%M:%S')}\n"
            invoice += f"Khách hàng: {customer_name if customer_name else 'Khách lẻ'}\n"
            invoice += "------------------------------------\n"

            for i, item in enumerate(
                st.session_state.cart,
                start=1
            ):

                invoice += f"{i}. {item['drink']}\n"
                invoice += f"   Size: {item['size']}\n"
                invoice += f"   Topping: {item['topping']}\n"
                invoice += f"   Đường: {item['sugar']}\n"
                invoice += f"   Số lượng: {item['quantity']}\n"
                invoice += f"   Đơn giá: {item['unit_price']:,} VNĐ\n"
                invoice += f"   Thành tiền: {item['total']:,} VNĐ\n"
                invoice += "------------------------------------\n"

            invoice += f"TỔNG THANH TOÁN: {grand_total:,} VNĐ\n"
            invoice += "====================================\n"
            invoice += "        CẢM ƠN QUÝ KHÁCH!\n"
            invoice += "====================================\n"

            st.success("🎉 Thanh toán thành công!")

            st.download_button(
                label="📥 Tải hóa đơn",
                data=invoice,
                file_name=f"hoa_don_{invoice_code}.txt",
                mime="text/plain",
                use_container_width=True
            )

else:
    st.warning("🛒 Chưa có món nào trong hóa đơn.")
```
