# EXTRATOR MULTI-PÁGINAS - TÓPICO COMPLETO
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
from urllib.parse import urljoin, urlparse, parse_qs
import os
from datetime import datetime

# --- Configurações ---
THREAD_URL = 'https://www.forexfactory.com/thread/592890-a-very-simple-system-trade-with-arrow'
OUTPUT_DIR = 'topico_completo'
IMAGES_DIR = 'imagens_por_pagina'
USERNAME = 'user'
PASSWORD = 'passwd'

def criar_estrutura_diretorios():
    """Cria estrutura de diretórios organizados"""
    
    # Diretório principal
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Subdiretórios
    os.makedirs(os.path.join(OUTPUT_DIR, 'json_por_pagina'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'imagens_por_pagina'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'resumos'), exist_ok=True)
    
    print(f"📁 Estrutura criada em: {OUTPUT_DIR}/")

def detectar_total_paginas(soup):
    """Detecta o número total de páginas do tópico"""
    
    try:
        # Buscar paginação - diferentes seletores possíveis
        seletores_paginacao = [
            '.pagination a',
            '.pagelinks a',
            'td.alt1 a[href*="page"]',
            'div[class*="pagination"] a',
            'span[class*="pagination"] a'
        ]
        
        total_paginas = 1
        
        for seletor in seletores_paginacao:
            links_pagina = soup.select(seletor)
            if links_pagina:
                for link in links_pagina:
                    href = link.get('href', '')
                    texto = link.get_text().strip()
                    
                    # Buscar por números de página na URL
                    if 'page=' in href:
                        try:
                            parsed = urlparse(href)
                            query_params = parse_qs(parsed.query)
                            if 'page' in query_params:
                                pagina = int(query_params['page'][0])
                                total_paginas = max(total_paginas, pagina)
                        except:
                            pass
                    
                    # Buscar por números no texto do link
                    if texto.isdigit():
                        try:
                            pagina = int(texto)
                            total_paginas = max(total_paginas, pagina)
                        except:
                            pass
                
                if total_paginas > 1:
                    break
        
        # Fallback: buscar por "Last Page" ou similar
        if total_paginas == 1:
            last_links = soup.select('a[title*="Last"], a[href*="lastpost"], a[title*="Última"]')
            for link in last_links:
                href = link.get('href', '')
                if 'page=' in href:
                    try:
                        parsed = urlparse(href)
                        query_params = parse_qs(parsed.query)
                        if 'page' in query_params:
                            total_paginas = int(query_params['page'][0])
                            break
                    except:
                        pass
        
        return max(total_paginas, 1)
        
    except Exception as e:
        print(f"⚠️  Erro ao detectar páginas: {e}")
        return 1

def construir_url_pagina(base_url, numero_pagina):
    """Constrói URL para uma página específica"""
    
    if numero_pagina == 1:
        return base_url
    
    # ForexFactory usa ?page=N
    if '?' in base_url:
        return f"{base_url}&page={numero_pagina}"
    else:
        return f"{base_url}?page={numero_pagina}"

def criar_sessao_com_cookies(driver):
    """Cria sessão requests com cookies do Selenium"""
    session = requests.Session()
    
    cookies = driver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    session.headers.update({
        'User-Agent': driver.execute_script("return navigator.userAgent;"),
        'Referer': driver.current_url
    })
    
    return session

def extrair_conteudo_post(post_elemento):
    """Extrai conteúdo completo do post"""
    
    elem_mensagem = post_elemento.select_one('div[id*="post_message_"]')
    if elem_mensagem:
        conteudo_bruto = elem_mensagem.get_text(separator='\n', strip=True)
    else:
        for seletor in ['.threadpost-content__message', '.post-content']:
            elem = post_elemento.select_one(seletor)
            if elem:
                conteudo_bruto = elem.get_text(separator='\n', strip=True)
                break
        else:
            conteudo_bruto = post_elemento.get_text(separator='\n', strip=True)
    
    # Limpar conteúdo
    linhas = conteudo_bruto.split('\n')
    linhas_limpas = []
    
    skip_phrases = [
        'view profile', 'send message', 'private message', 'add to ignore list',
        'joined:', 'posts:', 'location:', 'reputation:', 'last online:',
        'edit post', 'quote post', 'multi-quote', 'quick reply'
    ]
    
    for linha in linhas:
        linha = linha.strip()
        if linha and len(linha) > 2:
            linha_lower = linha.lower()
            if not any(skip in linha_lower for skip in skip_phrases):
                if not (re.match(r'^[A-Z][a-z]{2} \d{1,2}, \d{4} \d{1,2}:\d{2}[ap]m$', linha) and len(linha) < 25):
                    linhas_limpas.append(linha)
    
    return '\n'.join(linhas_limpas)

