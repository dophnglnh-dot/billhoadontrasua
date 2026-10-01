import streamlit as st
from datetime import datetime

# ==========================================
# CẤU HÌNH APP
# ==========================================

st.set_page_config(
    page_title="Quán Trà Sữa Lin Lin",
    page_icon="🧋",
    layout="centered"
)

st.title("🧋 QUÁN TRÀ SỮA LIN LIN")
st.caption("Hệ thống tính bill và thanh toán")

# ==========================================
# MENU
# ==========================================

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

# ==========================================
# KHỞI TẠO GIỎ HÀNG
# ==========================================

if "cart" not in st.session_state:
    st.session_state.cart = []

# ==========================================
# THÔNG TIN KHÁCH HÀNG
# ==========================================

st.subheader("👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)

# ==========================================
# THÊM MÓN VÀO BILL
# ==========================================

st.divider()
st.subheader("➕ Thêm món")

col1, col2 = st.columns(2)

with col1:
    drink = st.selectbox(
        "🥤 Món",
        list(menu.keys())
    )

with col2:
    size = st.selectbox(
        "📏 Size",
        ["M", "L"]
    )

col3, col4 = st.columns(2)

with col3:
    topping = st.selectbox(
        "🍮 Topping",
        list(toppings.keys())
    )

with col4:
    sugar = st.selectbox(
        "🍬 Mức đường",
        sugar_levels
    )

quantity = st.number_input(
    "🔢 Số lượng",
    min_value=1,
    max_value=50,
    value=1,
    step=1
)

# ==========================================
# TÍNH GIÁ MÓN
# ==========================================

size_price = 5000 if size == "L" else 0

unit_price = (
    menu[drink]
    + size_price
    + toppings[topping]
)

item_total = unit_price * quantity

st.info(
    f"Đơn giá: **{unit_price:,} VNĐ**  |  "
    f"Thành tiền: **{item_total:,} VNĐ**"
)

# ==========================================
# NÚT THÊM MÓN
# ==========================================

if st.button(
    "➕ THÊM MÓN VÀO BILL",
    use_container_width=True
):

    item = {
        "drink": drink,
        "size": size,
        "topping": topping,
        "sugar": sugar,
        "quantity": quantity,
        "unit_price": unit_price,
        "total": item_total
    }

    st.session_state.cart.append(item)

    st.success(
        f"✅ Đã thêm {quantity} x {drink} vào bill!"
    )

# ==========================================
# HIỂN THỊ BILL
# ==========================================

st.divider()
st.subheader("🧾 BILL HIỆN TẠI")

if len(st.session_state.cart) > 0:

    customer = (
        customer_name
        if customer_name
        else "Khách lẻ"
    )

    st.write(f"👤 **Khách hàng:** {customer}")

    grand_total = 0

    # --------------------------------------
    # HIỂN THỊ TỪNG MÓN
    # --------------------------------------

    for i, item in enumerate(
        st.session_state.cart
    ):

        st.markdown(
            f"### 🥤 {i + 1}. {item['drink']}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"📏 Size: {item['size']}")
            st.write(f"🍮 Topping: {item['topping']}")

        with col2:
            st.write(f"🍬 Đường: {item['sugar']}")
            st.write(f"🔢 Số lượng: {item['quantity']}")

        st.write(
            f"💰 {item['unit_price']:,} VNĐ/ly "
            f"× {item['quantity']} = "
            f"**{item['total']:,} VNĐ**"
        )

        # Nút xóa từng món
        if st.button(
            f"🗑️ Xóa món {i + 1}",
            key=f"delete_{i}"
        ):

            st.session_state.cart.pop(i)
            st.rerun()

        grand_total += item["total"]

        st.divider()

    # ======================================
    # TỔNG TIỀN
    # ======================================

    st.subheader(
        f"💵 TỔNG TIỀN: {grand_total:,} VNĐ"
    )

    # ======================================
    # PHƯƠNG THỨC THANH TOÁN
    # ======================================

    st.subheader("💳 Phương thức thanh toán")

    payment_method = st.radio(
        "Chọn phương thức:",
        [
            "💵 Tiền mặt",
            "🏦 Chuyển khoản"
        ],
        horizontal=True
    )

    # ======================================
    # TIỀN KHÁCH ĐƯA
    # ======================================

    cash_received = 0
    change = 0

    if payment_method == "💵 Tiền mặt":

        cash_received = st.number_input(
            "💰 Tiền khách đưa",
            min_value=0,
            value=0,
            step=1000
        )

        if cash_received > 0:

            if cash_received >= grand_total:

                change = cash_received - grand_total

                st.success(
                    f"💸 Tiền thối: "
                    f"**{change:,} VNĐ**"
                )

            else:

                st.error(
                    f"⚠️ Khách đưa chưa đủ tiền. "
                    f"Còn thiếu "
                    f"**{grand_total - cash_received:,} VNĐ**"
                )

    else:

        st.info(
            "🏦 Khách hàng thanh toán bằng chuyển khoản."
        )

    # ======================================
    # THANH TOÁN
    # ======================================

    st.divider()

    if st.button(
        "✅ THANH TOÁN",
        use_container_width=True
    ):

        # Kiểm tra tiền mặt
        if payment_method == "💵 Tiền mặt":

            if cash_received < grand_total:

                st.error(
                    "❌ Không thể thanh toán vì "
                    "số tiền khách đưa chưa đủ!"
                )

            else:

                # Tạo hóa đơn
                now = datetime.now()

                invoice_code = now.strftime(
                    "%Y%m%d%H%M%S"
                )

                invoice = ""

                invoice += (
                    "====================================\n"
                )
                invoice += (
                    "       QUÁN TRÀ SỮA LIN LIN\n"
                )
                invoice += (
                    "====================================\n"
                )

                invoice += (
                    f"Mã hóa đơn: {invoice_code}\n"
                )

                invoice += (
                    f"Thời gian: "
                    f"{now.strftime('%d/%m/%Y %H:%M:%S')}\n"
                )

                invoice += (
                    f"Khách hàng: {customer}\n"
                )

                invoice += (
                    "------------------------------------\n"
                )

                for i, item in enumerate(
                    st.session_state.cart,
                    start=1
                ):

                    invoice += (
                        f"{i}. {item['drink']}\n"
                    )

                    invoice += (
                        f"   Size: {item['size']}\n"
                    )

                    invoice += (
                        f"   Topping: "
                        f"{item['topping']}\n"
                    )

                    invoice += (
                        f"   Đường: "
                        f"{item['sugar']}\n"
                    )

                    invoice += (
                        f"   Số lượng: "
                        f"{item['quantity']}\n"
                    )

                    invoice += (
                        f"   Đơn giá: "
                        f"{item['unit_price']:,} VNĐ\n"
                    )

                    invoice += (
                        f"   Thành tiền: "
                        f"{item['total']:,} VNĐ\n"
                    )

                    invoice += (
                        "------------------------------------\n"
                    )

                invoice += (
                    f"TỔNG TIỀN: "
                    f"{grand_total:,} VNĐ\n"
                )

                invoice += (
                    f"Thanh toán: {payment_method}\n"
                )

                if payment_method == "💵 Tiền mặt":

                    invoice += (
                        f"Tiền khách đưa: "
                        f"{cash_received:,} VNĐ\n"
                    )

                    invoice += (
                        f"Tiền thối: "
                        f"{change:,} VNĐ\n"
                    )

                invoice += (
                    "====================================\n"
                )

                invoice += (
                    "        CẢM ƠN QUÝ KHÁCH!\n"
                )

                invoice += (
                    "        HẸN GẶP LẠI ❤️\n"
                )

                invoice += (
                    "====================================\n"
                )

                st.success(
                    "🎉 THANH TOÁN THÀNH CÔNG!"
                )

                st.download_button(
                    "📥 TẢI HÓA ĐƠN",
                    data=invoice,
                    file_name=(
                        f"hoa_don_{invoice_code}.txt"
                    ),
                    mime="text/plain",
                    use_container_width=True
                )

        # ----------------------------------
        # CHUYỂN KHOẢN
        # ----------------------------------

        else:

            now = datetime.now()

            invoice_code = now.strftime(
                "%Y%m%d%H%M%S"
            )

            invoice = ""

            invoice += (
                "====================================\n"
            )
            invoice += (
                "       QUÁN TRÀ SỮA LIN LIN\n"
            )
            invoice += (
                "====================================\n"
            )

            invoice += (
                f"Mã hóa đơn: {invoice_code}\n"
            )

            invoice += (
                f"Thời gian: "
                f"{now.strftime('%d/%m/%Y %H:%M:%S')}\n"
            )

            invoice += (
                f"Khách hàng: {customer}\n"
            )

            invoice += (
                "------------------------------------\n"
            )

            for i, item in enumerate(
                st.session_state.cart,
                start=1
            ):

                invoice += (
                    f"{i}. {item['drink']} - "
                    f"Size {item['size']}\n"
                )

                invoice += (
                    f"   Topping: {item['topping']}\n"
                )

                invoice += (
                    f"   Đường: {item['sugar']}\n"
                )

                invoice += (
                    f"   Số lượng: {item['quantity']}\n"
                )

                invoice += (
                    f"   Thành tiền: "
                    f"{item['total']:,} VNĐ\n"
                )

                invoice += (
                    "------------------------------------\n"
                )

            invoice += (
                f"TỔNG TIỀN: "
                f"{grand_total:,} VNĐ\n"
            )

            invoice += (
                "Phương thức: CHUYỂN KHOẢN\n"
            )

            invoice += (
                "====================================\n"
            )

            invoice += (
                "        CẢM ƠN QUÝ KHÁCH!\n"
            )

            invoice += (
                "        HẸN GẶP LẠI ❤️\n"
            )

            invoice += (
                "====================================\n"
            )

            st.success(
                "🎉 THANH TOÁN THÀNH CÔNG!"
            )

            st.download_button(
                "📥 TẢI HÓA ĐƠN",
                data=invoice,
                file_name=(
                    f"hoa_don_{invoice_code}.txt"
                ),
                mime="text/plain",
                use_container_width=True
            )

else:

    st.info(
        "🛒 Chưa có món nào. "
        "Hãy chọn món ở phía trên và bấm "
        "\"THÊM MÓN VÀO BILL\"."
    )
