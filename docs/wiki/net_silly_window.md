---
# Wiki Page Template v1.0
author: Gemini
last_updated: 2026-06-01
tags: [컴퓨터 네트워크, 실리 윈도우 증후군, SWS, TCP, 최적화]
version: 0.0.1
---

# 실리 윈도우 증후군 (Silly Window Syndrome, SWS)

> 슬라이딩 윈도우 메커니즘에서 송수신 측의 처리 속도 불균형으로 인해 극히 작은 데이터 패킷이 자주 전송되어 대역폭을 낭비하는 현상.

## 1. 개요 (Overview)
실리 윈도우 증후군(SWS)은 TCP 통신에서 발생하는 비효율적인 현상으로, 송수신 측의 버퍼 처리 속도 차이로 인해 발생합니다. 페이로드보다 헤더의 크기가 훨씬 큰 작은 패킷들이 네트워크에 범람하게 되어 대역폭의 낭비와 네트워크 성능 저하를 초래합니다.

## 2. 상세 내용 (Details)
- **리시버 사이드 SWS (Receiver-side SWS)**:
  - **원인**: 수신 프로세스(Application)의 읽기 속도가 너무 느린 경우 발생합니다. 수신 TCP 버퍼에서 딱 1바이트만 읽어내고 rwnd(수신 윈도우)가 1바이트 비었다고 송신 측에 광고하면, 송신 측은 1바이트의 데이터를 보내기 위해 40바이트(TCP 20 + IP 20)의 헤더를 붙여 전송하는 극심한 오버헤드가 발생합니다.
  - **해결책**:
    - **클라크 솔루션 (Clark's Solution)**: 버퍼의 절반이 비거나 1 MSS(Maximum Segment Size) 크기만큼 공간이 채워질 때까지 rwnd=0으로 광고하여 송신 측의 전송을 막습니다.
    - **지연 에크 (Delayed ACK)**: ACK 전송을 일정 시간 지연시켜 수신 버퍼에 충분한 공간이 확보된 후 광고합니다.

- **샌더 사이드 SWS (Sender-side SWS)**:
  - **원인**: 송신 응용 프로그램(예: 터미널 입력, 텔넷 등)이 너무 빈번하게 작은 데이터(예: 1바이트)를 OS 송신 버퍼에 쓸 때 발생합니다.
  - **해결책**:
    - **네이글 알고리즘 (Nagle's Algorithm)**: 처음 들어온 작은 데이터는 즉시 전송하지만, 이후 버퍼에 들어오는 데이터는 이전에 보낸 패킷의 ACK가 돌아오거나 버퍼에 1 MSS만큼의 데이터가 쌓일 때까지 전송을 지연시키고 모아서 한 번에 전송합니다.

## 3. 연관 항목 (Relationships)
- **상위 개념**: [[컴퓨터 네트워크]], [[슬라이딩 윈도우]], [[TCP]]
- **하위 개념**: [[클라크 솔루션(Clark's Solution)]], [[네이글 알고리즘(Nagle's Algorithm)]], [[지연 에크(Delayed ACK)]]
- **참조 링크**: [[흐름 제어]], [[MSS(Maximum Segment Size)]]

## 4. 비고 (Notes)
- Nagle 알고리즘과 지연 ACK(Delayed ACK)가 함께 동작하면 데드락과 유사한 지연 현상이 발생할 수 있으므로 특정 실시간 애플리케이션에서는 Nagle 알고리즘을 비활성화(TCP_NODELAY)하기도 합니다.

---

## 🛠 LLM Maintenance Log
*이 구역은 에이전트가 자동으로 관리합니다. 직접 수정하지 마세요.*

| Date | Agent | Action | Description |
| :--- | :--- | :--- | :--- |
| 2026-06-01 | Gemini | Rewrite | Fixed broken formatting and extracted entity from raw source (net_silly_window.txt.txt). |

<!-- [Human Protected: Start] -->
### 👨‍💻 Human Annotations
*이 섹션 하위의 내용은 에이전트가 덮어쓰지 않습니다.*
- 
<!-- [Human Protected: End] -->
