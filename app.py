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
# KHỞI TẠO CHATBOT
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Xin chào 👋 Mình là trợ lý của Lin Lin! "
                "Bạn có thể hỏi mình về menu, giá món, topping "
                "hoặc bill hiện tại nha 🧋"
            )
        }
    ]

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
# TÍNH GIÁ
# ==========================================

size_price = 5000 if size == "L" else 0

unit_price = (
    menu[drink]
    + size_price
    + toppings[topping]
)

item_total = unit_price * quantity

st.info(
    f"Đơn giá: **{unit_price:,} VNĐ** | "
    f"Thành tiền: **{item_total:,} VNĐ**"
)

# ==========================================
# THÊM MÓN
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
# BILL
# ==========================================

st.divider()
st.subheader("🧾 BILL HIỆN TẠI")

grand_total = 0

if len(st.session_state.cart) > 0:

    customer = (
        customer_name
        if customer_name
        else "Khách lẻ"
    )

    st.write(f"👤 **Khách hàng:** {customer}")

    for i, item in enumerate(
        st.session_state.cart
    ):

        st.markdown(
            f"### 🥤 {i + 1}. {item['drink']}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"📏 Size: {item['size']}")
            st.write(
                f"🍮 Topping: {item['topping']}"
            )

        with col2:
            st.write(
                f"🍬 Đường: {item['sugar']}"
            )
            st.write(
                f"🔢 Số lượng: {item['quantity']}"
            )

        st.write(
            f"💰 {item['unit_price']:,} VNĐ/ly × "
            f"{item['quantity']} = "
            f"**{item['total']:,} VNĐ**"
        )

        if st.button(
            f"🗑️ Xóa món {i + 1}",
            key=f"delete_{i}"
        ):
            st.session_state.cart.pop(i)
            st.rerun()

        grand_total += item["total"]

        st.divider()

    st.subheader(
        f"💵 TỔNG TIỀN: {grand_total:,} VNĐ"
    )

    # ======================================
    # THANH TOÁN
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

    cash_received = 0
    change = 0

    if payment_method == "💵 Tiền mặt":

        cash_received = st.number_input(
            "💰 Tiền khách đưa",
            min_value=0,
            value=0,
            step=1000
        )

        if cash_received >= grand_total:
            change = cash_received - grand_total

            if cash_received > 0:
                st.success(
                    f"💸 Tiền thối: "
                    f"**{change:,} VNĐ**"
                )

        elif cash_received > 0:

            st.error(
                f"⚠️ Còn thiếu "
                f"**{grand_total - cash_received:,} VNĐ**"
            )

    else:

        st.info(
            "🏦 Khách hàng thanh toán bằng chuyển khoản."
        )

    # ======================================
    # THANH TOÁN
    # ======================================

    if st.button(
        "✅ THANH TOÁN",
        use_container_width=True
    ):

        if (
            payment_method == "💵 Tiền mặt"
            and cash_received < grand_total
        ):

            st.error(
                "❌ Số tiền khách đưa chưa đủ!"
            )

        else:

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
                    f"{i}. {item['drink']}\n"
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
                    f"   Số lượng: {item['quantity']}\n"
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
                f"Phương thức: {payment_method}\n"
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

            invoice += "====================================\n"
            invoice += "        CẢM ƠN QUÝ KHÁCH!\n"
            invoice += "        HẸN GẶP LẠI ❤️\n"
            invoice += "====================================\n"

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
        "Hãy chọn món và bấm "
        "\"THÊM MÓN VÀO BILL\"."
    )

# ==========================================
# 🤖 CHATBOT LIN LIN
# ==========================================

st.divider()

st.subheader("🤖 Trợ lý Lin Lin")

st.caption(
    "Bạn có thể hỏi về món, giá, topping hoặc bill hiện tại."
)

# Hiển thị lịch sử chat

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# ==========================================
# HÀM XỬ LÝ CHATBOT
# ==========================================

