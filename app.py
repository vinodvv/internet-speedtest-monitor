import streamlit as st
import pandas as pd
import speed_test
import os


FILENAME = "test_results.csv"

st.title("🌐 Internet Speed Monitor")
st.write("Track your internet performance overtime.")

# Streamlit session state to keep latest result after button click
if "last_result" not in st.session_state:
    st.session_state["last_result"] = speed_test.load_last_result(FILENAME)

st.subheader("Latest Speed Test")
last_result = st.session_state["last_result"]
c1, c2, c3 = st.columns(3)

if last_result is not None:
    c1.metric("⬇️ Download Speed", f"{last_result['download']} Mbps")
    c2.metric("⬆️ Upload Speed", f"{last_result['upload']} Mbps")
    c3.metric("📶 Ping", f"{last_result['ping']} ms")

    isp = last_result['host'].split(".")[1]
    server = last_result['host'].split(".")[0]

    st.write("ISP: ", f"{isp}")
    st.write(f"Server: {server} ({last_result['server']}, {last_result['country']})")
    st.caption(f"Last test: {last_result['datetime']}")
else:
    c1.metric("Download (Mbps)", "N/A")
    c2.metric("Upload (Mbps)", "N/A")
    c3.metric("Ping (ms)", "N/A")
    st.caption("No speed test result found.")

if st.button("Run Speed Test"):
    results = speed_test.get_speedtest_results()
    speed_test.save_results(FILENAME, results)
    speed_test.load_last_result(filename=FILENAME)

# Performance statistics
df = pd.read_csv(FILENAME)

st.subheader("Performance statistics")
df["download"] = pd.to_numeric(df["download"])
df["upload"] = pd.to_numeric(df["upload"])
df["ping"] = pd.to_numeric(df["ping"])

# Statistics
best = [df["download"].max(), df["upload"].max(), df["ping"].min()]
worst = [df["download"].min(), df["upload"].min(), df["ping"].max()]
mean = [df["download"].mean(), df["upload"].mean(), df["ping"].mean(), ]
std_dev = [df["download"].std(), df["upload"].std(), df["ping"].std()]


c1, c2, c3 = st.columns(3)

c1.write("⬇️ Download")
c2.write("⬆️️ Upload")
c3.write("📶 Ping")
c1.metric("Best", f"{best[0]} Mbps")
c2.metric("Best", f"{best[1]} Mbps")
c3.metric("Best", f"{best[-1]} ms")

c1.metric("Worst", f"{worst[0]} Mbps")
c2.metric("Worst", f"{worst[1]} Mbps")
c3.metric("Worst", f"{worst[-1]} ms")

c1.metric("Average", f"{mean[0]:.2f} Mbps")
c2.metric("Average", f"{mean[1]:.2f} Mbps")
c3.metric("Average", f"{mean[-1]:.2f} ms")

c1.metric("Std Dev", f"{std_dev[0]:.2f} Mbps")
c2.metric("Std Dev", f"{std_dev[1]:.2f} Mbps")
c3.metric("Std Dev", f"{std_dev[-1]:.2f} ms")


# Show speed test history
if os.path.isfile(FILENAME):
    if st.checkbox("Show Test History"):
        df = pd.read_csv(FILENAME)
        st.dataframe(df)
