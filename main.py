from terraform import *
from utils import *
from color import Color
def main_menu():
    while True:
        print(Color.DARKCYAN + '\n--------------------------------------------------' + Color.END)
        print(Color.YELLOW + 'Выберите вариант:' + Color.END)
        print(Color.GREEN + '1. ' + Color.END + 'Просмотр созданных ВМ')
        print(Color.GREEN + '2. ' + Color.END + 'Создать ВМ - Simple Ubuntu-22-04 (params. 2-4-30)')
        print(Color.GREEN + '3. ' + Color.END + 'Создать ВМ - Simple Custom')
        print(Color.GREEN + '4. ' + Color.END + 'Создать ВМ - Roles')
        print(Color.GREEN + '5. ' + Color.END + 'Удалить ВМ')
        print(Color.GREEN + '6. ' + Color.END + 'Выход')

        choice = input('\nВведите номер варианта: ')
        
        if choice == '1':
            print(Color.YELLOW + '\nСозданные ВМ:' + Color.END)
            display_vm_data()

        elif choice == '2':
            while True:
                try:
                    number_of_vms = int(input('\nВведите количество ВМ для создания (' + Color.GREEN+ 'не более 3' + Color.END + '): '))
                    if number_of_vms > 3:
                        print(Color.RED + '\nОшибка: можно создать не более 3 виртуальных машин. Попробуйте снова.' + Color.END)
                        print(Color.YELLOW + 'Чтобы вернуться на главное меню нажмите: 0' + Color.END)
                    elif number_of_vms < 0:
                        print(Color.RED + '\nОшибка: А вы случаем не тестер? Попробуйте снова.' + Color.END)
                        print(Color.YELLOW + 'Чтобы вернуться на главное меню нажмите: 0' + Color.END)
                    elif number_of_vms == 0:
                        print(Color.YELLOW + '\nНу и ладно :)' + Color.END)
                        break
                    else:
                        create_vms(number_of_vms, 2, 4, 100, 30)
                        break
                except ValueError:
                    print(Color.RED + '\nОшибка: необходимо ввести числовое значение. Попробуйте снова.' + Color.END)
                    print(Color.YELLOW + 'Чтобы вернуться на главное меню нажмите: 0' + Color.END)

        elif choice == '3':
            while True:
                try:
                    # Ввод количества виртуальных машин
                    number_of_vms = int(input('\nВведите количество ВМ для создания (' + Color.GREEN + 'не более 3' + Color.END + '): '))
                    if number_of_vms > 3:
                        print(Color.RED + '\nОшибка: можно создать не более 3 виртуальных машин. Попробуйте снова.' + Color.END)
                        print(Color.YELLOW + 'Чтобы вернуться на главное меню нажмите: 0' + Color.END)
                        continue
                    elif number_of_vms < 0:
                        print(Color.RED + '\nОшибка: значение не может быть отрицательным. Попробуйте снова.' + Color.END)
                        print(Color.YELLOW + 'Чтобы вернуться на главное меню нажмите: 0' + Color.END)
                        continue
                    elif number_of_vms == 0:
                        print(Color.YELLOW + '\nНу и ладно :)' + Color.END)
                        break

                    # Допустимые комбинации CPU, RAM и cpu_fraction на основе Yandex Cloud
                    valid_cpu_ram_options = {
                        (2, 2, 20), (2, 2, 50), (2, 2, 100),
                        (2, 4, 20), (2, 4, 50), (2, 4, 100),
                        (2, 8, 20), (2, 8, 50), (2, 8, 100),
                        (4, 4, 20), (4, 4, 50), (4, 4, 100),
                        (4, 8, 20), (4, 8, 50), (4, 8, 100),
                        (4, 16, 20), (4, 16, 50), (4, 16, 100),
                        (8, 8, 100), (8, 16, 100), (8, 32, 100)
                    }
                    # Формируем строку с допустимыми комбинациями
                    valid_combinations_message = '\nДопустимые комбинации CPU, RAM и CPU фракции:\n' + '\n'.join(
                        [
                            f'{Color.CYAN}CPU: {cpu}{Color.END}, '
                            f'{Color.GREEN}RAM: {ram} ГБ{Color.END}, '
                            f'{Color.YELLOW}CPU фракция: {cpu_fraction}%{Color.END}'
                            for cpu, ram, cpu_fraction in sorted(valid_cpu_ram_options)
                        ]
                    )

                    print(valid_combinations_message) 

                    # Максимально значения для hdd
                    valid_hdd = 200

                    # Ввод и проверка CPU и RAM
                    cpu = int(input('\nВведите количество CPU (2, 4 или 8): '))
                    ram = int(input('\nВведите объем оперативной памяти (в ГБ) - 2, 4, 8, 16 или 32: '))
                    cpu_fraction = int(input('\nВведите фракцию CPU (20, 50 или 100): '))

                    # Проверка допустимости комбинации
                    if (cpu, ram, cpu_fraction) not in valid_cpu_ram_options:
                        print(Color.RED + '\nОшибка: недопустимая комбинация CPU, RAM и фракции CPU. Попробуйте снова.' + Color.END)
                        continue
                    
                    # Ввод объема HDD
                    hdd = int(input('Введите объем HDD (в ГБ) - не более 200: '))
                    if hdd > valid_hdd:
                        print(Color.RED + '\nОшибка: недопустимое значение объема HDD. Попробуйте снова.' + Color.END)
                        continue
                    
                    create_vms(number_of_vms, cpu, ram, cpu_fraction, hdd)
                    break
                except ValueError:
                    print(Color.RED + '\nОшибка: необходимо ввести числовое значение. Попробуйте снова.' + Color.END)
                    print(Color.YELLOW + 'Чтобы вернуться на главное меню нажмите: 0' + Color.END)
        elif choice == '4':
            create_vm_roles()

        elif choice == '5':
            unique_id = input('\nВведите уникальный ID для удаления: ')
            working_dir = f'vms_{unique_id}'
            
            if os.path.exists(working_dir):
                # Подтверждение удаления
                confirmation = input(f'Вы действительно хотите удалить VMs с ID {unique_id}? Введите "yes" для подтверждения: ')
                
                if confirmation.lower() == "yes":
                    destroy_vms(working_dir)  # terraform destroy + remove_directory
                    remove_vm_data(unique_id)  # удаление информации о VM из файла vm_data.json
                    print(Color.YELLOW + f'Удаление завершено!' + Color.END)
                else:
                    print(Color.RED + 'Удаление отменено.' + Color.END)
            else:
                print(Color.RED + f'\nВМ с ID {unique_id} не найдены.' + Color.END)

        elif choice == '6':
            print(Color.BLUE + '\nУдачи путник...' + Color.END)
            break

        else:
            print(Color.RED + '\nНекорректный вариант, попробуйте снова.' + Color.END)

if __name__ == '__main__':
    main_menu()