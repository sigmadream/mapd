# Lifelong MAPD with TSP v0.5

> Multi-Agent Pickup and Delivery에 관련된 실험 코드 및 알고리즘을 구현하고 있습니다. `TSP`를 적용해서 MAPD 문제를 실시간으로 해결하는데 관심이 있습니다.

## 목표

- [x] 환경 설정
- [x] Task 배당(배치처리)
- [x] Agent 이동(충돌허용)
- [ ] Agent 이동(충돌하지 않음)
  - [ ] TSP Solver를 이용할 수 있을까?
  - [ ] CBS를 적용할 수 있을까?
  - [ ] LNS-wPBS를 적용할 수 있을까?

> 제한사항) Lifelong 관련한 알고리즘의 경우 실시간 계산 부하를 견딜 수 없어서 `C++` 등과 같은 계산효율을 중시하는 알고리즘을 선택하는 경향성이 있으며 시각화와 관련된 내용을 신경쓰지 않는다. 본 연구의 경우 관련 연구기관과의 논의 및 협의를 위해서 시각화가 필수적이라 시각화가 상대적으로 불편한 `C++`등을 사용하는데 제한이 있음.

## Python 설정

```
$ python -m venv venv
$ .\venv\Scripts\activate
$ (venv) python.exe -m pip install --upgrade pip setuptools wheel
```

## Ref.

- [Task and Path Planning for Multi-Agent Pickup and Delivery](https://dl.acm.org/doi/10.5555/3306127.3331816)

  - [Efficient multi-agent task allocation for collaborative route planning with multiple unmanned vehicles](https://www.sciencedirect.com/science/article/pii/S2405896317310777)
  - [Market-based approaches for coordination of multi-robot teams at different granularities of interaction](https://kilthub.cmu.edu/articles/journal_contribution/Market-based_Approaches_for_Coordination_of_Multi-robot_Teams_at_Different_Granularities_of_Interaction/6555491/1/files/12037724.pdf)
  - [A Parallel Meta-heuristic for Solving a Multiple Asymmetric Traveling Salesman Problem with Simulateneous Pickup and Delivery Modeling Demand Responsive Transport Problems](https://link.springer.com/chapter/10.1007/978-3-319-19644-2_46)
  - [The multiple traveling salesman problem: an overview of formulations and solution procedures](https://www.sciencedirect.com/science/article/abs/pii/S0305048304001550)

- [Integrated Task Assignment and Path Planning for Capacitated Multi-Agent Pickup and Delivery](https://arxiv.org/abs/2110.14891)
  - [Codes for paper Integrated Task Assignment and Path Planning forCapacitated Multi-Agent Pickup and Delivery](https://github.com/nobodyczcz/MCA-RMCA)
