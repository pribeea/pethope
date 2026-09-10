<template>
<div class="page-doacoes">
    <div class="container">
      <h1>💜 Fazer uma doação</h1>
      <p class="subtitle">Escolha uma ONG parceira para apoiar financeiramente.</p>

      <div v-if="carregando" class="loading">
        <p>🔄 Carregando ONGs...</p>
      </div>

      <div v-else-if="erro" class="erro">
        <p>❌ {{ erro }}</p>
      </div>

      <p v-else-if="ongs.length === 0" class="mensagem">Nenhuma ONG cadastrada no momento.</p>

      <div v-else class="card" v-for="ong in ongs" :key="ong.id">
        <h3>{{ ong.nome }}</h3>
        <p><strong>Endereço:</strong> {{ ong.endereco || 'Não informado' }}</p>
        <p><strong>Contato:</strong> {{ ong.contato || 'Não informado' }}</p>
        <router-link class="btn" :to="{ name: 'formulario_doacao', params: { ongId: ong.id } }">
          Fazer doação
        </router-link>
      </div>

      <a href="#" class="btn-voltar" @click.prevent="$router.back()">Voltar</a>
    </div>
</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import http from '../api/http'

const ongs = ref([])
const carregando = ref(true)
const erro = ref('')

async function carregar() {
  carregando.value = true
  erro.value = ''

  try {
    const { data } = await http.get('/api/ongs')
    ongs.value = data
  } catch (err) {
    console.error('Erro ao carregar ONGs:', err)
    erro.value = err.response?.data?.detail || 'Erro ao carregar ONGs. Tente novamente.'
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

<style scoped src="../styles/doacoes.css"></style>
