import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DownloadsHandler(FileSystemEventHandler):
    def __init__(self, pasta_downloads):
        self.pasta_downloads = pasta_downloads

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"Arquivo adicionado: {event.src_path}")
        organizar_downloads(self.pasta_downloads)


def organizar_downloads(pasta_downloads):
    # Verificar se a pasta de downloads existe
    if not os.path.exists(pasta_downloads):
        print("A pasta de downloads não foi encontrada.")
        return

    # Mapear extensões para pastas correspondentes
    categorias = {
        "imagens": [".jpg", ".jpeg", ".png", ".gif"],
        "documentos": [".pdf", ".doc", ".docx", ".txt", ".csv"],
        "videos": [".mp4", ".avi", ".mkv"],
        "musicas": [".mp3", ".wav"],
        "compactados": [".zip", ".rar", ".7z", ".tar"],
        "outros": []  # Extensões não mapeadas serão colocadas nesta pasta
    }

    # Criar pastas para cada categoria, se elas não existirem
    for categoria in categorias:
        pasta_categoria = os.path.join(pasta_downloads, categoria)
        if not os.path.exists(pasta_categoria):
            os.makedirs(pasta_categoria)

    # Iterar sobre os arquivos na pasta de downloads
    for arquivo in os.listdir(pasta_downloads):
        # Ignorar diretórios
        if os.path.isdir(os.path.join(pasta_downloads, arquivo)):
            continue

        # Obter a extensão do arquivo
        _, extensao = os.path.splitext(arquivo)
        extensao = extensao.lower()  # Converter para minúsculas para garantir correspondência

        # Encontrar a categoria correspondente para esta extensão
        categoria_encontrada = False
        for categoria, extensoes in categorias.items():
            if extensao in extensoes:
                pasta_destino = os.path.join(pasta_downloads, categoria)
                shutil.move(os.path.join(pasta_downloads, arquivo),
                            os.path.join(pasta_destino, arquivo))
                categoria_encontrada = True
                break

        # Se a extensão não corresponder a nenhuma categoria, mover para "outros"
        if not categoria_encontrada:
            pasta_destino = os.path.join(pasta_downloads, "outros")
            shutil.move(os.path.join(pasta_downloads, arquivo),
                        os.path.join(pasta_destino, arquivo))

    print("Organização concluída.")


def monitorar_downloads(pasta_downloads):
    event_handler = DownloadsHandler(pasta_downloads)
    observer = Observer()
    observer.schedule(event_handler, pasta_downloads, recursive=False)
    observer.start()
    print(f"Monitorando a pasta de downloads: {pasta_downloads}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    # Caminho para a pasta de downloads
    pasta_downloads = os.path.expanduser("~/Downloads")
    monitorar_downloads(pasta_downloads)
