import streamlit as st
from datetime import datetime
st.image("Lin.png")
# =========================
# CẤU HÌNH
# =========================

st.set_page_config(
    page_title="Quán Trà Sữa Lin Lin",
    page_icon="🧋",
    layout="centered"
)

st.title("🧋 QUÁN TRÀ SỮA LIN LIN")
st.write("Tính bill và xuất hóa đơn")

# =========================
# MENU
# =========================

menu = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa socola": 35000,
    "Trà sữa matcha": 35000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
    "Cacao Latte": 40000
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
# GIỎ HÀNG
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
# CHỌN SỐ LƯỢNG LY
# =========================

st.divider()

st.subheader("🧋 Chọn món")

number_of_cups = st.number_input(
    "Bạn muốn chọn bao nhiêu ly?",
    min_value=1,
    max_value=20,
    value=1,
    step=1
)

# =========================
# TẠO GIAO DIỆN CHO TỪNG LY
# =========================

selected_items = []

for i in range(number_of_cups):

    st.markdown(f"### 🥤 Ly {i + 1}")

    col1, col2 = st.columns(2)

    with col1:
        drink = st.selectbox(
            "Thức uống",
            list(menu.keys()),
            key=f"drink_{i}"
        )

    with col2:
        size = st.selectbox(
            "Size",
            ["M", "L"],
            key=f"size_{i}"
        )

    col3, col4 = st.columns(2)

    with col3:
        topping = st.selectbox(
            "Topping",
            list(toppings.keys()),
            key=f"topping_{i}"
        )

    with col4:
        sugar = st.selectbox(
            "Mức đường",
            sugar_levels,
            key=f"sugar_{i}"
        )

    # Tính giá từng ly
    size_price = 5000 if size == "L" else 0

    unit_price = (
        menu[drink]
        + size_price
        + toppings[topping]
    )

    st.info(
        f"💰 Giá ly {i + 1}: **{unit_price:,} VNĐ**"
    )

    selected_items.append({
        "drink": drink,
        "size": size,
        "topping": topping,
        "sugar": sugar,
        "quantity": 1,
        "unit_price": unit_price,
        "total": unit_price
    })

# =========================
# THÊM TẤT CẢ LY
# =========================

if st.button(
    "➕ THÊM TẤT CẢ VÀO HÓA ĐƠN",
    use_container_width=True
):

    for item in selected_items:
        st.session_state.cart.append(item)

    st.success(
        f"✅ Đã thêm {number_of_cups} ly vào hóa đơn!"
    )

# =========================
# HÓA ĐƠN
# =========================

if st.session_state.cart:

    st.divider()

    st.subheader("🧾 HÓA ĐƠN")

    customer = (
        customer_name
        if customer_name
        else "Khách lẻ"
    )

    st.write(f"👤 **Khách hàng:** {customer}")

    grand_total = 0

    for i, item in enumerate(
        st.session_state.cart,
        start=1
    ):

        st.markdown(
            f"**🥤 Ly {i}: {item['drink']} - Size {item['size']}**"
        )

        st.write(
            f"🍮 Topping: {item['topping']}"
        )

        st.write(
            f"🍬 Đường: {item['sugar']}"
        )

        st.write(
            f"💰 Thành tiền: "
            f"**{item['total']:,} VNĐ**"
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
    # XÓA
    # =========================

    with col1:

        if st.button(
            "🗑️ XÓA HÓA ĐƠN",
            use_container_width=True
        ):

            st.session_state.cart = []

            st.rerun()

    # =========================
    # THANH TOÁN
    # =========================

    with col2:

        if st.button(
            "💳 THANH TOÁN",
            use_container_width=True
        ):

            now = datetime.now()

            invoice_code = now.strftime(
                "%Y%m%d%H%M%S"
            )

            invoice = ""

            invoice += "====================================\n"
            invoice += "       QUÁN TRÀ SỮA LIN LIN\n"
            invoice += "====================================\n"
            invoice += f"Mã hóa đơn: {invoice_code}\n"
            invoice += (
                f"Thời gian: "
                f"{now.strftime('%d/%m/%Y %H:%M:%S')}\n"
            )
            invoice += f"Khách hàng: {customer}\n"
            invoice += "------------------------------------\n"

            for i, item in enumerate(
                st.session_state.cart,
                start=1
            ):

                invoice += (
                    f"Ly {i}: {item['drink']}\n"
                )

                invoice += (
                    f"   Size: {item['size']}\n"
                )

                invoice += (
                    f"   Topping: {item['topping']}\n"
                )

                invoice += (
                    f"   Đường: {item['sugar']}\n"
                )

                invoice += (
                    f"   Giá: "
                    f"{item['total']:,} VNĐ\n"
                )

                invoice += (
                    "------------------------------------\n"
                )

            invoice += (
                f"TỔNG THANH TOÁN: "
                f"{grand_total:,} VNĐ\n"
            )

            invoice += (
                "====================================\n"
            )

            invoice += (
                "        CẢM ƠN QUÝ KHÁCH!\n"
            )

            invoice += (
                "====================================\n"
            )

            st.success("🎉 Thanh toán thành công!")

            st.download_button(
                label="📥 TẢI HÓA ĐƠN",
                data=invoice,
                file_name=f"hoa_don_{invoice_code}.txt",
                mime="text/plain",
                use_container_width=True
            )

else:

    st.warning(
        "🛒 Chưa có món nào trong hóa đơn."
    )
