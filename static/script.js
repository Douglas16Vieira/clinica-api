const Busca = document.getElementById('btn-buscar');
const AgendarBtn = document.getElementById('agendar');
const telCont = document.getElementById('telefone');
const nomeUs = document.getElementById('nome');
const HDisponivel = document.getElementById('horarios');
const dataAgen = document.getElementById('data');

Busca.addEventListener('click', buscarDados);
AgendarBtn.addEventListener('click', AgendarData);

function buscarDados() {
    const data = dataAgen.value;
    const url =  '/available_slots?date=${data}';

        fetch(url)
        .then(res => res.json())
        .then(horarios => {
           HDisponivel.innerHTML = '';

           horarios.forEach(hora => {
                const option = document.createElement('option');
                option.value = hora;
                option.textContent = hora;
                HDisponivel.appendChild(option);
            });
        });

}

function AgendarConsulta {
         const = dados { nome = nomeUs.value,
            telefone = telCont.value,
            horario = HDisponivel.value,
            data = dataAgen.value
         }

         fetch('schedule', {
             method: 'post',
             body: json.stringify(dados)
         })
}
