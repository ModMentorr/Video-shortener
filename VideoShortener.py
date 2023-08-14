import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip
from threading import Thread
from ttkthemes import ThemedTk

stop_processing = False

def cut_video(input_path, output_folder, max_duration=60, progress_callback=None, custom_output_name=None):
    global stop_processing
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_clip = VideoFileClip(input_path)
    duration = video_clip.duration
    num_clips = int(duration / max_duration) + (1 if duration % max_duration > 0 else 0)

    for i in range(num_clips):
        if stop_processing:
            break
        
        start_time = i * max_duration
        end_time = min(start_time + max_duration, duration) 
        max_duration = end_time - start_time 
        
        if custom_output_name:
            output_name = f"{custom_output_name}_{i + 1}.mp4"
        else:
            output_name = f"clip_{i + 1}.mp4"
            
        output_path = os.path.join(output_folder, output_name)
        
        subclip = video_clip.subclip(start_time, end_time)
        subclip.write_videofile(output_path, codec="libx264")

        if progress_callback:
            progress_callback((i + 1) / num_clips, i + 1, num_clips)

    if progress_callback:
        progress_callback(1.0, num_clips, num_clips)

def update_progress(progress, current_clip, total_clips):
    progress_bar["value"] = progress * 100
    progress_text = f"Processing {current_clip}/{total_clips} clips"
    status_label.config(text=progress_text)
    app.update_idletasks()

def stop_processing_thread():
    global stop_processing
    stop_processing = True
    status_label.config(text="Processing stopped.")
    progress_bar["value"] = 0

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)

def start_processing():
    global stop_processing
    stop_processing = False

    input_path = input_entry.get()
    output_folder = output_entry.get()
    custom_output_name = output_name_entry.get() 
    

    duration_map = {
        "10 seconds": 10,
        "15 seconds": 15,
        "25 seconds": 25,
        "30 seconds": 30,
        "45 seconds": 45,
        "1 minute": 60,
        "1:30 minutes": 90,
        "2 minutes": 120,
        "2:30 minutes": 150,
        "3 minutes": 180,
        "3:30 minutes": 210
    }
    selected_duration = clip_duration_combobox.get()
    clip_duration = duration_map[selected_duration]

    def processing_thread():
        cut_video(input_path, output_folder, max_duration=clip_duration, progress_callback=update_progress, custom_output_name=custom_output_name)
        if not stop_processing:
            status_label.config(text="Processing complete!")
        else:
            status_label.config(text="Processing stopped.")
        progress_bar["value"] = 0

    processing_thread = Thread(target=processing_thread)
    processing_thread.start()

app = ThemedTk(theme="arc")
app.title("Video Shortener by ")
app.configure(background="#F0F0F0")  


app.style = ttk.Style()
app.style.configure("Custom.TButton", font=("Helvetica", 12), foreground="black", background="#191919")

input_label = tk.Label(app, text="Input Video:")
input_label.pack(pady=10)  

input_entry = tk.Entry(app)
input_entry.pack(pady=5)  

input_button = ttk.Button(app, text="Select Video", command=select_input_file, style="Custom.TButton")
input_button.pack(pady=5)  

output_label = tk.Label(app, text="Output Folder:")
output_label.pack(pady=10)

output_entry = tk.Entry(app)
output_entry.pack(pady=5)

output_button = ttk.Button(app, text="Select Folder", command=select_output_folder, style="Custom.TButton")
output_button.pack(pady=5)


output_name_label = tk.Label(app, text="Custom Output Name:")
output_name_label.pack(pady=10)

output_name_entry = tk.Entry(app)
output_name_entry.pack(pady=5)


clip_duration_label = tk.Label(app, text="Clip Duration:")
clip_duration_label.pack(pady=10)

duration_options = [
    "10 seconds", "15 seconds", "25 seconds", "30 seconds",
    "45 seconds", "1 minute", "1:30 minutes", "2 minutes",
    "2:30 minutes", "3 minutes", "3:30 minutes"
]

clip_duration_combobox = ttk.Combobox(app, values=duration_options)
clip_duration_combobox.pack(pady=5)

process_button = ttk.Button(app, text="Start Processing", command=start_processing, style="Custom.TButton")
process_button.pack(pady=10)

stop_button = ttk.Button(app, text="Stop Processing", command=stop_processing_thread, style="Custom.TButton")
stop_button.pack(pady=5)

app.style.configure("Custom.Horizontal.TProgressbar", background="#007ACC", troughcolor="#ddd")

status_label = tk.Label(app, text="")
status_label.pack()

progress_bar = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate", style="Custom.Horizontal.TProgressbar")
progress_bar.pack(pady=20)

app.mainloop()
