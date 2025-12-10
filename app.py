import streamlit as st
import pandas as pd
import datetime
import os

# --- 設定 ---
CSV_FILE = "attendance_log.csv"
# ここに社員の名前をリストアップします
MEMBERS = ["佐藤", "鈴木", "田中", "高橋"]
ADMIN_PASSWORD = "1234"  # 管理者用パスワード（簡易的なもの）

# ページ設定
st.set_page_config(page_title="チーム勤怠管理", layout="centered")
st.title("🕒 チーム勤怠管理システム")

# --- データの読み込み・保存の関数 ---
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["日時", "名前", "種別"])

def save_data(name, action):
    df = load_data()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 新しいデータを作成
    new_data = pd.DataFrame({"日時": [now], "名前": [name], "種別": [action]})
    # 結合して保存
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# --- サイドバー：モード選択 ---
menu = st.sidebar.radio("メニューを選択", ["打刻画面", "管理者モード"])

# ================================
# 1. 打刻画面（みんなが使う画面）
# ================================
if menu == "打刻画面":
    st.header("打刻入力")
    
    # 自分の名前を選ぶ
    selected_user = st.selectbox("あなたの名前を選んでください", MEMBERS)
    
    st.write(f"**{selected_user}** さん、おはようございます！")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("出勤", use_container_width=True):
            save_data(selected_user, "出勤")
            st.success(f"{selected_user}さん、出勤しました！")
            
    with col2:
        if st.button("退勤", use_container_width=True):
            save_data(selected_user, "退勤")
            st.success(f"{selected_user}さん、お疲れ様でした！")

# ================================
# 2. 管理者モード（パスワード制限）
# ================================
elif menu == "管理者モード":
    st.header("管理者メニュー")
    
    password = st.text_input("管理者パスワードを入力してください", type="password")
    
    if password == ADMIN_PASSWORD:
        st.success("ログイン成功")
        
        # データの表示
        df = load_data()
        st.subheader("全社員の勤怠ログ")
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # データダウンロードボタン
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                "CSVをダウンロード",
                csv,
                "attendance_log.csv",
                "text/csv"
            )
        else:
            st.info("まだデータがありません。")
            
    elif password != "":
        st.error("パスワードが違います")