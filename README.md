# Python Cloud Manager

## Описание

**Python Cloud Manager** — это проект для управления виртуальными машинами и облачными ресурсами с использованием Python. Этот проект служит моей тренировочной площадкой для изучения программирования на Python и работы с облачными сервисами.
Далее проект будет служить основой перевода на `бота telegram` 

## Функциональность

Пока в проекте реализованы следующие функции:
- Создание виртуальных машин (ВМ) в облаке;
- Удаление виртуальных машин;
- Просмотр списка созданных виртуальных машин (файл `vm_data.json`);
- Интерактивный консольный интерфейс для выбора действий;
- **to be continued...** 👉
    - Задание характеристик ВМ;
    - Отображение подробной информации;
    - Логирование
    - Managed Cluster K8s;
    - и т.д. 🤫

## Технологии

- Python
- Terraform
- Yandex Cloud

## Предварительные требования
1. Аккаунт в Yandex Cloud.
2. Установленный [Terraform](https://yandex.cloud/ru/docs/tutorials/infrastructure-management/terraform-quickstart).
3. Установленный [Yandex Cloud CLI](https://cloud.yandex.ru/docs/cli/quickstart).
4. Полученный [OAuth-токен](https://yandex.cloud/ru/docs/iam/concepts/authorization/oauth-token).
5. В корне репозитория должен лежать SSH-key - **id_ed25519.pub**