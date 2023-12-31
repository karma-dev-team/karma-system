Система кармы 
-------------
Кратко система кармы это централизованная 
онлайн система учета репутации в конкретных жанрах игр. 

Эта часть является логикой и сайтом системы кармы. 

Архектиктура 
----------
См. docs/architecture.md 

Установка 
---------
Сперва создайте два файла в папке deploy/ это 
config.toml, .env для настройки приложения. 

Скопируйте содержимое `config_example.toml` в `config.toml` 

Скопируйте содержимое `.env.dist` в `.env`

Вставьте нужные данные в содержимое config.toml, в особенности 
данные части mailing, вставьте данные для доступа к почтовому яшику 
через SMTP, поддерживается только yandex, gmail будет в будущем. 
См. раздел документации яндекса - [ссылка](https://yandex.ru/support/mail/mail-clients/others.html)

Во вторых установите и запустите докер декстоп. 

Дефолтные настройки .env и config.toml сделаны для запуска через docker. 

Запуск через докер требует ввода трех этих комманд. 
```shell
$ docker-compose -f deploy/docker-compose.yml build api 
$ docker-compsoe -f deploy/docker-compose.yml --profile migration up 
$ docker-compose -f deploy/docker-compose.yml up api 
```
После этого проверьте в браузере адрес http://localhost:8000/ все должно работать 

При изменении любых файлов введите те же комманды для применения изменении

Изменения базы данных
-----
При добавлении или изменении модели в файлах models.py надо зафиксировать 
изменения для миграции с помощью команды: 
```shell
$ alembic revision --autogenerate -m "<Описание изменении>"
```
