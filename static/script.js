const Busca = document.getElementById('btn-buscar');
const AgendarBtn = document.getElementById('agendar');
const telCont = document.getElementById('telefone');
const nomeUs = document.getElementById('nome');
const HDisponivel = document.getElementById('horarios');
const dataAgen = document.getElementById('data');

let horarioSelecionado = null;
const API = "http://localhost:8000";

Busca.addEventListener('click', buscarDados);
AgendarBtn.addEventListener('click', AgendarData);

function buscarDados() {
    const data = dataAgen.value;
    if (!data) return alert("Escolha a data");

    const url = `${API}/available?date=${data}`;

    HDisponivel.innerHTML = 'Carregando...';

    fetch(url)
        .then(res => res.json().then(json => ({ ok: res.ok, json })))
        .then(({ ok, json }) => {
           HDisponivel.innerHTML = '';

           if (!ok) {
               HDisponivel.innerHTML = `<div class="erro">${json.detail}</div>`;
               return;
           }

           const horarios = json.horarios_disponiveis;

           horarios.forEach(hora => {
                const btn = document.createElement('button');
                btn.textContent = hora;
                btn.onclick = () => {
                    document.querySelectorAll('#horarios button').forEach(b => b.classList.remove('selecionado'));
                    btn.classList.add('selecionado');
                    horarioSelecionado = hora; // salva
                };
                HDisponivel.appendChild(btn);
            });

           if (horarios.length === 0) {
                HDisponivel.innerHTML = `<div class="erro">Sem horários livres</div>`;
           }
        });
}

function AgendarData() {
         if (!horarioSelecionado) return alert("Selecione um horário");
         if (!nomeUs.value) return alert("Digite seu nome");

         const dados = { 
            nome: nomeUs.value,
            telefone: telCont.value,
            hora: horarioSelecionado,
            data: dataAgen.value
         };

         fetch(`${API}/appointments`, {
             method: 'POST',
             headers: { "Content-Type": "application/json" },
             body: JSON.stringify(dados)
         })
         .then(res => res.json().then(j => ({ok: res.ok, j})))
         .then(({ok, j}) => {
            if (!ok) alert(j.detail);
            else HDisponivel.innerHTML = `<div class="sucesso">✅ ${j.mensagem} - ${j.data} às ${j.hora}</div>`;
         });
}

function AgendarConsulta() { return AgendarData(); }