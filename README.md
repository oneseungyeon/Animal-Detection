## 연구 내용
현재 국립공원공단은 무인센서카메라를 통하여 야생동물 데이터가 수집해 육안으로 판독하는데 이에 많은 시간이 소요되며 일관성 유지가 힘들어 딥러닝을 활용한 연구를 통해 해결하고자 함

## 연구 과정
영상 내 동물의 개체와 수를 판독하기 위한 딥러닝 활용 연구로서 효율적인 데이터 구축과 딥러닝 모델 학습을 위해 아래와 같은 프로세스로 연구 진행

<img src = "https://user-images.githubusercontent.com/74392995/180735806-4245e7bb-a9dd-4fcf-89c3-58e8a6da6964.png" width = "60%" height = "40%">

1. 데이터 구축과정에 있어 megadetector에서 제공하는 사전 학습 모델을 이용해 semi-supervised learning의 일종인 의사라벨링(pseudo-labeling) 진행
2. 의사라벨링 후 데이터 정제과정을 거쳐 정제된 데이터을 이용해 모델 학습 진행
3. 배경으로부터 동물의 구별의 난의도에 따라 평가 데이터를 구분하여 정밀 평가 수행

## 딥러닝 모델

<img src = "https://user-images.githubusercontent.com/74392995/180745170-8f3a53ac-3e81-4c23-b2f9-84206ca0fd05.png" width = "60%" height = "40%">

1. Microsoft AI for Earth에서 개발한 Faster R-CNN(InceptionResNetv2 	Backbone)기반의 모델인 Megadetector을 이용하며 Megadetector는 동물, 사람, 탈것 탐지
2. 대규모 이미지를 훈련시킨 사전 학습 모델을 제공해 효과적으로 학습을 수행할 수 있음 

## 평가 결과
1. 평가 지표
* 기존 객체 탐지 모델 성능 지표인 mAP는 바운딩 박스의 정확도와 클래스별 정확도를 고려한 지표이지만 실무에서는 동영상에 나타난 동물 중 몇 마리를 제대로 탐지했는지가 더 중요해 객체 단위 재현율을 제안함!
* 재현율은 정답 객체 중 딥러닝 모델이 탐지한 객체의 비중을 의미하며 영상에 나타난 동물을 빠짐없이 탐지하여야 하기 때문에 재현율이 더 중요함

<img src = "https://user-images.githubusercontent.com/74392995/180736133-a7e8519e-b805-4a36-a368-b72a8081ef74.png" width = "40%" height = "40%">

2. 평가 데이터셋
* 배경과 동물 구별이 쉬운(Dataset 1)과 어려운(Dataset 2)를 이용해 평가 수행

<img src = "https://user-images.githubusercontent.com/74392995/180734906-3df3ed97-6e03-48de-9d92-cd68f0ad4398.png" width = "60%" height = "40%">

3. 평가 결과

<img src = "https://user-images.githubusercontent.com/74392995/180736280-fbf46ee0-ee92-47eb-8556-e325161f1a55.png" width = "60%" height = "40%">

## 결론
* 딥러닝 활용으로 기존 육안판독 작업을 보다 효율적이고 일관성있게 수행 가능(with 문서작업)
* 객체기반 성능지표로 정답과 예측의 중심을 비교해 본 연구 목적에 부합한 성능지표로 성능 평가 
* 향후 : SORT를 통한 후처리방법으로 탐지 정확도 향상 기대



