import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, colorchooser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Chart Generator")
        self.master.style = ttk.Style()
        self.master.style.theme_use("clam")

        # Configure the colors of the UI
        self.master.style.configure('.', background='#C3DFE0')
        self.master.style.configure('TLabel', background='#C3DFE0', foreground='#405A53', font=('Arial', 12))
        self.master.style.configure('TEntry', fieldbackground='#FFFFFF', foreground='#405A53', font=('Arial', 12))
        self.master.style.configure('TButton', background='#405A53', foreground='#C3DFE0', font=('Arial', 12))

        ttk.Label(master, text="Chart Type:", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)
        self.chart_type = ttk.Combobox(master, values=["Bar Chart", "Pie Chart", "Line Chart"], font=('Arial', 12))
        self.chart_type.grid(row=0, column=1, padx=10, pady=10)
        self.chart_type.current(0)
        self.chart_type.bind("<<ComboboxSelected>>", self.change_chart_type)

        ttk.Label(master, text="Number of bars/slices/lines:", font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)
        self.entry_num = ttk.Entry(master, font=('Arial', 12))
        self.entry_num.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(master, text="X Label:", font=('Arial', 14)).grid(row=2, column=0, padx=10, pady=10)
        self.entry_x = ttk.Entry(master, font=('Arial', 12))
        self.entry_x.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(master, text="Y Label:", font=('Arial', 14)).grid(row=3, column=0, padx=10, pady=10)
        self.entry_y = ttk.Entry(master, font=('Arial', 12))
        self.entry_y.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(master, text="Title:", font=('Arial', 14)).grid(row=4, column=0, padx=10, pady=10)
        self.entry_title = ttk.Entry(master, font=('Arial', 12))
        self.entry_title.grid(row=4, column=1, padx=10, pady=10)

        self.button = ttk.Button(master, text="Generate", command=self.generate)
        self.button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.entries_bar = []
        self.entries_value = []
        self.entries_color = []

        # Default colors
        self.default_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    def change_chart_type(self, event):
        chart_type = self.chart_type.get()
        if chart_type == "Bar Chart":
            self.clear_pie_chart_entries()
            self.clear_line_chart_entries()
            self.entry_x.grid(row=2, column=1, padx=10, pady=10)
            self.entry_y.grid(row=3, column=1, padx=10, pady=10)
        elif chart_type == "Pie Chart":
            self.clear_bar_chart_entries()
            self.clear_line_chart_entries()
            self.entry_x.grid_remove()
            self.entry_y.grid_remove()
        elif chart_type == "Line Chart":
            self.clear_bar_chart_entries()
            self.clear_pie_chart_entries()
            self.entry_x.grid(row=2, column=1, padx=10, pady=10)
            self.entry_y.grid(row=3, column=1, padx=10, pady=10)

    def clear_bar_chart_entries(self):
        for entry in self.entries_bar + self.entries_value + self.entries_color:
            entry.destroy()
        self.entries_bar = []
        self.entries_value = []
        self.entries_color = []
        if hasattr(self, 'button_draw'):
            self.button_draw.grid_remove()

    def clear_pie_chart_entries(self):
        for entry in self.entries_bar + self.entries_value:
            entry.destroy()
        self.entries_bar = []
        self.entries_value = []
        if hasattr(self, 'button_draw'):
            self.button_draw.grid_remove()

    def clear_line_chart_entries(self):
        for entry in self.entries_bar + self.entries_value:
            entry.destroy()
        self.entries_bar = []
        self.entries_value = []
        if hasattr(self, 'button_draw'):
            self.button_draw.grid_remove()

    def generate(self):
        chart_type = self.chart_type.get()
        if chart_type == "Bar Chart":
            self.generate_bar_chart()
        elif chart_type == "Pie Chart":
            self.generate_pie_chart()
        elif chart_type == "Line Chart":
            self.generate_line_chart()

    def generate_bar_chart(self):
        self.clear_bar_chart_entries()

        num_bars = int(self.entry_num.get())

        for i in range(num_bars):
            ttk.Label(self.master, text="Bar {} name:".format(i+1), font=('Arial', 14)).grid(row=6+i*3, column=0, padx=10, pady=10)
            entry_bar = ttk.Entry(self.master, font=('Arial', 12))
            entry_bar.grid(row=6+i*3, column=1, padx=10, pady=10)
            self.entries_bar.append(entry_bar)

            ttk.Label(self.master, text="Bar {} value:".format(i+1), font=('Arial', 14)).grid(row=6+i*3+1, column=0, padx=10, pady=10)
            entry_value = ttk.Entry(self.master, font=('Arial', 12))
            entry_value.grid(row=6+i*3+1, column=1, padx=10, pady=10)
            self.entries_value.append(entry_value)

            color_frame = ttk.Frame(self.master)
            color_frame.grid(row=6+i*3+2, column=0, padx=10, pady=10)
            ttk.Label(color_frame, text="Bar {} color:".format(i+1), font=('Arial', 14)).pack(side=tk.LEFT)
            color_box = ttk.Label(color_frame, width=10, relief=tk.SOLID)
            color_box.pack(side=tk.LEFT)
            color_box.bind("<Button-1>", lambda event, i=i: self.choose_color(i))
            self.entries_color.append(color_box)

            # Assign default color
            if i < len(self.default_colors):
                color_box.configure(background=self.default_colors[i])

        self.button_draw = ttk.Button(self.master, text="Draw", command=self.draw_bar_chart)
        self.button_draw.grid(row=6+3*num_bars, column=0, columnspan=2, padx=10, pady=10)

    def generate_pie_chart(self):
        self.clear_pie_chart_entries()

        num_slices = int(self.entry_num.get())

        for i in range(num_slices):
            ttk.Label(self.master, text="Slice {} name:".format(i+1), font=('Arial', 14)).grid(row=6+i*2, column=0, padx=10, pady=10)
            entry_slice = ttk.Entry(self.master, font=('Arial', 12))
            entry_slice.grid(row=6+i*2, column=1, padx=10, pady=10)
            self.entries_bar.append(entry_slice)

            ttk.Label(self.master, text="Slice {} value:".format(i+1), font=('Arial', 14)).grid(row=6+i*2+1, column=0, padx=10, pady=10)
            entry_value = ttk.Entry(self.master, font=('Arial', 12))
            entry_value.grid(row=6+i*2+1, column=1, padx=10, pady=10)
            self.entries_value.append(entry_value)

        self.button_draw = ttk.Button(self.master, text="Draw", command=self.draw_pie_chart)
        self.button_draw.grid(row=6+2*num_slices, column=0, columnspan=2, padx=10, pady=10)

    def generate_line_chart(self):
        self.clear_line_chart_entries()

        num_lines = int(self.entry_num.get())

        for i in range(num_lines):
            ttk.Label(self.master, text="Line {} name:".format(i+1), font=('Arial', 14)).grid(row=6+i*2, column=0, padx=10, pady=10)
            entry_line = ttk.Entry(self.master, font=('Arial', 12))
            entry_line.grid(row=6+i*2, column=1, padx=10, pady=10)
            self.entries_bar.append(entry_line)

            ttk.Label(self.master, text="Line {} values (comma-separated):".format(i+1), font=('Arial', 14)).grid(row=6+i*2+1, column=0, padx=10, pady=10)
            entry_values = ttk.Entry(self.master, font=('Arial', 12))
            entry_values.grid(row=6+i*2+1, column=1, padx=10, pady=10)
            self.entries_value.append(entry_values)

        self.button_draw = ttk.Button(self.master, text="Draw", command=self.draw_line_chart)
        self.button_draw.grid(row=6+2*num_lines, column=0, columnspan=2, padx=10, pady=10)

    def choose_color(self, i):
        color_code = colorchooser.askcolor(title="Choose color")
        self.entries_color[i].configure(background=color_code[1])

    def draw_bar_chart(self):
        bars = [entry.get() for entry in self.entries_bar]
        values = [float(entry.get()) for entry in self.entries_value]
        colors = [str(self.entries_color[i].cget('background')) for i in range(len(self.entries_color))]
        x_label = self.entry_x.get()
        y_label = self.entry_y.get()
        title = self.entry_title.get()

        self.display_bar_chart(bars, values, colors, x_label, y_label, title)

    def draw_pie_chart(self):
        slices = [entry.get() for entry in self.entries_bar]
        values = [float(entry.get()) for entry in self.entries_value]
        colors = self.default_colors[:len(slices)]
        x_label = ""
        y_label = ""
        title = self.entry_title.get()

        self.display_pie_chart(slices, values, colors, x_label, y_label, title)

    def draw_line_chart(self):
        lines = [entry.get() for entry in self.entries_bar]
        values = [list(map(float, entry.get().split(','))) for entry in self.entries_value]
        x_label = self.entry_x.get()
        y_label = self.entry_y.get()
        title = self.entry_title.get()

        self.display_line_chart(lines, values, x_label, y_label, title)

    def display_bar_chart(self, bars, values, colors, x_label, y_label, title):
        sns.set(style="whitegrid")
        fig = plt.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        for bar, value, color in zip(bars, values, colors):
            ax.bar(bar, value, color=color)
        ax.set_xlabel(x_label, fontsize=14)
        ax.set_ylabel(y_label, fontsize=14)
        ax.set_title(title, fontsize=16)
        ax.set_xticks(range(len(bars)))
        ax.set_xticklabels(bars, horizontalalignment='right', fontweight='light')

        # Save the figure with a unique file name
        file_name = 'bar_chart.png'
        if os.path.exists(file_name):
            i = 1
            while os.path.exists(f"bar_chart_{i}.png"):
                i += 1
            file_name = f"bar_chart_{i}.png"
        fig.savefig(file_name)

        # Display the figure in a new window
        new_window = tk.Toplevel(self.master)
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def display_pie_chart(self, slices, values, colors, x_label, y_label, title):
        fig = plt.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.pie(values, labels=slices, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_xlabel(x_label, fontsize=14)
        ax.set_ylabel(y_label, fontsize=14)
        ax.set_title(title, fontsize=16)

        # Save the figure with a unique file name
        file_name = 'pie_chart.png'
        if os.path.exists(file_name):
            i = 1
            while os.path.exists(f"pie_chart_{i}.png"):
                i += 1
            file_name = f"pie_chart_{i}.png"
        fig.savefig(file_name)

        # Display the figure in a new window
        new_window = tk.Toplevel(self.master)
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def display_line_chart(self, lines, values, x_label, y_label, title):
        fig = plt.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        for line, value in zip(lines, values):
            ax.plot(value, label=line)
        ax.set_xlabel(x_label, fontsize=14)
        ax.set_ylabel(y_label, fontsize=14)
        ax.set_title(title, fontsize=16)
        ax.legend()

        # Save the figure with a unique file name
        file_name = 'line_chart.png'
        if os.path.exists(file_name):
            i = 1
            while os.path.exists(f"line_chart_{i}.png"):
                i += 1
            file_name = f"line_chart_{i}.png"
        fig.savefig(file_name)

        # Display the figure in a new window
        new_window = tk.Toplevel(self.master)
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root = tk.Tk()
app = App(root)
root.mainloop()