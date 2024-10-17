
from vnstock3 import Vnstock
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Lấy thời gian hiện tại
now = datetime.now().strftime('%Y-%m-%d')
# Tạo tiêu đề
st.title('Biểu đồ nến theo cổ phiếu')

# Danh sách các mã cổ phiếu bạn muốn cho phép chọn
#symbols = ['SMC', 'VND', 'HPG', 'FPT', 'VIC']

# Tạo hộp chọn để người dùng chọn mã cổ phiếu
#selected_symbol = st.selectbox('Chọn mã cổ phiếu:', symbols)
# Tạo đối tượng lấy dữ liệu cổ phiếu theo mã cổ phiếu được chọn
#stock = Vnstock().stock(symbol=selected_symbol, source='TCBS')

selected_stock = st.session_state['selected_stock']
stock = Vnstock().stock(symbol=selected_stock, source='TCBS')

# Hàm lấy và vẽ dữ liệu
@st.cache_data
def load_data():
    data = stock.quote.history(start='2000-07-28', end=now, interval='1H')
    data['time'] = pd.to_datetime(data['time'])

    # Vẽ biểu đồ nến
    fig = go.Figure(data=[go.Candlestick(x=data['time'], open=data['open'],
                                         high=data['high'],
                                         low=data['low'],
                                         close=data['close'])])

    # Đặt tiêu đề và nhãn
    fig.update_layout(title=f'Biểu đồ nến của cổ phiếu {selected_stock}',
                      xaxis_title='Ngày',
                      yaxis_title='Giá',
                      xaxis_rangeslider_visible=False,
                      yaxis=dict(range=[0, max(data['high'])]))  # Thiết lập giá trị nhỏ nhất của trục y là 0

    # Cập nhật định dạng trục x
    fig.update_xaxes(
        type='date',
        tickformat='%Y-%m-%d',
        ticklabelmode="instant"
    )
    
    # Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(fig)

# Gọi hàm vẽ biểu đồ
load_data()

