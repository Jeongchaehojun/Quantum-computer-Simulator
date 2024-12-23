import tkinter as tk
from tkinter import ttk, messagebox
import math
import time
import random
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 게이트 시뮬레이터 클래스 정의
class GateSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("양자 게이트 시뮬레이터")

        # 초기 큐비트 상태 정의
        self.state = np.array([1, 0])  # 단일 큐비트 |0>
        self.state_cnot = np.array([1, 0, 0, 0])  # 두 큐비트 상태 |00>

        # 게이트 정의
        self.X_gate = np.array([[0, 1], [1, 0]])  # Pauli-X 게이트
        self.H_gate = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])  # Hadamard 게이트
        self.CNOT_gate = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 0, 1],
                                   [0, 0, 1, 0]])  # CNOT 게이트

        # 상태 표시 캔버스
        self.canvas = tk.Canvas(self.master, width=800, height=400, bg="white")
        self.canvas.pack()

        # 큐비트 및 회로 시각화
        self.canvas.create_text(100, 50, text="Qubit 1", font=("Arial", 14))
        self.canvas.create_text(100, 150, text="Qubit 2", font=("Arial", 14))

        self.line1 = self.canvas.create_line(150, 50, 700, 50, width=2)  # 첫 번째 큐비트 선
        self.line2 = self.canvas.create_line(150, 150, 700, 150, width=2)  # 두 번째 큐비트 선

        # 게이트 시각화 초기 상태
        self.gate_visuals = []  # 게이트를 나타내는 시각적 요소를 저장
        self.gate_texts = []  # 게이트 알파벳 텍스트를 저장

        # 큐비트 시각적 요소
        self.qubit1_circle = self.canvas.create_oval(150, 40, 180, 70, fill="blue")
        self.qubit1_text = self.canvas.create_text(165, 55, text="|0>", font=("Arial", 14))

        self.qubit2_circle = self.canvas.create_oval(150, 140, 180, 170, fill="blue")
        self.qubit2_text = self.canvas.create_text(165, 155, text="|00>", font=("Arial", 14))

        # 버튼 추가
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=10)

        btn_x = tk.Button(btn_frame, text="Apply X Gate", command=self.apply_x_gate)
        btn_x.pack(side=tk.LEFT, padx=5)

        btn_h = tk.Button(btn_frame, text="Apply H Gate", command=self.apply_h_gate)
        btn_h.pack(side=tk.LEFT, padx=5)

        btn_cnot = tk.Button(btn_frame, text="Apply CNOT Gate", command=self.apply_cnot_gate)
        btn_cnot.pack(side=tk.LEFT, padx=5)

        btn_reset = tk.Button(btn_frame, text="Reset", command=self.reset)
        btn_reset.pack(side=tk.LEFT, padx=5)

        # 초기 상태 업데이트
        self.update_visual_state()

    # 상태 업데이트 함수
    def update_visual_state(self):
        # 첫 번째 큐비트 상태 표시
        if np.array_equal(self.state, [1, 0]):
            self.canvas.itemconfig(self.qubit1_circle, fill="blue")
            self.canvas.itemconfig(self.qubit1_text, text="|0>")
        elif np.array_equal(self.state, [0, 1]):
            self.canvas.itemconfig(self.qubit1_circle, fill="red")
            self.canvas.itemconfig(self.qubit1_text, text="|1>")
        else:
            self.canvas.itemconfig(self.qubit1_circle, fill="purple")
            self.canvas.itemconfig(self.qubit1_text, text="Superposition")

        # 두 번째 큐비트 상태 표시
        if np.array_equal(self.state_cnot, [1, 0, 0, 0]):
            self.canvas.itemconfig(self.qubit2_circle, fill="blue")
            self.canvas.itemconfig(self.qubit2_text, text="|00>")
        elif np.array_equal(self.state_cnot, [0, 1, 0, 0]):
            self.canvas.itemconfig(self.qubit2_circle, fill="green")
            self.canvas.itemconfig(self.qubit2_text, text="|01>")
        elif np.array_equal(self.state_cnot, [0, 0, 1, 0]):
            self.canvas.itemconfig(self.qubit2_circle, fill="orange")
            self.canvas.itemconfig(self.qubit2_text, text="|10>")
        elif np.array_equal(self.state_cnot, [0, 0, 0, 1]):
            self.canvas.itemconfig(self.qubit2_circle, fill="red")
            self.canvas.itemconfig(self.qubit2_text, text="|11>")

    # 게이트 추가 함수
    def add_gate(self, gate_type):
        # 모든 기존 게이트를 지움
        for gate in self.gate_visuals:
            self.canvas.delete(gate)
        for text in self.gate_texts:
            self.canvas.delete(text)
        self.gate_visuals.clear()
        self.gate_texts.clear()

        # 새로운 게이트 추가
        if gate_type == "X":
            gate = self.canvas.create_rectangle(200, 30, 250, 70, fill="lightblue")
            text = self.canvas.create_text(225, 50, text="X", font=("Arial", 14))
        elif gate_type == "H":
            gate = self.canvas.create_rectangle(300, 30, 350, 70, fill="lightgreen")
            text = self.canvas.create_text(325, 50, text="H", font=("Arial", 14))
        elif gate_type == "CNOT":
            gate = self.canvas.create_rectangle(400, 30, 450, 90, fill="orange")
            text = self.canvas.create_text(425, 50, text="CNOT", font=("Arial", 14))
            control_line = self.canvas.create_line(425, 90, 425, 150, width=2, dash=(5, 2))  # CNOT 제어선
            target_dot = self.canvas.create_oval(420, 140, 430, 150, fill="black")  # CNOT 대상
            self.gate_visuals.extend([control_line, target_dot])

        self.gate_visuals.append(gate)
        self.gate_texts.append(text)

    # X 게이트 적용 함수
    def apply_x_gate(self):
        self.add_gate("X")
        self.state = np.dot(self.X_gate, self.state)
        self.update_visual_state()

    # H 게이트 적용 함수
    def apply_h_gate(self):
        self.add_gate("H")
        self.state = np.dot(self.H_gate, self.state)
        self.update_visual_state()

    # CNOT 게이트 적용 함수 (수정된 부분)
    def apply_cnot_gate(self):
        self.add_gate("CNOT")

        # 첫 번째 큐비트가 |1>인 경우 두 번째 큐비트를 반전
        # 상태_cnot는 |00>, |01>, |10>, |11> 중 하나로 가정
        if np.array_equal(self.state, [0, 1]):  # 제어 큐비트가 |1>
            if np.array_equal(self.state_cnot, [1, 0, 0, 0]):  # |00>
                self.state_cnot = np.array([0, 0, 1, 0])  # → |10>
            elif np.array_equal(self.state_cnot, [0, 1, 0, 0]):  # |01>
                self.state_cnot = np.array([0, 0, 0, 1])  # → |11>
            elif np.array_equal(self.state_cnot, [0, 0, 1, 0]):  # |10>
                self.state_cnot = np.array([0, 0, 0, 1])  # → |11>
            elif np.array_equal(self.state_cnot, [0, 0, 0, 1]):  # |11>
                self.state_cnot = np.array([0, 0, 1, 0])  # → |10>
        # 만약 제어 큐비트가 |0>이라면 대상 큐비트는 변화 없음
        self.update_visual_state()

    # 초기화 함수
    def reset(self):
        self.state = np.array([1, 0])
        self.state_cnot = np.array([1, 0, 0, 0])
        for gate in self.gate_visuals:
            self.canvas.delete(gate)
        for text in self.gate_texts:
            self.canvas.delete(text)
        self.gate_visuals.clear()
        self.gate_texts.clear()
        self.update_visual_state()


