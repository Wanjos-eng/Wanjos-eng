#!/usr/bin/env python3
"""
Script de atualização automática do README.md
Atualiza estatísticas dos repositórios e seção de atividade recente.
 
Usa marcadores START/END para substituição segura:
  <!-- SECTION_START --> ... conteúdo gerado ... <!-- SECTION_END -->
"""
 
import os
import re
from datetime import datetime, timezone
from github import Github
 
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME', 'Wanjos-eng')
 
REPOS_TO_SHOWCASE = [
    'GhostApply',
    'logic-forge',
    'Sua-Barbearia-backend',
    'API-CalculoNumerico',
    'rust-paris-transit-a-star',
]
 
 
# ---------------------------------------------------------------------------
# Busca de dados via API
# ---------------------------------------------------------------------------
 
def get_repo_stats(g: Github, repo_name: str) -> dict | None:
    try:
        repo = g.get_repo(f"{GITHUB_USERNAME}/{repo_name}")
        return {
            'name': repo.name,
            'description': repo.description or f"Engenharia de Software — {repo.language or 'Multi-language'}",
            'language': repo.language or 'Unknown',
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'url': repo.html_url,
            'updated_at': repo.updated_at.strftime('%Y-%m-%d'),
        }
    except Exception as e:
        print(f"⚠️  Repo não encontrado ou privado: {repo_name} ({e})")
        return None
 
 
def get_recent_activity(g: Github) -> list[dict]:
    try:
        user = g.get_user()
        recent: list[dict] = []
        for event in user.get_events(per_page=30):
            if event.type != 'PushEvent':
                continue
            repo_short = event.repo.name.split('/')[-1]
            for commit in event.payload.get('commits', [])[:2]:
                msg = commit['message'].split('\n')[0][:60]
                ts = commit.get('timestamp', '')[:10]
                recent.append({'repo': repo_short, 'message': msg, 'date': ts})
            if len(recent) >= 5:
                break
        return recent[:5]
    except Exception as e:
        print(f"⚠️  Erro ao buscar atividade: {e}")
        return []
 
 
# ---------------------------------------------------------------------------
# Geração de seções Markdown
# ---------------------------------------------------------------------------
 
def generate_projects_section(repos: list[dict]) -> str:
    lines = [f'<h2 align="center">🚀 Engineering Showcase</h2>\n', '<table align="center">']
    valid = [r for r in repos if r]
    for i in range(0, len(valid), 2):
        lines.append('  <tr>')
        for repo in valid[i:i+2]:
            lines.append(f"""    <td>
      <a href="{repo['url']}">
        <img src="https://github-readme-stats.vercel.app/api/pin/?username={GITHUB_USERNAME}&repo={repo['name']}&theme=dark&hide_border=true&bg_color=00000000" alt="{repo['name']}"/>
      </a>
      <br/><sub><b>{repo['name']}</b> — {repo['description']}</sub>
    </td>""")
        lines.append('  </tr>')
    lines.append('</table>')
    return '\n'.join(lines)
 
 
def generate_activity_section(activity: list[dict]) -> str:
    if not activity:
        return ''
    lines = [
        '<h2 align="center">🔨 Recent Activity</h2>\n',
        '| Repositório | Último Commit | Data |',
        '|---|---|---|',
    ]
    for act in activity:
        lines.append(
            f"| [{act['repo']}](https://github.com/{GITHUB_USERNAME}/{act['repo']}) "
            f"| {act['message']} | {act['date']} |"
        )
    return '\n'.join(lines)
 
 
def generate_articles_section() -> str:
    return (
        '<h2 align="center">📝 Technical Writing & Documentation</h2>\n\n'
        '> 📌 **Em breve:** Documentações técnicas e artigos sobre arquitetura de software.\n'
    )
 
 
# ---------------------------------------------------------------------------
# Substituição segura com marcadores START/END
# ---------------------------------------------------------------------------
 
def replace_section(content: str, section_name: str, new_body: str) -> str:
    """
    Substitui o conteúdo entre <!-- SECTION_START --> e <!-- SECTION_END -->.
    Se os marcadores não existirem, retorna o conteúdo sem alteração e avisa.
    """
    start_tag = f'<!-- {section_name}_START -->'
    end_tag   = f'<!-- {section_name}_END -->'
 
    pattern = re.compile(
        re.escape(start_tag) + r'.*?' + re.escape(end_tag),
        re.DOTALL,
    )
 
    if not pattern.search(content):
        print(f"⚠️  Marcadores não encontrados: {section_name}")
        return content
 
    replacement = f'{start_tag}\n{new_body}\n{end_tag}'
    updated = pattern.sub(replacement, content)
    print(f"✅ Seção atualizada: {section_name}")
    return updated
 
 
# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
 
def update_readme() -> None:
    print(f"🔄 Iniciando atualização do README para {GITHUB_USERNAME}...")
 
    g = Github(GITHUB_TOKEN)
 
    repos_data  = [get_repo_stats(g, name) for name in REPOS_TO_SHOWCASE]
    activity    = get_recent_activity(g)
 
    readme_path = 'README.md'
    try:
        with open(readme_path, encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ {readme_path} não encontrado!")
        return
 
    content = replace_section(content, 'PROJECTS',  generate_projects_section(repos_data))
    content = replace_section(content, 'ACTIVITY',  generate_activity_section(activity))
    content = replace_section(content, 'ARTICLES',  generate_articles_section())
 
    # Atualiza ou adiciona timestamp no rodapé
    now = datetime.now(timezone.utc).strftime('%d/%m/%Y às %H:%M UTC')
    timestamp_line = f'<!-- auto-updated: {now} -->'
    content = re.sub(r'<!-- auto-updated:.*?-->', timestamp_line, content)
    if '<!-- auto-updated:' not in content:
        content = content.rstrip() + f'\n\n{timestamp_line}\n'
 
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
 
    print("✅ README atualizado com sucesso!")
 
 
if __name__ == '__main__':
    update_readme(
