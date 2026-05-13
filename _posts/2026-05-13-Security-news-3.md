---
layout: post
title: "AXIOS 공급망 해킹 사례" 
description: 최신 보안사고 사례 분석
date: 2026-05-13
categories: [블로그/기술문서]
tags: []
---
<style>
  .footnote-text {
  font-size: 0.9rem;
  color: #666666;
  margin-top: -4px;
  margin-bottom: 16px;
  line-height: 1.6;
}
</style>

# AXIOS 공급망 해킹사례 정리

## 1. 사건 내용 

<p class="footnote-text">
※npm: Node Package Manager의 약자로, Node.js 환경에서 자바스크립트 라이브러리, 패키지, 모듈을 설치하고 공유하고 관리하는 오픈소스 패키지 생태계이자 도구이다. AXIOS 오픈소스 코드도 npm을 통해 배포되고 있었다. </p>

2026년 3월 말, 자바스크립트에서 HTTP 요청을 보낼 때 많이 사용하는 라이브러리인 **Axios**에서 공급망 공격이 발생하였다.

Axios는 프론트엔드와 백엔드에서 API 요청을 처리할 때 자주 사용되는 라이브러리이다. 많은 개발자와 기업이 사용하는 패키지였기 때문에, 공격자가 Axios 배포 과정에 악성코드를 넣는 데 성공하면 매우 큰 피해로 이어질 수 있었다.

공격자는 먼저 npm에 **plain-crypto-js**라는 패키지를 업로드하였다. 이 이름은 실제로 많이 사용되는 **crypto-js** 패키지와 비슷하게 보이도록 만든 이름이었다. 처음에는 정상적인 패키지처럼 보이도록 구성한 뒤, 이후 악성코드가 포함된 **plain-crypto-js@4.2.1** 버전을 업로드하였다.

그 후 공격자는 Axios 주요 관리자의 npm 계정을 탈취하였다. 그리고 탈취한 계정을 이용해 악성 의존성이 포함된 Axios 버전을 npm에 게시하였다.

문제가 된 Axios 버전은 다음과 같다.

```text
axios@1.14.1
axios@0.30.4
```

이 두 버전에는 **plain-crypto-js@4.2.1**이라는 악성 의존성이 추가되어 있었다. 겉으로 보면 Axios의 정상적인 업데이트처럼 보였지만, 실제로는 설치 과정에서 악성코드가 실행될 수 있는 상태였다.

특히 이번 공격에서 중요한 부분은 npm의 **postinstall** 기능이 악용되었다는 점이다.

postinstall은 패키지가 설치된 직후 자동으로 실행되는 스크립트이다. 원래는 설치 후 필요한 설정을 자동으로 처리하기 위한 기능이지만, 이번 사건에서는 악성코드를 자동 실행하는 용도로 사용되었다.

감염된 Axios 버전이 설치되면 악성 의존성도 함께 설치되고, 그 과정에서 악성 스크립트가 자동으로 실행될 수 있었다.

악성코드는 사용자의 운영체제를 확인한 뒤 Windows, macOS, Linux 환경에 맞는 악성 파일을 내려받았다. 이렇게 다운로드된 2단계 악성코드는 RAT 형태였다.
<p class="footnote-text">
※RAT: Remote Access Trojan의 약자로, 공격자가 감염된 컴퓨터에 원격으로 접근하거나 명령을 실행할 수 있게 만드는 악성코드이다. </p>

이 RAT는 시스템 정보를 수집하고, 공격자의 명령제어 서버와 통신하며, 추가 명령을 받아 실행할 수 있도록 설계되어 있었다.

또한 악성코드는 실행된 뒤 자신의 흔적을 줄이기 위해 일부 파일을 삭제하거나 정상 파일처럼 보이게 바꾸는 기능도 가지고 있었다. 이 때문에 나중에 단순히 설치된 파일만 확인하면 공격 흔적을 발견하기 어려울 수 있었다.

공개된 분석에 따르면, 이번 공격은 북한과 연계된 위협 그룹인 **UNC1069**와 관련이 있는 것으로 알려졌다. 이 그룹은 개발자나 오픈소스 관리자에게 접근해 신뢰를 쌓은 뒤, 회의나 협업을 가장해 악성 링크를 전달하는 방식을 사용헀다.

이번 사건에서도 공격자는 신분을 숨기고 관리자를 대상으로 접근한 뒤, 온라인 회의나 문제 해결을 가장해 악성 파일 실행을 유도한 것으로 알려졌다.

결국 npm 관리자 계정이 탈취되면서 공격자는 Axios의 정상 배포 경로를 악용할 수 있게 되었고, 그 결과 많은 개발 환경이 위험에 노출되었다.

---

## 2. 주요 원인

이번 사건의 주요 원인은 다음과 같다고 생각한다.

```text
Axios 관리자의 npm 계정이 탈취된 것.
npm 패키지 설치 후 자동 실행되는 postinstall 기능이 악용된 것.
plain-crypto-js라는 가짜 의존성 패키지가 정상 패키지처럼 위장한 것.
개발자들이 신뢰하는 공식 npm 배포 경로가 공격에 이용된 것.
오픈소스 관리자 계정과 토큰 관리가 충분히 안전하지 않았던 것.
```

