---
# Wiki Page Template v1.0
author: Gemini
last_updated: 2026-06-01
tags: [컴퓨터 네트워크, 슬라이딩 윈도우, 흐름 제어, TCP]
version: 0.0.1
---

# 슬라이딩 윈도우 (Sliding Window)

> 네트워크 통신에서 송수신 측의 버퍼 상태를 관리하고 데이터 전송량을 동적으로 조절하여 효율적인 흐름 제어를 실현하는 메커니즘.

## 1. 개요 (Overview)
슬라이딩 윈도우는 전송 측이 수신 측의 처리 능력을 초과하여 데이터를 보내지 않도록 관리하는 기법입니다. 수신 측이 허용하는 범위(윈도우 크기) 내에서 ACK를 기다리지 않고 연속적으로 데이터를 보낼 수 있게 하여 네트워크 이용률을 높입니다.

## 2. 상세 내용 (Details)
- **샌더 사이드 슬라이딩 윈도우 (Sender-side Sliding Window)**:
  송신 측 버퍼는 윈도우 상태에 따라 4가지 영역으로 관리됩니다.
  - **카테고리 1**: 이미 전송되었고 수신 측으로부터 ACK 확인까지 완료된 영역 (윈도우 외부 좌측).
  - **카테고리 2**: 데이터를 보냈으나 아직 ACK를 받지 못한 영역 (In-flight / Outstanding).
  - **카테고리 3**: 윈도우 범위 내에 있어 즉시 보낼 수 있으나 아직 전송하지 않은 영역 (Usable Window).
  - **카테고리 4**: 윈도우 범위를 벗어나 아직 보낼 수 없는 영역 (윈도우 외부 우측).

- **윈도우 제어 동작**:
  - **클로징 (Closing)**: ACK를 수신함에 따라 윈도우의 왼쪽 경계를 오른쪽으로 이동시키는 행위입니다.
  - **오프닝 (Opening) / 슈링킹 (Shrinking)**: 네트워크 혼잡 상황이나 수신 측 버퍼 상태에 따라 윈도우의 전체 크기를 늘리거나 줄이는 행위입니다.
  - **최종 윈도우 사이즈 결정**: `min(rwnd, cwnd)` 공식을 통해 흐름 제어를 위한 수신 윈도우(rwnd)와 혼잡 제어를 위한 혼잡 윈도우(cwnd) 중 작은 값을 최종 전송 크기로 결정합니다.

- **리시버 사이드 슬라이딩 윈도우 (Receiver-side Sliding Window)**:
  - 수신 측 역시 자신의 버퍼 공간을 관리하기 위해 윈도우를 유지합니다.
  - 수신 측은 자신이 현재 수용 가능한 빈 버퍼의 크기를 송신 측에 계속해서 알리는데, 이를 **광고된 수신 윈도우(Advertised Receive Window)**라고 합니다. 이는 운영체제의 커널 버퍼 관리와 밀접하게 연동됩니다.

## 3. 연관 항목 (Relationships)
- **상위 개념**: [[컴퓨터 네트워크]], [[흐름 제어]], [[TCP]]
- **하위 개념**: [[Advertised Receive Window]], [[rwnd]], [[cwnd]]
- **참조 링크**: [[ARQ]], [[실리 윈도우 증후군(SWS)]]

## 4. 비고 (Notes)
- 슬라이딩 윈도우의 효율적인 관리는 TCP 성능 최적화의 핵심이며, BDP(Bandwidth-Delay Product)와 윈도우 크기의 관계를 이해하는 것이 중요합니다.

---

## 🛠 LLM Maintenance Log
*이 구역은 에이전트가 자동으로 관리합니다. 직접 수정하지 마세요.*

| Date | Agent | Action | Description |
| :--- | :--- | :--- | :--- |
| 2026-06-01 | Gemini | Rewrite | Fixed conversational text corruption and extracted entity from raw source (net_sliding_window.txt.txt). |

<!-- [Human Protected: Start] -->
### 👨‍💻 Human Annotations
*이 섹션 하위의 내용은 에이전트가 덮어쓰지 않습니다.*
- 
<!-- [Human Protected: End] -->
