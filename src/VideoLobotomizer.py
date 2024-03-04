from moviepy.editor import VideoFileClip, CompositeVideoClip
import os
import random

def list_video_files(directory):
    """Devuelve una lista con los nombres de archivo de todos los vídeos en el directorio."""
    video_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.mp4', '.mov', '.avi'))]
    return video_files

def combine_videos(video1_path, video2_path, output_dir):
    """Combina dos vídeos en uno solo en formato vertical."""
    original_clip = VideoFileClip(video1_path)
    lobotomy_clip = VideoFileClip(video2_path)
    
    # Determinar la duración del original_video para adaptar lobotomy_video a esta duración
    original_duration = original_clip.duration

    # Ajustar lobotomy_clip a la duración de original_clip
    if lobotomy_clip.duration < original_duration:
        # Si lobotomy_clip es más corto, se repite hasta alcanzar la duración de original_clip
        lobotomy_clip = lobotomy_clip.loop(duration=original_duration)
    else:
        # Si lobotomy_clip es más largo, se recorta para coincidir con la duración de original_clip
        lobotomy_clip = lobotomy_clip.subclip(0, original_duration)

    # Ajustar ambos clips a la misma altura
    original_clip_resized = original_clip.resize(height=1920)
    lobotomy_clip_resized = lobotomy_clip.resize(height=1920)

    # Calcular la posición y para el segundo clip
    y_pos = original_clip_resized.size[1]  # La altura del primer clip

    # Crear un CompositeVideoClip para apilar verticalmente
    final_clip = CompositeVideoClip([original_clip_resized.set_position(("center", 0)), lobotomy_clip_resized.set_position(("center", y_pos))], size=(original_clip_resized.size[0], original_clip_resized.size[1]*2))

    # Ajustar la duración del clip final para que coincida con la duración de original_clip
    final_clip = final_clip.set_duration(original_duration)

    # Extraer el nombre del archivo sin la ruta y sin la extensión
    original_video_name = os.path.splitext(os.path.basename(video1_path))[0]
    output_path = os.path.join(output_dir, f"{original_video_name}_lobotomized.mp4")
    
    # Escribir el vídeo resultante, utilizando solo el audio de original_clip
    final_clip.write_videofile(output_path, codec='libx264', fps=30, audio=video1_path)
    print(f"Vídeo combinado guardado como {output_path}")

def process_folders(original_dir, lobotomy_dir, output_dir):
    """Procesa los directorios y combina los vídeos."""
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
