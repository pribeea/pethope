<template>
  <div class="page-solicitacoes">
    <h1>Solicitações de adoção</h1>

    <div v-if="carregando" class="loading">
      <p>🔄 Carregando solicitações...</p>
    </div>

    <div v-else-if="erro" class="erro">
      <p>❌ {{ erro }}</p>
      <button type="button" @click="carregar">Tentar novamente</button>
    </div>

    <template v-else-if="solicitacoes.length">
      <div v-for="s in solicitacoes" :key="s.id">
        <hr />
        <h3>{{ s.animal.nome }}</h3>
        <p><strong>Interessado:</strong> {{ s.usuario.nome }} ({{ s.usuario.email }})</p>
        <p><strong>Status:</strong> {{ s.status }}</p>

        <template v-if="s.formulario">
          <p><strong>Telefone:</strong> {{ s.formulario.telefone }}</p>
          <p><strong>Endereço:</strong> {{ s.formulario.endereco }}</p>
          <p><strong>CPF:</strong> {{ s.formulario.cpf }}</p>
          <p><strong>RG:</strong> {{ s.formulario.rg }}</p>
          <p><strong>Motivo da adoção:</strong> {{ s.formulario.motivo }}</p>
        </template>

        <template v-if="s.status === 'Pendente'">
          <button type="button" @click="aprovar(s.id)">Aprovar</button>
          <button type="button" @click="recusar(s.id)">Recusar</button>
        </template>
        <p v-else-if="s.status === 'Aprovada'" style="color: green">✅ Solicitação aprovada.</p>
        <p v-else-if="s.status === 'Recusada'" style="color: red">❌ Solicitação recusada.</p>
      </div>
    </template>

    <p v-else>Nenhuma solicitação de adoção encontrada.</p>

    <br />
    <router-link to="/dashboard_ong" class="btn-voltar">Voltar</router-link>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import http from '../api/http'

const solicitacoes = ref([])
const carregando = ref(true)
const erro = ref('')

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
</style>