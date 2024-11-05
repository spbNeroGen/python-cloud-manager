import os, json
from color import Color
from datetime import datetime
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
        print(Color.RED + 'Нет данных о ВМ.' + Color.END)
        return
    for unique_id, details in data.items():
        # Форматируем информацию о каждой ВМ
        additional_info = details.get('additional_info', {})
        resource_info = additional_info.get('resource_info', {})

        print(Color.CYAN + f'ID: {unique_id}' + Color.END)
        print(f'    {Color.GREEN}Количество ВМ: {details.get("count", "N/A")}' + Color.END)
        print(f'    {Color.GREEN}Директория: {details.get("directory", "N/A")}' + Color.END)
        print(f'    Дополнительная информация:')
        print(f'        {Color.PURPLE}Статус: {additional_info.get("status", "N/A")}' + Color.END)
        print(f'        {Color.PURPLE}Дата создания: {additional_info.get("creation_date", "N/A")}' + Color.END)
        print(f'        Информация о ресурсах:')
        print(f'            {Color.BLUE}Количество ВМ: {resource_info.get("vm_count", "N/A")}' + Color.END)
        print(f'            {Color.BLUE}CPU: {resource_info.get("cpu", "N/A")} vCPU' + Color.END)
        print(f'            {Color.BLUE}RAM: {resource_info.get("ram", "N/A")} ГБ' + Color.END)
        print(f'            {Color.BLUE}CPU фракция: {resource_info.get("cpu_fraction", "N/A")}% ' + Color.END)
        print(f'            {Color.BLUE}Размер диска: {resource_info.get("disk_size", "N/A")} ГБ' + Color.END)
        print()

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

# def generate_vm_data_from_tfstate(working_dir):
#     pass
def generate_vm_data_from_tfstate(working_dir):
    # Путь к файлу tfstate
    tfstate_path = os.path.join(working_dir, 'terraform.tfstate')
    vm_data_path = os.path.join(working_dir, 'vm_data2.json')

    # Проверка наличия файла tfstate
    if not os.path.isfile(tfstate_path):
        print(f"Файл {tfstate_path} не найден.")
        return

    try:
        # Чтение данных из tfstate
        with open(tfstate_path, 'r') as tfstate_file:
            tfstate_data = json.load(tfstate_file)
        
        # Извлечение ресурсов ВМ
        resources = tfstate_data.get('resources', [])
        vm_instances = []

        for resource in resources:
            if resource.get('type') == 'yandex_compute_instance':  # Проверка на нужный тип ресурса
                # Обработка каждого экземпляра внутри ресурса
                instances = resource.get('instances', [])
                
                for instance in instances:
                    attributes = instance.get('attributes', {})
                    
                    # Извлечение параметров boot_disk и resources, если они присутствуют
                    boot_disk = attributes.get('boot_disk', [{}])[0]
                    initialize_params = boot_disk.get('initialize_params', [{}])[0] if isinstance(boot_disk, dict) else {}
                    resources_params = attributes.get('resources', [{}])[0] if isinstance(attributes.get('resources'), list) else {}

                    # Заполнение информации о ВМ
                    vm_info = {
                        'id': attributes.get('id', 'N/A'),
                        'name': attributes.get('name', 'N/A'),
                        'zone': attributes.get('zone', 'N/A'),
                        'cpu': resources_params.get('cores', 'N/A'),
                        'ram': resources_params.get('memory', 'N/A'),
                        'disk_size': initialize_params.get('size', 'N/A'),
                        'status': attributes.get('status', 'created'),
                        'creation_date': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    }
                    vm_instances.append(vm_info)

        # Запись информации о ВМ в vm_data2.json
        with open(vm_data_path, 'w') as vm_data_file:
            json.dump(vm_instances, vm_data_file, indent=4)

        print(f"Файл {vm_data_path} успешно создан на основе анализа tfstate.")

    except (json.JSONDecodeError, KeyError, IOError) as e:
        print(f"Ошибка при обработке tfstate: {e}")

