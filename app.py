<h3 style="text-align: center; color: #e83e8c; margin-bottom: 5px;">QUÁN TRÀ SỮA HAPPY</h3>
            <p style="text-align: center; font-size: 12px; color: #666;">Địa chỉ: 123 Đường Sữa, TP. Hồ Chí Minh<br>Thời gian: {thoi_gian}</p>
            <hr style="border: 0.5px dashed #ccc;">
            <p><b>Tên khách hàng:</b> {ten_khach}</p>
            <p><b>Danh sách các món đã đặt:</b></p>
            {danh_sach_html}
            <hr style="border: 0.5px dashed #ccc;">
            <h2 style="text-align: right; color: #d63384;">TỔNG THANH TOÁN: {tong_thanh_toan:,}đ</h2>
            <hr style="border: 0.5px dashed #ccc;">
            <p style="text-align: center; font-style: italic; font-size: 13px;">Cảm ơn quý khách và hẹn gặp lại!</p>
        </div>
        """
        st.markdown(hoa_don_html, unsafe_allow_html=True)

        # Tạo nội dung file xuất TXT
        noi_dung_file = f"""========================================
           QUÁN TRÀ SỮA HAPPY
========================================
Thời gian: {thoi_gian}
Tên khách hàng: {ten_khach}
----------------------------------------
DANH SÁCH MÓN ĐÃ ĐẶT:
"""
        for idx, item in enumerate(st.session_state.cart, 1):
            topping_str = ', '.join(item['topping']) if item['topping'] else 'Không có'
            noi_dung_file += f"""
{idx}. {item['ten_mon']} (Số lượng: {item['so_luong']})
   - Đường: {item['muc_duong']}
   - Topping: {topping_str}
   - Thành tiền: {item['thanh_tien']:,} VNĐ
----------------------------------------"""

        noi_dung_file += f"""
========================================
TỔNG THANH TOÁN: {tong_thanh_toan:,} VNĐ
========================================
         Cảm ơn quý khách!
"""

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Tải xuống file hóa đơn (.txt)",
            data=noi_dung_file,
            file_name=f"HoaDon_{ten_khach.replace(' ', '_')}.txt",
            mime="text/plain"
        )
