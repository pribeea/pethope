<template>
  <div class="page-inscricoes">
    <header>
      <h2><img src="/pata-branca.png" class="logo-pata" alt="" /> PetHope</h2>
      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <main class="container">
      <h1>Voluntários inscritos</h1>

      <p v-if="carregando" class="mensagem">Carregando inscrições...</p>

      <p v-else-if="erro" class="mensagem erro">{{ erro }}</p>

      <p v-else-if="inscricoes.length === 0" class="mensagem">Ainda não há voluntários inscritos.</p>

      <div v-else class="inscricoes">
        <article v-for="inscricao in inscricoes" :key="inscricao.id" class="inscricao-card">
          <div class="cabecalho-card">
            <div>
              <h2>{{ inscricao.voluntario_nome }}</h2>
              <p>{{ inscricao.voluntario_email }}</p>
            </div>

            <span class="status" :class="statusClasse(inscricao.status)">{{ inscricao.status }}</span>
          </div>

          <div class="dados">
            <p><strong>Telefone:</strong> {{ inscricao.telefone }}</p>
            <p><strong>Motivo:</strong> {{ inscricao.motivo }}</p>
          </div>

          <div v-if="inscricao.status === 'Pendente'" class="acoes">
            <button type="button" class="btn-aprovar" @click="alterarStatus(inscricao.id, 'Aprovada')">Aprovar</button>
            <button type="button" class="btn-recusar" @click="alterarStatus(inscricao.id, 'Recusada')">Recusar</button>
          </div>
        </article>
      </div>

      <button type="button" class="btn-voltar" @click="voltar">Voltar</button>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import http from '../api/http'

const route = useRoute()
const router = useRouter()

const inscricoes = ref([])
const carregando = ref(true)
const erro = ref('')

async function carregar() {
  try {
    const { data: sessao } = await http.get('/api/auth/me')

    if (!sessao.autenticado || sessao.tipo_sessao !== 'ong') {
      router.push('/login_ong')
      return
    }

    const { data } = await http.get(`/api/atividades/${route.params.atividadeId}/inscricoes`)
    inscricoes.value = data
  } catch (err) {
    console.error(err)
    erro.value = err.response?.data?.detail || 'Erro ao carregar inscrições.'
  } finally {
    carregando.value = false
  }
}

async function alterarStatus(inscricaoId, status) {
  try {
    await http.put(`/api/inscricoes-atividade/${inscricaoId}/status`, null, {
      params: {
        status_novo: status
      }
    })

    await carregar()
  } catch (err) {
    console.error(err)
    alert(err.response?.data?.detail || 'Erro ao alterar status.')
  }
}

function statusClasse(status) {
  if (status === 'Aprovada') {
    return 'aprovada'
  }

  if (status === 'Recusada') {
    return 'recusada'
  }

  return 'pendente'
}

function voltar() {
  router.push('/atividades-ong')
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

<style scoped src="../styles/inscricoes_atividade.css"></style>