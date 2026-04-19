#!/usr/bin/env python3
"""
Script de atualização automática do README.md
Atualiza estatísticas dos repositórios e seção de Technical Writing
"""

import os
import requests
from datetime import datetime
from github import Github

# Configurações
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'Wanjos-eng')

# Repositórios para monitorar (substitua pelos seus reais)
REPOS_TO_SHOWCASE = [
    'GhostApply',
    'logic-forge',
    'Sua-Barbearia-backend',
    'API-CalculoNumerico',
    'rust-paris-transit-a-star'
]

def get_repo_stats(repo_name):
    """Busca estatísticas de um repositório"""
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(f"{GITHUB_USERNAME}/{repo_name}")
        return {
            'name': repo.name,
            'description': repo.description or f"Engenharia de Software - {repo.language or 'Multi-language'}",
            'language': repo.language or 'Unknown',
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'url': repo.html_url,
            'updated_at': repo.updated_at.strftime('%Y-%m-%d')
        }
    except Exception as e:
        print(f"Erro ao buscar {repo_name}: {e}")
        return None

def get_recent_activity():
    """Busca atividade recente (commits, issues fechadas)"""
    try:
        g = Github(GITHUB_TOKEN)
        user = g.get_user()
        
        # Últimos commits
        events = user.get_events(per_page=10)
        recent_commits = []
        
        for event in events:
            if event.type == 'PushEvent':
                repo_name = event.repo.name
                for commit in event.payload.get('commits', [])[:2]:
                    recent_commits.append({
                        'repo': repo_name.split('/')[1],
                        'message': commit['message'][:50],
                        'date': commit['timestamp'][:10]
                    })
        
        return recent_commits[:3]  # Retorna últimos 3 commits
    except Exception as e:
        print(f"Erro ao buscar atividade: {e}")
        return []

def generate_projects_section(repos_data):
    """Gera a seção de projetos com dados atualizados"""
    section = "### 🚀 Engineering Showcase\n\n"
    section += "<table><tr>\n"
    
    for i, repo in enumerate(repos_data[:4]):
        if repo is None:
            continue
            
        col = i % 2
        if col == 0 and i > 0:
            section += "</tr><tr>\n"
        
        section += f"""<td align="center">
<a href="{repo['url']}">
<img src="https://github-readme-stats.vercel.app/api/pin/?username={GITHUB_USERNAME}&repo={repo['name']}&theme=dark&bg_color=0D1117&border_color=30363D&title_color=58A6FF&text_color=C9D1D9&hide_border=true" alt="{repo['name']}"/>
</a>
</td>\n"""
    
    section += "</tr></table>\n"
    return section

def generate_activity_section(activity):
    """Gera a seção de atividade recente"""
    if not activity:
        return ""
    
    section = "\n### 🔨 What I'm Building Right Now\n\n"
    section += "| Repositório | Última Atividade | Data |\n"
    section += "|------------|------------------|------|\n"
    
    for act in activity:
        section += f"| [{act['repo']}](https://github.com/{GITHUB_USERNAME}/{act['repo']}) | {act['message']} | {act['date']} |\n"
    
    return section

def generate_articles_placeholder():
    """Gera placeholder para artigos (para você preencher depois)"""
    section = "\n### 📝 Technical Writing & Documentation\n\n"
    section += "> 📌 **Em breve:** Documentações técnicas e artigos sobre arquitetura de software.\n\n"
    section += "<!-- \nINSTRUÇÕES PARA ADICIONAR ARTIGOS:\n1. Coloque seus PDFs/documentações em uma pasta /docs no seu perfil\n2. Ou publique no Medium/Dev.to e atualize os links abaixo\n3. Exemplo de formato:\n\n- [Título do Artigo](link) - Breve descrição\n- [Clean Architecture em Go](link) - Como implementei domain-driven design\n- [Algoritmos de Busca em Rust](link) - A* e otimizações de performance\n-->\n"
    
    return section

def update_readme():
    """Função principal de atualização"""
    print(f"🔄 Atualizando README para {GITHUB_USERNAME}...")
    
    # Busca dados dos repositórios
    repos_data = [get_repo_stats(repo) for repo in REPOS_TO_SHOWCASE]
    repos_data = [r for r in repos_data if r is not None]  # Remove nulos
    
    # Busca atividade recente
    activity = get_recent_activity()
    
    # Lê o README atual
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ README.md não encontrado!")
        return
    
    # Marcações para inserção (placeholders)
    markers = {
        '<!-- PROJECTS_SECTION -->': generate_projects_section(repos_data),
        '<!-- ACTIVITY_SECTION -->': generate_activity_section(activity),
        '<!-- ARTICLES_SECTION -->': generate_articles_placeholder()
    }
    
    # Atualiza conteúdo
    updated = False
    for marker, new_content in markers.items():
        if marker in content:
            # Encontra a seção entre o marcador e o próximo marcador ou fim
            start_idx = content.find(marker)
            if start_idx != -1:
                # Procura o próximo marcador ou usa o fim do arquivo
                next_marker_idx = len(content)
                for m in markers.keys():
                    if m != marker:
                        idx = content.find(m, start_idx + len(marker))
                        if idx != -1 and idx < next_marker_idx:
                            next_marker_idx = idx
                
                # Substitui apenas o marcador, mantendo o conteúdo gerado após ele
                # (o conteúdo gerado já inclui tudo necessário)
                content = content[:start_idx] + marker + '\n' + new_content + content[next_marker_idx:]
                updated = True
                print(f"✅ Seção atualizada: {marker}")
    
    if updated:
        # Adiciona timestamp
        timestamp = f"\n\n_Última atualização automática: {datetime.now().strftime('%d/%m/%Y às %H:%M UTC')}_"
        
        # Remove timestamp antigo se existir
        import re
        content = re.sub(r'\n_Última atualização automática:.*?_', '', content)
        content = content.rstrip() + timestamp + '\n'
        
        # Salva o README atualizado
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ README atualizado com sucesso!")
    else:
        print("⚠️ Nenhum marcador encontrado. Verifique se o README tem os placeholders corretos.")

if __name__ == '__main__':
    update_readme()
