# Quantum-computer-Simulator
제작: 정채호준(1인)
<br>
<br>
과정: OpenAI의 ChatGPT를 사용하여 코드 작성 및 문제 해결에 도움을 받았습니다. ChatGPT는 인터넷의 정보를 기반으로 학습된 모델이지만, 개발 과정에서 직접적으로 사용된 코드는 깃허브의 다른 프로젝트에서 가져오지 않았습니다. MIT 라이선스를 따릅니다.
<br>
<br>
목적: 양자 컴퓨터 시뮬레이터는 양자 컴퓨터의 작동 원리를 초보자들도 쉽게 이해할 수 있도록 돕는 교육용 소프트웨어입니다.
<br>
<br>
양자 컴퓨터가 고전 컴퓨터와 달리 중첩(Superposition), 얽힘(Entanglement), 측정(Measurement)과 같은 양자역학의 개념을 기반으로 작동한다는 사실은 설명만으로 이해하기 쉽지 않다. 특히, 큐비트(Quantum bit)가 0과 1의 중첩 상태를 표현할 수 있다는 점이나, 이러한 원리가 실제로 어떻게 효율성을 향상시키는지는 많은 사람에게 생소하고 어렵게 느껴진다.
<br>
이를 해결하기 위해 시뮬레이터는 양자 컴퓨터의 핵심 개념을 시각적으로 표현하고, 사용자가 직접 조작할 수 있는 환경을 제공한다.
<br>
<br>
실행 시 필요 라이브러리: tkinter, numpy, matplotlib
<br>
<br>
6가지의 탭: 
<br>
1. 양자 컴퓨터와 고전적 컴퓨터의 검색 성능, 원리 비교
2. 복잡도 그래프
3. 양자 컴퓨터와 고전적 컴퓨터의 병렬처리 검색 원리 비교
4. 확률적 분포도 시각화
5. 추가요소
6. X, H, CNOT 게이트 시뮬레이터
<br>
<br>
고전적 컴퓨터 VS 양자 컴퓨터 검색 성능 비교
![화면 캡처 2024-12-23 163819](https://github.com/user-attachments/assets/60299728-34a7-4c34-abb0-301fec04ebfa)

<br>
고전적 컴퓨터 VS 양자 컴퓨터 복잡도 비교 (matplotlib 활용)
![화면 캡처 2024-12-23 163741](https://github.com/user-attachments/assets/d19fc2aa-1362-4abc-b0f2-fa69cdc78cab)

<br>

X게이트, H게이트, CNOT 게이트 로직 시뮬레이터 구현
![화면 캡처 2024-12-23 163905](https://github.com/user-attachments/assets/f45efc54-aea2-49bc-909d-04f04e23ca7e)