def identificar_autor_avancado(driver, post_id):
    """Identifica autor usando JavaScript"""
    try:
        script = f"""
        var postElement = document.getElementById('{post_id}');
        var author = '';
        
        if (postElement) {{
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
        
    except:
        return "Não identificado"

def baixar_imagens_pagina(post_elemento, session, pagina_num, post_num):
    """Baixa imagens de um post específico"""
    
    imagens_info = []
    imagens_baixadas = []
    
    pasta_pagina = os.path.join(OUTPUT_DIR, 'imagens_por_pagina', f'pagina_{pagina_num}')
    os.makedirs(pasta_pagina, exist_ok=True)
    
    for i, img in enumerate(post_elemento.find_all('img', src=True)):
        src_original = img.get('src')
        if src_original and 'attachment' in src_original:
            
            # Corrigir URL (remover /thumbnail)
            src_corrigida = src_original.replace('/thumbnail', '')
            if src_corrigida.startswith('/'):
                src_corrigida = 'https://www.forexfactory.com' + src_corrigida
            
            # Nome do arquivo
            nome_arquivo = f"pagina_{pagina_num}_post_{post_num}_img_{i+1}.jpg"
            caminho_arquivo = os.path.join(pasta_pagina, nome_arquivo)
            
            # Tentar baixar
            try:
                response = session.get(src_corrigida, timeout=10)
                if response.status_code == 200:
                    with open(caminho_arquivo, 'wb') as f:
                        f.write(response.content)
                    
                    imagens_baixadas.append({
                        'nome_arquivo': nome_arquivo,
                        'caminho_local': caminho_arquivo,
                        'url_original': src_original,
                        'url_corrigida': src_corrigida,
                        'tamanho_bytes': len(response.content)
                    })
                    
                    print(f"    ✅ Imagem: {nome_arquivo}")
                else:
                    print(f"    ❌ Erro {response.status_code}: {nome_arquivo}")
                    
            except Exception as e:
                print(f"    ❌ Erro ao baixar {nome_arquivo}: {e}")
            
            imagens_info.append({
                'url_original': src_original,
                'url_corrigida': src_corrigida,
                'nome_arquivo': nome_arquivo,
                'baixada': len(imagens_baixadas) > 0 and imagens_baixadas[-1]['nome_arquivo'] == nome_arquivo
            })
    
    return imagens_info, imagens_baixadas

def processar_pagina(driver, session, pagina_num, total_paginas):
    """Processa uma página específica do tópico"""
    
    print(f"\n📄 PROCESSANDO PÁGINA {pagina_num}/{total_paginas}")
    print("=" * 50)
    
    # Obter HTML da página
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # Buscar posts da página
    posts_elementos = soup.select('div.threadpost-content[id*="td_post_"]')
    print(f"✅ Encontrados {len(posts_elementos)} posts na página {pagina_num}")
    
    posts_pagina = []
    posts_processados = set()
    
    for i, post_elemento in enumerate(posts_elementos):
        try:
            print(f"  📝 Processando post {i+1}...")
            
            # Extrair conteúdo
            conteudo = extrair_conteudo_post(post_elemento)
            
            if len(conteudo) < 30:
                print(f"    ⏭️  Ignorado: muito pequeno ({len(conteudo)} chars)")
                continue
            
            # Verificar duplicatas
            hash_conteudo = hash(conteudo[:150])
            if hash_conteudo in posts_processados:
                print(f"    ⏭️  Ignorado: duplicado")
                continue
            posts_processados.add(hash_conteudo)
            
            # Identificar autor
            post_id = post_elemento.get('id', '')
            autor = identificar_autor_avancado(driver, post_id)
            
            # Baixar imagens
            imagens_info, imagens_baixadas = baixar_imagens_pagina(
                post_elemento, session, pagina_num, len(posts_pagina) + 1
            )
            
            # Extrair anexos
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
            
            # Criar post
            post_info = {
                'numero_na_pagina': len(posts_pagina) + 1,
                'numero_global': None,  # Será calculado depois
                'autor': autor,
                'data': "Não identificada",
                'conteudo': conteudo,
                'conteudo_tamanho': len(conteudo),
                'imagens_info': imagens_info,
                'imagens_baixadas': imagens_baixadas,
                'anexos': anexos,
                'numero_imagens': len(imagens_info),
                'numero_imagens_baixadas': len(imagens_baixadas),
                'numero_anexos': len(anexos),
                'post_id': post_id,
                'pagina': pagina_num
            }
            
            posts_pagina.append(post_info)
            
            # Preview
            preview = conteudo[:80].replace('\n', ' ')
            print(f"    ✅ {autor}: '{preview}...' ({len(conteudo)} chars, {len(imagens_baixadas)} imgs)")
            
        except Exception as e:
            print(f"    ❌ Erro no post {i+1}: {e}")
            continue
    
    # Salvar JSON da página
    arquivo_pagina = os.path.join(OUTPUT_DIR, 'json_por_pagina', f'pagina_{pagina_num}.json')
    
    dados_pagina = {
        'pagina': pagina_num,
        'total_paginas': total_paginas,
        'url': driver.current_url,
        'timestamp': datetime.now().isoformat(),
        'posts_encontrados': len(posts_elementos),
        'posts_extraidos': len(posts_pagina),
        'posts': posts_pagina
    }
    
    with open(arquivo_pagina, 'w', encoding='utf-8') as f:
        json.dump(dados_pagina, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Página {pagina_num} salva: {len(posts_pagina)} posts extraídos")
    
    return dados_pagina

def gerar_resumo_final(todas_paginas):
    """Gera resumo final de todo o tópico"""
    
    print(f"\n📊 GERANDO RESUMO FINAL...")
    
    # Calcular estatísticas globais
    total_posts = 0
    total_imagens = 0
    total_anexos = 0
    autores_unicos = set()
    posts_por_autor = {}
    
    # Renumerar posts globalmente
    numero_global = 1
    
    for pagina_dados in todas_paginas:
        for post in pagina_dados['posts']:
            post['numero_global'] = numero_global
            numero_global += 1
            
            total_posts += 1
            total_imagens += post['numero_imagens_baixadas']
            total_anexos += post['numero_anexos']
            
            autor = post['autor']
            autores_unicos.add(autor)
            
            if autor not in posts_por_autor:
                posts_por_autor[autor] = 0
            posts_por_autor[autor] += 1
    
    # Criar resumo
    resumo = {
        'topico_url': THREAD_URL,
        'timestamp_extracao': datetime.now().isoformat(),
        'estatisticas': {
            'total_paginas': len(todas_paginas),
            'total_posts': total_posts,
            'total_imagens_baixadas': total_imagens,
            'total_anexos': total_anexos,
            'autores_unicos': len(autores_unicos),
            'posts_por_autor': posts_por_autor
        },
        'estrutura_arquivos': {
            'json_por_pagina': f"{OUTPUT_DIR}/json_por_pagina/",
            'imagens_por_pagina': f"{OUTPUT_DIR}/imagens_por_pagina/",
            'resumo_completo': f"{OUTPUT_DIR}/resumos/topico_completo.json"
        },
        'paginas': [
            {
                'pagina': p['pagina'],
                'posts': len(p['posts']),
                'url': p['url']
            } for p in todas_paginas
        ]
    }
    
    # Salvar resumo
    arquivo_resumo = os.path.join(OUTPUT_DIR, 'resumos', 'resumo_geral.json')
    with open(arquivo_resumo, 'w', encoding='utf-8') as f:
        json.dump(resumo, f, ensure_ascii=False, indent=2)
    
    # Salvar todas as páginas em um único arquivo
    arquivo_completo = os.path.join(OUTPUT_DIR, 'resumos', 'topico_completo.json')
    with open(arquivo_completo, 'w', encoding='utf-8') as f:
        json.dump(todas_paginas, f, ensure_ascii=False, indent=2)
    
    return resumo

def main():
    """Função principal - extração multi-páginas"""
    
    print("\n🚀 EXTRATOR FOREXFACTORY - TÓPICO COMPLETO")
    print("=" * 65)
    
    print(f"\n📋 FUNCIONALIDADES:")
    print("1. ✅ Detecta TODAS as páginas do tópico")
    print("2. ✅ Navega automaticamente por cada página")
    print("3. ✅ Organização por PÁGINA (posts + imagens)")
    print("4. ✅ Estrutura hierárquica clara")
    print("5. ✅ Resumo final com estatísticas")
    
    confirmacao = input(f"\n▶️  Extrair tópico completo? (ENTER ou 'n'): ").strip()
    if confirmacao.lower() in ['n', 'no', 'nao']:
        return
    
    # Criar estrutura de diretórios
    criar_estrutura_diretorios()
    
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
        print(f"🎯 FAÇA LOGIN E NAVEGUE PARA A PRIMEIRA PÁGINA:")
        print(f"LOGIN: {USERNAME} / {PASSWORD}")
        print(f"URL: {THREAD_URL}")
        print(f"="*50)
        
        input(f"\n⏳ Pressione ENTER quando estiver na PRIMEIRA página: ")
        
        # Criar sessão com cookies
        print(f"\n🍪 Criando sessão com cookies...")
        session = criar_sessao_com_cookies(driver)
        
        # Detectar total de páginas
        print(f"\n🔍 Detectando número total de páginas...")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        total_paginas = detectar_total_paginas(soup)
        
        print(f"📊 TOTAL DE PÁGINAS DETECTADAS: {total_paginas}")
        
        if total_paginas > 10:
            confirmacao = input(f"\n⚠️  {total_paginas} páginas detectadas. Continuar? (s/N): ")
            if not confirmacao.lower().startswith('s'):
                print("❌ Cancelado pelo usuário")
                return
        
        # Processar todas as páginas
        todas_paginas = []
        
        for pagina_num in range(1, total_paginas + 1):
            try:
                # Navegar para a página (se não for a primeira)
                if pagina_num > 1:
                    url_pagina = construir_url_pagina(THREAD_URL, pagina_num)
                    print(f"\n🧭 Navegando para página {pagina_num}: {url_pagina}")
                    driver.get(url_pagina)
                    time.sleep(2)  # Aguardar carregamento
                
                # Processar página atual
                dados_pagina = processar_pagina(driver, session, pagina_num, total_paginas)
                todas_paginas.append(dados_pagina)
                
                # Pausa entre páginas
                if pagina_num < total_paginas:
                    time.sleep(1)
                
            except Exception as e:
                print(f"❌ Erro na página {pagina_num}: {e}")
                continue
        
        # Gerar resumo final
        resumo = gerar_resumo_final(todas_paginas)
        
        # Exibir estatísticas finais
        print(f"\n" + "="*60)
        print(f"🎉 EXTRAÇÃO COMPLETA FINALIZADA!")
        print(f"="*60)
        print(f"📊 ESTATÍSTICAS FINAIS:")
        print(f"  Páginas processadas: {resumo['estatisticas']['total_paginas']}")
        print(f"  Posts extraídos: {resumo['estatisticas']['total_posts']}")
        print(f"  Imagens baixadas: {resumo['estatisticas']['total_imagens_baixadas']}")
        print(f"  Anexos encontrados: {resumo['estatisticas']['total_anexos']}")
        print(f"  Autores únicos: {resumo['estatisticas']['autores_unicos']}")
        
        print(f"\n📁 ARQUIVOS CRIADOS:")
        print(f"  📄 JSON por página: {OUTPUT_DIR}/json_por_pagina/")
        print(f"  🖼️  Imagens por página: {OUTPUT_DIR}/imagens_por_pagina/")
        print(f"  📊 Resumos: {OUTPUT_DIR}/resumos/")
        
        print(f"\n🏆 TÓPICO COMPLETO EXTRAÍDO COM SUCESSO!")
        
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