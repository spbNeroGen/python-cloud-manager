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
        ip_addresses = resource_info.get("ip_addresses", [])         # Вывод IP-адресов
        ip_list = ', '.join(ip_addresses)
        print(f'            {Color.BLUE}IP-адреса: {ip_list}' + Color.END)
        print(f'            {Color.BLUE}CPU: {resource_info.get("cpu", "N/A")} vCPU' + Color.END)
        print(f'            {Color.BLUE}RAM: {resource_info.get("ram", "N/A")} ГБ' + Color.END)
        print(f'            {Color.BLUE}CPU фракция: {resource_info.get("cpu_fraction", "N/A")}% ' + Color.END)
        print(f'            {Color.BLUE}Размер диска: {resource_info.get("disk_size", "N/A")} ГБ' + Color.END)

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

####################### Функция для создания ВМ на основе ролей #################
def create_vm_roles():
    # Выбор роли
    roles = {
        "1": ("Web Server", [(2, 4, 50), (4, 8, 100)]),
        "2": ("Jenkins Master", [(4, 8, 50), (8, 16, 100)]),
        "3": ("Database Server", [(4, 8, 100), (8, 16, 200)]),
    }
    
    print("\nВыберите роль для новой ВМ:")
    for key, (role_name, _) in roles.items():
        print(f"{key}. {role_name}")

    role_choice = input("Введите номер роли: ")
    if role_choice not in roles:
        print("Некорректный выбор роли. Попробуйте снова.")
        return

    # Выбор характеристик для выбранной роли
    role_name, configurations = roles[role_choice]
    print(f"\nВы выбрали роль: {role_name}. Выберите конфигурацию:")
    for index, (cpu, ram, disk) in enumerate(configurations, start=1):
        print(f"{index}. CPU: {cpu} cores, RAM: {ram} GB, Disk: {disk} GB")

    config_choice = input("Введите номер конфигурации: ")
    try:
        selected_config = configurations[int(config_choice) - 1]
    except (IndexError, ValueError):
        print("Некорректный выбор конфигурации. Попробуйте снова.")
        return

    cpu, ram, disk = selected_config
    print(f"\nСоздание ВМ с параметрами - Роль: {role_name}, CPU: {cpu}, RAM: {ram}, Disk: {disk} GB")
    
    # логика для запуска процесса создания ВМ с выбранными параметрами
    create_vm_with_role(role_name, cpu, ram, disk)

def create_vm_with_role(role, cpu, ram, disk):
    # Логика создания ВМ с заданными характеристиками
    ip_address = "192.168.1.11" 
    update_inventory(role, ip_address)
    print(f"Создание ВМ с ролью '{role}' и характеристиками: CPU={cpu}, RAM={ram}GB, Disk={disk}GB")
    # потом сюда вызов Ansible playbook


####################### тестово for ansible ################################
def update_inventory(role, ip_address):
    pass