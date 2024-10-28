import os, json
from color import Color
import threading
import time

VM_DATA_FILE = 'vm_data.json'

def load_vm_data():
    if not os.path.exists(VM_DATA_FILE):
        return {}
    with open(VM_DATA_FILE, 'r') as file:
        return json.load(file)
    
def save_vm_data(data):
    with open(VM_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Функция просмотра ВМ
def display_vm_data():
    data = load_vm_data()
    if not data:
        print('Нет данных о ВМ.')
        return
    for unique_id, details in data.items():
        print(f'ID: {unique_id}, Количество ВМ: {details['count']}, '
              f'Директория: {details['directory']}, '
              f'Дополнительная информация: {details['additional_info']}\n')

# Функция добавления информации о ВМ  
def add_vm_data(unique_id, vm_count, directory_path, additional_info=None):
    data = load_vm_data()
    data[unique_id] = {
        'count': vm_count,
        'directory': directory_path,
        'additional_info': additional_info if additional_info else {}
    }
    save_vm_data(data)
    
# Функция удаления информации о ВМ  
def remove_vm_data(unique_id):
    data = load_vm_data()
    if unique_id in data:
        del data[unique_id]
        save_vm_data(data)
        print(f'Информация о ВМ с ID {unique_id} удалена.')
    else:
        print(f'Информация о ВМ с ID {unique_id} не найдена.')

# Функция удаление директории https://stackoverflow.com/questions/10989005/do-i-understand-os-walk-right
def remove_directory(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(dir_path)

# Функция для анимации загрузки
def loading_animation(stop_event):
    spinner = ['-', '\\', '|', '/']
    while not stop_event.is_set():
        for symbol in spinner:
            print(f'\r{symbol} Выполняется... ', end='', flush=True)
            time.sleep(0.1)