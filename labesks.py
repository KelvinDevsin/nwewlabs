
# ESSE CODIGO É USADO PARA CELULAR VIA USB



import time
import uiautomator2 as u2
import os
import sys
import customtkinter as ctk
import base64
from PIL import Image
import subprocess
import threading
from email_handler import create_email, get_inbox
import random
from secmail import gerar_email_temporario, esperar_codigo_de_confirmacao
from anticaptchaofficial.imagecaptcha import imagecaptcha
from inboxes import gerar_email, ativar_inbox, aguardar_codigo 

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
        
        with open("labeskhys.py", "w", encoding="utf-8") as f:
            f.write(conteudo)
        
        os.replace("labeskhys.py", __file__)
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
    
executando = True
lock = threading.Lock()
pause_event = threading.Event()

# Função para capturar o captcha e enviar para resolução
def resolver_captcha(caminho_imagem, api_key):
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)

    # Converte a imagem para base64
    with open(caminho_imagem, "rb") as img_file:
        captcha_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    
    # Envia para o serviço AntiCaptcha
    captcha_text = solver.solve_and_return_solution(captcha_base64)
    
    if captcha_text != 0:
        print("Texto do captcha:", captcha_text)
        return captcha_text
    else:
        print("Erro ao resolver o captcha:", solver.error_code)
        return None
