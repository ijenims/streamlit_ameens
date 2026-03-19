import streamlit as st
import pandas as pd
import plotly.express as px

# 画面設定
st.set_page_config(layout="wide")

# 初期設定
data = pd.DataFrame()

## サイドバー
uploaded_file = st.sidebar.file_uploader("Excelファイルを選択してください", type="xlsx")

### メイン画面
st.title("Cheese Fair Ameen's")

if uploaded_file is not None:
    # ExcelファイルをPandasのデータフレームに読み込む
    data = pd.read_excel(uploaded_file, sheet_name="input").T

    # 最初の行を列名に設定
    data.columns = data.iloc[0]
    data = data.drop(data.index[0])
    data = data.reset_index(drop=True)

    # 日付文字列をdatetime型に変換 → 'm/d'形式へ
    data["date"] = pd.to_datetime(data["date"])
    data["date"] = data["date"].dt.strftime("%m/%d")

    ## chart_dataの作成
    chart_cols = data.columns[4:]
    df = data.groupby("date")[chart_cols].sum()

    # ===== 日毎の注文数（積上げ棒グラフ）=====
    st.markdown("<h4>日毎の注文数</h4>", unsafe_allow_html=True)

    df_daily_long = df.reset_index().melt(
        id_vars="date",
        var_name="cheese",
        value_name="count"
    )

    fig_daily = px.bar(
        df_daily_long,
        x="date",
        y="count",
        color="cheese",
        barmode="stack",
        height=500,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    fig_daily.update_layout(
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="left",
            x=0
        ),
        margin=dict(b=120)
    )

    st.plotly_chart(fig_daily, use_container_width=True)

    # ===== チーズ毎の注文数（積上げ棒グラフ）=====
    st.markdown("<h4>チーズ毎の注文数</h4>", unsafe_allow_html=True)

    df_cheese = df.T
    df_cheese["cheese"] = df_cheese.index

    df_cheese_long = df_cheese.melt(
        id_vars="cheese",
        var_name="date",
        value_name="count"
    )

    fig_cheese = px.bar(
        df_cheese_long,
        x="cheese",
        y="count",
        color="date",
        barmode="stack",
        height=500,
        color_discrete_sequence=px.colors.sequential.YlOrRd
    )

    fig_cheese.update_layout(
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            xanchor="left",
            x=0
        ),
        margin=dict(b=120)
    )

    st.plotly_chart(fig_cheese, use_container_width=True)

    # chart_dataの表示
    st.markdown("<h4>グラフデータ</h4>", unsafe_allow_html=True)
    st.dataframe(df)

    # data表示
    st.markdown("<h4>入力データ</h4>", unsafe_allow_html=True)
    st.dataframe(data)