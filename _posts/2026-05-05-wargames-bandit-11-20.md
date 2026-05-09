---
layout: post
title: "리눅스 기반 시스템 탐색 및 데이터 분석(11-25단계)"
description: bandit Wargame
date: 2026-05-07
categories: [Wargames,bandit]
tags: [Linux, wsl,명령어]
--- 
  
## Bandit Wargame 10 → 25 단계 풀이

---

## 10 → 11 단계

이번 단계에서는 `data.txt` 파일의 내용이 Base64로 인코딩되어 있었다.

Base64는 데이터를 문자 형태로 바꿔 표현하는 방식이고, 이를 다시 원래 형태로 되돌리는 과정을 **디코딩**이라고 한다.

따라서 다음 명령어를 사용해 디코딩했다.

```bash
base64 -d data.txt
````

이 명령어를 실행하면 원래의 문자열이 출력되고, 다음 단계의 비밀번호를 얻을 수 있다.

<img src="img/bandit/10-11.png" alt="0-1" width="500">

---

## 11 → 12 단계

`cat data.txt` 명령어로 파일을 열어보니 ROT13 방식으로 변환된 문장이 보였다.

ROT13은 알파벳을 13글자씩 밀어서 치환하는 방식이다. 예를 들어 `A`는 `N`으로, `B`는 `O`로 바뀐다.

이를 원래대로 되돌리기 위해 `tr` 명령어를 사용했다.

```bash
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

처음에는 `A-Za-z` 부분을 보고 `Za`가 하나의 단어처럼 취급되는 줄 알고 해석하는 데 헷갈렸다. 결국 LLM의 도움을 받아 `A-Z`와 `a-z` 범위를 의미한다는 것을 이해했다.
<img src="img/bandit/11-12.png" alt="0-1" width="500">

---

## 12 → 13 단계

이번 문제는 파일이 여러 번 압축되어 있었고, 압축 형식에 따라 적절한 명령어를 사용해 계속 압축을 해제해야 했다.

먼저 `file` 명령어를 사용해 현재 파일의 형식을 확인한다.

```bash
file data
```

파일 형식에 따라 다음과 같이 처리했다.

### gzip 형식일 경우

```bash
mv data data.gz
gunzip data.gz
```

### bzip2 형식일 경우

```bash
mv data data.bz2
bunzip2 data.bz2
```

### tar 형식일 경우

```bash
mv data data.tar
tar -xf data.tar
```

이 과정을 반복하다 보면 최종적으로 ASCII text 파일이 나온다.

tar 파일의 경우 압축 해제 후 파일명이 바뀌는 경우가 있었기 때문에, `ls` 명령어로 파일명을 확인한 뒤 다시 `data`라는 이름으로 변경하며 진행했다.

```bash
ls
mv 변경된파일명 data
```
<img src="img/bandit/12-13-1.png" alt="0-1" width="500">
<img src="img/bandit/12-13-2.png" alt="0-1" width="500">

---

## 13 → 14 단계

`ls` 명령어를 사용해보니 `sshkey.private` 파일이 있었다.

처음에는 다음 명령어로 접속을 시도했다.

```bash
ssh -i sshkey.private bandit14@localhost -p 2220
```

하지만 다음과 같은 오류가 발생했다.

```bash
Could not create directory '/home/bandit13/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit13/.ssh/known_hosts)
```

구글링해보니 호스트 키를 저장할 권한이 없다는 경고였다. 여러 방법을 시도했지만 계속 접속이 불가능했다.

이후 LLM의 도움을 받아, 키 내용을 복사해서 WSL 환경에 저장한 뒤 사용하는 방법을 시도했다.

먼저 키 내용을 확인했다.

```bash
cat sshkey.private
```

출력된 키 내용을 복사한 뒤 WSL에서 새 파일을 만들었다.

```bash
nano bandit.key
```

복사한 키 내용을 붙여넣고 저장한 다음, 권한을 설정했다.

