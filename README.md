## 🔐 Configuração de Segurança

### Primeira Instalação:

1. Copie `.env.example` para `.env`
2. **EDITE O .ENV** com valores seguros:
   ```bash
   SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   ADMIN_PASSWORD=sua-senha-super-forte-aqui