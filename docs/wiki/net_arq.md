---
# Wiki Page Template v1.0
author: Gemini
last_updated: 2026-06-01
tags: [컴퓨터 네트워크, ARQ, 에러 제어, TCP]
version: 0.0.1
---

# ARQ (Automatic Repeat Request)

> 데이터 전송 과정에서 에러 발생 시 송신자가 자동으로 데이터를 재전송하여 통신의 신뢰성을 보장하는 에러 제어 기법.

## 1. 개요 (Overview)
데이터 전송 시 압축(소스 코딩), 에러 정정(채널 코딩), 신호 변환(모듈레이션) 등 비용이 큰 연산이 수반됩니다. 전송 실패 시 응용 계층이 매번 재전송을 책임지면 비효율적이므로, 개념적인 장치인 트랜스미트 컨트롤러가 인간이나 상위 계층의 개입 없이 자동으로 재전송을 실현하는 기술이 ARQ입니다. 성공 여부를 알리는 피드백 정보로 ACK(성공)와 NAK(실패)를 사용합니다.

## 2. 상세 내용 (Details)
- **전통적인 3가지 ARQ 기법**:
  1. **Stop-and-Wait ARQ**: 패킷 1개를 보내고 ACK가 올 때까지 멈춰서 기다리는 방식. 로직은 단순하나 1 RTT(Round Trip Time) 동안 파이프를 활용하지 못해 비효율적입니다.
  2. **Go-Back-N (GBN) ARQ**: ACK를 기다리지 않고 파이프라인에 여러 패킷을 밀어 넣는 방식(Pipelined Protocol). 최대 전송량(윈도우 사이즈)은 BDP(Bandwidth-Delay Product)와 연결됩니다. 오류(NAK) 발생 시 문제가 발생한 위치의 맨 앞 데이터부터 윈도우 크기(N)만큼 전부 다시 전송합니다.
  3. **Selective Repeat (SR) ARQ**: 정상 수신되지 않은 특정 패킷만 선택적으로 재전송하는 방식. 효율적이지만 모든 패킷에 시퀀스 넘버를 붙여야 하고 구현 및 버퍼 관리 로직이 매우 복잡합니다.
- **TCP의 ARQ 및 에러 제어**:
  - TCP는 SR이 필수가 아니며, GBN의 변형(Variant)을 사용합니다.
  - NAK가 없고 누적 에크(Cumulative ACK) 체계를 사용한다는 점에서 전통적인 GBN과 차이가 있습니다.
  - **에러 제어 구성 요소**: 에러 감지를 위한 체크섬(Checksum), 수신 여부를 알리는 에크(ACK), 자동 재전송 시간을 결정하는 타임아웃(Timeout)이 유기적으로 동작하여 신뢰성을 보장합니다.

## 3. 연관 항목 (Relationships)
- **상위 개념**: [[컴퓨터 네트워크]], [[에러 제어]]
- **하위 개념**: [[Stop-and-Wait ARQ]], [[Go-Back-N ARQ]], [[Selective Repeat ARQ]]
- **참조 링크**: [[Sliding Window]], [[TCP]]

## 4. 비고 (Notes)
- TCP의 에러 제어 메커니즘은 흐름 제어, 혼잡 제어와 함께 네트워크의 안정성을 유지하는 핵심 요소입니다.

---

## 🛠 LLM Maintenance Log
*이 구역은 에이전트가 자동으로 관리합니다. 직접 수정하지 마세요.*

| Date | Agent | Action | Description |
| :--- | :--- | :--- | :--- |
| 2026-06-01 | Gemini | Create | Initial entity extraction from raw source (net_arq.txt.txt). |

<!-- [Human Protected: Start] -->
### 👨‍💻 Human Annotations
*이 섹션 하위의 내용은 에이전트가 덮어쓰지 않습니다.*
- 
<!-- [Human Protected: End] -->
