---
author: Gemini
last_updated: 2026-06-16
tags: [컴퓨터 네트워크, SWS, 실리 윈도우 증후군, TCP, 최적화]
version: 1.0.2
---

# 실리 윈도우 증후군 (Silly Window Syndrome, SWS)

> 슬라이딩 윈도우 메커니즘에서 송수신 측의 처리 속도 불균형으로 인해 극히 작은 데이터 패킷이 빈번하게 전송되어 네트워크 대역폭이 낭비되는 현상.

## 1. 개요 (Overview)
TCP 슬라이딩 윈도우 환경에서 송신 측이 너무 작은 데이터를 자주 보내거나, 수신 측이 데이터를 너무 느리게 읽어 들일 때 발생합니다. 1바이트의 데이터를 보내기 위해 40바이트의 TCP/IP 헤더를 붙여야 하므로 전송 효율이 극도로 저하되는 증후군입니다.

## 2. 상세 내용 (Details)
### 2.1 리시버 사이드 SWS (Receiver-Side SWS)
수신 측 응용 프로그램(Application)의 데이터 소모 속도가 네트워크 전송 속도보다 느릴 때 발생합니다.
- **현상**: 수신 버퍼에서 딱 1바이트만 비었을 때 이를 송신 측에 알리면(`rwnd=1`), 송신 측은 오버헤드가 큰 1바이트 패킷을 전송하게 됩니다.
- **해결책**:
  - **클라크 솔루션 (Clark's Solution)**: 수신 버퍼의 절반이 비거나, 최소 1 MSS(Maximum Segment Size) 크기만큼 공간이 확보될 때까지 `rwnd=0`을 광고하여 송신을 차단합니다.
  - **지연 에크 (Delayed ACK)**: 패킷 수신 즉시 ACK를 보내지 않고 대기하여, 수신 버퍼가 더 비워지거나 다음 패킷과 함께 응답하도록 유도합니다.

### 2.2 샌더 사이드 SWS (Sender-Side SWS)
송신 측 응용 프로그램(예: 텔넷 터미널 입력 등)이 아주 작은 데이터를 빈번하게 생성하여 OS 송신 버퍼에 쓸 때 발생합니다.
- **해결책**:
  - **네이글 알고리즘 (Nagle's Algorithm)**: 
    - 첫 번째 작은 데이터는 즉시 전송합니다.
    - 그 다음 데이터부터는 이전에 보낸 패킷의 ACK가 돌아오거나, 버퍼에 1 MSS만큼 데이터가 쌓일 때까지 전송하지 않고 데이터를 모아두었다가(Coalescing) 한꺼번에 전송합니다.

## 3. 연관 항목 (Relationships)
- **상위 개념**: [[슬라이딩 윈도우]], [[TCP 흐름 제어]]
- **하위 개념**: [[네이글 알고리즘]], [[클라크 솔루션]]
- **참조 링크**: [[MSS (Maximum Segment Size)]], [[TCP 헤더]], [[Delayed ACK]]

## 4. 비고 (Notes)
### 🛡 Security Audit: SWS 관련 취약점
- **CVE-2019-11479 (SACK Slowness)**: 
  - **설명**: 공격자가 의도적으로 매우 작은 MSS를 강제하여 커널의 재전송 큐를 파편화시키는 DoS 공격입니다.
  - **영향**: 커널이 파편화된 리스트를 처리하며 CPU 자원을 과다 소모하게 됩니다.
  - **대응**: 커널 업데이트 및 최소 MSS 값 제한.

---

## 🛠 LLM Maintenance Log
*이 구역은 에이전트가 자동으로 관리합니다. 직접 수정하지 마세요.*

| Date | Agent | Action | Description |
| :--- | :--- | :--- | :--- |
| 2026-06-16 | Gemini | Create | Initial entity extraction from raw source. |
| 2026-06-16 | Gemini | Update | `data/raw/net_silly_window.txt` 기반으로 해결책 및 보안 취약점 정보 보강. |

<!-- [Source Reference: data/raw/net_silly_window.txt] -->

<!-- [Human Protected: Start] -->
### 👨‍💻 Human Annotations
*이 섹션 하위의 내용은 에이전트가 덮어쓰지 않습니다.*
- 
<!-- [Human Protected: End] -->
