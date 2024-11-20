import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import noisereduce as nr
import librosa
import soundfile as sf
import os

class AudioEnhancerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Audio Noise Reducer")
        self.root.geometry("500x300")
        self.input_file = None
        self.output_file = None

        # Layout
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="AI Audio Noise Reducer", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # File selection
        select_button = tk.Button(self.root, text="Select Audio File", command=self.select_file, width=25)
        select_button.pack(pady=10)

        self.file_label = tk.Label(self.root, text="No file selected.", fg="gray")
        self.file_label.pack(pady=5)

        # Noise reduction slider
        self.noise_reduction_var = tk.DoubleVar(value=0.5)
        slider_label = tk.Label(self.root, text="Noise Reduction Intensity")
        slider_label.pack(pady=5)
        self.noise_reduction_slider = tk.Scale(self.root, from_=0.1, to=1.0, resolution=0.1, orient="horizontal",
                                               variable=self.noise_reduction_var, length=300)
        self.noise_reduction_slider.pack(pady=5)

        # Enhance button
        self.enhance_button = tk.Button(self.root, text="Reduce Noise", command=self.reduce_noise, width=25, state="disabled")
        self.enhance_button.pack(pady=10)

        # Progress bar
        self.progress = Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        self.progress.pack_forget()

        # Play buttons
        self.play_original_button = tk.Button(self.root, text="Play Original Audio", command=self.play_original, width=25, state="disabled")
        self.play_original_button.pack(pady=5)

        self.play_enhanced_button = tk.Button(self.root, text="Play Enhanced Audio", command=self.play_enhanced, width=25, state="disabled")
        self.play_enhanced_button.pack(pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
        if file_path:
            self.input_file = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}", fg="black")
            self.enhance_button.config(state="normal")
            self.play_original_button.config(state="normal")

    def reduce_noise(self):
        if not self.input_file:
            messagebox.showerror("Error", "Please select an audio file first.")
            return

        noise_level = self.noise_reduction_var.get()

        self.progress.pack()
        self.progress["value"] = 0
        self.root.update()

        try:
            # Load audio
            self.progress["value"] = 20
            self.root.update()
            y, sr = librosa.load(self.input_file, sr=None)

            # Assume first 0.5 seconds is noise
            noise_sample = y[:int(0.5 * sr)]

            # Reduce noise
            self.progress["value"] = 50
            self.root.update()
            reduced_audio = nr.reduce_noise(y=y, sr=sr, y_noise=noise_sample, prop_decrease=noise_level)

            # Save enhanced audio
            self.output_file = os.path.splitext(self.input_file)[0] + "_enhanced.wav"
            sf.write(self.output_file, reduced_audio, sr)

            self.progress["value"] = 100
            self.root.update()
            self.progress.pack_forget()

            messagebox.showinfo("Success", f"Enhanced audio saved as: {self.output_file}")
            self.play_enhanced_button.config(state="normal")
        except Exception as e:
            self.progress.pack_forget()
            messagebox.showerror("Error", f"Failed to enhance audio: {e}")

    def play_original(self):
        if self.input_file:
            os.system(f'start {self.input_file}')

    def play_enhanced(self):
        if self.output_file:
            os.system(f'start {self.output_file}')


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioEnhancerApp(root)
    root.mainloop()
