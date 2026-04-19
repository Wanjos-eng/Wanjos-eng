# 🚀 Configuração do GitHub Actions - README Automático

## ✅ O que já está pronto:

1. **Workflow configurado** em `.github/workflows/update-readme.yml`
   - Roda automaticamente todo dia às 00:00 UTC
   - Pode ser executado manualmente pela aba "Actions" do GitHub
   - Atualiza projetos e atividade recente automaticamente

2. **Script Python** em `.github/scripts/update_readme.py`
   - Busca dados reais dos seus repositórios via API do GitHub
   - Gera seção de projetos com estatísticas atualizadas
   - Gera seção de atividade recente (últimos commits)
   - Prepara espaço para artigos/documentações

3. **README.md** com placeholders corretos
   - `<!-- PROJECTS_SECTION -->` - Cards dos projetos
   - `<!-- ACTIVITY_SECTION -->` - Atividade recente
   - `<!-- ARTICLES_SECTION -->` - Artigos técnicos

## 🔧 Passos para ativar no seu GitHub:

### Passo 1: Push para o repositório do perfil
```bash
git add .
git commit -m "feat: setup GitHub Actions for auto-updating README"
git push origin main
```

### Passo 2: Habilitar Workflow
1. Vá até https://github.com/Wanjos-eng/Wanjos-eng
2. Clique na aba **"Actions"**
3. Se aparecer um aviso amarelo, clique em **"I understand my workflows, go ahead and enable them"**

### Passo 3: Testar manualmente (opcional)
1. Na aba **Actions**, clique em **"🔄 Auto-Update README"**
2. Clique em **"Run workflow"** → **"Run workflow"**
3. Aguarde ~30 segundos e veja o README ser atualizado!

## 📝 Como adicionar artigos futuramente:

### Opção A: Links diretos (mais simples)
Edite o script `.github/scripts/update_readme.py` e adicione na função `generate_articles_placeholder()`:

```python
section += "- [Título do Artigo](https://link) - Descrição\n"
```

### Opção B: Pasta /docs no repositório
1. Crie uma pasta `docs/` no seu repositório de perfil
2. Coloque seus PDFs lá
3. O script pode listar automaticamente os arquivos

### Opção C: Medium/Dev.to integration
Publique seus artigos nessas plataformas e o script pode puxar via RSS/API

## 🎯 O que o workflow atualiza automaticamente:

- ✅ Cards dos projetos com estrelas/forks atualizados
- ✅ Tabela de atividade recente (últimos 3 commits)
- ✅ Timestamp de última atualização
- ✅ Linguagem principal de cada repo

## ⚠️ Importante:

- Os repositórios precisam ser **públicos** para aparecerem nos cards
- O workflow usa o `GITHUB_TOKEN` automático (já incluso)
- Se algum repo for privado, ele será ignorado silenciosamente

## 🐛 Troubleshooting:

Se o workflow falhar:
1. Verifique se os nomes dos repositórios no script estão corretos
2. Confira a aba "Actions" para ver o log do erro
3. Re-executa manualmente para testar

---

**Próximo nível:** Quando tiver artigos prontos, é só editar a seção `generate_articles_placeholder()` no script Python!