```bash
chmod 600 bandit.key
```

그 후 다음 명령어로 접속했다.

```bash
ssh -i bandit.key bandit14@bandit.labs.overthewire.org -p 2220
```

이 방법으로 bandit14 계정에 접속할 수 있었다.
<img src="img/bandit/13-14-1.png" alt="0-1" width="500">
<img src="img/bandit/13-14-2.png" alt="0-1" width="500">
<img src="img/bandit/13-14-3.png" alt="0-1" width="500">

---

## 14 → 15 단계

이번 단계에서는 현재 비밀번호를 localhost의 30000번 포트로 전송해야 했다.

먼저 현재 비밀번호를 확인한 뒤, `nc` 명령어를 사용했다.

```bash
nc localhost 30000
```

연결 후 현재 레벨의 비밀번호를 입력하면 다음 단계의 비밀번호가 출력된다.

또는 다음과 같이 `echo`와 파이프를 이용해 한 번에 전송할 수도 있다.

```bash
echo "현재비밀번호" | nc localhost 30000
```
<img src="img/bandit/14-15.png" alt="0-1" width="500">

---

## 15 → 16 단계

이번 단계에서는 SSL/TLS 암호화 연결을 사용해야 했다.

14단계와 비슷하게 현재 비밀번호를 전송해야 하지만, 단순한 `nc`가 아니라 `openssl s_client`를 사용해야 한다.

```bash
openssl s_client -connect localhost:30001
```

연결 정보가 많이 출력되기 때문에, 불필요한 출력 정보를 줄이기 위해 `-quiet` 옵션을 추가했다.

```bash
openssl s_client -connect localhost:30001 -quiet
```

이후 현재 비밀번호를 입력하면 다음 단계의 비밀번호를 얻을 수 있다.

---

## 16 → 17 단계

이번 단계에서는 localhost의 31000~32000번대 포트 중 올바른 포트를 찾아야 했다.

먼저 어떤 포트가 열려 있고, 어떤 서비스가 동작하는지 확인하기 위해 `nmap`을 사용했다.

```bash
nmap -sV -p 31000-32000 localhost
```

스캔 결과를 확인한 뒤, SSL 연결이 가능한 포트를 대상으로 테스트했다.

```bash
openssl s_client -connect localhost:31518 -quiet
openssl s_client -connect localhost:31790 -quiet
```

테스트 결과, `31790`번 포트에서 다음 단계로 접속할 수 있는 SSH private key를 얻을 수 있었다.

이후 과정은 13 → 14 단계와 비슷하게 진행했다. 키를 파일로 저장하고 권한을 설정한 뒤 SSH 접속을 시도했다.

```bash
chmod 600 sshkey
ssh -i sshkey bandit17@bandit.labs.overthewire.org -p 2220
```
<img src="img/bandit/16-17-1.png" alt="0-1" width="500">
<img src="img/bandit/16-17-2.png" alt="0-1" width="500">

---

## 17 → 18 단계

이번 단계의 핵심은 두 파일의 차이점을 찾는 것이었다.

디렉터리를 확인해보면 두 개의 파일이 존재한다. 두 파일의 차이를 비교하기 위해 `diff` 명령어를 사용했다.

```bash
diff passwords.old passwords.new
```

`diff` 명령어는 두 파일에서 서로 다른 부분을 출력해준다. 이를 통해 다음 단계의 비밀번호를 확인할 수 있었다.
<img src="img/bandit/17-18.png" alt="0-1" width="500">

---

## 18 → 19 단계

이번 단계에서는 로그인하면 바로 접속이 종료되는 문제가 있었다.