공격자는 Axios 자체를 해킹한 것이 아니라, Axios를 배포할 수 있는 권한을 가진 계정을 탈취하였다. 이 계정을 통해 악성 버전을 npm에 게시했기 때문에 사용자 입장에서는 정상적인 Axios 업데이트처럼 보일 수밖에 없었다.

공격자는 Axios 코드 안에 직접 악성코드를 크게 넣기보다는, **plain-crypto-js@4.2.1**이라는 악성 패키지를 의존성으로 추가하였다. 사용자가 감염된 Axios 버전을 설치하면 이 악성 패키지도 자동으로 설치되었다.

그리고 이 악성 패키지는 npm의 postinstall 기능을 이용해 설치 직후 악성 스크립트를 실행하였다.

```text
패키지 설치
→ plain-crypto-js 설치
→ postinstall 스크립트 실행
→ 운영체제 확인
→ Windows, macOS, Linux에 맞는 악성코드 다운로드
→ RAT 실행
```

---

## 3. 대응 방법

Axios 관리자가 계정 탈취 사실을 확인한 뒤, 먼저 npm 측에 연락하여 악성 버전을 내려달라고 요청하였다.

이후 npm 관리팀은 문제가 된 Axios 버전을 npm 저장소에서 제거하였다.

문제가 된 버전은 다음과 같다.

```text
axios@1.14.1
axios@0.30.4
```

또한 악성 의존성으로 사용된 패키지도 함께 제거되었다.

```text
plain-crypto-js@4.2.1
```

이 조치로 인해 새로운 사용자가 악성 버전을 추가로 설치하는 것은 막을 수 있었다.

하지만 이미 해당 버전을 설치한 사용자의 경우, 설치 과정에서 악성코드가 실행되었을 가능성이 있었다. 그래서 Axios 측은 감염된 버전을 사용한 사람들에게 해당 환경을 침해된 것으로 보고 조치하라고 안내하였다.

구체적으로는 문제가 된 Axios 버전을 삭제하고, 안전한 버전으로 되돌리거나 최신 정상 버전으로 업데이트하도록 안내하였다.

또한 감염된 환경에서 사용되었을 가능성이 있는 npm 토큰, GitHub 토큰, API 키, 클라우드 인증정보 등을 교체해야 한다고 권고하였다.

Axios 프로젝트 측에서는 이후 사건에 대한 사후 분석을 공개하고, 어떤 버전이 영향을 받았는지와 사용자가 어떤 조치를 해야 하는지를 안내하였다.

---

## 4. 느낀점 

이번 사례는 오픈소스 공급망 공격이 얼마나 위험한지 잘 보여주고있다. 특히 이번 사건에서 인상 깊었던 점은 공격자가 Axios의 핵심 코드를 직접 바꾼 것이 아니라, 의존성 패키지와 npm 설치 스크립트를 이용했다는 점이다. 사용자는 평소처럼 패키지를 설치했을 뿐인데, 그 과정에서 악성코드가 실행될 수 있었다.

이번 사건을 통해 유명한 오픈소스 패키지라고 해서 무조건 안전하다고 생각하면 안 된다는 것을 느꼈다. 앞으로는 패키지 버전 관리, lock 파일 관리, 토큰 관리, npm 계정 보안, CI/CD 보안까지 함께 신경 써야 한다고 생각한다.

특히 공급망 공격은 피해자가 직접 수상한 파일을 다운로드하지 않아도 발생할 수 있다는 점에서 더 위험하다. 사용자가 신뢰하는 정상적인 업데이트 경로가 공격에 이용되기 때문이다.

따라서 개발자와 기업은 오픈소스 패키지를 사용할 때 단순히 설치만 하는 것이 아니라, 어떤 버전이 설치되는지, 어떤 의존성이 추가되는지, 설치 과정에서 어떤 스크립트가 실행되는지까지 확인하는 습관이 필요하다고 생각한다.

## 참고자료

Axios GitHub Issue, 「Post Mortem: axios npm supply chain compromise」  
https://github.com/axios/axios/issues/10636

Google Cloud Blog, 「North Korea-Nexus Threat Actor Compromises Widely Used Axios NPM Package in Supply Chain Attack」  
https://cloud.google.com/blog/topics/threat-intelligence/north-korea-threat-actor-targets-axios-npm-package

StepSecurity, 「axios Compromised on npm - Malicious Versions Drop Remote Access Trojan」  
https://www.stepsecurity.io/blog/axios-compromised-on-npm-malicious-versions-drop-remote-access-trojan

Snyk, 「Axios npm Package Compromised: Supply Chain Attack Delivers Cross-Platform RAT」  
https://snyk.io/blog/axios-npm-package-compromised-supply-chain-attack-delivers-cross-platform/

The Hacker News, 「UNC1069 Social Engineering of Axios Maintainer Led to npm Supply Chain Attack」  
https://thehackernews.com/2026/04/unc1069-social-engineering-of-axios.html
