#!/bin/bash
# 📄 install.sh
echo "🔧 INSTALADOR DO SISTEMA DE GESTÃO DE MANUTENÇÃO"
echo "=============================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

echo "✅ Python 3 encontrado"

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso!"
else
    echo "❌ Erro ao instalar dependências."
    exit 1
fi

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "📄 Criando arquivo .env de exemplo..."
    cat > .env << EOL
DB_NAME=gestao_manutencao
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
EOL
    echo "⚠️  Configure o arquivo .env com suas credenciais do PostgreSQL"
fi

# Criar estrutura de pastas
echo "📁 Criando estrutura de pastas..."
mkdir -p logs
mkdir -p backups

echo "🎉 Instalação concluída!"
echo ""
echo "📝 PRÓXIMOS PASSOS:"
echo "1. Configure o arquivo .env com suas credenciais do PostgreSQL"
echo "2. Execute o sistema: python main.py"
echo "3. O sistema criará automaticamente as tabelas no primeiro uso"