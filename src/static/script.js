// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    // Configura botões de exemplo
    document.querySelectorAll('.exemplo-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const pergunta = this.getAttribute('data-pergunta');
            document.getElementById('pergunta').value = pergunta;
            document.getElementById('empresa').focus();
        });
    });
    
    // Validação do formulário
    const form = document.getElementById('consultaForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const empresa = document.getElementById('empresa').value;
            const pergunta = document.getElementById('pergunta').value.trim();
            
            if (!empresa) {
                e.preventDefault();
                alert('Por favor, selecione uma empresa.');
                document.getElementById('empresa').focus();
            } else if (!pergunta) {
                e.preventDefault();
                alert('Por favor, digite sua pergunta.');
                document.getElementById('pergunta').focus();
            }
        });
    }
    
    // Auto-focus na pergunta quando empresa é selecionada
    const empresaSelect = document.getElementById('empresa');
    if (empresaSelect) {
        empresaSelect.addEventListener('change', function() {
            if (this.value) {
                document.getElementById('pergunta').focus();
            }
        });
    }
});