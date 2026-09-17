<template>
  <div class="page-solicitacoes">
    <div class="solicitacoes-intro">
      <h1>Solicitações de adoção</h1>
      <p>Analise os pedidos e acompanhe o andamento das adoções da sua ONG.</p>
    </div>

    <div v-if="carregando" class="loading">
      <p>🔄 Carregando solicitações...</p>
    </div>

    <div v-else-if="erro" class="erro">
      <p>❌ {{ erro }}</p>
      <button type="button" @click="carregar">Tentar novamente</button>
    </div>

    <p v-if="solicitacoes.length" class="solicitacoes-resumo">{{ solicitacoes.length }} solicitação(ões) encontrada(s)</p>

    <template v-if="solicitacoes.length">
      <div v-for="s in solicitacoes" :key="s.id" class="solicitacao-card">
        <div v-if="s.animal.foto" class="solicitacao-foto">
          <img :src="urlFoto(s.animal.foto)" :alt="`Foto de ${s.animal.nome}`" />
        </div>
        <div v-else class="solicitacao-foto sem-foto">
          <span>🐾</span>
        </div>

        <div class="solicitacao-info">
          <h3>{{ s.animal.nome }}</h3>
          <p class="interessado"><strong>Interessado:</strong> {{ s.usuario.nome }}</p>

          <template v-if="s.formulario">
            <p><strong>CPF:</strong> {{ s.formulario.cpf }}</p>
            <p><strong>RG:</strong> {{ s.formulario.rg }}</p>
            <p><strong>Telefone:</strong> {{ s.formulario.telefone }}</p>
            <p><strong>Endereço:</strong> {{ s.formulario.endereco }}</p>

            <p class="motivo-titulo"><strong>Por que deseja adotar esse animal?</strong></p>
            <p class="motivo-texto">{{ s.formulario.motivo }}</p>
          </template>

          <div v-if="s.status === 'Pendente'" class="solicitacao-acoes">
            <button type="button" class="btn-recusar" @click="recusar(s.id)">Recusar</button>
            <button type="button" class="btn-aceitar" @click="aprovar(s.id)">Aceitar</button>
          </div>
          <p v-else-if="s.status === 'Aprovada'" class="status-msg status-aprovada">✅ Solicitação aprovada.</p>
          <p v-else-if="s.status === 'Recusada'" class="status-msg status-recusada">❌ Solicitação recusada.</p>
        </div>
      </div>
    </template>

    <p v-else class="mensagem">Nenhuma solicitação de adoção encontrada.</p>

    <router-link to="/dashboard_ong" class="btn-voltar">Voltar</router-link>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import http from '../api/http'

const solicitacoes = ref([])
const carregando = ref(true)
const erro = ref('')

function urlFoto(caminho) {
  if (!caminho) {
    return ''
  }

  if (caminho.startsWith('http')) {
    return caminho
  }

  const baseURL = http.defaults.baseURL || 'http://localhost:8000'

  return `${baseURL}${caminho}`
}

async function carregar() {
  carregando.value = true
  erro.value = ''

  try {
    const { data } = await http.get('/api/adoptions/requests')
    solicitacoes.value = data
  } catch (err) {
    console.error('Erro ao carregar solicitações:', err)
    erro.value = err.response?.data?.detail || 'Erro ao carregar solicitações'
  } finally {
    carregando.value = false
  }
}

async function aprovar(id) {
  try {
    await http.post(`/api/adoptions/${id}/approve`)
    carregar()
  } catch (err) {
    console.error('Erro ao aprovar solicitação:', err)
    erro.value = err.response?.data?.detail || 'Erro ao aprovar solicitação'
  }
}

async function recusar(id) {
  try {
    await http.post(`/api/adoptions/${id}/reject`)
    carregar()
  } catch (err) {
    console.error('Erro ao recusar solicitação:', err)
    erro.value = err.response?.data?.detail || 'Erro ao recusar solicitação'
  }
}

onMounted(carregar)
</script>

<style scoped src="../styles/solicitacoes.css"></style>

<style scoped>
.loading {
  text-align: center;
  padding: 40px;
  color: #3C0D3C;
  font-weight: bold;
  font-size: 18px;
}

.erro {
  text-align: center;
  padding: 40px;
  color: #d9534f;
  font-weight: bold;
  font-size: 18px;
}

.erro button {
  margin-top: 15px;
}
</style>
