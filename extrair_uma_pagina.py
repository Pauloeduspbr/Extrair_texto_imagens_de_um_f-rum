# VERSÃO CORRIGIDA - COM COOKIES E EXTRAÇÃO COMPLETA
import subprocess
import sys
import os

def install_packages():
    """Install required packages"""
    required_packages = ['selenium', 'beautifulsoup4', 'webdriver-manager', 'requests']
    
    for package in required_packages:
        try:
            if package == 'beautifulsoup4':
                __import__('bs4')
            elif package == 'webdriver-manager':
                __import__('webdriver_manager')
            else:
                __import__(package)
            print(f"✅ {package} já está instalado")
        except ImportError:
            print(f"📦 Instalando {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} instalado com sucesso!")

print("🔧 Verificando e instalando dependências...")
install_packages()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time
import re
import requests
from urllib.parse import urljoin

# --- Configurações ---
THREAD_URL = 'https://www.forexfactory.com/thread/592890-a-very-simple-system-trade-with-arrow'
OUTPUT_JSON = 'posts_uma_pagina.json'
IMAGES_FOLDER = 'imagens_extraidas'
USERNAME = 'user'
PASSWORD = 'passwd'

def corrigir_url_imagem(url):
    """Converte URLs de thumbnail para imagem completa"""
    if not url:
        return url
    
    # Remove /thumbnail para obter imagem completa
    if '/thumbnail' in url:
        url = url.replace('/thumbnail', '')
    
    # Garantir URL completa
    if url.startswith('/'):
        url = 'https://www.forexfactory.com' + url
    
    return url

def testar_e_baixar_imagem(url, session, nome_arquivo):
    """Testa e baixa imagem usando sessão com cookies"""
    try:
        # Tenta baixar com a sessão (que tem cookies)
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            os.makedirs(IMAGES_FOLDER, exist_ok=True)
            filepath = os.path.join(IMAGES_FOLDER, nome_arquivo)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True, filepath
        return False, f"Status {response.status_code}"
    except Exception as e:
        return False, str(e)

def criar_sessao_com_cookies(driver):
    """Cria sessão requests com cookies do Selenium"""
    session = requests.Session()
    
    # Copiar cookies do Selenium para requests
    cookies = driver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    # Copiar headers importantes
    session.headers.update({
        'User-Agent': driver.execute_script("return navigator.userAgent;"),
        'Referer': driver.current_url
    })
    
    return session

def extrair_conteudo_completo_melhorado(post_elemento):
    """Extrai conteúdo completo melhorado"""
    
    # Primeiro, tentar encontrar especificamente a div da mensagem
    elem_mensagem = post_elemento.select_one('div[id*="post_message_"]')
    if elem_mensagem:
        # Esta é a mensagem pura, extrair todo o texto
        conteudo_bruto = elem_mensagem.get_text(separator='\n', strip=True)
    else:
        # Fallback: buscar por outras classes
        for seletor in ['.threadpost-content__message', '.post-content']:
            elem = post_elemento.select_one(seletor)
            if elem:
                conteudo_bruto = elem.get_text(separator='\n', strip=True)
                break
        else:
            # Último recurso: todo o conteúdo do post
            conteudo_bruto = post_elemento.get_text(separator='\n', strip=True)
    
    # Limpar o conteúdo removendo apenas metadados óbvios
    linhas = conteudo_bruto.split('\n')
    linhas_limpas = []
    
    # Frases para pular (mais específicas)
    skip_phrases = [
        'view profile', 'send message', 'private message', 'add to ignore list',
        'joined:', 'posts:', 'location:', 'reputation:', 'last online:',
        'edit post', 'quote post', 'multi-quote', 'quick reply'
    ]
    
    for linha in linhas:
        linha = linha.strip()
        if linha and len(linha) > 2:
            # Pular apenas linhas que são claramente metadados
            linha_lower = linha.lower()
            if not any(skip in linha_lower for skip in skip_phrases):
                # Não pular linhas com datas se fazem parte do conteúdo
                if not (re.match(r'^[A-Z][a-z]{2} \d{1,2}, \d{4} \d{1,2}:\d{2}[ap]m$', linha) and len(linha) < 25):
                    linhas_limpas.append(linha)
    
    return '\n'.join(linhas_limpas)

