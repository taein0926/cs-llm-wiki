---
author: Gemini
last_updated: 2026-06-16
tags: [컴퓨터 네트워크, ARQ, 에러 제어, TCP, 신뢰성 전송]
version: 1.0.2
---

# ARQ (Automatic Repeat Request)

> 데이터 전송 오류 발생 시, 송신 측이 자동으로 해당 데이터를 재전송하여 신뢰성을 보장하는 자동 재전송 요청 기법.

## 1. 개요 (Overview)
데이터 전송 시에는 소스 코딩(압축), 채널 코딩(에러 정정), 모듈레이션(신호 변환) 등 비용이 큰 연산이 수반됩니다. 전송 실패 시 상위 응용 계층이 매번 재전송을 관리하는 것은 비효율적이므로, **트랜스미트 컨트롤러(Transmit Controller)**라는 개념적 장치가 인간이나 상위 계층의 개입 없이 자동으로 재전송을 수행하는 기술이 ARQ입니다. 이 과정에서 성공을 알리는 **ACK**와 실패를 알리는 **NAK** 피드백 정보를 활용합니다.

## 2. 상세 내용 (Details)
### 2.1 전통적인 3가지 ARQ 기법
1. **Stop-and-Wait ARQ**: 
   - 패킷 1개를 전송한 후 ACK가 도착할 때까지 대기합니다.
   - 로직이 단순하지만, 1 RTT(Round Trip Time) 동안 통신 파이프라인을 활용하지 못해 전송 효율이 매우 낮습니다.
2. **Go-Back-N (GBN) ARQ**:
   - ACK를 기다리지 않고 파이프라인에 여러 패킷을 밀어 넣는 방식(Pipelined Protocol)입니다.
   - 최대 전송량(윈도우 사이즈)은 **BDP(Bandwidth-Delay Product)**와 밀접하게 연관됩니다.
   - 오류(NAK) 발생 시, 문제가 발생한 위치의 패킷부터 윈도우 크기(N)만큼의 모든 데이터를 다시 전송합니다.
3. **Selective Repeat (SR) ARQ**:
   - 정상적으로 수신되지 않은 특정 패킷만을 선택적으로 재전송합니다.
   - 효율성은 가장 높지만, 모든 패킷에 시퀀스 넘버를 부여해야 하며 수신 측의 버퍼 관리 로직이 매우 복잡해집니다.

### 2.2 TCP의 에러 제어 (Error Control)
- **TCP의 특징**: 표준 TCP는 SR이 필수가 아니며, GBN의 변형(Variant)된 형태를 사용합니다. 전통적인 GBN과 달리 NAK가 없으며, **누적 에크(Cumulative ACK)** 체계를 사용합니다.
- **핵심 구성 요소**:
  - **Checksum**: 데이터 손상 여부를 감지하는 에러 감지 도구.
  - **ACK**: 수신 성공 여부를 송신 측에 알림.
  - **Timeout**: 패킷 유실 시 재전송을 트리거하는 시간 설정 (RTT 기반 동적 결정).

## 3. 연관 항목 (Relationships)
- **상위 개념**: [[신뢰성 전송 (Reliable Transfer)]], [[전송 계층 (Transport Layer)]]
- **하위 개념**: [[Stop-and-Wait]], [[Go-Back-N]], [[Selective Repeat]]
- **참조 링크**: [[TCP]], [[슬라이딩 윈도우]], [[BDP (Bandwidth-Delay Product)]]

## 4. 비고 (Notes)
### 🛡 Security Audit: ARQ/재전송 관련 취약점
- **CVE-2019-11477 (SACK Panic)**:
  - **설명**: TCP의 Selective Acknowledgment(SACK) 옵션을 처리하는 리눅스 커널의 정수 오버플로우 취약점입니다.
  - **영향**: 유실된 구간을 정밀하게 보고하는 SACK 정보를 처리할 때, 특정 조건(낮은 MSS)에서 커널 패닉을 유발하여 시스템을 다운시킬 수 있습니다.
  - **대응**: 최신 보안 패치 적용 또는 `net.ipv4.tcp_sack=0` 설정을 통한 SACK 비활성화.

---

## 🛠 LLM Maintenance Log
*이 구역은 에이전트가 자동으로 관리합니다. 직접 수정하지 마세요.*

| Date | Agent | Action | Description |
| :--- | :--- | :--- | :--- |
| 2026-06-16 | Gemini | Create | Initial entity extraction from raw source. |
| 2026-06-16 | Gemini | Update | `data/raw/net_arq.txt` 기반 최신 스키마 적용 및 내용 보강. |

<!-- [Source Reference: data/raw/net_arq.txt] -->

<!-- [Human Protected: Start] -->
### 👨‍💻 Human Annotations
*이 섹션 하위의 내용은 에이전트가 덮어쓰지 않습니다.*
- 
<!-- [Human Protected: End] -->
