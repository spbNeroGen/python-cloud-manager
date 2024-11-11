import subprocess, os, uuid, shutil
import threading
from utils import *
from color import Color
from datetime import datetime

# Пути к исходным Terraform файлам
SOURCE_PROVIDER_TF = "provider.tf"
SOURCE_VARIABLES_TF = "variables.tf"
SOURCE_TERRAFORM_RC = ".terraformrc"
TERRAFORM_CREDS = "creds.auto.tfvars"

# Шаблон для генерации main.tf - задел на будущее
TEMPLATE_MAIN_TF = """
data "yandex_compute_image" "ubuntu-2204" {
  family = "ubuntu-2204-lts"
}

data "yandex_vpc_network" "default" {
  name = "default"
}

data "yandex_vpc_subnet" "default-ru-central1-a" {
  name = "default-ru-central1-a"
}

resource "yandex_compute_instance" "simple-vm" {
  count       = var.instance_count
  name        = "vms-${var.instance_name}-${count.index + 1}"
  platform_id = "standard-v3"

  resources {
    cores         = var.instance_cores
    memory        = var.instance_memory
    core_fraction = var.instance_core_fraction
  }

  boot_disk {
    initialize_params {
      size     = var.instance_disk_size
      type     = "network-hdd"
      image_id = data.yandex_compute_image.ubuntu-2204.id
    }
  }

  network_interface {
    subnet_id = data.yandex_vpc_subnet.default-ru-central1-a.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("../id_ed25519.pub")}"
  }
}

output "instance_ips" {
  value = yandex_compute_instance.simple-vm[*].network_interface[0].nat_ip_address
}
"""

# Функция для копирования конфигурационных файлов и создания `main.tf` с переменными
def generate_main_tf(working_dir, instance_name, instance_count, instance_cores, instance_memory, instance_core_fraction, instance_disk_size):
    # Копируем provider.tf и variables.tf и .terraformrc и cred.auto.tfvars  в рабочую директорию
    shutil.copy(SOURCE_PROVIDER_TF, working_dir)
    shutil.copy(SOURCE_VARIABLES_TF, working_dir)
    shutil.copy(SOURCE_TERRAFORM_RC, working_dir)
    shutil.copy(TERRAFORM_CREDS, working_dir)

    # Создаем main.tf с шаблоном конфигурации
    with open(os.path.join(working_dir, "main.tf"), "w") as f:
        f.write(TEMPLATE_MAIN_TF)

    # Записываем переменные в params.auto.tfvars
    with open(os.path.join(working_dir, "params.auto.tfvars"), "w") as f:
        f.write(f'instance_name = "{instance_name}"\n')
        f.write(f'instance_count = {instance_count}\n')
        f.write(f'instance_cores = {instance_cores}\n')
        f.write(f'instance_memory = {instance_memory}\n')
        f.write(f'instance_core_fraction = {instance_core_fraction}\n')
        f.write(f'instance_disk_size = {instance_disk_size}\n')

# Функция для выполнения команды Terraform
def run_terraform(command, working_dir):
    result = subprocess.run(command, shell=True, cwd=working_dir, capture_output=True, text=True)
    print(f'Результат:\n{result.stdout}')
    if result.stderr:
        print(f'Ошибка:\n{result.stderr}')
        raise subprocess.CalledProcessError(result.returncode, command)  # Генерируем исключение при ошибке
    
def terraform_init(working_dir):
    try:
        run_terraform("terraform init", working_dir)
    except subprocess.CalledProcessError:
        print(Color.RED + f'Ошибка при инициализации Terraform в директории {working_dir}.' + Color.END)
        destroy_vms(working_dir)
        raise

def terraform_apply(working_dir):
    try:
        run_terraform("terraform apply -auto-approve", working_dir)
    except subprocess.CalledProcessError:
        print(Color.RED + f'Ошибка при применении Terraform в директории {working_dir}.' + Color.END)
        destroy_vms(working_dir)
        raise

def terraform_destroy(working_dir):
    try:
      run_terraform("terraform destroy -auto-approve", working_dir)
    except subprocess.CalledProcessError:
        print(Color.RED + f'Ошибка при удалении конфигурации Terraform в директории {working_dir}.' + Color.END)