def chatbot_response(user_text):

    text = user_text.lower().strip()

    # --------------------------------------
    # MENU
    # --------------------------------------

    if (
        "menu" in text
        or "món gì" in text
        or "có món" in text
        or "thức uống" in text
    ):

        result = "🧋 Menu của Lin Lin:\n\n"

        for name, price in menu.items():

            result += (
                f"• {name}: "
                f"{price:,} VNĐ\n"
            )

        return result

    # --------------------------------------
    # TOPPING
    # --------------------------------------

    if (
        "topping" in text
        or "thêm gì" in text
    ):

        result = "🍮 Topping của Lin Lin:\n\n"

        for name, price in toppings.items():

            if price == 0:

                result += (
                    f"• {name}: miễn phí\n"
                )

            else:

                result += (
                    f"• {name}: "
                    f"+{price:,} VNĐ\n"
                )

        return result

    # --------------------------------------
    # SIZE
    # --------------------------------------

    if "size" in text:

        return (
            "📏 Lin Lin hiện có 2 size:\n\n"
            "• Size M: giá gốc\n"
            "• Size L: +5.000 VNĐ"
        )

    # --------------------------------------
    # MỨC ĐƯỜNG
    # --------------------------------------

    if (
        "đường" in text
        or "ngọt" in text
    ):

        return (
            "🍬 Bạn có thể chọn 3 mức đường:\n\n"
            "• 100% - ngọt bình thường\n"
            "• 70% - ít ngọt\n"
            "• 0% - không đường"
        )

    # --------------------------------------
    # BILL
    # --------------------------------------

    if (
        "bill" in text
        or "hóa đơn" in text
        or "hoa don" in text
        or "tổng" in text
        or "bao nhiêu tiền" in text
    ):

        if len(st.session_state.cart) == 0:

            return (
                "🛒 Bill hiện tại chưa có món nào."
            )

        total = sum(
            item["total"]
            for item in st.session_state.cart
        )

        number_of_items = sum(
            item["quantity"]
            for item in st.session_state.cart
        )

        return (
            f"🧾 Bill hiện tại có "
            f"**{number_of_items} ly**.\n\n"
            f"💰 Tổng tiền: "
            f"**{total:,} VNĐ**"
        )

    # --------------------------------------
    # ĐẾM MÓN
    # --------------------------------------

    if (
        "mấy món" in text
        or "bao nhiêu ly" in text
    ):

        if len(st.session_state.cart) == 0:

            return (
                "🛒 Hiện tại bill chưa có món nào."
            )

        number_of_items = sum(
            item["quantity"]
            for item in st.session_state.cart
        )

        return (
            f"🧋 Hiện tại bill có "
            f"**{number_of_items} ly**."
        )

    # --------------------------------------
    # GIÁ TỪNG MÓN
    # --------------------------------------

    for name, price in menu.items():

        if name.lower() in text:

            return (
                f"🥤 {name} có giá "
                f"**{price:,} VNĐ/ly** "
                f"(size M, chưa tính topping).\n\n"
                f"Size L thêm 5.000 VNĐ nha!"
            )

    # --------------------------------------
    # GỢI Ý
    # --------------------------------------

    if (
        "gợi ý" in text
        or "tư vấn" in text
        or "nên uống" in text
    ):

        return (
            "🧋 Nếu bạn thích vị cacao, "
            "mình gợi ý **Cacao Latte**.\n\n"
            "Nếu thích vị truyền thống, "
            "bạn có thể thử **Trà sữa truyền thống "
            "+ Trân châu đen**.\n\n"
            "Nếu thích vị trái cây, "
            "có thể thử **Trà đào** hoặc "
            "**Trà vải** 🍑"
        )

    # --------------------------------------
    # THANH TOÁN
    # --------------------------------------

    if (
        "thanh toán" in text
        or "thanh toan" in text
        or "chuyển khoản" in text
        or "tiền mặt" in text
    ):

        return (
            "💳 Lin Lin hỗ trợ 2 hình thức:\n\n"
            "• 💵 Tiền mặt\n"
            "• 🏦 Chuyển khoản\n\n"
            "Bạn chọn phương thức ngay "
            "bên phần thanh toán của bill nha!"
        )

    # --------------------------------------
    # CHÀO HỎI
    # --------------------------------------

    if (
        "hello" in text
        or "hi" in text
        or "chào" in text
        or "xin chào" in text
    ):

        return (
            "Xin chào bạn 👋 "
            "Mình là trợ lý Lin Lin 🧋\n\n"
            "Bạn muốn hỏi về menu, giá món, "
            "topping hay bill?"
        )

    # --------------------------------------
    # CẢM ƠN
    # --------------------------------------

    if (
        "cảm ơn" in text
        or "thanks" in text
    ):

        return (
            "Không có gì nha 🥰 "
            "Cảm ơn bạn đã ghé Lin Lin!"
        )

    # --------------------------------------
    # MẶC ĐỊNH
    # --------------------------------------

    return (
        "🤖 Mình chưa hiểu câu hỏi này lắm 😭\n\n"
        "Bạn có thể hỏi mình như:\n"
        "• Quán có món gì?\n"
        "• Quán có món nào là ngon nhất?\n"
        "• Cacao Latte bao nhiêu?\n"
        "• Có topping gì?\n"
        "• Size L thêm bao nhiêu?\n"
        "• Bill của tôi bao nhiêu?\n"
        "• Tôi đang có mấy ly?\n"
        "• Có thanh toán chuyển khoản không?"
    )


# ==========================================
# Ô NHẬP CHAT
# ==========================================

user_message = st.chat_input(
    "💬 Nhập câu hỏi cho Lin Lin..."
)

if user_message:

    # Tin nhắn người dùng
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Phản hồi chatbot
    response = chatbot_response(
        user_message
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()
