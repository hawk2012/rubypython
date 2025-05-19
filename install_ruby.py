import os
import subprocess
import shutil

# Проверка прав root
if os.geteuid() != 0:
    print("❌ Этот скрипт должен быть запущен от имени root.")
    exit(1)

# Конфигурация
ruby_version = "3.2.2"
ruby_source_url = f"https://cache.ruby-lang.org/pub/ruby/ {ruby_version}/ruby-{ruby_version}.tar.gz"
install_path = "/usr/local"
source_dir = f"/tmp/ruby-{ruby_version}"
archive_path = "/tmp/ruby.tar.gz"
path_line = f'export PATH="$PATH:{install_path}/bin"'

def run(cmd, cwd=None):
    """Выполняет команду и выводит лог в консоль"""
    print(f"🔧 Выполняю: {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=cwd
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0:
        print(f"❌ Ошибка выполнения команды: {cmd}")
        raise RuntimeError(f"Команда завершилась с кодом {result.returncode}")
    return result

def check_existing_ruby():
    """Проверяет, установлен ли Ruby в указанной директории"""
    ruby_bin = os.path.join(install_path, "bin", "ruby")
    if os.path.exists(ruby_bin):
        print(f"⚠️ Ruby уже установлен в {install_path}")
        choice = input("Хотите продолжить? (y/n): ").strip().lower()
        if choice != 'y':
            print("✅ Отмена установки.")
            exit(0)

def add_to_path():
    """Добавляет путь к Ruby в профильные файлы, если ещё не добавлено"""
    for profile_file in ["/etc/profile", "/etc/bash.bashrc"]:
        if not os.path.exists(profile_file):
            continue
        with open(profile_file, "r") as f:
            content = f.read()
        if path_line not in content:
            print(f"➕ Добавляю PATH в {profile_file}")
            with open(profile_file, "a") as f:
                f.write(f"\n{path_line}\n")

def cleanup():
    """Очистка временных файлов"""
    print("🧹 Очищаю временные файлы...")
    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)
    if os.path.exists(archive_path):
        os.remove(archive_path)

def install_ruby():
    try:
        check_existing_ruby()

        # Скачивание
        print(f"⬇️ Скачиваю Ruby {ruby_version}...")
        if os.path.exists(archive_path):
            print("🗂️ Используется существующий архив")
        else:
            run(f"wget -O {archive_path} {ruby_source_url}")

        # Распаковка
        print("📦 Распаковываю архив...")
        if os.path.exists(source_dir):
            shutil.rmtree(source_dir)
        run(f"tar xzf {archive_path} -C /tmp")

        # Конфигурация и сборка
        print("⚙️ Конфигурирую и собираю Ruby...")
        run("./configure --prefix=/usr/local", cwd=source_dir)
        run("make", cwd=source_dir)
        run("make install", cwd=source_dir)

        # Добавление пути
        add_to_path()

        # Очистка
        cleanup()

        print("🎉 Ruby успешно установлен!")
        print("🛠️ Не забудьте перезагрузить сеанс или выполнить:")
        print("source /etc/profile")

    except RuntimeError as e:
        print(e)
        print("❌ Установка прервана.")
        cleanup()
        exit(1)
    except KeyboardInterrupt:
        print("\n⛔ Установка прервана пользователем.")
        cleanup()
        exit(1)

if __name__ == "__main__":
    install_ruby()
