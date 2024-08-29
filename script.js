document.getElementById('chamadoForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const sistema = document.getElementById('sistema').value;
    const descricao = document.getElementById('descricao').value;
    const evidencia = document.getElementById('evidencia').files[0];
    const prioridade = document.querySelector('input[name="prioridade"]:checked').value;

    const formData = new FormData();
    formData.append('sistema', sistema);
    formData.append('descricao', descricao);
    formData.append('evidencia', evidencia);
    formData.append('prioridade', prioridade);

    fetch('http://127.0.0.1:5000/api/chamado', {  // Corrigido: URL do servidor Flask
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('Chamado enviado com sucesso!');
        // Você pode adicionar mais lógica aqui, como limpar o formulário ou redirecionar o usuário
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao enviar chamado.');
    });
});
