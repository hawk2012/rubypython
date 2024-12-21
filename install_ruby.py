import os
import subprocess

# Проверка наличия прав администратора
if not os.geteuid() == 0:
    print("Необходимо запустить этот скрипт от имени root.")
    exit()

# Определение пути к папке установки
install_path = "/usr/local"
ruby_version = "3.2.2"
ruby_source_url = f"https://cache.ruby-lang.org/pub/ruby/{ruby_version}/ruby-{ruby_version}.tar.gz"

def run_command(command):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc

def install_ruby():
    # Скачивание архива с исходниками Ruby
    print(f"Скачиваю архив с исходными кодами Ruby {ruby_version}")
    wget_command = f"wget -O /tmp/ruby.tar.gz {ruby_source_url}"
    if run_command(wget_command) != 0:
        print("Ошибка при скачивании архива")
        return False

    # Распаковка архива
    print("Распаковываю архив")
    tar_command = "tar xzf /tmp/ruby.tar.gz -C /tmp"
    if run_command(tar_command) != 0:
        print("Ошибка при распаковке архива")
        return False

    # Переход в директорию с исходным кодом
    source_dir = f"/tmp/ruby-{ruby_version}"
    os.chdir(source_dir)
    
    # Конфигурация, компиляция и установка
    print("Конфигурирование и сборка Ruby")
    configure_command = "./configure --prefix={}".format(install_path)
    make_command = "make"
    make_install_command = "make install"

    if run_command(configure_command) != 0 or \
       run_command(make_command) != 0 or \
       run_command(make_install_command) != 0:
        print("Ошибка при установке Ruby")
        return False

    # Добавление путей в нужные файлы
    print("Добавляю пути в нужные файлы")
    bashrc_file = "/etc/bash.bashrc"
    profile_file = "/etc/profile"
    path_line = 'export PATH="$PATH:{}"'.format(os.path.join(install_path, "bin"))

    with open(bashrc_file, "a") as file:
        file.write("\n{}\n".format(path_line))

    with open(profile_file, "a") as file:
        file.write("\n{}\n".format(path_line))

    print("Установка завершена успешно!")
    return True

if __name__ == "__main__":
    install_ruby()
