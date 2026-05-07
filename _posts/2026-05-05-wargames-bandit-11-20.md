---
layout: post
title: "리눅스 기반 시스템 탐색 및 데이터 분석(11-25단계)"
description: bandit Wargame
date: 2026-05-07
categories: [Wargames,bandit]
tags: [Linux, wsl,명령어]
--- 

10->11단계 
Base64명령어는 데이터를 문자 형태로 바꿔 표현하는 것. 이걸 다시 원래대로 돌리는 것이 디코딩. 디코딩을 하기 위해서 base -d data.txt 활용.

11->12단계
cat data.txt로 열어보니 ROT13으로 바뀐 문장이 보인다. ROT13은 a-n으로 바뀌었다는 걸 의미하니까 tr 'A-Za-z' 'N-ZA-Mn-za-m'을 활용해서 원래대로 돌려줘야한다.
어떻게 원래대로 돌려야하는지 몰라서 llm을 참고했다. 처음에 A-Za-z로 표시되어있어서 Za가 한 단어처럼 취급되는줄 알고 해석을 해맸다.

12->13단계
이 문제는 어떻게 압축되어있는 지에 따라서 다른 명령어를 사용하는 과정을 반복하여 최종적으로 ASCII.text를 찾아내면 된다. 

결과가 gzip이면:

mv data data.gz
gunzip data.gz

결과가 bzip2면:

mv data data.bz2
bunzip2 data.bz2

결과가 tar면:

mv data data.tar
tar -xf data.tar

이 과정을 계속 반복한다. 단, tar의 경우 파일명이 변경되기때문에 ls을 통해 변경된 파일명을 확인하고 파일명을 data로 변경 후 계속 진행하였다. 

13->14단계
ls명령어를 사용해보니 힌트로 sshkey.private가 나왔다. 이걸 활용하여 ssh -i sshkey.private bandit14@localhost -p 2220 을 하여 접근하려고 했지만 실패했다. 

실패 메시지 
Could not create directory '/home/bandit13/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit13/.ssh/known_hosts) 
구글링 해보니 호스트키를 저장할 수 없다는 경고라고 한다. 
이 외에도 다양한 방법을 시도해보았으나 계속 접속이 불가능했다. llm에 도움을 요청해보니 먼저 키 내용을 복사하여 wsl에 저장한 후 저장된 키를 활용하여 접속을 시도해보라는 조언을 얻었다. 

따라서 cat sshkey.private를 하여 key내용을 복사한 후 nano bandit.key을 실행하여 파일을 저장하였다. 그 후 chmod 600 bandit.key로 권한을 설정하고 ssh -i bandit.key bandit14@bandit.labs.overthewire.org -p 2220 하여 접속에 성공하였다.

14->15단계
echo명령어를 사용해 현재 비밀번호를 출력하고, nc localhost 30000를 하여 현재 레벨의 비밀번호를 localhost의 30000번 포트 로 전송하였다. 

15-16단계
15단계에서는 SSL/TLS암호화를 사용해야한다고 한다. 14단계에서와 마찬가지로 echo를 통해 현재 비밀번호를 출력하였고, openssl s_client -connect localhost:30001 이 명령어를 사용했다. 여기서 불팔요한 연결정보를 줄여주기 위해 -quiet를 추가하였다. 

16-17단계
localhost의 31000~32000번대 포트로 전송하여 얻을 수 있다고 되어있으니, 각 포트가 어떻게 연결되어있고, 어떤 서비스인지 확인하기 위해서 nmap -sV -p 31000-32000 local 명령어를 사용했다. 그 후 31518번과 31790번을 openssl명령어를 사용해 테스트해본 결과 31790번 포트에서 비밀번호 키를 얻었다. 이후의 방식은 13->14단계와 비슷하다. 

17-18단계
이 문제의 포인트는 두 파일의 차이점을 찾아내는 것이다. diff명령어를 사용해서 두 파일의 차이를 찾았다. 

18-19단계
ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme 이 명령어를 사용했다. 

19-20단계
먼저 setuid 프로그램이 어떤식으로 명령어를 시랭하는지 확인한 후 setuid프로그램을 통해 /etc/bandit_pass파일을 찾아보았다. ls명령어를 사용해보니 bandit20-do 가 나왔다. ./bandit20-do whoami 명령어를 사용하여 bandit20을 얻은 후 ./bandit20-do cat /etc/bandit_pass/bandit20로 비밀번호를 찾았다.

20-21단계
먼저 12345 포트를 열었다. 그 후 ./suconnect 12345로 접속한 후 비밀번호를 찾았다.

21-22단계
/etc/cron.d/을 열어보니 22단계와 관련되어 보이는 cronjob_bandit22 파일이있었다. cronjob_bandit22을 열어보니 다른 파일주소가 있었고, 계속해서 나오는 파일을 열어보니 비밀번호가 나왔다.

22-23단계
21단계와 비슷하다. 이번단계도 llm의 도움을 받아 문제를 해결했다. 이번 문제는 /etc/cron.d/에 있는 cron 설정 파일을 확인하는 것이 핵심이다. 먼저 /etc/cron.d/ 디렉터리를 확인해보니 cronjob_bandit23 파일이 있었고, 이 파일을 열어보니 /usr/bin/cronjob_bandit23.sh 스크립트가 주기적으로 실행되고 있었다. 해당 스크립트를 확인해보니 whoami 명령어로 현재 사용자의 이름을 구한 뒤, echo I am user $myname | md5sum | cut -d ' ' -f 1 명령어를 통해 /tmp/에 저장될 파일명을 만들고 있었다. cron은 이 스크립트를 bandit23 권한으로 실행하므로 $myname에는 bandit23이 들어간다고 판단했다. 따라서 echo I am user bandit23 | md5sum | cut -d ' ' -f 1 명령어로 파일명을 직접 구했고, 그 결과 나온 /tmp/8ca319486bfbbc3663ea0fbe81326349 파일을 읽어서 bandit23의 비밀번호를 얻었다.

23-24단계