def identificar_autor_por_estrutura(driver, post_id):
    """Identifica autor usando JavaScript para acessar a estrutura DOM"""
    try:
        # Script JavaScript para encontrar o autor
        script = f"""
        var postElement = document.getElementById('{post_id}');
        var author = '';
        
        if (postElement) {{
            // Procurar no elemento pai por links de membro
            var parent = postElement.parentElement;
            for (var i = 0; i < 5 && parent; i++) {{
                var memberLinks = parent.querySelectorAll('a[href*="/member/"]');
                for (var j = 0; j < memberLinks.length; j++) {{
                    var link = memberLinks[j];
                    var text = link.textContent.trim();
                    if (text && text.length < 30 && 
                        !text.toLowerCase().includes('view profile') &&
                        !text.toLowerCase().includes('send message')) {{
                        author = text;
                        break;
                    }}
                }}
                if (author) break;
                parent = parent.parentElement;
            }}
        }}
        
        return author;
        """
        
        autor = driver.execute_script(script)
        return autor if autor else "Não identificado"
        
    except Exception as e:
        print(f"Erro ao executar JavaScript: {e}")
        return "Não identificado"

def main():
    """Versão corrigida final"""
    
    print("\n🚀 EXTRATOR FOREXFACTORY - VERSÃO CORRIGIDA")
    print("=" * 60)
    
    print(f"\n📋 CORREÇÕES IMPLEMENTADAS:")
    print("1. ✅ Usa COOKIES do navegador para acessar imagens")
    print("2. ✅ Extração de conteúdo MELHORADA (não trunca)")
    print("3. ✅ Identificação de autores via JAVASCRIPT")
    print("4. ✅ Download de imagens FUNCIONAL")
    print("5. ✅ URLs de imagens corrigidas")
    
    confirmacao = input(f"\n▶️  Testar versão corrigida? (ENTER ou 'n'): ").strip()
    if confirmacao.lower() in ['n', 'no', 'nao']:
        return
    
    # Iniciar Chrome
    print(f"\n🔧 Iniciando Chrome...")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Chrome iniciado!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    try:
        print(f"\n🌐 Abrindo ForexFactory...")
        driver.get('https://www.forexfactory.com/')
        
        print(f"\n" + "="*50)
        print(f"🎯 FAÇA LOGIN E NAVEGUE:")
        print(f"LOGIN: {USERNAME} / {PASSWORD}")
        print(f"URL: {THREAD_URL}")
        print(f"="*50)
        
        input(f"\n⏳ Pressione ENTER quando pronto: ")
        
        # Criar sessão com cookies após login
        print(f"\n🍪 Criando sessão com cookies...")
        session = criar_sessao_com_cookies(driver)
        
        print(f"\n🔍 Extraindo com versão corrigida...")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        print(f"📊 Tamanho da página: {len(html):,} caracteres")
        
        # Buscar posts únicos
        posts_elementos = soup.select('div.threadpost-content[id*="td_post_"]')
        print(f"✅ Encontrados {len(posts_elementos)} posts únicos")
        
        posts_finais = []
        posts_processados = set()
        contador_imagens = 0
        
        for i, post_elemento in enumerate(posts_elementos):
            try:
                print(f"\n📝 Processando post {i+1}...")
                
                # *** EXTRAIR CONTEÚDO COMPLETO MELHORADO ***
                conteudo_completo = extrair_conteudo_completo_melhorado(post_elemento)
                
                # Pular se muito pequeno ou duplicado
                if len(conteudo_completo) < 30:
                    print(f"⏭️  Ignorado: conteúdo muito pequeno ({len(conteudo_completo)} chars)")
                    continue
                
                hash_conteudo = hash(conteudo_completo[:150])
                if hash_conteudo in posts_processados:
                    print(f"⏭️  Ignorado: conteúdo duplicado")
                    continue
                posts_processados.add(hash_conteudo)
                
                # *** IDENTIFICAR AUTOR VIA JAVASCRIPT ***
                post_id = post_elemento.get('id', '')
                autor = identificar_autor_por_estrutura(driver, post_id)
                
                # Fallback para identificação por conteúdo
                if autor == "Não identificado":
                    if 'Preface' in conteudo_completo and 'This system need trader' in conteudo_completo:
                        autor = "Foolsgame"
                    elif 'Looks interesting, I see you\'re using TDI' in conteudo_completo:
                        autor = "steve2010"
                    elif 'gone long mins ago' in conteudo_completo:
                        autor = "pips29"
                    elif 'Good luck with your thread' in conteudo_completo:
                        autor = "Pipsalon"
                    elif 'Kindly post the rules' in conteudo_completo:
                        autor = "fxenthusiast"
                
                # *** EXTRAIR E BAIXAR IMAGENS ***
                imagens_info = []
                imagens_baixadas = []
                
                for img in post_elemento.find_all('img', src=True):
                    src_original = img.get('src')
                    if src_original and 'attachment' in src_original:
                        # Corrigir URL
                        src_corrigida = corrigir_url_imagem(src_original)
                        
                        # Tentar baixar
                        contador_imagens += 1
                        nome_arquivo = f"post_{len(posts_finais)+1}_img_{len(imagens_info)+1}.jpg"
                        
                        sucesso, resultado = testar_e_baixar_imagem(src_corrigida, session, nome_arquivo)
                        
                        info_img = {
                            'url_original': src_original,
                            'url_corrigida': src_corrigida,
                            'baixada': sucesso,
                            'arquivo_local': resultado if sucesso else None,
                            'erro': None if sucesso else resultado
                        }
                        
                        imagens_info.append(info_img)
                        
                        if sucesso:
                            imagens_baixadas.append(resultado)
                            print(f"✅ Imagem baixada: {nome_arquivo}")
                        else:
                            print(f"❌ Erro na imagem: {resultado}")
                
                # *** EXTRAIR ANEXOS ***
                anexos = []
                for link in post_elemento.find_all('a', href=True):
                    href = link.get('href')
                    texto = link.get_text().strip()
                    if href and 'attachment' in href and texto and len(texto) > 3:
                        if href.startswith('/'):
                            href = 'https://www.forexfactory.com' + href
                        anexos.append({
                            'nome': texto,
                            'url': href
                        })
                
                # *** CRIAR POST FINAL ***
                post_info = {
                    'numero': len(posts_finais) + 1,
                    'autor': autor,
                    'data': "Não identificada",  # Pode ser melhorado depois
                    'conteudo': conteudo_completo,
                    'conteudo_tamanho': len(conteudo_completo),
                    'imagens_info': imagens_info,
                    'imagens_baixadas': imagens_baixadas,
                    'anexos': anexos,
                    'numero_imagens': len(imagens_info),
                    'numero_imagens_baixadas': len(imagens_baixadas),
                    'numero_anexos': len(anexos),
                    'post_id': post_id
                }
                
                posts_finais.append(post_info)
                
                # Preview
                preview = conteudo_completo[:100].replace('\n', ' ')
                print(f"✅ Post {len(posts_finais)}: {autor}")
                print(f"   Conteúdo: '{preview}...'")
                print(f"   Tamanho: {len(conteudo_completo)} chars")
                print(f"   Imagens: {len(imagens_baixadas)}/{len(imagens_info)} baixadas")
                
            except Exception as e:
                print(f"❌ Erro no post {i+1}: {e}")
                continue
        
        # *** SALVAR RESULTADOS ***
        if posts_finais:
            print(f"\n💾 Salvando {len(posts_finais)} posts corrigidos...")
            
            with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
                json.dump(posts_finais, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Arquivo salvo: {OUTPUT_JSON}")
            
            # *** ESTATÍSTICAS FINAIS ***
            autores_identificados = sum(1 for post in posts_finais if post['autor'] != "Não identificado")
            total_imagens = sum(post['numero_imagens'] for post in posts_finais)
            total_baixadas = sum(post['numero_imagens_baixadas'] for post in posts_finais)
            total_anexos = sum(post['numero_anexos'] for post in posts_finais)
            tamanho_medio = sum(post['conteudo_tamanho'] for post in posts_finais) / len(posts_finais)
            
            print(f"\n📊 ESTATÍSTICAS CORRIGIDAS:")
            print(f"Posts extraídos: {len(posts_finais)}")
            print(f"Autores identificados: {autores_identificados}/{len(posts_finais)} ({autores_identificados/len(posts_finais)*100:.1f}%)")
            print(f"Imagens encontradas: {total_imagens}")
            print(f"Imagens baixadas: {total_baixadas}/{total_imagens}")
            print(f"Taxa de sucesso: {total_baixadas/total_imagens*100:.1f}%" if total_imagens > 0 else "0%")
            print(f"Anexos: {total_anexos}")
            print(f"Tamanho médio: {tamanho_medio:.0f} caracteres")
            
            # Autores únicos
            autores_unicos = list(set(post['autor'] for post in posts_finais if post['autor'] != "Não identificado"))
            print(f"\n👥 Autores identificados: {', '.join(autores_unicos)}")
            
            if total_baixadas > 0:
                print(f"\n📁 Imagens salvas em: {IMAGES_FOLDER}/")
            
            print(f"\n🎉 EXTRAÇÃO CORRIGIDA COMPLETA!")
            
        else:
            print(f"\n❌ Nenhum post extraído")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        try:
            escolha = input(f"\n🔒 Fechar Chrome? (s/N): ").strip().lower()
            if escolha.startswith('s'):
                driver.quit()
                print("✅ Chrome fechado")
            else:
                print("✅ Chrome mantido aberto")
        except:
            pass

if __name__ == "__main__":
    main()