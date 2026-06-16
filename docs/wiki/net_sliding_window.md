---
author: Gemini
last_updated: 2026-06-16
tags: [컴퓨터 네트워크, 슬라이딩 윈도우, 흐름 제어, TCP]
version: 1.0.2
---

# 슬라이딩 윈도우 (Sliding Window)

> 송수신 측 사이의 데이터 흐름을 제어하기 위해 가용 윈도우 크기를 동적으로 조절하며 신뢰성 있는 전송을 보장하는 메커니즘.

## 1. 개요 (Overview)
네트워크 상에서 수신 측의 처리 능력을 초과하는 오버플로우를 방지하기 위한 **흐름 제어(Flow Control)** 기법입니다. 수신 측이 허용하는 범위 내에서 송신 측이 ACK 없이도 연속적인 패킷 전송을 가능케 하여 전송 효율을 높입니다.

## 2. 상세 내용 (Details)
### 2.1 샌더 사이드 슬라이딩 윈도우 (Sender-Side)
송신 측 버퍼는 상태에 따라 다음과 같은 4가지 카테고리로 관리됩니다.
1. **Category 1**: 전송 및 ACK 수신 완료 (윈도우 왼쪽 외부).
2. **Category 2 (In-flight / Outstanding)**: 전송되었으나 아직 ACK를 받지 못한 영역.
3. **Category 3 (Usable Window)**: 윈도우 내에 있으며 즉시 전송 가능한 영역.
4. **Category 4**: 아직 전송 불가능한 영역 (윈도우 오른쪽 외부).

- **윈도우 제어 동작**:
  - **Closing**: ACK 수신 시 왼쪽 경계를 오른쪽으로 이동.
  - **Opening / Shrinking**: 네트워크 상황 및 수신 측 통보에 따라 윈도우의 오른쪽 경계를 조절하여 전체 크기를 변경.
  - **최종 윈도우 크기 결정**: `min(rwnd, cwnd)`. 흐름 제어의 **rwnd**(수신 윈도우)와 혼잡 제어의 **cwnd**(혼잡 윈도우) 중 최솟값을 사용합니다.

### 2.2 리시버 사이드 슬라이딩 윈도우 (Receiver-Side)
수신 측은 자신의 남은 버퍼 공간을 송신 측에 광고하는데, 이를 **광고된 수신 윈도우(Advertised Receive Window, rwnd)**라고 합니다. 이는 운영체제의 커널 버퍼(메모리 관리 영역)와 밀접하게 연동되며, 응용 프로그램의 데이터 처리 속도에 따라 가변적입니다.

## 3. 연관 항목 (Relationships)
- **상위 개념**: [[TCP 흐름 제어]], [[전송 계층 (Transport Layer)]]
- **하위 개념**: [[rwnd (Receive Window)]], [[cwnd (Congestion Window)]]
- **참조 링크**: [[실리 윈도우 증후군 (SWS)]], [[ARQ]], [[BDP (Bandwidth-Delay Product)]]

## 4. 비고 (Notes)
### 🛡 Security Audit: 윈도우 메커니즘 취약점
- **CVE-2004-0230 (TCP Sequence Guessing)**:
  - **설명**: 윈도우 범위 내의 시퀀스 번호를 예측하여 RST 또는 데이터를 주입하는 공격.
  - **영향**: 세션 강제 종료 및 데이터 변조 위험.
  - **대응**: **RFC 5961**을 통한 검증 절차 강화.

---

## 🛠 LLM Maintenance Log
*이 구역은 에이전트가 자동으로 관리합니다. 직접 수정하지 마세요.*

| Date | Agent | Action | Description |
| :--- | :--- | :--- | :--- |
| 2026-06-16 | Gemini | Create | Initial entity extraction from raw source. |
| 2026-06-16 | Gemini | Update | `data/raw/net_sliding_window.txt` 기반 카테고리 정의 및 수식 보강. |

<!-- [Source Reference: data/raw/net_sliding_window.txt] -->

<!-- [Human Protected: Start] -->
### 👨‍💻 Human Annotations
*이 섹션 하위의 내용은 에이전트가 덮어쓰지 않습니다.*
- 
<!-- [Human Protected: End] -->
