import streamlit as st
from datetime import datetime
import requests


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
                "Xin chào 👋 Mình là trợ lý AI của Lin Lin! 🧋\n\n"
                "Bạn có thể hỏi mình về menu, giá món, topping, "
                "size, mức đường hoặc bill hiện tại nha."
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

st.subheader("🤖 Trợ lý AI Lin Lin")

st.caption(
    "Hỏi AI về menu, giá món, topping, "
    "size, mức đường hoặc bill hiện tại."
)


# ==========================================
# TẠO THÔNG TIN BILL CHO AI
# ==========================================

def get_cart_summary():

    if len(st.session_state.cart) == 0:
        return "Bill hiện tại chưa có món nào."

    summary = []

    total = 0
    total_quantity = 0

    for i, item in enumerate(
        st.session_state.cart,
        start=1
    ):

        summary.append(
            f"{i}. {item['drink']} | "
            f"Size {item['size']} | "
            f"Topping: {item['topping']} | "
            f"Đường: {item['sugar']} | "
            f"Số lượng: {item['quantity']} | "
            f"Đơn giá: {item['unit_price']:,} VNĐ | "
            f"Thành tiền: {item['total']:,} VNĐ"
        )

        total += item["total"]
        total_quantity += item["quantity"]

    result = "\n".join(summary)

    result += (
        f"\n\nTổng số ly: {total_quantity}"
        f"\nTổng tiền: {total:,} VNĐ"
    )

    return result


# ==========================================
# GỌI OPENROUTER API
# ==========================================

def chatbot_response(user_text):

    # --------------------------------------
    # LẤY API KEY TỪ STREAMLIT SECRETS
    # --------------------------------------

    try:

        api_key = st.secrets["OPENROUTER_API_KEY"]

    except Exception:

        return (
            "⚠️ Chưa cấu hình API Key.\n\n"
            "Bà vào:\n"
            "**Streamlit Cloud → Settings → Secrets**\n\n"
            "Sau đó thêm:\n\n"
            "```toml\n"
            'OPENROUTER_API_KEY = "API_KEY_MỚI_CỦA_BÀ"\n'
            "```\n\n"
            "Sau khi lưu Secrets, hãy chạy lại app."
        )


    # --------------------------------------
    # THÔNG TIN MENU
    # --------------------------------------

    menu_text = "\n".join(
        [
            f"- {name}: {price:,} VNĐ"
            for name, price in menu.items()
        ]
    )


    # --------------------------------------
    # THÔNG TIN TOPPING
    # --------------------------------------

    topping_text = "\n".join(
        [
            (
                f"- {name}: miễn phí"
                if price == 0
                else f"- {name}: +{price:,} VNĐ"
            )
            for name, price in toppings.items()
        ]
    )


    # --------------------------------------
    # BILL HIỆN TẠI
    # --------------------------------------

    cart_summary = get_cart_summary()


    # --------------------------------------
    # TÊN KHÁCH
    # --------------------------------------

    current_customer = (
        customer_name
        if customer_name
        else "Khách lẻ"
    )


    # --------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------

    system_prompt = f"""
Bạn là trợ lý AI của Quán Trà Sữa Lin Lin.

Hãy trả lời bằng tiếng Việt, thân thiện,
ngắn gọn, dễ hiểu và giống nhân viên tư vấn
của một quán trà sữa.

THÔNG TIN QUÁN:

Tên quán:
Quán Trà Sữa Lin Lin

MENU:
{menu_text}

TOPPING:
{topping_text}

SIZE:
- Size M: giá gốc
- Size L: cộng thêm 5.000 VNĐ

MỨC ĐƯỜNG:
- 100%
- 70%
- 0%

KHÁCH HÀNG HIỆN TẠI:
{current_customer}

BILL HIỆN TẠI:
{cart_summary}

QUY TẮC:

1. Nếu khách hỏi về menu hoặc giá,
hãy sử dụng đúng thông tin ở trên.

2. Không tự bịa món hoặc giá không có trong menu.

3. Nếu khách hỏi bill hiện tại,
hãy dựa vào BILL HIỆN TẠI.

4. Nếu khách hỏi tư vấn món,
hãy đưa ra gợi ý dựa trên sở thích
mà khách mô tả.

5. Nếu khách hỏi cách tính tiền,
hãy giải thích:
Giá món + giá size L nếu có
+ giá topping rồi nhân số lượng.

6. Không được nói rằng bạn có thể tự thêm
món vào bill nếu giao diện chưa có chức năng đó.

7. Nếu khách muốn thay đổi bill,
hãy hướng dẫn họ sử dụng phần
"Thêm món" hoặc nút "Xóa món".

8. Khi trả lời giá tiền,
hãy ghi rõ đơn vị VNĐ.

9. Trả lời tự nhiên, không quá dài.

10. Bạn là trợ lý của quán,
không phải một chatbot chung chung.
"""


    # --------------------------------------
    # LẤY LỊCH SỬ CHAT
    # --------------------------------------

    chat_history = []

    for message in st.session_state.messages[-10:]:

        chat_history.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )


    # Thêm câu hỏi mới

    chat_history.append(
        {
            "role": "user",
            "content": user_text
        }
    )


    # --------------------------------------
    # GỬI REQUEST ĐẾN OPENROUTER
    # --------------------------------------

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://streamlit.io",
                "X-Title": "Quán Trà Sữa Lin Lin"
            },

            json={
                "model": "openrouter/auto",

                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ] + chat_history,

                "temperature": 0.4,
                "max_tokens": 500
            },

            timeout=60
        )


        # ----------------------------------
        # KIỂM TRA RESPONSE
        # ----------------------------------

        if response.status_code != 200:

            try:
                error_data = response.json()

                error_message = (
                    error_data
                    .get("error", {})
                    .get("message", "")
                )

            except Exception:

                error_message = response.text


            return (
                "⚠️ Không gọi được AI.\n\n"
                f"Chi tiết: {error_message}"
            )


        # ----------------------------------
        # LẤY NỘI DUNG AI
        # ----------------------------------

        data = response.json()

        answer = (
            data["choices"][0]["message"]["content"]
        )

        return answer


    except requests.exceptions.Timeout:

        return (
            "⏳ AI phản hồi hơi lâu.\n"
            "Bà thử gửi lại câu hỏi sau nha!"
        )


    except requests.exceptions.RequestException as e:

        return (
            "⚠️ Có lỗi kết nối đến OpenRouter.\n\n"
            f"Chi tiết: {str(e)}"
        )


    except Exception as e:

        return (
            "⚠️ Có lỗi xảy ra với chatbot.\n\n"
            f"Chi tiết: {str(e)}"
        )


# ==========================================
# HIỂN THỊ LỊCH SỬ CHAT
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ==========================================
# Ô NHẬP CHAT
# ==========================================

user_message = st.chat_input(
    "💬 Nhập câu hỏi cho Lin Lin..."
)


# ==========================================
# XỬ LÝ TIN NHẮN
# ==========================================

if user_message:

    # --------------------------------------
    # LƯU TIN NHẮN USER
    # --------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # --------------------------------------
    # HIỂN THỊ LOADING
    # --------------------------------------

    with st.spinner("🤖 Lin Lin đang suy nghĩ..."):

        response = chatbot_response(
            user_message
        )


    # --------------------------------------
    # LƯU CÂU TRẢ LỜI
    # --------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


    # --------------------------------------
    # LOAD LẠI APP
    # --------------------------------------

    st.rerun()
