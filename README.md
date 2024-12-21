### Описание работы скрипта:

1. Скрипт сначала проверяет, запущен ли он с правами суперпользователя (`root`), так как для установки Ruby требуются права администратора.
   
2. В переменных задаются версия Ruby и путь для установки.

3. Архив с исходниками Ruby скачивается командой `wget`. Затем архив распаковывается в `/tmp`.

4. Выполняется конфигурация, компиляция и установка Ruby через команды `./configure`, `make` и `make install`.

5. Путь до установленной Ruby добавляется в глобальные файлы конфигурации системы (`/etc/bash.bashrc` и `/etc/profile`) для всех пользователей.

6. **Сообщение об успехе**: Если всё прошло без ошибок, выводится сообщение о завершении установки.

### Как использовать:

1. Сохраните данный скрипт в файл, например, `install_ruby.py`.
2. Запустите его с правами суперпользователя:

   ```bash
   sudo python3 install_ruby.py
   ```

После выполнения этого скрипта у вас будет установлена последняя версия Ruby, а также настроены необходимые пути для её использования всеми пользователями системы.

------------------------------------------------------------------------

### Description of the script:

1. The script first checks whether it is running with superuser rights (`root`), since Ruby requires administrator rights to install.
   
2. The variables specify the Ruby version and the installation path.

3. The Ruby source archive is downloaded by the `wget' command. The archive is then unpacked to `/tmp`.

4. Ruby is configured, compiled, and installed using the `./configure`, `make`, and `make install` commands.

5. The path to the installed Ruby is added to the global system configuration files (`/etc/bash.bashrc` and `/etc/profile') for all users.

6. **Success Message**: If everything went smoothly, an installation completion message is displayed.

### How to use:

1. Save this script to a file, for example, `install_ruby.py `.
2. Run it with superuser rights:

   ```bash
   sudo python3 install_ruby.py
   ```

After executing this script, you will have the latest version of Ruby installed, as well as the necessary paths configured for its use by all users of the system.
