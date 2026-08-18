<template>
<div class="page-animais-por-ong">
    <header>
      <h2><img src="/pata-branca.png" class="logo-pata" alt="" />PetHope</h2>
      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <div class="container">
      <router-link :to="{ name: 'ongs' }" class="btn-voltar-topo">&larr; Todas as ONGs</router-link>

      <div v-if="carregandoOng" class="loading">
        <p>🔄 Carregando ONG...</p>
      </div>
      <div v-else-if="erroOng" class="erro">
        <p>❌ {{ erroOng }}</p>
      </div>
      <template v-else-if="ong">
        <h1>🏠 {{ ong.nome }}</h1>
        <div class="ong-info">
          <p v-if="ong.endereco"><strong>Endereço:</strong> {{ ong.endereco }}</p>
          <p v-if="ong.contato"><strong>Contato:</strong> {{ ong.contato }}</p>
        </div>
      </template>

      <h2 class="titulo-animais">🐾 Animais disponíveis para adoção</h2>

      <div v-if="carregandoAnimais" class="loading">
        <p>🔄 Carregando animais...</p>
      </div>

      <div v-else-if="erroAnimais" class="erro">
        <p>❌ {{ erroAnimais }}</p>
      </div>

      <p v-else-if="animais.length === 0" class="mensagem">
        Esta ONG não tem animais disponíveis para adoção no momento.
      </p>

      <div v-else class="card" v-for="animal in animais" :key="animal.id">
        <h2>{{ animal.nome }}</h2>
        <p><strong>Espécie:</strong> {{ animal.especie }}</p>
        <p><strong>Raça:</strong> {{ animal.raca || 'Não informada' }}</p>
        <p><strong>Sexo:</strong> {{ animal.sexo || 'Não informado' }}</p>
        <p><strong>Idade:</strong> {{ animal.idade || 'Não informada' }}</p>
        <p><strong>Descrição:</strong> {{ animal.descricao || 'Sem descrição cadastrada.' }}</p>

        <span v-if="animal.status === 'Disponível'">🟢 Disponível</span>
        <span v-else-if="animal.status === 'Em processo de adoção'">🟡 Em processo de adoção</span>
        <span v-else-if="animal.status === 'Adotado'">🔴 Adotado</span>
        <span v-else>⚪ Status não definido</span>

        <button type="button" @click="$router.push(`/adotar/${animal.id}`)">Quero adotar</button>
      </div>

      <a href="#" class="btn-voltar" @click.prevent="$router.back()">Voltar</a>
    </div>
</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const props = defineProps({ ongId: { type: [String, Number], required: true } })

const router = useRouter()
const ong = ref(null)
const carregandoOng = ref(true)
const erroOng = ref('')

const animais = ref([])
const carregandoAnimais = ref(true)
const erroAnimais = ref('')

async function carregar() {
  const { data: me } = await http.get('/api/auth/me')
  if (!me.autenticado || me.tipo_sessao !== 'usuario') {
    router.push('/login')
    return
  }

  await Promise.all([carregarOng(), carregarAnimais()])
}

async function carregarOng() {
  carregandoOng.value = true
  erroOng.value = ''
  try {
    const { data } = await http.get(`/api/ongs/${props.ongId}`)
    ong.value = data
  } catch (err) {
    console.error('Erro ao carregar ONG:', err)
    erroOng.value = err.response?.data?.detail || 'Não foi possível carregar os dados desta ONG.'
  } finally {
    carregandoOng.value = false
  }
}

async function carregarAnimais() {
  carregandoAnimais.value = true
  erroAnimais.value = ''
  try {
    const { data } = await http.get('/api/animals', {
      params: { ong_id: props.ongId, status_filtro: 'Disponível' },
    })
    animais.value = data
  } catch (err) {
    console.error('Erro ao carregar animais:', err)
    erroAnimais.value = err.response?.data?.detail || 'Não foi possível carregar os animais desta ONG.'
  } finally {
    carregandoAnimais.value = false
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

<style scoped src="../styles/animais_por_ong.css"></style>