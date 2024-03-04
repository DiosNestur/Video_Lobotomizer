from moviepy.editor import VideoFileClip, clips_array, vfx
import os
import random

def list_video_files(directory):
    """Devuelve una lista con los nombres de archivo de todos los vídeos en el directorio."""
    video_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.mp4', '.mov', '.avi'))]
    return video_files

def combine_videos(video1_path, video2_path, output_dir):
    """Combina dos vídeos en uno solo en formato vertical y lo guarda con el nombre del primer vídeo más '_lobotomized'."""
    clip1 = VideoFileClip(video1_path).resize(height=1920)
    clip2 = VideoFileClip(video2_path).resize(height=1920)
    
    min_duration = min(clip1.duration, clip2.duration)
    clip1 = clip1.subclip(0, min_duration)
    clip2 = clip2.subclip(0, min_duration)
    
    final_clip = clips_array([[clip1, clip2]]).resize(width=1080)
    
    # Extraer el nombre del archivo sin la ruta y sin la extensión
    original_video_name = os.path.splitext(os.path.basename(video1_path))[0]
    output_path = os.path.join(output_dir, f"{original_video_name}_lobotomized.mp4")
    final_clip.write_videofile(output_path, codec='libx264', fps=30)
    print(f"Vídeo combinado guardado como {output_path}")

def process_folders(original_dir, lobotomy_dir, output_dir):
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    original_videos = list_video_files(original_dir)
    lobotomy_videos = list_video_files(lobotomy_dir)
    random.shuffle(lobotomy_videos)  # Mezclar para asegurar selección aleatoria si es necesario

    for idx, original_video in enumerate(original_videos, start=1):
        if idx <= len(lobotomy_videos):
            lobotomy_video = lobotomy_videos[idx - 1]
        else:
            lobotomy_video = random.choice(lobotomy_videos)
        
        combine_videos(original_video, lobotomy_video, output_dir)

if __name__ == "__main__":
    original_dir = "original_videos"
    lobotomy_dir = "lobotomy_videos"
    output_dir = "lobotomized_videos"
    process_folders(original_dir, lobotomy_dir, output_dir)
