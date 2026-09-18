<template>
  <div class="page-solicitacoes">
    <div class="solicitacoes-intro">
      <h1>Minhas solicitações de adoção</h1>

      <p>Acompanhe o andamento dos pedidos de adoção que você realizou.</p>
    </div>

    <div v-if="carregando" class="loading">
      <p>🔄 Carregando suas solicitações...</p>
    </div>

    <div v-else-if="erro" class="erro">
      <p>❌ {{ erro }}</p>

      <button type="button" @click="carregar">
        Tentar novamente
      </button>
    </div>

    <p v-if="adocoes.length" class="solicitacoes-resumo">
      {{ adocoes.length }}
      solicitação(ões) encontrada(s)
    </p>

    <template v-if="adocoes.length">
      <div v-for="adocao in adocoes" :key="adocao.id" class="solicitacao-card">
        <div v-if="adocao.animal.foto" class="solicitacao-foto">
          <img :src="urlFoto(adocao.animal.foto)" :alt="`Foto de ${adocao.animal.nome}`" />
        </div>

        <div v-else class="solicitacao-foto sem-foto">
          <span>🐾</span>
        </div>

        <div class="solicitacao-info">
          <h3>{{ adocao.animal.nome }}</h3>

          <p>
            <strong>Espécie:</strong>
            {{ adocao.animal.especie }}
          </p>

          <p>
            <strong>Data do pedido:</strong>
            {{ adocao.data }}
          </p>

          <p v-if="adocao.status === 'Pendente'" class="status-msg status-pendente">
            🟡 Sua solicitação está em análise pela ONG.
          </p>

          <p v-else-if="adocao.status === 'Aprovada'" class="status-msg status-aprovada">
            ✅ Parabéns! Sua solicitação foi aprovada.
          </p>

          <p v-else-if="adocao.status === 'Recusada'" class="status-msg status-recusada">
            ❌ Sua solicitação foi recusada.
          </p>
        </div>
      </div>
    </template>

    <p v-else class="mensagem">
      Você ainda não fez nenhuma solicitação de adoção.
    </p>

    <router-link to="/dashboard_adotante" class="btn-voltar">
      Voltar
    </router-link>

  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import http from '../api/http'

const adocoes = ref([])
const carregando = ref(true)
const erro = ref('')

function urlFoto(caminho) {
  if (!caminho) {
    return ''
  }

  if (caminho.startsWith('http')) {
    return caminho
  }

  const baseURL =
    http.defaults.baseURL || 'http://localhost:8000'

  return `${baseURL}${caminho}`
}

async function carregar() {
  carregando.value = true
  erro.value = ''

  try {
    const { data } = await http.get('/api/adoptions/mine')

    adocoes.value = data
  } catch (err) {
    console.error(
      'Erro ao carregar adoções:',
      err
    )

    erro.value =
      err.response?.data?.detail ||
      'Erro ao carregar suas adoções'
  } finally {
    carregando.value = false
  }
}

onMounted(carregar)
</script>

<style scoped src="../styles/minhas_adocoes.css"></style>

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
  background-color: #3C0D3C;
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 30px;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
}

.erro button:hover {
  background-color: #2D0A2D;
}
</style>
<style scoped src="../styles/minhas_adocoes.css"></style>
