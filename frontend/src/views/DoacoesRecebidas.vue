<template>
  <div class="main-wrapper">
    <h1>Doações recebidas</h1>

    <div v-if="carregando" class="loading">
      <p>🔄 Carregando doações...</p>
    </div>

    <div v-else-if="erro" class="erro">
      <p>❌ {{ erro }}</p>
      <button @click="carregar" class="btn-tentar">Tentar novamente</button>
    </div>

    <div v-else-if="doacoes.length" class="card" v-for="doacao in doacoes" :key="doacao.id">
      <h2>R$ {{ doacao.valor.toFixed(2) }}</h2>
      <p><strong>Doador:</strong> {{ doacao.nome_doador || 'Anônimo' }}</p>
      <p><strong>Data:</strong> {{ formatarData(doacao.data_criacao) }}</p>

      <p v-if="doacao.status === 'Pendente'" class="status-pendente">🟡 Pagamento pendente</p>
      <p v-else class="status-aprovada">✅ Pagamento confirmado</p>
    </div>

    <p v-else class="empty-state">Sua ONG ainda não recebeu nenhuma doação.</p>

    <div class="footer-actions">
      <router-link to="/dashboard_ong" class="btn-back">Voltar</router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import http from '../api/http'

const doacoes = ref([])
const carregando = ref(true)
const erro = ref('')

function formatarData(iso) {
  return new Date(iso).toLocaleDateString('pt-BR')
}

async function carregar() {
  carregando.value = true
  erro.value = ''

  try {
    const { data } = await http.get('/api/doacoes/recebidas')
    doacoes.value = data
  } catch (err) {
    console.error('Erro ao carregar doações recebidas:', err)
    erro.value = err.response?.data?.detail || 'Erro ao carregar doações recebidas'
  } finally {
    carregando.value = false
  }
}

onMounted(carregar)
</script>

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

.btn-tentar {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #3C0D3C;
  color: white;
  border: none;
  border-radius: 20px;
  font-weight: bold;
  cursor: pointer;
}

.btn-tentar:hover {
  background-color: #2D0A2D;
}
</style>

<style scoped src="../styles/doacoes_recebidas.css"></style>
