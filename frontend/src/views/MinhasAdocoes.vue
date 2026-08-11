<template>
  <div class="main-wrapper">
    <h1>Minhas solicitações de adoção</h1>

    <div v-if="carregando" class="loading">
      <p>🔄 Carregando suas solicitações...</p>
    </div>

    <div v-else-if="erro" class="erro">
      <p>❌ {{ erro }}</p>
      <button @click="carregar" class="btn-tentar">Tentar novamente</button>
    </div>

    <div v-else-if="adocoes.length" class="card" v-for="adocao in adocoes" :key="adocao.id">
      <h2>{{ adocao.animal.nome }}</h2>
      <p><strong>Espécie:</strong> {{ adocao.animal.especie }}</p>
      <p><strong>Data do pedido:</strong> {{ adocao.data }}</p>

      <p v-if="adocao.status === 'Pendente'" class="status-pendente">
        🟡 Sua solicitação está em análise pela ONG.
      </p>
      <p v-else-if="adocao.status === 'Aprovada'" class="status-aprovada">
        ✅ Parabéns! Sua solicitação foi aprovada.
      </p>
      <p v-else-if="adocao.status === 'Recusada'" class="status-recusada">
        ❌ Sua solicitação foi recusada.
      </p>
    </div>

    <p v-else class="empty-state">Você ainda não fez nenhuma solicitação de adoção.</p>

    <div class="footer-actions">
      <router-link to="/dashboard_adotante" class="btn-back">Voltar</router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import http from '../api/http'

const adocoes = ref([])
const carregando = ref(true)
const erro = ref('')

async function carregar() {
  carregando.value = true
  erro.value = ''
  
  try {
    const { data } = await http.get('/api/adoptions/mine')
    adocoes.value = data
  } catch (err) {
    console.error('Erro ao carregar adoções:', err)
    erro.value = err.response?.data?.detail || 'Erro ao carregar suas adoções'
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

<style scoped src="../styles/minhas_adocoes.css"></style>
