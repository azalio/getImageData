Сервис позволяющий по запросу получить картинку.

Не использует напрямую lorempixel.com так как он не позволяет
получать постоянный урл на картинку.

Установка:
- git clone https://github.com/azalio/getImageData.git
- положить конфиг nginx в папку с конфигами для nginx
- положить конфиг для systemd в /etc/systemd/system
- творчески отредактировать конфиги выше
- создать виртуальное окружение **virtualenv venv**
- установить туда все из requirements.txt
- работа приложения тестировалась на python3

Пример запроса:
wget -O /dev/null http://getimagedata.azalio.net/image/12349397-d4af-49fb-b6d2-6df7a6ccd8ee/200/200/