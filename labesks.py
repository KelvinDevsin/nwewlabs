import time
import uiautomator2 as u2
import os
import sys
import customtkinter as ctk
import base64
import threading
import requests
from anticaptchaofficial.imagecaptcha import imagecaptcha
import subprocess

# URL do arquivo hospedado com o código atualizado
URL = "https://raw.githubusercontent.com/KelvinDevsin/nwewlabs/refs/heads/main/labesks.py"

def verificar_atualizacao():
    """
    Verifica e baixa a versão mais recente do programa.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()

        # Adiciona declaração de codificação no início do arquivo
        conteudo = "# -*- coding: utf-8 -*-\n" + response.text
        
        with open("criador_celular_atualizado.py", "w", encoding="utf-8") as f:
            f.write(conteudo)
        
        os.replace("criador_celular_atualizado.py", __file__)
        return True
    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        return False

def reiniciar_programa():
    """
    Reinicia o programa atual.
    """
    print("Reiniciando o programa...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Função para ativar/desativar modo avião
def alternar_modo_aviao(device_id):
    """
    Alterna o modo avião no dispositivo especificado via ADB.
    """
    try:
        print(f"Ativando modo avião no dispositivo {device_id}...")
        subprocess.run(
            ["adb", "-s", device_id, "shell", "cmd", "connectivity", "airplane-mode", "enable"],
            check=True
        )
        time.sleep(4)

        print(f"Desativando modo avião no dispositivo {device_id}...")
        subprocess.run(
            ["adb", "-s", device_id, "shell", "cmd", "connectivity", "airplane-mode", "disable"],
            check=True
        )
        time.sleep(4)

        print("Modo avião alternado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando ADB no dispositivo {device_id}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao alternar modo avião no dispositivo {device_id}: {e}")

# Função para iniciar o driver usando `uiautomator2`
def iniciar_driver(device_id, port=None):
    try:
        driver = u2.connect(device_id) if port is None else u2.connect(f"{device_id}:{port}")
        print(f"Conectado ao dispositivo {'USB' if port is None else f'IP {device_id}:{port}'}")
        return driver
    except Exception as e:
        print(f"Erro ao conectar ao dispositivo {device_id}: {e}")
        return None

# Função para iniciar Instagram Lite
def iniciar_instagram_lite(d):
    try:
        print("Iniciando Instagram Lite...")
        d.app_clear("com.polestar.super.clone")
        d.app_start("com.polestar.super.clone")
        return True
    except Exception as e:
        print(f"Erro ao iniciar o Instagram Lite: {e}")
        return False

# Função principal para criar contas
def criar_conta_instagram_lite(d, device_id):
    try:
        print("Criando conta no Instagram Lite...")
        alternar_modo_aviao(device_id)
        time.sleep(4)
    except Exception as e:
        print(f"Erro ao criar conta: {e}")

# Executar processo principal
def executar_processo(device_id):
    d = iniciar_driver(device_id)
    if d and iniciar_instagram_lite(d):
        criar_conta_instagram_lite(d, device_id)

# Função para salvar o device_id em um arquivo
def salvar_device_id(device_id):
    with open("config.txt", "w") as f:
        f.write(device_id)

# Função para carregar o device_id do arquivo
def carregar_device_id():
    if os.path.exists("config.txt"):
        with open("config.txt", "r") as f:
            return f.read().strip()
    return ""

# Interface gráfica com customtkinter
def iniciar_interface():
    def iniciar_processo():
        global executando
        device_id = entrada_device_id.get().strip()
        if not device_id:
            label_status.configure(text="Insira o Device ID antes de iniciar.", text_color="red")
            return

        salvar_device_id(device_id)
        label_status.configure(text="Processo em execução...", text_color="blue")

        def thread_process():
            try:
                executar_processo(device_id)
                label_status.configure(text="Processo finalizado.", text_color="green")
            except Exception as e:
                label_status.configure(text=f"Erro: {e}", text_color="red")

        threading.Thread(target=thread_process, daemon=True).start()

    # Função para parar o processo
    def parar():
        label_status.configure(text="Processo interrompido.", text_color="red")

    def fechar_janela():
        janela.destroy()
        sys.exit()

    # Configuração da janela
    ctk.set_appearance_mode("dark")
    janela = ctk.CTk()
    janela.title("Gerador de Conta Instagram Lite")
    janela.geometry("400x300")
    janela.protocol("WM_DELETE_WINDOW", fechar_janela)

    label_device_id = ctk.CTkLabel(janela, text="Device ID:")
    label_device_id.pack(pady=(10, 0))
    entrada_device_id = ctk.CTkEntry(janela, width=250)
    entrada_device_id.pack(pady=(0, 10))

    device_id_salvo = carregar_device_id()
    entrada_device_id.insert(0, device_id_salvo)

    botao_iniciar = ctk.CTkButton(janela, text="Iniciar", command=iniciar_processo)
    botao_iniciar.pack(pady=10)

    botao_parar = ctk.CTkButton(janela, text="Parar", command=parar)
    botao_parar.pack(pady=10)

    label_status = ctk.CTkLabel(janela, text="")
    label_status.pack(pady=10)

    janela.mainloop()

if __name__ == "__main__":
    if verificar_atualizacao():
        reiniciar_programa()
    iniciar_interface()
