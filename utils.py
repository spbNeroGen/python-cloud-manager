import os, json, time, subprocess

from color import Color
from datetime import datetime

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
        print(f'        {Color.PURPLE}Роль: {additional_info.get("roles", "N/A")}' + Color.END)
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

# Функция для запуска Ansible Playbook
def run_ansible_playbook(ip_address, playbook, playbooks_dir):
    # current_directory = os.getcwd()
    # print(f"Текущая рабочая директория: {current_directory}")
    user = 'ubuntu'
    playbook_path = os.path.join(playbooks_dir, playbook)
    #command = f"ansible-playbook -i {user}@{ip_address}, {playbook_path} --private-key id_ed25519 --ssh-common-args='-o StrictHostKeyChecking=no' --become --become-user=root"
    command = [
        "ansible-playbook",
        "-i", f"{user}@{ip_address},",
        playbook_path,
        "--private-key", "id_ed25519",
        "--ssh-common-args='-o StrictHostKeyChecking=no'",
        "--become",
        "--become-user", "root"
    ]
    print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    print("stdout:", result.stdout)  # Вывод stdout
    print("stderr:", result.stderr)  # Вывод stderr
    if result.returncode != 0:
        print(f"Установка роли завершилась с ошибкой: {result.returncode}")
        raise subprocess.CalledProcessError(result.returncode, command)
    else:
        print("Установка роли выполнена успешно!")
        