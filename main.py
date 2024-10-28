from terraform import *
from utils import *
from color import Color
def main_menu():
    while True:
        print(Color.DARKCYAN + '\n--------------------------------------------------' + Color.END)
        print(Color.YELLOW + 'Выберите вариант:' + Color.END)
        print(Color.GREEN + '1. ' + Color.END + 'Просмотр созданных ВМ')
        print(Color.GREEN + '2. ' + Color.END + 'Создать ВМ - Ubuntu-2204(2-4-30)')
        print(Color.GREEN + '3. ' + Color.END + 'Удалить ВМ')
        print(Color.GREEN + '4. ' + Color.END + 'Выход')

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
                        create_vms(number_of_vms)
                        break
                except ValueError:
                    print(Color.RED + '\nОшибка: необходимо ввести числовое значение. Попробуйте снова.' + Color.END)
                    print(Color.YELLOW + 'Чтобы вернуться на главное меню нажмите: 0' + Color.END)

        elif choice == '3':
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

        elif choice == '4':
            print(Color.BLUE + '\nУдачи путник...' + Color.END)
            break

        else:
            print(Color.RED + '\nНекорректный вариант, попробуйте снова.' + Color.END)

if __name__ == '__main__':
    main_menu()