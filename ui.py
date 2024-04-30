import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from analyze import analyze_ballistic
class BallisticAnalysisApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ballistic Analysis")

        # 选择图片文件按钮
        self.select_image_button = tk.Button(master, text="选择图片文件", command=self.select_image)
        self.select_image_button.pack()

        # 画布
        self.canvas = tk.Canvas(master, width=2121//2, height=1500//2)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.img = None
        self.img_path = None
        self.points = []

        # 执行分析按钮
        self.analyze_button = tk.Button(master, text="执行分析并保存结果", command=self.analyze)
        self.analyze_button.pack()

        # 分析结果显示
        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def select_image(self):
        print("Select image button clicked")
        self.img_path = filedialog.askopenfilename()

        print("Selected image path:", self.img_path)
        if self.img_path:
            self.points.clear()
            self.img = cv2.imread(self.img_path)
            self.img = cv2.resize(self.img, (2121//2, 1500//2))
            self.display_image()

    def display_image(self):
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas.image = img_tk

    def on_canvas_click(self, event):
        if self.img is not None:
            x, y = event.x, event.y
            self.points.append((x-2, y-2))
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red", outline="")
    def save_result(self, result):
        if self.img is None:
            return
        # 在这里执行分析，将分析结果显示在result_label上
        # 然后将结果显示在result_label上
        # 显示所有点的平均值
        score, distance, hit_small, hit_large, hit_dart, min_radius, self.img = result
        # 获取img的路径
        img_path = self.img_path
        # 将结果存储在同级目录下的同名字的.txt中
        # 获取文件名
        file_name = img_path.split('/')[-1].split('.')[0]
        # 获取文件路径
        file_path = img_path.split('/')[:-1]
        file_path = '/'.join(file_path)
        # 将结果写入文件
        print(f'save to:{file_path}/{file_name}.txt')
        with open(f'{file_path}/{file_name}.txt', 'w') as f:
            f.write(f"{self.points}\nScore: {score}\nDistance: {distance}\nHit Small: {hit_small}\nHit Large: {hit_large}\nHit Dart: {hit_dart}\nMin Radius: {min_radius}")
        # 保存图片
        cv2.imwrite(f'{file_path}/{file_name}_result.jpg', self.img)

    def analyze(self):
        if self.img is None:
            return
        # 在这里执行分析，将分析结果显示在result_label上
        # 然后将结果显示在result_label上
        # 显示所有点的平均值
        score, distance, hit_small, hit_large, hit_dart, min_radius, self.img = analyze_ballistic(self.points, self.img)

        self.result_label['text'] = f"Score: {score}\nDistance: {distance}\nHit Small: {hit_small}\nHit Large: {hit_large}\nHit Dart: {hit_dart}\nMin Radius: {min_radius}"
        self.display_image()
        self.save_result((score, distance, hit_small, hit_large, hit_dart, min_radius, self.img))

def main():
    root = tk.Tk()
    app = BallisticAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
