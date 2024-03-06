import datetime
import random
import subprocess
import os
import shutil
from moviepy.editor import VideoFileClip, CompositeVideoClip

def generate_random_datetime_within_months(months=4, start_hour=9, end_hour=21):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=months*30)
    random_days = random.randrange((end_date - start_date).days)
    random_date = start_date + datetime.timedelta(days=random_days)
    
    random_hour = random.randint(start_hour, end_hour - 1)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    
    return datetime.datetime.combine(random_date.date(), datetime.time(random_hour, random_minute, random_second))

def remove_all_metadata_and_set_random_dates(file_path, destination_folder):
    random_datetime = generate_random_datetime_within_months()
    formatted_datetime = random_datetime.strftime('%Y:%m:%d %H:%M:%S')
    
    try:
        commands = [
            '-all=',
            '-FileModifyDate=' + formatted_datetime,
            '-FileAccessDate=' + formatted_datetime,
            '-FileCreateDate=' + formatted_datetime,
            '-CreateDate=' + formatted_datetime,
            '-ModifyDate=' + formatted_datetime,
            '-TrackCreateDate=' + formatted_datetime,
            '-TrackModifyDate=' + formatted_datetime,
            '-MediaCreateDate=' + formatted_datetime,
            '-MediaModifyDate=' + formatted_datetime,
            '-overwrite_original'
        ]
        
        subprocess.run(['exiftool', *commands, file_path], check=True, stdout=subprocess.PIPE)
        
        file_name = os.path.basename(file_path)
        new_file_path = os.path.join(destination_folder, file_name)
        shutil.move(file_path, new_file_path)
        print(f"Metadatos borrados y actualizados, archivo movido a {new_file_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error al modificar metadatos: {e}")
    except Exception as e:
        print(f"Error al mover el archivo: {e}")

def list_video_files(directory):
    video_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.mp4', '.mov', '.avi'))]
    return video_files

def combine_videos(video1_path, video2_path, output_dir):
    original_clip = VideoFileClip(video1_path)
    lobotomy_clip = VideoFileClip(video2_path)
    
    original_duration = original_clip.duration

    if lobotomy_clip.duration < original_duration:
        lobotomy_clip = lobotomy_clip.loop(duration=original_duration)
    else:
        lobotomy_clip = lobotomy_clip.subclip(0, original_duration)

    original_clip_resized = original_clip.resize(height=1920)
    lobotomy_clip_resized = lobotomy_clip.resize(height=1920)

    y_pos = original_clip_resized.size[1]

    final_clip = CompositeVideoClip([original_clip_resized.set_position(("center", 0)), lobotomy_clip_resized.set_position(("center", y_pos))], size=(original_clip_resized.size[0], original_clip_resized.size[1]*2))

    final_clip = final_clip.set_duration(original_duration)

    original_video_name = os.path.splitext(os.path.basename(video1_path))[0]
    output_path = os.path.join(output_dir, f"{original_video_name}_lobotomized.mp4")
    
    final_clip.write_videofile(output_path, codec='libx265', fps=30, audio=video1_path)
    print(f"Vídeo combinado guardado como {output_path}")

def process_folders_for_metadata_removal(source_folder, destination_folder):
    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)
        remove_all_metadata_and_set_random_dates(file_path, destination_folder)

def process_folders_for_lobotomy(original_dir, lobotomy_dir, output_dir):
    original_videos = list_video_files(original_dir)
    lobotomy_videos = list_video_files(lobotomy_dir)
    random.shuffle(lobotomy_videos)

    for idx, original_video in enumerate(original_videos, start=1):
        if idx <= len(lobotomy_videos):
            lobotomy_video = lobotomy_videos[idx - 1]
        else:
            lobotomy_video = random.choice(lobotomy_videos)
        
        combine_videos(original_video, lobotomy_video, output_dir)

def main_menu():
    print("1. Borrar metadatos")
    print("2. Lobotomizar videos")
    print("3. Lobotomizar y borrar metadatos")
    choice = input("Seleccione una opción: ")

    if choice == '1':
        source_folder = input("Ingrese la carpeta de origen de los videos para borrar metadatos: ")
        destination_folder = input("Ingrese la carpeta de destino para los videos procesados: ")
        process_folders_for_metadata_removal(source_folder, destination_folder)
    elif choice == '2':
        original_dir = input("Ingrese la carpeta de los videos originales: ")
        lobotomy_dir = input("Ingrese la carpeta de los videos de lobotomía: ")
        output_dir = input("Ingrese la carpeta de destino para los videos lobotomizados: ")
        process_folders_for_lobotomy(original_dir, lobotomy_dir, output_dir)
    elif choice == '3':
        original_dir = input("Ingrese la carpeta de los videos originales: ")
        lobotomy_dir = input("Ingrese la carpeta de los videos de lobotomía: ")
        output_dir = input("Ingrese la carpeta de destino para los videos lobotomizados: ")
        process_folders_for_lobotomy(original_dir, lobotomy_dir, output_dir)
        process_folders_for_metadata_removal(output_dir, output_dir)
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main_menu()
