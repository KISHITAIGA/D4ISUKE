import streamlit as st
import time
from PIL import Image
import pandas as pd
import numpy as np
st.title('よろしくです。')
st.write("D4isukeです。これから始めます")

text = st.text_input('あなたのなまえをおしえてください')
st.write("あなたの名前"+text+"です。")

condition = st.slider("あなたの今の調子は?",0,100,50) #最小値，最大値，スタート位置

option = st.selectbox("好きな数字を教えてください。",list(['1番',"2番",'3番',"4番"]))
st.write("あなたが選択したのは",option,"です。")


st.sidebar.write('プログレスバーの表示') 
'Start!'

latest_iteration = st.empty()#空コンテンツと一緒に変数を作成 
bar = st.progress(0)#プログレスを作る 値は0
for i in range(100):
    latest_iteration.text(f'Iteration{i+1}')#空のIterationにテキストを入れていく 
    bar.progress(i+1)#barの中身をぐいぐい増やしていく
    time.sleep(0.1)
'Done!!!'

left_column, right_column = st.columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラムです') 


img = Image.open("room.jpg")
st.image(img,caption='生活場面',use_column_width=True)

df = pd.DataFrame(
    np.random.rand(100,2)/[50,50] + [35.69,139.70], 
    columns = ['lat','lon',]
    )
st.map(df)

df = pd.DataFrame(
    np.random.rand(20,3), #20行3列
    columns = ['a','b','c'] )#表として表示する 
st.table(df.style.highlight_max(axis=0))

st.bar_chart(df)