def get_instance_ips(working_dir):
    # Выполняем terraform output для получения выходных данных
    output_command = "terraform output -json"
    output_result = subprocess.run(output_command, shell=True, cwd=working_dir, capture_output=True, text=True)
    # Проверяем, что вывод не пустой
    if output_result.returncode != 0:
        raise RuntimeError(f"Ошибка выполнения команды: {output_result.stderr}")
    # Загружаем JSON
    try:
        outputs = json.loads(output_result.stdout)
    except json.JSONDecodeError as e:
        raise ValueError("Ошибка при декодировании JSON: " + str(e))
    # Проверяем, что ключ "instance_ips" существует
    if "instance_ips" in outputs and "value" in outputs["instance_ips"]:
        return outputs["instance_ips"]["value"]
    else:
        raise KeyError("Ключ 'instance_ips' не найден в выходных данных Terraform.")

# Создаем уникальную директорию для каждого вызова
def create_vms(vm_count, instance_cores, instance_memory, instance_core_fraction, instance_disk_size):
    unique_id = str(uuid.uuid4())[:8]
    working_dir = f'vms_{unique_id}'
    stop_event = threading.Event() # Для Выполняется \|/
    thread = threading.Thread(target=loading_animation, args=(stop_event,))

    try:
        # Создаем директорию для хранения конфигурации
        os.makedirs(working_dir, exist_ok=True)
        absolute_path = os.path.abspath(working_dir)
        terraform_rc_path = os.path.join(absolute_path, ".terraformrc")

        # Генерируем конфигурацию Terraform
        generate_main_tf(working_dir, unique_id, vm_count, instance_cores, instance_memory, instance_core_fraction, instance_disk_size)
        print(Color.GREEN + f'\nДиректория хранения конфигурации и .tfstate создана: {absolute_path}' + Color.END)

        print(Color.YELLOW + f'Запускаем terraform init & apply' + Color.END)
        os.environ["TF_CLI_CONFIG_FILE"] = terraform_rc_path
        
        # Запускаем анимацию в отдельном потоке
        thread.start()
        
        # Инициализируем и применяем Terraform
        terraform_init(working_dir)
        terraform_apply(working_dir)
        # Получаем IP-адреса после terraform apply
        instance_ips = get_instance_ips(working_dir)
        
        # Тестовая дополнительная информация
        creation_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        additional_info = {
            'status': 'test', 
            'creation_date': creation_date,
            'resource_info': {  
                'vm_count': vm_count,                       # Информация о ресурсах ВМ
                'cpu': instance_cores,
                'ram': instance_memory,
                'cpu_fraction': instance_core_fraction,
                'disk_size': instance_disk_size,
                'ip_addresses': instance_ips
                }
            }
        # generate_vm_data_from_tfstate(working_dir)
        add_vm_data(unique_id, vm_count, absolute_path, additional_info) 
        print(Color.GREEN + f'\nФайл информации о созданных ВМ обновлен!' + Color.END)

    except FileExistsError:
        print(Color.RED + f'\nОшибка: Директория "{working_dir}" уже существует.' + Color.END)
    except PermissionError:
        print(Color.RED + f'\nОшибка: У вас нет прав на создание директории "{working_dir}".' + Color.END)
    except subprocess.CalledProcessError as e:
        print(Color.RED + f'\nОшибка выполнения команды Terraform: {e}' + Color.END)
    except Exception as e:
        print(f'\nОшибка: {e}')  # Обработка любых других ошибок
    else:
        print(Color.YELLOW + f'ВМ созданы в кол-ве {vm_count} шт, ID - {unique_id}' + Color.END)
    finally:
        # Останавливаем анимацию
        stop_event.set()
        thread.join() 

def destroy_vms(working_dir):
    try:
        print(f'\nУдаляем {working_dir}...')
        stop_event = threading.Event()
        thread = threading.Thread(target=loading_animation, args=(stop_event,))
        thread.start()

        terraform_destroy(working_dir)

        stop_event.set()
        thread.join()

    except Exception as e:
        print(f'Ошибка при удалении ВМ: {e}')
    else:
        # Удаляем директорию с рабочими файлами
        try:
            remove_directory(working_dir)
        except Exception as e:
            print(f'Ошибка при удалении директории {working_dir}: {e}')
        else:
            print(f'Директория {working_dir} успешно удалена.')