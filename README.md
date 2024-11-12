# Python Cloud Manager

## Описание

**Python Cloud Manager** — это проект для управления виртуальными машинами и облачными ресурсами с использованием Python. Этот проект служит моей тренировочной площадкой для изучения программирования на Python и работы с облачными сервисами.
Далее проект будет служить основой для проекта `бота в Telegram`

## Функциональность

Пока в проекте реализованы следующие функции:

- Создание виртуальных машин (ВМ) в облаке;
- Удаление виртуальных машин;
- Просмотр списка созданных виртуальных машин (файл `vm_data.json`);
- Интерактивный консольный интерфейс для выбора действий;
- Задание характеристик ВМ;
- **to be continued...** 👉

        - Заготовленные роли, например, - Web Server, Jenkins, Gitlab и тд;
        - Логирование?;
        - Managed Cluster K8s?;
        - и т.д. 🤫

## Интерфейс

- <img src="./pics/img1.png" alt="interface" title="screen" width="400"/>

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
6. Заполненный файл **creds.auto.tfvars**

    ```terraform
    token     = ""
    cloud_id  = ""
    folder_id = ""
    ```
