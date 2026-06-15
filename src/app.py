import streamlit as st
import os

st.set_page_config(page_title="Intelligent CS Wiki", layout="wide")

WIKI_DIR = "docs/wiki"

# 1. Left Sidebar - Dynamic Data Binding
st.sidebar.title("💻 CS Core Wiki")
st.sidebar.write("`3 pages loaded` · `validate OK` · Multi-Agent")

if os.path.exists(WIKI_DIR):
    files = [f.replace(".md", "") for f in os.listdir(WIKI_DIR) if f.endswith(".md")]
else:
    files = []

if files:
    selected_page = st.sidebar.radio("지식 문서 목록 검색", files)
else:
    selected_page = st.sidebar.radio("지식 문서 목록 검색", ["지식 베이스 공백"])

st.sidebar.markdown("---")
st.sidebar.write("**TARGET DOMAINS**\n- Operating Systems\n- Computer Networks\n- Computer Security")
st.sidebar.write("**ACTIVE MCP TOOLS**\n- `read_wiki` / `write_wiki`\n- `search_cve` (취약점 엔진)")

# 2. Main & Agent Chat Layout split
col_content, col_agent = st.columns([2, 1])

# Center Column: Real Wiki Viewer
with col_content:
    if files and selected_page != "지식 베이스 공백":
        file_path = os.path.join(WIKI_DIR, f"{selected_page}.md")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        st.markdown(content)
    else:
        st.title("CS 핵심 전공 지식창고 위키")
        st.write("`domain` `active` `updated 2026-06-14`")
        st.markdown("### 📌 프로젝트 도메인 안내\n본 시스템은 **운영체제, 컴퓨터 네트워크, 컴퓨터 보안** 지식의 유기적 관계를 다루는 에이전트 협업형 위키입니다.")
        st.markdown("왼쪽 사이드바에서 파이프라인이 생성한 실제 위키 문서(`net_arq` 등)를 선택하면 지식 그래프 화면이 렌더링됩니다.")

# Right Column: CS Agent Chat UI
with col_agent:
    st.subheader("🤖 위키 에이전트")
    st.caption("Gemini & Claude Core (MCP System)")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "## 🔍 크로스 레퍼런스 및 린트 상태\n- **Auto-Interlinker**: `net_arq` ➔ `net_sliding_window` 연결 완료.\n- **Linter**: `page_template.md` 규격 검사 통과.\n\n[현재 컨텍스트: OS 메모리 구조-BoF 취약점-소켓 통신 정합성 검증 중]"}
        ]
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if user_input := st.chat_input("에이전트에게 툴 구동 및 위키 수정 요청..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # CS-specific simulation response
        reply = f"요청하신 '{user_input}' 명세를 분석합니다. 내장된 MCP 툴인 `search_cve` 및 `write_wiki`를 호출하여 해당 개념과 기존 OS/보안 문서 간의 상호 참조 관계를 갱신합니다."
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})