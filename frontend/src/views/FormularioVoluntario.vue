<template>
  <div class="page-formulario-voluntario">
    <header>
      <h2><img src="/pata-branca.png" class="logo-pata" alt="" /> PetHope</h2>
      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <main class="container">

      <div v-if="carregando" class="mensagem">Carregando atividade...</div>

      <div v-else-if="erro && !atividade" class="mensagem erro">{{ msg }}</div>

      <div v-else-if="atividade" class="form-card">

        <div class="atividade-header">
          <span class="ong">{{ atividade.ong_nome }}</span>
          <h1>{{ atividade.titulo }}</h1>
        </div>

        <hr />

        <div class="formulario-header">
          <h2>Inscrição</h2>
          <p>Preencha os dados abaixo para enviar sua inscrição para esta atividade.</p>
        </div>

        <form @submit.prevent="enviar">

          <div class="campos-linha">
            <div class="form-group">
              <label for="telefone">Telefone</label>
              <input id="telefone" v-model="form.telefone" type="tel" required placeholder="(84) 99999-9999" />
            </div>
          </div>

          <div class="form-group">
            <label for="motivo">Por que deseja participar?</label>
            <textarea id="motivo" v-model="form.motivo" rows="5" required maxlength="1000" placeholder="Conte um pouco sobre seu interesse em participar desta atividade..."></textarea>
          </div>

          <p v-if="msg" :class="['mensagem-form', { erro: erro }]">{{ msg }}</p>

          <div class="button-group">
            <button type="button" class="btn-back" @click="router.push({ name: 'detalhes_atividade', params: { atividadeId: atividade.id } })">Voltar</button>
            <button type="submit" class="btn-next" :disabled="enviando">{{ enviando ? 'Enviando...' : 'Enviar inscrição' }}</button>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import http from '../api/http'

const route = useRoute()
const router = useRouter()

const atividade = ref(null)
const carregando = ref(true)
const enviando = ref(false)
const msg = ref('')
const erro = ref(false)

const form = reactive({
  telefone: '',
  motivo: '',
})

async function carregar() {
  try {
    const { data: usuario } = await http.get('/api/auth/me')

    if (!usuario.autenticado || usuario.tipo_sessao !== 'usuario' || usuario.tipo_usuario !== 'voluntario') {
      router.push('/login')
      return
    }

    const { data } = await http.get(`/api/atividades/${route.params.atividadeId}`)
    atividade.value = data
  } catch (err) {
    console.error('Erro ao carregar atividade:', err)
    erro.value = true
    msg.value = err.response?.data?.detail || 'Erro ao carregar atividade.'
  } finally {
    carregando.value = false
  }
}

async function enviar() {
  msg.value = ''
  erro.value = false

  try {
    enviando.value = true

    await http.post(`/api/atividades/${route.params.atividadeId}/inscricao`, form)

    msg.value = 'Inscrição enviada com sucesso!'

    setTimeout(() => {
      router.push({
        name: 'minhas_atividades_voluntario'
      })
    }, 1000)
  } catch (err) {
    console.error('Erro ao realizar inscrição:', err)
    erro.value = true
    msg.value = err.response?.data?.detail || 'Erro ao realizar inscrição.'
  } finally {
    enviando.value = false
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

<style scoped src="../styles/formulario_voluntario.css"></style>