# Contador para controlar o número de threads ativas
threads_ativas = 3
threads_lock = threading.Lock()
ip_ja_trocado = False
ip_lock = threading.Lock()
# Função para ativar e desativar o modo avião
def alternar_modo_aviao(device_id):
    """
    Alterna o modo avião no dispositivo especificado via ADB.

    Args:
        device_id (str): ID do dispositivo conectado via ADB.
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

# Função para iniciar o driver usando IP e porta
def iniciar_driver(device_id, port=None):
    # Código de conexão com o dispositivo (por exemplo, usando uma biblioteca como `uiautomator2` ou `adb`)
    # Aqui, conecte-se ao dispositivo e retorne o objeto do driver
    try:
        # Exemplo de criação de driver usando `uiautomator2` (substitua com a sua implementação)
        import uiautomator2 as u2
        driver = u2.connect(device_id) if port is None else u2.connect(f"{device_id}:{port}")
        print(f"Conectado ao dispositivo {'USB' if port is None else f'IP {device_id}:{port}'}")
        return driver
    except Exception as e:
        print(f"Erro ao conectar ao dispositivo {device_id}: {e}")
        return None


# Função para iniciar o Instagram Lite no emulador
def iniciar_instagram_lite(d):
    try:
        print("Iniciando Instagram Lite...")
        d.app_clear("com.polestar.super.clone")
        d.app_start("com.polestar.super.clone")
    except Exception as e:
        print(f"Erro ao iniciar o Instagram Lite: {e}")
        return False
    return True

def reiniciar_aplicativo(d):
    print("Reiniciando o aplicativo e limpando dados...")
    d.app_clear("com.polestar.super.clone")
    d.app_start("com.polestar.super.clone")


# Função para criar a conta no Instagram Lite
def criar_conta_instagram_lite(d, device_id):
    while True:  # Loop para tentar até ter sucesso
        global threads_ativas
        try:
            with threads_lock:
                threads_ativas += 1  # Incrementa contador ao iniciar thread

            time.sleep(3)
                    # Clica em MAIS
            botao_entrar = d.xpath('//android.view.View[@resource-id="com.polestar.super.clone:id/addApp_btn"]').get()
            botao_entrar.click()

            # Clica em clonar instagram
            botao_entrar = d.xpath('//android.widget.TextView[@resource-id="com.polestar.super.clone:id/item_app_name" and @text="Instagram"]').get()
            botao_entrar.click()

            # Clica em OK
            botao_entrar = d.xpath('//android.widget.TextView[@resource-id="com.polestar.super.clone:id/button_positive"]').get()
            botao_entrar.click()
            time.sleep(2)
            # PERMISSÃO
            d.xpath('//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]').click(timeout=8)

            # Clica START
            botao_entrar = d.xpath('//android.widget.Button[@resource-id="com.polestar.super.clone:id/btn_start"]').get()
            botao_entrar.click()

            print("Iniciando processo de criação de conta...")
            # Criar nova conta
            time.sleep(5)
            d.xpath('//android.view.View[@content-desc="Criar nova conta"]').click()
            try:
             d.xpath('//android.view.View[@content-desc="Criar nova conta"]').click(timeout=1)
            except:
               pass
            print("Aceitando permissões de contatos.")
            time.sleep(1)
            try:
                d.xpath('//android.widget.TextView[@text="A Página não está disponível no momento"]').click(timeout=1)
                reiniciar_aplicativo(d)
                continue  # Reinicia o loop para tentar criar outra conta
            except u2.XPathElementNotFoundError:
                pass  # Segue com a criação da conta caso não encontre o elemento

            try:
                d.xpath('//android.view.View[@content-desc="Criar conta"]').click(timemout=4)
                print("Apertando em Criar conta")
            except:
                try:
                    d.xpath('//android.view.View[@content-desc="Começar"]').click(timeout=1)
                except:
                   pass
            
            
            # Apertar em "Avançar" apos adicionar o email
            d.xpath('//android.view.View[@content-desc="Cadastrar-se com o email"]').click()
            print("Apertou 'Cadastrar-se com o email'.")

            # Criar e adicionar o email temporário (1secmail)
            email_copied = gerar_email_temporario()
                        # Gerar e adicionar o email temporário usando inboxes
            #email_copied = gerar_email()
            #ativar_inbox(email_copied)  # Ativar a inbox para o email gerado
            print(f"E-mail temporário gerado: {email_copied}")
            time.sleep(1)
            # Inserir o email
            d.xpath('//android.widget.EditText').set_text(email_copied)
            print("Email inserido.")
            time.sleep(1)

            # Apertar em "Avançar" apos adicionar o email
            d.xpath('//android.view.View[@content-desc="Avançar"]').click()
            print("Apertou 'Avançar'.")

            try:
                d.xpath('//android.view.View[@content-desc="Restringimos determinadas atividades para proteger nossa comunidade. Diga-nos se você acha que isto foi um engano."]').click(timeout=5)
                alternar_modo_aviao(device_id)
                time.sleep(4)
                reiniciar_aplicativo(d)
                criar_conta_instagram_lite(d, device_id) 
            except u2.XPathElementNotFoundError:
                pass  # Segue com a criação da conta caso não encontre o elemento

            # Aguardar código de verificação no email (1secmail)
            codigo = esperar_codigo_de_confirmacao(email_copied)
            #codigo = aguardar_codigo(email_copied)
            if codigo:
                print(f"Código recebido: {codigo}")

                # Inserir o código de verificação
                d.xpath('//android.widget.EditText').set_text(codigo)
                print("Código inserido.")

                # Apertar em "Avançar" após inserir o código
                d.xpath('//android.view.View[@content-desc="Avançar"]').click()
                print("Apertou 'Avançar'.")
                time.sleep(5)

                # Criar senha
                senha = "@DSFFDSFddHBHGByhH!?$"
                d.xpath('//android.widget.EditText').set_text(senha)
                print(f"Senha '{senha}' inserida.")
                time.sleep(2)

                # Apertar em "Avançar" após criar a senha
                d.xpath('//android.view.View[@content-desc="Avançar"]').click()
                print("Apertou 'Avançar' após senha.")
                time.sleep(1)
                try:
                    # Apertar em "Agora não" após criar a senha
                    d.xpath('//android.widget.Button[@resource-id="android:id/button2"]').click(timeout=5)
                    print("Apertou 'criar nova conta' após senha.")
                    time.sleep(1) 
                except:
                    pass

                # Apertar em "Agora não" após criar a senha
                d.xpath('//android.view.View[@content-desc="Agora não"]').click()
                print("Apertou 'Agora não' após senha.")
                time.sleep(1)

                # Deslizar para selecionar a data de nascimento
                for _ in range(4):
                    d.swipe(739, 1143, 757, 2189, duration=0)
                time.sleep(2)
                
                # Apertar em "Avançar" final após a data de nascimento
                try:
                   d.xpath('//android.widget.EditText[@resource-id="android:id/numberpicker_input" and @text="1999"]').click(timeout=1)
                   print("Ano 2000 adicionado")
                except:
                        d.xpath('//android.widget.EditText[@resource-id="android:id/numberpicker_input" and @text="2000"]').click()
                        print("Ano 2002 adicionado")

                # Apertar em "Avançar" final
                d.xpath('//android.widget.Button[@resource-id="android:id/button1"]').click()
                print("Apertou 'DEFINIR'.")
                time.sleep(1.5)
                
                # Apertar em "Avançar" final
                d.xpath('//android.view.View[@content-desc="Avançar"]').click()
                print("Apertou 'Avançar'.")
                time.sleep(1.5)
                # Apertar em "Avançar" final
                d.xpath('//android.view.View[@content-desc="Avançar"]').click()
                print("Apertou 'Avançar'.")
                time.sleep(1.5)

                # Apertar em "Avançar" final
                d.xpath('//android.view.View[@content-desc="Avançar"]').click()
                print("Apertou 'Avançar'.")

                time.sleep(2)
                # *** Sincronizar o clique no botão final ***
                with lock:
                    try:
                       d.xpath('//android.view.View[@content-desc="Concordo"]').click()
                       print("Apertou 'CONCORDO'.")
                    except:
                           print('Não foi possivel apertar em avnaçar')
                attempt_count = 0  # Inicializa o contador de tentativas
                while True:


                    try:
                        # Verifica se o primeiro xpath existe
                        if d.xpath('//android.view.View[@content-desc="Adicionar foto"]').exists:
                            print("CONTA CRIADA")
                            with open("contas.txt", "a") as file:
                            #file.write(f"{chave_dinamica}\n")
                             email_username = email_copied.split('@')[0]
                             file.write(f"{email_username}\n")
                             file.write("Kelvin2002\n")
                            # Reinicia o aplicativo e tenta criar outra conta
                            reiniciar_aplicativo(d)
                            criar_conta_instagram_lite(d, device_id)
                            break  # Sai do loop se a resolução do captcha for bem-sucedida
                    except:
                        pass
                            
                    try:
                        # Em seguida, você pode permitir o acesso aos seus contatos para conseguir encontrar amigos no Instagram com mais facilidade
                        if d.xpath('//android.widget.TextView[@resource-id="com.instagram.android:id/connect_contacts_title_igds"]').exists:
                            print("permitir o acesso aos seus contatos")
                            d.xpath('//android.widget.Button[@resource-id="com.instagram.android:id/button_text"]').click(timeout=2)
                            time.sleep(1)
                            d.xpath('//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]').click(timeout=2)

                    except:
                        pass

                    try:
                        # Ativar notificações push?
                        if d.xpath('//android.widget.TextView[@resource-id="com.instagram.android:id/igds_headline_headline"]').exists:
                            print("Ativar notificações push?")
                            d.xpath('//android.widget.Button[@resource-id="com.instagram.android:id/auxiliary_button"]').click(timeout=5)

                    except:
                        pass

                    try:
                        # Em seguida, você poderá sincronizar seus contatos para encontrar seus amigos
                        if d.xpath('//android.widget.TextView[@resource-id="com.instagram.android:id/connect_contacts_subtitle"]').exists:
                            print("Ativar notificações push?")
                            d.xpath('//android.widget.Button[@resource-id="com.instagram.android:id/button_text"]').click(timeout=2)
                            time.sleep(1)
                            d.xpath('//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]').click(timeout=2)

                    except:
                        pass

                    try:
                        # Receba sugestões do Facebook
                        if d.xpath('//android.widget.TextView[@resource-id="com.instagram.android:id/connect_text"]').exists:
                            print("Receba sugestões do Facebook")
                            d.xpath('//android.widget.Button[@resource-id="com.instagram.android:id/skip_button"]').click(timeout=2)
                            d.xpath('//android.widget.Button[@resource-id="com.instagram.android:id/negative_button"]').click(timeout=2)

                    except:
                        pass

                    try:
                        # Número do celular
                        if d.xpath('//android.widget.TextView[@resource-id="com.instagram.android:id/form_field_label_inline"]').exists:
                            print("Receba sugestões do Facebook")
                            d.xpath('//android.widget.Button[@resource-id="com.instagram.android:id/skip_button"]').click(timeout=2)

                    except:
                        pass

                    try:
                        # Convide amigos para seguirem você
                        if d.xpath('//android.widget.TextView[@resource-id="com.instagram.android:id/igds_headline_headline"]').exists:
                            print("Convide amigos para seguirem você")
                            d.xpath('//android.widget.Button[@resource-id="com.instagram.android:id/skip_button"]').click(timeout=2)

                    except:
                        pass

                    try:
                        # Convide amigos para seguirem você
                        if d.xpath('//android.widget.TextView[@content-desc="Encontrar pessoas"]').exists:
                            print("Convide amigos para seguirem você")
                            d.xpath('//android.widget.Button[@content-desc="Avançar"]/android.widget.ImageView').click(timeout=2)
                            time.sleep(0.5)

                    except:
                        pass
                    try:
                        # Tente seguir mais de 5 pessoas
                        if d.xpath('//android.widget.TextView[@content-desc="Tente seguir mais de 5 pessoas"]').exists:
                            print("Tente seguir mais de 5 pessoas")
                            time.sleep(2)
                            d.xpath('//android.widget.Button[@resource-id="com.instagram.android:id/button_text"]').click(timeout=12)

                    except:
                        pass

                    try:
                        # Ativar notificações
                        if d.xpath('//android.widget.TextView[@resource-id="com.instagram.android:id/igds_headline_body"]').exists:
                            print("Ativar notificações")
                            d.xpath('//android.widget.Button[@resource-id="com.instagram.android:id/button_text"]').click(timeout=8)

                    except:
                        pass

                    try:
                        # Receba sugestões do Facebook
                        if d.xpath('//android.view.ViewGroup[@resource-id="com.instagram.android:id/field_title_igds"]"]').exists:
                            print("Ativar notificações")
                            d.xpath('//android.widget.Button[@content-desc="Pular"]').click(timeout=8)
                            time.sleep(1)
                            d.xpath('//android.widget.Button[@resource-id="com.instagram.android:id/negative_button"]').click(timeout=8)

                    except:
                        pass

                    try:
                        # perfil
                        if d.xpath('//android.widget.FrameLayout[@content-desc="Perfil"]').exists:
                            time.sleep(1)
                            print("clicando em perfil")
                            '''
                            d.xpath('//android.widget.FrameLayout[@content-desc="Perfil"]').click()
                            try:
                                # As notificações estão desativadas no momento
                                if d.xpath('//android.view.View[@text="As notificações estão desativadas no momento"]').exists:

                                   d.xpath('//android.widget.Button[@content-desc="Dismiss"]/android.widget.ImageView').click()
                            except:
                                pass
                            # Apertar no icone Casa
                            d.xpath('(//android.widget.ImageView[@resource-id="com.instagram.android:id/tab_icon"])[1]').click()
                            time.sleep(2)
                            # Perfil 
                            d.xpath('//android.widget.FrameLayout[@content-desc="Perfil"]').click()

                            d.xpath('//android.widget.Button[@content-desc="Opções"]').click(timeout=8)

                            # Definindo o número máximo de tentativas
                            max_attempts = 3
                            attempt = 0

                            while attempt < max_attempts:
                                try:
                                    # Tenta clicar no elemento
                                    d.xpath('//android.widget.TextView[@text="Senha, segurança, dados pessoais, preferências de anúncios"]').click(timeout=8)
                                    print("Elemento encontrado e clicado.")
                                    break  # Sai do loop se a ação for bem-sucedida

                                except Exception as e:
                                    # Caso o elemento não seja encontrado, realiza o swipe
                                    print(f"Elemento não encontrado. Realizando swipe. Tentativa {attempt + 1} de {max_attempts}.")
                                    d.swipe(382, 372, 384, 923, duration=0)
                                    
                                    # Incrementa o contador de tentativas
                                    attempt += 1

                            # Verifica se todas as tentativas foram usadas sem sucesso
                            if attempt == max_attempts:
                                print("Não foi possível encontrar e clicar no elemento após várias tentativas.")
                            time.sleep(2)
                            # Clica em "Senha e segurança"
                            d.xpath('//android.view.View[@content-desc="Senha e segurança"]').click(timeout=8)
                            time.sleep(2)
                            # Clica em "Autenticação de dois fatores"
                            d.xpath('//android.view.View[@content-desc="Autenticação de dois fatores"]').click(timeout=8)
                            time.sleep(2)
                            # Clica em "Instagram"
                            d.xpath('//android.view.View[@content-desc="Instagram"]').click(timeout=8)
                            time.sleep(2)
                            d.xpath('//android.view.View[@content-desc="Avançar"]').click(timeout=8)
                            # Captura a chave dinâmica e salva em 'contas.txt'
                            # Clica no botão "Copiar chave"
                            d.xpath('//android.view.View[@content-desc="Copiar chave"]').click(timeout=8)
                            chave_dinamica = d.clipboard               
                            time.sleep(2)
                            # Gera o código usando a chave dinâmica
                            import pyotp
                            totp = pyotp.TOTP(chave_dinamica.replace(' ', ''))
                            codigo = totp.now()
                            print(f"Código gerado: {codigo}")
                            d.xpath('//android.view.View[@content-desc="Avançar"]').click(timeout=8)

                            # Insere o código no campo de entrada
                            d.xpath('//android.widget.EditText').click(timeout=8)
                            d(className='android.widget.EditText').send_keys(codigo)
                            time.sleep(2)
                            # Clica em "Avançar"
                            d.xpath('//android.view.View[@content-desc="Avançar"]').click(timeout=1)
                            time.sleep(2)
                            '''
                            with open("contas.txt", "a") as file:
                                #file.write(f"{chave_dinamica}\n")
                                email_username = email_copied.split('@')[0]
                                file.write(f"{email_username}\n")
                                file.write("Kelvin2002\n")
                            reiniciar_aplicativo(d)
                            time.sleep(1)
                            break

                    except:
                        pass
                    
                    try:
                        d.xpath('//android.widget.TextView[@text="Tente novamente mais tarde"]').click(timeout=1)
                        alternar_modo_aviao(device_id)
                        time.sleep(4)
                        reiniciar_aplicativo(d)
                        criar_conta_instagram_lite(d, device_id)   # Reinicia o loop para tentar criar outra conta
                    except:
                        pass  # Segue com a criação da conta caso não encontre o elemento


                    try:
                        # Clica no botão "Fazer uma apelação"
                        d.xpath('//android.view.View[@text="Fazer uma apelação"]').click(timeout=1)
                        '''                        
                        time.sleep(4)
                        # Captura o captcha como uma imagem e salva como "captcha.jpeg"
                        d.screenshot("captcha.jpeg")
                        print("Imagem do captcha salva como 'captcha.jpeg'")

                        # Abre a imagem e realiza o corte
                        with Image.open("captcha.jpeg") as img:
                            # Ajuste estas coordenadas para definir a área do captcha
                            left = 73  # Posição x inicial
                            top = 633   # Posição y inicial
                            right = 996  # Posição x final
                            bottom = 877  # Posição y final
                            captcha_cropped = img.crop((left, top, right, bottom))
                            captcha_cropped.save("captcha_cropped.jpeg")
                            print("Imagem do captcha cortada e salva como 'captcha_cropped.jpeg'")
                        # Configura o AntiCaptcha para resolver o captcha
                        solver = imagecaptcha()
                        solver.set_verbose(1)
                        solver.set_key("387d329fea05e04c4fd907d80f4eb276")

                        max_retries = 15  # Número máximo de tentativas
                        retry_delay = 2  # Tempo de espera entre tentativas em segundos

                        for attempt in range(max_retries):
                            try:
                                # Envia o captcha para resolução usando o caminho do arquivo diretamente
                                captcha_text = solver.solve_and_return_solution("captcha_cropped.jpeg")
                                
                                if captcha_text != 0:
                                    print("Texto do captcha:", captcha_text)
                                    
                                    # Insere o texto do captcha no campo de código
                                    d.xpath('//android.widget.EditText[@text="Código"]').set_text(captcha_text)
                                    
                                    # Clica no botão "Próximo"
                                    d.xpath('//android.view.View[@text="Próximo"]').click()
                                    time.sleep(4)
                                    # Alterna o modo avião
                                    alternar_modo_aviao(device_id)
                                    time.sleep(4)
                                    
                                    # Grava o email copiado e a senha em um arquivo
                                    with open("sms.txt", "a") as file:
                                        file.write(f"{email_copied}\n")
                                        file.write("Kelvin2002!?\n")
                                    
                                    # Reinicia o aplicativo e tenta criar outra conta
                                    reiniciar_aplicativo(d)
                                    criar_conta_instagram_lite(d, device_id)
                                    break  # Sai do loop se a resolução do captcha for bem-sucedida

                                else:
                                    print("Erro ao resolver o captcha:", solver.error_code)

                            except Exception as e:
                                print("Erro ao resolver o captcha:", e)
                                if str(e) == "ERROR_NO_SLOT_AVAILABLE" and attempt < max_retries - 1:
                                    print(f"Tentativa {attempt + 1} falhou. Aguardando {retry_delay} segundos para tentar novamente.")
                                    time.sleep(retry_delay)
                                else:
                                    print("Número máximo de tentativas atingido ou erro crítico. Encerrando.")
                                    break
                            '''
                    except u2.XPathElementNotFoundError:
                        pass  # Segue com a criação da conta caso não encontre o elemento


                    try:
                        d.xpath('//android.view.View[@text="Confirme seu número de telefone"]').click(timeout=1)
                        alternar_modo_aviao(device_id)
                        time.sleep(4)
                        reiniciar_aplicativo(d)
                        criar_conta_instagram_lite(d, device_id)    # Reinicia o loop para tentar criar outra conta
                    except u2.XPathElementNotFoundError:
                        pass  # Segue com a criação da conta caso não encontre o elemento
                    # Incrementar o contador de tentativas
                    attempt_count += 1

                    if attempt_count >= 35:
                        reiniciar_aplicativo(d)
                        criar_conta_instagram_lite(d, device_id)   # Se o número de tentativas for 5, dá um refresh na página
                        attempt_count = 0  # Reinicia o contador de tentativas

                break

        except (u2.UiObjectNotFoundError, u2.XPathElementNotFoundError) as e:
            print(f"Erro ao criar conta: {e}. Reiniciando aplicativo...")
            alternar_modo_aviao(device_id)
            time.sleep(4)
            reiniciar_aplicativo(d)
            time.sleep(5)  # Aguardar um pouco antes de tentar novamente

# Função para executar o processo principal em um dispositivo específico
def executar_processo(device_id):
    d = iniciar_driver(device_id, port=None)  # Define um valor padrão para a porta
    if d is not None:
        if iniciar_instagram_lite(d):
            criar_conta_instagram_lite(d, device_id)
    else:
        print("Falha ao conectar ao dispositivo. Processo interrompido.")

# Interface gráfica com customtkinter
# Função para salvar o device_id em um arquivo
def salvar_device_id(device_id):
    with open("config.txt", "w") as f:
        f.write(device_id)

# Função para carregar o device_id do arquivo
def carregar_device_id():
    if os.path.exists("config.txt"):
        with open("config.txt", "r") as f:
            return f.read().strip()
    return ""  # Retorna uma string vazia se o arquivo não existir

def iniciar_interface():
    def iniciar_processo():
        global executando
        device_id = entrada_device_id.get().strip()  # Obtém o device_id da entrada
        if not device_id:
            label_status.configure(text="Insira o Device ID antes de iniciar.", text_color="red")
            return

        salvar_device_id(device_id)  # Salva o device_id no arquivo
        label_status.configure(text="Processo em execução...", text_color="blue")
        executando = True  # Define a flag como True para iniciar o processo

        # Função interna que será executada na thread
        def thread_process():
            global executando
            while executando:  # Loop para tentar criar contas enquanto 'executando' for True
                try:
                    executar_processo(device_id)  # Passa apenas o device_id
                    label_status.configure(text="Processo finalizado. Reiniciando...", text_color="green")

                except Exception as e:
                    print(f"Erro durante o processo no dispositivo {device_id}: {e}.")
                    label_status.configure(text=f"Erro: {e}", text_color="red")

            if not executando:
                label_status.configure(text="Processo interrompido.", text_color="red")

        # Cria a thread para executar o processo
        processo_thread = threading.Thread(target=thread_process)
        processo_thread.daemon = True  # Configura a thread como "daemon"
        processo_thread.start()  # Inicia a thread

    def reiniciar():
        label_status.configure(text="")
        botao_reiniciar.pack_forget()

    # Função para parar o processo
    def parar():
        global executando
        executando = False  # Define a flag como False para interromper o processo
        label_status.configure(text="Processo interrompido pelo usuário.", text_color="red")

    # Função chamada quando o "X" é clicado
    def fechar_janela():
        parar()  # Interrompe o processo em execução
        janela.destroy()  # Fecha a janela da interface gráfica
        sys.exit()  # Finaliza o programa no terminal e interrompe todas as threads

    # Configurações da janela
    ctk.set_appearance_mode("dark")
    janela = ctk.CTk()
    janela.title("Gerador de Conta Instagram Lite")
    janela.geometry("400x300")

    # Capturar o evento de fechamento (clicar no "X")
    janela.protocol("WM_DELETE_WINDOW", fechar_janela)

    # Entrada para o Device ID
    label_device_id = ctk.CTkLabel(janela, text="Device ID:")
    label_device_id.pack(pady=(10, 0))
    entrada_device_id = ctk.CTkEntry(janela, width=250)
    entrada_device_id.pack(pady=(0, 10))

    # Carregar o device_id salvo, se existir
    device_id_salvo = carregar_device_id()
    entrada_device_id.insert(0, device_id_salvo)

    # Botão para iniciar o processo
    botao_iniciar = ctk.CTkButton(janela, text="Iniciar", command=iniciar_processo)
    botao_iniciar.pack(pady=10)

    # Botão para parar o processo
    botao_parar = ctk.CTkButton(janela, text="Parar", command=parar)
    botao_parar.pack(pady=10)

    # Label de status
    label_status = ctk.CTkLabel(janela, text="")
    label_status.pack(pady=10)

    # Botão reiniciar
    botao_reiniciar = ctk.CTkButton(janela, text="Reiniciar", command=reiniciar)

    janela.mainloop()

if __name__ == "__main__":
    verificar_atualizacao()
    reiniciar_programa()
    iniciar_interface()