따라서 SSH 접속과 동시에 명령어를 실행하는 방식을 사용했다.

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme
```

이 명령어는 bandit18 계정으로 접속한 뒤, 바로 `cat readme` 명령어를 실행한다.

이를 통해 `readme` 파일 안에 있는 다음 단계의 비밀번호를 확인할 수 있었다.

---

## 19 → 20 단계

이번 단계에서는 setuid가 설정된 실행 파일을 이용해야 했다.

먼저 현재 디렉터리를 확인했다.

```bash
ls
```

확인해보니 `bandit20-do`라는 실행 파일이 있었다.

이 파일이 어떤 권한으로 명령어를 실행하는지 확인하기 위해 다음 명령어를 사용했다.

```bash
./bandit20-do whoami
```

결과로 `bandit20`이 출력되었다. 즉, 이 프로그램은 명령어를 bandit20 권한으로 실행할 수 있다는 뜻이다.

따라서 bandit20의 비밀번호 파일을 읽었다.

```bash
./bandit20-do cat /etc/bandit_pass/bandit20
```

이를 통해 다음 단계의 비밀번호를 얻었다.
<img src="img/bandit/19-20.png" alt="0-1" width="500">

---

## 20 → 21 단계

이번 단계에서는 `suconnect` 프로그램을 사용해야 했다.

먼저 한 터미널에서 포트를 열어 현재 비밀번호를 대기시켰다.

```bash
echo "현재비밀번호" | nc -l -p 12345
```

그 다음 다른 터미널에서 `suconnect`를 실행했다.

```bash
./suconnect 12345
```

`suconnect`가 해당 포트로 접속하여 비밀번호를 확인하고, 올바르면 다음 단계의 비밀번호를 출력한다.
<img src="img/bandit/20-21.png" alt="0-1" width="500">

---

## 21 → 22 단계

이번 단계부터는 cron 작업을 분석하는 문제가 등장한다.

먼저 cron 설정 파일들이 있는 디렉터리로 이동했다.

```bash
cd /etc/cron.d/
ls
```

확인해보니 `cronjob_bandit22` 파일이 있었다.

```bash
cat cronjob_bandit22
```

파일 내용을 확인해보면 특정 스크립트가 주기적으로 실행되고 있음을 알 수 있다. 해당 스크립트 파일을 열어보면 다음 단계의 비밀번호가 저장된 위치를 확인할 수 있었다.

```bash
cat /usr/bin/cronjob_bandit22.sh
```

스크립트 내용을 따라가며 파일을 확인한 결과, bandit22의 비밀번호를 얻을 수 있었다.

<img src="img/bandit/21-22.png" alt="0-1" width="500">

---

## 22 → 23 단계

이번 단계도 cron 설정 파일을 분석하는 문제였다.

먼저 `/etc/cron.d/` 디렉터리를 확인했다.

```bash
cd /etc/cron.d/
ls
```

그중 `cronjob_bandit23` 파일을 확인했다.

```bash
cat cronjob_bandit23
```

해당 파일을 보면 `/usr/bin/cronjob_bandit23.sh` 스크립트가 주기적으로 실행되고 있음을 알 수 있다.

```bash
cat /usr/bin/cronjob_bandit23.sh
```

스크립트 내용을 보면 `whoami` 명령어로 현재 사용자 이름을 구한 뒤, 다음 명령어를 통해 `/tmp/`에 저장될 파일명을 만들고 있었다.

```bash
echo I am user $myname | md5sum | cut -d ' ' -f 1
```

cron은 이 스크립트를 bandit23 권한으로 실행하므로, `$myname`에는 `bandit23`이 들어간다고 판단했다.

따라서 직접 다음 명령어를 실행해 파일명을 구했다.

```bash
echo I am user bandit23 | md5sum | cut -d ' ' -f 1
```

그 결과 나온 파일명은 다음과 같았다.

```bash
8ca319486bfbbc3663ea0fbe81326349
```

따라서 `/tmp/` 아래의 해당 파일을 읽었다.

```bash
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```

이를 통해 bandit23의 비밀번호를 얻을 수 있었다.
<img src="img/bandit/22-23.png" alt="0-1" width="500">

---

## 23 → 24 단계

이번 단계 역시 cron 작업을 분석해야 했다.

먼저 cron 설정 디렉터리로 이동했다.

```bash
cd /etc/cron.d/
ls
```

확인해보니 bandit24와 관련된 cron 파일이 있었다. 해당 파일을 열어 실제 실행되는 스크립트를 확인했다.

```bash
cat cronjob_bandit24
cat /usr/bin/cronjob_bandit24.sh
```

스크립트의 동작은 다음과 같았다.

1. 이 스크립트는 bandit24 권한으로 실행된다.
2. `myname=$(whoami)`이므로 `myname`은 `bandit24`가 된다.
3. `/var/spool/bandit24/foo` 디렉터리로 이동한다.
4. 그 안의 파일들을 하나씩 확인한다.
5. 파일 소유자가 bandit23이면 실행한다.
6. 실행 후 파일을 삭제한다.

즉, bandit23 사용자가 만든 스크립트를 해당 디렉터리에 넣으면, cron이 bandit24 권한으로 실행해주는 구조였다.

먼저 결과를 저장할 임시 디렉터리를 만들었다.

```bash
mkdir /tmp/bandit23_to_24
```

그 다음 비밀번호를 읽어 저장하는 스크립트를 작성했다.

```bash
nano getpass.sh
```

스크립트 내용은 다음과 같다.

```bash
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/bandit23_to_24/password
```

파일에 실행 권한을 부여했다.

```bash
chmod +x getpass.sh
```

그리고 cron이 실행하는 디렉터리로 복사했다.

```bash
cp getpass.sh /var/spool/bandit24/foo/
```

잠시 후 결과 파일을 확인했다.

```bash
cat /tmp/bandit23_to_24/password
```

이를 통해 bandit24의 비밀번호를 얻을 수 있었다.

<img src="img/bandit/23-24-1.png" alt="0-1" width="500">
<img src="img/bandit/23-24-2.png" alt="0-1" width="500">
<img src="img/bandit/23-24-3.png" alt="0-1" width="500">

---

## 24 → 25 단계

이번 단계에서는 localhost의 30002번 포트에 현재 레벨의 비밀번호와 4자리 PIN 번호를 함께 전송해야 했다.

먼저 `nc`로 연결해보았다.

```bash
nc localhost 30002
```

연결해보면 bandit24의 비밀번호와 secret pincode를 한 줄에 공백으로 구분해 입력하라는 안내가 나온다.

입력 형식은 다음과 같다.

```bash
현재비밀번호 PIN번호
```

PIN 번호는 `0000`부터 `9999`까지 존재할 수 있으므로 직접 하나씩 입력하기는 어렵다. 따라서 반복문을 사용해 brute force를 진행했다.

먼저 현재 비밀번호를 변수에 저장했다.

```bash
PASS="현재_bandit24_비밀번호"
```

그 다음 `seq -w` 명령어로 `0000`부터 `9999`까지의 값을 생성했다.

```bash
seq -w 0000 9999
```

이를 반복문과 함께 사용해 비밀번호와 PIN 번호 조합을 만들었다.

```bash
for i in $(seq -w 0000 9999); do
  echo "$PASS $i"
done
```

이 결과를 `nc`로 전달하면 모든 PIN을 자동으로 시도할 수 있다.

```bash
for i in $(seq -w 0000 9999); do
  echo "$PASS $i"
done | nc localhost 30002
```

하지만 실패 메시지가 너무 많이 출력되기 때문에, `grep -v "Wrong"`을 사용해 틀린 결과를 제외했다.

```bash
for i in $(seq -w 0000 9999); do
  echo "$PASS $i"
done | nc localhost 30002 | grep -v "Wrong"
```

이 명령어를 통해 올바른 PIN이 입력되었을 때 출력되는 bandit25의 비밀번호를 확인할 수 있었다.

<img src="img/bandit/24-25.png" alt="0-1" width="500">