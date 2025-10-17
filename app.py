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


# Show speed test history
if os.path.isfile(FILENAME):
    if st.checkbox("Show Test History"):
        df = pd.read_csv(FILENAME)
        st.dataframe(df)
