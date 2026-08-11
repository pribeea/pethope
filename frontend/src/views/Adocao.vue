<template>
<div class="page-adocao">
    <div class="container">
      <h1>🐾 Animais para adoção</h1>

      <div v-if="carregando" class="loading">
        <p>🔄 Carregando animais disponíveis...</p>
      </div>

      <div v-else-if="animais.length" class="card" v-for="animal in animais" :key="animal.id">
        <h2>{{ animal.nome }}</h2>
        <p><strong>Espécie:</strong> {{ animal.especie }}</p>
        <p><strong>Raça:</strong> {{ animal.raca || 'Não informada' }}</p>
        <p><strong>Sexo:</strong> {{ animal.sexo || 'Não informada' }}</p>
        <p><strong>Idade:</strong> {{ animal.idade || 'Não informada' }}</p>
        <p><strong>Descrição:</strong> {{ animal.descricao || 'Sem descrição cadastrada.' }}</p>

        <span v-if="animal.status === 'Disponível'">🟢 Disponível</span>
        <span v-else-if="animal.status === 'Em processo de adoção'">🟡 Em processo de adoção</span>
        <span v-else-if="animal.status === 'Adotado'">🔴 Adotado</span>
        <span v-else>⚪ Status não definido</span>

        <button type="button" @click="$router.push(`/adotar/${animal.id}`)">Quero adotar</button>
      </div>

      <div v-else-if="erro" class="erro">
        <p>❌ {{ erro }}</p>
      </div>

      <p v-else class="mensagem">Nenhum animal disponível para adoção no momento.</p>

      <router-link to="/dashboard_adotante" class="btn-voltar">Voltar</router-link>
    </div>
</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import http from '../api/http'

const animais = ref([])
const carregando = ref(true)
const erro = ref('')

async function carregar() {
  carregando.value = true
  erro.value = ''
  
  try {
    const { data } = await http.get('/api/animals', { 
      params: { status_filtro: 'Disponível' } 
    })
    animais.value = data
  } catch (err) {
    console.error('Erro ao carregar animais:', err)
    if (err.response?.data?.detail) {
      erro.value = err.response.data.detail
    } else {
      erro.value = 'Erro ao carregar animais. Tente novamente.'
    }
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
</style>

<style scoped src="../styles/adocao.css"></style>