# 메인 애플리케이션 클래스 정의
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("고전 vs 양자 검색 비교 프로젝트")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # 기존 탭들 설정
        self.setup_existing_tabs()

        # 게이트 시뮬레이터 탭 추가
        self.gate_simulator_frame = tk.Frame(self.notebook)
        self.notebook.add(self.gate_simulator_frame, text="게이트 시뮬레이터")
        self.setup_gate_simulator_tab()

    def setup_existing_tabs(self):
        # 메인 탭
        self.main_frame = tk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="검색 애니메이션")
        self.setup_main_tab()

        # 복잡도 그래프 탭
        self.graph_frame = tk.Frame(self.notebook)
        self.notebook.add(self.graph_frame, text="복잡도 그래프")
        self.setup_graph_tab()

        # 병렬 검색 시뮬레이션 탭
        self.parallel_frame = tk.Frame(self.notebook)
        self.notebook.add(self.parallel_frame, text="병렬 검색 시뮬레이션")
        self.setup_parallel_tab()

        # 확률 분포 시뮬레이션 탭
        self.probability_frame = tk.Frame(self.notebook)
        self.notebook.add(self.probability_frame, text="확률 분포 시뮬레이션")
        self.setup_probability_tab()

        # 추가 정보 탭
        self.info_frame = tk.Frame(self.notebook)
        self.notebook.add(self.info_frame, text="추가 정보")
        self.setup_info_tab()

    def setup_main_tab(self):
        # 한 줄 소개 레이블 추가
        intro_label = tk.Label(self.main_frame, text="고전적 컴퓨터와 양자 컴퓨터의 검색 알고리즘 비교", font=("Arial", 12, "bold"))
        intro_label.pack(pady=10)
        intro_label = tk.Label(self.main_frame, text="데이터 크기(N)에서 입력한 값(M)을 찾는 과정을 봅시다 \n M<N", font=("Arial", 12))
        intro_label.pack(pady=10)

        # 입력 프레임
        input_frame = tk.Frame(self.main_frame)
        input_frame.pack(padx=10, pady=10)

        # N 입력
        tk.Label(input_frame, text="데이터 크기(N) 직접입력:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_N_main = tk.Entry(input_frame)
        self.entry_N_main.grid(row=0, column=1, padx=5, pady=5)

        # 예시 버튼 프레임
        btn_frame_N_main = tk.Frame(input_frame)
        btn_frame_N_main.grid(row=0, column=2, padx=5, pady=5)
        for val in [16, 32, 64]:
            btn = tk.Button(btn_frame_N_main, text=str(val), width=5,
                            command=lambda v=val, entry=self.entry_N_main: self.set_N(entry, v))
            btn.pack(side=tk.LEFT, padx=2)

        # M 입력
        tk.Label(input_frame, text="찾아낼 값(M)").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_M_main = tk.Entry(input_frame)
        self.entry_M_main.grid(row=1, column=1, padx=5, pady=5)

        # 실행 버튼
        self.run_button_main = tk.Button(input_frame, text="실행", command=self.run_search)
        self.run_button_main.grid(row=2, column=0, columnspan=3, pady=10)

        # 결과 레이블
        self.result_label_main = tk.Label(self.main_frame, text="결과 대기중...", font=("Arial", 10))
        self.result_label_main.pack(pady=5)

        # 검색 패널
        self.panel_main = tk.Frame(self.main_frame)
        self.panel_main.pack(padx=10, pady=10)

        # 고전적 검색 프레임
        self.classical_frame_main = tk.Frame(self.panel_main, bd=2, relief=tk.SUNKEN)
        self.classical_frame_main.pack(side=tk.LEFT, padx=10)
        tk.Label(self.classical_frame_main, text="클래식 컴퓨터 검색").pack(pady=5)
        self.classical_canvas_main = tk.Canvas(self.classical_frame_main, width=400, height=300, bg="white")
        self.classical_canvas_main.pack()

        # 양자적 검색 프레임
        self.quantum_frame_main = tk.Frame(self.panel_main, bd=2, relief=tk.SUNKEN)
        self.quantum_frame_main.pack(side=tk.LEFT, padx=10)
        tk.Label(self.quantum_frame_main, text="양자 컴퓨터 검색").pack(pady=5)
        self.quantum_canvas_main = tk.Canvas(self.quantum_frame_main, width=400, height=300, bg="white")
        self.quantum_canvas_main.pack()

    def set_N(self, entry_widget, value):
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, str(value))

    def run_search(self):
        # 입력값 파싱
        try:
            N = int(self.entry_N_main.get())
            M = int(self.entry_M_main.get())
        except ValueError:
            self.result_label_main.config(text="N과 M을 정수로 입력해주세요.")
            return

        if M < 0 or M >= N:
            self.result_label_main.config(text="0 <= M < N 범위로 입력해주세요.")
            return

        # 기존 캔버스 초기화
        self.classical_canvas_main.delete("all")
        self.quantum_canvas_main.delete("all")
        self.result_label_main.config(text="실행 중...")

        box_width = 20
        spacing = 5
        max_per_row = 15  # 한 행에 최대 15개
        start_x = 10
        start_y = 10

        def draw_boxes(canvas, N, initial_color="#d0d0ff"):
            boxes = []
            for i in range(N):
                row = i // max_per_row
                col = i % max_per_row
                x0 = start_x + col * (box_width + spacing)
                y0 = start_y + row * (box_width + spacing)
                x1 = x0 + box_width
                y1 = y0 + box_width
                rect = canvas.create_rectangle(x0, y0, x1, y1, fill=initial_color, outline="black")
                canvas.create_text(x0 + box_width / 2, y0 + box_width / 2, text=str(i), font=("Arial", 8))
                boxes.append(rect)
            return boxes

        # 고전적 검색
        classical_boxes = draw_boxes(self.classical_canvas_main, N, initial_color="lightgray")
        classical_count = 0
        for i in range(N):
            self.classical_canvas_main.itemconfig(classical_boxes[i], fill="yellow")
            self.classical_canvas_main.update()
            time.sleep(0.05)
            classical_count += 1
            if i == M:
                self.classical_canvas_main.itemconfig(classical_boxes[i], fill="green")
                self.classical_canvas_main.update()
                break
            else:
                self.classical_canvas_main.itemconfig(classical_boxes[i], fill="pink")

        # 양자적 검색
        quantum_boxes = draw_boxes(self.quantum_canvas_main, N, initial_color="#d0d0ff")
        self.quantum_canvas_main.update()
        time.sleep(0.5)

        # 오라클 마킹
        self.quantum_canvas_main.itemconfig(quantum_boxes[M], fill="red")
        self.quantum_canvas_main.update()
        time.sleep(0.5)

        # 증폭 단계 (단순 색상 변환)
        for step in range(3):
            for i in range(N):
                if i == M:
                    colors = ["#ff8080", "#ffb080", "#80ff80"]
                    self.quantum_canvas_main.itemconfig(quantum_boxes[i], fill=colors[step])
                else:
                    shades = ["#c0c0ff", "#a0a0ff", "#90ffa0"]
                    self.quantum_canvas_main.itemconfig(quantum_boxes[i], fill=shades[step])
            self.quantum_canvas_main.update()
            time.sleep(0.5)

        # 측정
        self.quantum_canvas_main.itemconfig(quantum_boxes[M], fill="green")
        for i in range(N):
            if i != M:
                self.quantum_canvas_main.itemconfig(quantum_boxes[i], fill="#e0ffe0")
        self.quantum_canvas_main.update()

        q_steps = math.ceil(math.sqrt(N))
        self.result_label_main.config(text=f"클래식 컴퓨터: {classical_count}회 / 양자 컴퓨터: {q_steps}회\nN이 커질수록 차이가 커집니다!")

        # 추가 재미 요소: 실행 후 랜덤한 양자 잡학/농담 표시
        fun_facts = [
            "양자 중첩 덕분에 한 번에 여러 경로를 탐색할 수도 있지!",
            "얽힘 상태의 큐비트는 떨어져 있어도 서로를 알 수 있대!",
            "쇼어 알고리즘: 큰 수의 인수분해를 훨씬 빠르게!",
            "양자 난수는 진짜 난수가 될 수도 있어!"
        ]
        fact = random.choice(fun_facts)
        self.result_label_main.config(text=self.result_label_main.cget("text") + "\n" + fact)

    def setup_graph_tab(self):
        # 한 줄 소개 레이블 추가
        intro_label = tk.Label(self.graph_frame, text="연산 복잡도 시각화 및 비교", font=("Arial", 12, "bold"))
        intro_label.pack(pady=10)

        # 상단 프레임
        top_frame = tk.Frame(self.graph_frame)
        top_frame.pack(pady=10)

        # N 입력
        tk.Label(top_frame, text="직접입력 \n(스크롤을 이용할 경우 빈칸으로 남겨주세요):").pack(side=tk.LEFT, padx=5)
        self.entry_N_graph = tk.Entry(top_frame, width=10)
        self.entry_N_graph.pack(side=tk.LEFT, padx=5)
        btn_frame_N_graph = tk.Frame(top_frame)
        btn_frame_N_graph.pack(side=tk.LEFT, padx=5)
        for val in [16, 32, 64]:
            btn = tk.Button(btn_frame_N_graph, text=str(val), width=5,
                            command=lambda v=val, entry=self.entry_N_graph: self.set_N(entry, v))
            btn.pack(side=tk.LEFT, padx=2)

        # 실행 버튼
        self.run_button_graph = tk.Button(top_frame, text="실행", command=self.update_graph_with_entry)
        self.run_button_graph.pack(side=tk.LEFT, padx=5)

        # 슬라이더
        self.N_slider_graph = tk.Scale(self.graph_frame, from_=1, to=200, orient="horizontal", command=self.update_graph)
        self.N_slider_graph.set(50)
        self.N_slider_graph.pack(pady=10)

        # 그래프 정보 레이블
        self.info_label_graph = tk.Label(self.graph_frame, text="", font=("Arial", 12))
        self.info_label_graph.pack(pady=5)

        # Matplotlib Figure
        self.fig_graph = Figure(figsize=(6,4), dpi=100)
        self.ax_graph = self.fig_graph.add_subplot(111)
        self.canvas_mpl_graph = FigureCanvasTkAgg(self.fig_graph, master=self.graph_frame)
        self.canvas_mpl_graph.get_tk_widget().pack()

        self.update_graph(None)

    def update_graph_with_entry(self):
        # N 입력값을 슬라이더에 반영하고 그래프 업데이트
        try:
            N = int(self.entry_N_graph.get())
            if N < 1 or N > 200:
                raise ValueError
            self.N_slider_graph.set(N)
            self.update_graph(N)
        except ValueError:
            messagebox.showerror("입력 오류", "N을 1에서 200 사이의 정수로 입력해주세요.")

    def update_graph(self, event):
        if isinstance(event, int):
            N = event
        else:
            try:
                N = int(self.entry_N_graph.get())
                if N < 1 or N > 200:
                    raise ValueError
            except ValueError:
                N = self.N_slider_graph.get()

        classical = [i for i in range(1, N+1)]  # O(N)
        quantum = [math.sqrt(i) for i in range(1, N+1)]  # O(√N)

        self.ax_graph.clear()
        # O(N) Scatter Plot (Red)
        self.ax_graph.scatter(range(1, N+1), classical, c='red', label="Classical: O(N)", s=10)
        # O(√N) Scatter Plot (Blue)
        self.ax_graph.scatter(range(1, N+1), quantum, c='blue', label="Quantum: O(√N)", s=10)

        # Set Y-axis range from 0 to N*1.1 for clarity
        self.ax_graph.set_xlim(0, N+10)
        self.ax_graph.set_ylim(0, N*1.1)
        self.ax_graph.set_xlabel("Data Size N")  # X축 레이블 수정
        self.ax_graph.set_ylabel("Computational Steps (Conceptual)")  # Y축 레이블 수정
        self.ax_graph.set_title("Complexity Comparison: Classical vs Quantum")  # 제목 수정
        self.ax_graph.legend()

        self.info_label_graph.config(text=f"N={N}, 클래식 컴퓨터: {N} steps, 양자컴퓨터: {int(math.sqrt(N))} steps (Conceptual)")
        self.canvas_mpl_graph.draw()

    def setup_parallel_tab(self):
        # 한 줄 소개 레이블 추가
        intro_label = tk.Label(self.parallel_frame, text="고전적 검색과 병렬적 검색 알고리즘 비교", font=("Arial", 12, "bold"))
        intro_label.pack(pady=10)
        

        # 입력 프레임
        input_frame = tk.Frame(self.parallel_frame)
        input_frame.pack(padx=10, pady=10)

        # N 입력
        tk.Label(input_frame, text="데이터 크기(N) 직접입력:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_parallel_N = tk.Entry(input_frame)
        self.entry_parallel_N.grid(row=0, column=1, padx=5, pady=5)

        # 예시 버튼 프레임
        btn_frame_parallel_N = tk.Frame(input_frame)
        btn_frame_parallel_N.grid(row=0, column=2, padx=5, pady=5)
        for val in [16, 32, 64]:
            btn = tk.Button(btn_frame_parallel_N, text=str(val), width=5,
                            command=lambda v=val, entry=self.entry_parallel_N: self.set_N(entry, v))
            btn.pack(side=tk.LEFT, padx=2)

        # M 입력
        tk.Label(input_frame, text="찾아낼 값(M)").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_parallel_M = tk.Entry(input_frame)
        self.entry_parallel_M.grid(row=1, column=1, padx=5, pady=5)

        # 실행 버튼
        self.run_parallel_button = tk.Button(input_frame, text="실행", command=self.run_parallel_search)
        self.run_parallel_button.grid(row=2, column=0, columnspan=3, pady=10)

        # 결과 레이블
        self.parallel_result_label = tk.Label(self.parallel_frame, text="결과 대기중...", font=("Arial", 10))
        self.parallel_result_label.pack(pady=5)

        # 검색 패널
        self.parallel_panel = tk.Frame(self.parallel_frame)
        self.parallel_panel.pack(padx=10, pady=10)

        # 고전적 검색 프레임
        self.parallel_classical_frame = tk.Frame(self.parallel_panel, bd=2, relief=tk.SUNKEN)
        self.parallel_classical_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(self.parallel_classical_frame, text="고전적 검색").pack(pady=5)
        self.parallel_classical_canvas = tk.Canvas(self.parallel_classical_frame, width=400, height=300, bg="white")
        self.parallel_classical_canvas.pack()

        # 병렬 검색 프레임
        self.parallel_quantum_frame = tk.Frame(self.parallel_panel, bd=2, relief=tk.SUNKEN)
        self.parallel_quantum_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(self.parallel_quantum_frame, text="병렬 검색").pack(pady=5)
        self.parallel_quantum_canvas = tk.Canvas(self.parallel_quantum_frame, width=400, height=300, bg="white")
        self.parallel_quantum_canvas.pack()

    def run_parallel_search(self):
        # 입력값 파싱
        try:
            N = int(self.entry_parallel_N.get())
            M = int(self.entry_parallel_M.get())
        except ValueError:
            self.parallel_result_label.config(text="N과 M을 정수로 입력해주세요.")
            return

        if M < 0 or M >= N:
            self.parallel_result_label.config(text="0 <= M < N 범위로 입력해주세요.")
            return

        # 기존 캔버스 초기화
        self.parallel_classical_canvas.delete("all")
        self.parallel_quantum_canvas.delete("all")
        self.parallel_result_label.config(text="실행 중...")

        box_width = 20
        spacing = 5
        max_per_row = 15  # 한 행에 최대 15개
        start_x = 10
        start_y = 10

        def draw_boxes(canvas, N, initial_color="#d0d0ff"):
            boxes = []
            for i in range(N):
                row = i // max_per_row
                col = i % max_per_row
                x0 = start_x + col * (box_width + spacing)
                y0 = start_y + row * (box_width + spacing)
                x1 = x0 + box_width
                y1 = y0 + box_width
                rect = canvas.create_rectangle(x0, y0, x1, y1, fill=initial_color, outline="black")
                canvas.create_text(x0 + box_width / 2, y0 + box_width / 2, text=str(i), font=("Arial", 8))
                boxes.append(rect)
            return boxes

        # 고전적 검색
        classical_boxes = draw_boxes(self.parallel_classical_canvas, N, initial_color="lightgray")
        classical_count = 0
        for i in range(N):
            self.parallel_classical_canvas.itemconfig(classical_boxes[i], fill="yellow")
            self.parallel_classical_canvas.update()
            time.sleep(0.05)
            classical_count += 1
            if i == M:
                self.parallel_classical_canvas.itemconfig(classical_boxes[i], fill="green")
                self.parallel_classical_canvas.update()
                break
            else:
                self.parallel_classical_canvas.itemconfig(classical_boxes[i], fill="pink")

        # 병렬 검색
        quantum_boxes = draw_boxes(self.parallel_quantum_canvas, N, initial_color="#d0d0ff")
        self.parallel_quantum_canvas.update()
        time.sleep(0.5)

        # 병렬적으로 여러 박스를 동시에 검사하는 애니메이션
        steps = math.ceil(math.sqrt(N))
        found = False
        q_steps = 0
        for step in range(steps):
            q_steps += 1
            # 랜덤하게 k개의 박스를 선택 (k = steps)
            k = min(steps, N)
            indices = random.sample(range(N), k)
            for i in indices:
                if i == M:
                    self.parallel_quantum_canvas.itemconfig(quantum_boxes[i], fill="green")
                    found = True
                else:
                    self.parallel_quantum_canvas.itemconfig(quantum_boxes[i], fill="yellow")
            self.parallel_quantum_canvas.update()
            time.sleep(0.5)
            # 선택한 박스 다시 원래 색으로
            for i in indices:
                if i != M:
                    self.parallel_quantum_canvas.itemconfig(quantum_boxes[i], fill="#d0d0ff")
            if found:
                break

        self.parallel_result_label.config(text=f"고전적: {classical_count}회 / 병렬적: {q_steps}회\n병렬적 검색은 동시에 여러 시도를 함으로써 빠르게 결과를 얻습니다!")

    def setup_probability_tab(self):
        # 한 줄 소개 레이블 추가
        intro_label = tk.Label(self.probability_frame, text="고전적 검색과 양자적 검색의 확률 분포 비교", font=("Arial", 12, "bold"))
        intro_label.pack(pady=10)

        # 입력 프레임
        input_frame = tk.Frame(self.probability_frame)
        input_frame.pack(padx=10, pady=10)

        # N 입력
        tk.Label(input_frame, text="데이터 크기(N) 직접입력:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_prob_N = tk.Entry(input_frame)
        self.entry_prob_N.grid(row=0, column=1, padx=5, pady=5)

        # 예시 버튼 프레임
        btn_frame_prob_N = tk.Frame(input_frame)
        btn_frame_prob_N.grid(row=0, column=2, padx=5, pady=5)
        for val in [16, 32, 64]:
            btn = tk.Button(btn_frame_prob_N, text=str(val), width=5,
                            command=lambda v=val, entry=self.entry_prob_N: self.set_N(entry, v))
            btn.pack(side=tk.LEFT, padx=2)

        # M 입력
        tk.Label(input_frame, text="찾아낼 값(M)").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_prob_M = tk.Entry(input_frame)
        self.entry_prob_M.grid(row=1, column=1, padx=5, pady=5)

        # 실행 버튼
        self.run_prob_button = tk.Button(input_frame, text="실행", command=self.run_probability_simulation)
        self.run_prob_button.grid(row=2, column=0, columnspan=3, pady=10)

        # 결과 레이블
        self.prob_result_label = tk.Label(self.probability_frame, text="결과 대기중...", font=("Arial", 10))
        self.prob_result_label.pack(pady=5)

        # 확률 분포 패널
        self.prob_panel = tk.Frame(self.probability_frame)
        self.prob_panel.pack(padx=10, pady=10)

        # 고전적 검색 확률 분포 프레임
        self.classical_prob_frame = tk.Frame(self.prob_panel, bd=2, relief=tk.SUNKEN)
        self.classical_prob_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(self.classical_prob_frame, text="고전적 검색 확률 분포").pack(pady=5)
        self.classical_prob_canvas = tk.Canvas(self.classical_prob_frame, width=400, height=300, bg="white")
        self.classical_prob_canvas.pack()

        # 양자적 검색 확률 분포 프레임
        self.quantum_prob_frame = tk.Frame(self.prob_panel, bd=2, relief=tk.SUNKEN)
        self.quantum_prob_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(self.quantum_prob_frame, text="양자적 검색 확률 분포").pack(pady=5)
        self.quantum_prob_canvas = tk.Canvas(self.quantum_prob_frame, width=400, height=300, bg="white")
        self.quantum_prob_canvas.pack()

    def run_probability_simulation(self):
        # 입력값 파싱
        try:
            N = int(self.entry_prob_N.get())
            M = int(self.entry_prob_M.get())
        except ValueError:
            self.prob_result_label.config(text="N과 M을 정수로 입력해주세요.")
            return

        if M < 0 or M >= N:
            self.prob_result_label.config(text="0 <= M < N 범위로 입력해주세요.")
            return

        # 기존 캔버스 초기화
        self.classical_prob_canvas.delete("all")
        self.quantum_prob_canvas.delete("all")
        self.prob_result_label.config(text="실행 중...")

        box_width = 20
        spacing = 5
        max_per_row = 15  # 한 행에 최대 15개
        start_x = 10
        start_y = 10

        def draw_prob_distribution(canvas, N, M, is_classical=True):
            for i in range(N):
                row = i // max_per_row
                col = i % max_per_row
                x0 = start_x + col * (box_width + spacing)
                y0 = start_y + row * (box_width + spacing)
                x1 = x0 + box_width
                y1 = y0 + box_width

                if is_classical:
                    # 고전적 검색: 모든 박스 확률 동일
                    prob = 1 / N
                    color_intensity = int(255 * prob)
                    color = f"#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}"
                else:
                    # 양자적 검색: 목표 박스 확률 높음
                    if i == M:
                        prob = 0.5  # 예시: 50% 확률
                        color = "#80ff80"  # 초록색
                    else:
                        prob = (1 - 0.5) / (N - 1)  # 나머지 분포
                        color_intensity = int(255 * prob)
                        color = f"#{color_intensity:02x}{color_intensity:02x}{color_intensity:02x}"

                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
                canvas.create_text(x0 + box_width / 2, y0 + box_width / 2, text=f"{prob:.2f}", font=("Arial", 8))

        # 고전적 확률 분포
        draw_prob_distribution(self.classical_prob_canvas, N, M, is_classical=True)
        self.classical_prob_canvas.update()

        # 양자적 확률 분포
        draw_prob_distribution(self.quantum_prob_canvas, N, M, is_classical=False)
        self.quantum_prob_canvas.update()

        self.prob_result_label.config(text=f"N={N}, M={M}\n고전적 검색: 모든 항목이 동일 확률\n양자적 검색: 목표 항목 확률 증가")

    def setup_info_tab(self):
        # 한 줄 소개 레이블 추가
        intro_label = tk.Label(self.info_frame, text="추가 정보 및 재미 요소", font=("Arial", 12, "bold"))
        intro_label.pack(pady=10)

        # 정보 텍스트
        info_text = (
            "양자컴퓨터, 이제는 알아야 합니다:\n\n"
            "- 암호 해독 (쇼어 알고리즘)\n"
            "- 최적화 문제 (금융 포트폴리오 최적화, 물류 최적화)\n"
            "- 양자 머신러닝\n"
            
        )
        tk.Label(self.info_frame, text="추가 정보", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(self.info_frame, text=info_text, justify="left").pack(pady=5, padx=10)
        tk.Label(self.info_frame, text="🔍🔮💻", font=("Arial", 24)).pack(pady=10)

        # 추가 재미 요소 1: Quantum Joke 버튼
        joke_button = tk.Button(self.info_frame, text="양자 농담", command=self.show_quantum_joke)
        joke_button.pack(pady=5)

        # 추가 재미 요소 2: Schrodinger's Cat 버튼
        cat_button = tk.Button(self.info_frame, text="슈뢰딩거의 고양이", command=self.show_cat)
        cat_button.pack(pady=5)

        # 추가 재미 요소 3: Schrodinger's Cat 버튼
        me_button = tk.Button(self.info_frame, text="만든 이", command=self.show_me)
        me_button.pack(pady=5)

    def show_quantum_joke(self):
        jokes = [
            "양자 역학에서 고양이가 상자 안에 있을 때, '있으면서 없을 수도 있다'고 생각하면...\n그냥 열어서 확인하면 되잖아!",
            "양자 회의록: 오늘도 불확실성 때문에 결론 못 냈다.",
            "양자 엔지니어: '이 문제를 해결했어요!'\n동료: '정말요?'\n양자 엔지니어: '음, 측정하기 전까진 확신할 수 없네요.'",
            "양자개그: 듣는 순간 이미 잊혀졌을 수도 있어!"
        ]
        messagebox.showinfo("양자 농담", random.choice(jokes))

    def show_cat(self):
        if hasattr(self, 'cat_label') and self.cat_label is not None:
            self.cat_label.destroy()
            self.cat_label = None
            return  # Toggle off

        # 슈뢰딩거의 고양이 ASCII 아트
        cat_art = (
            "   /\\___/\\\n"
            "  (  o o  )\n"
            "  /   *   \\\n"
            "  \\__\\_/__/  ~ 이 고양이는 살아있으면서\n"
            "    /   \\     죽어있을지도 몰라!\n"
            "   / ___ \\ \n"
            "   \\/___\\/ "
        )
        self.cat_label = tk.Label(self.info_frame, text=cat_art, font=("Courier",10))
        self.cat_label.pack(pady=10)

    def show_me(self):
        me = [
            
            "2024.12.23 정채호준 제작.\n소감: 양자컴퓨터는 너무 어려울 줄 알았는데 역시 어렵고 멋진 것"
        ]
        messagebox.showinfo("만든 이의 말", random.choice(me))

    def setup_gate_simulator_tab(self):
        # 게이트 시뮬레이터 탭에 실행 버튼 추가
        run_button = tk.Button(self.gate_simulator_frame, text="게이트 시뮬레이터 실행", command=self.launch_gate_simulator)
        run_button.pack(pady=20)

        # 안내 레이블 추가
        info_label = tk.Label(self.gate_simulator_frame, text="아래 버튼을 눌러 양자 게이트 시뮬레이터를 실행하세요.", font=("Arial", 12))
        info_label.pack(pady=10)

    def launch_gate_simulator(self):
        # 새로운 창 생성
        simulator_window = tk.Toplevel(self.root)
        simulator = GateSimulator(simulator_window)


# 메인 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
