<template>
<div class="page-ongs">
    <header>
      <h2><img src="/pata-branca.png" class="logo-pata" alt="" />PetHope</h2>
      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <div class="container">
      <h1>ONGs parceiras</h1>
      <p class="subtitle">Conheça as ONGs cadastradas e veja os animais disponíveis em cada uma.</p>

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
        <router-link class="btn" :to="{ name: 'animais_por_ong', params: { ongId: ong.id } }">
          Ver animais disponíveis
        </router-link>
      </div>

      <a href="#" class="btn-voltar" @click.prevent="$router.back()">Voltar</a>
    </div>
</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()
const ongs = ref([])
const carregando = ref(true)
const erro = ref('')

async function carregar() {
  carregando.value = true
  erro.value = ''

  try {
    const { data: me } = await http.get('/api/auth/me')
    if (!me.autenticado || me.tipo_sessao !== 'usuario') {
      router.push('/login')
      return
    }

    const { data } = await http.get('/api/ongs')
    ongs.value = data
  } catch (err) {
    console.error('Erro ao carregar ONGs:', err)
    erro.value = err.response?.data?.detail || 'Erro ao carregar ONGs. Tente novamente.'
  } finally {
    carregando.value = false
  }
}

async function sair() {
  try {
    await http.post('/api/auth/logout')
    router.push('/')
  } catch (err) {
    console.error('Erro ao fazer logout:', err)
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

<style scoped src="../styles/ongs.css"></style>