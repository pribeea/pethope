<template>
<div class="page-detalhes-atividade">
    <header>
      <h2>
        <img src="/pata-branca.png" class="logo-pata" alt="" />
        PetHope
      </h2>

      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <main class="main-wrapper">
      <div v-if="carregando" class="mensagem">
        <p>🔄 Carregando atividade...</p>
      </div>

      <div v-else-if="erro" class="mensagem erro">
        <p>❌ {{ erro }}</p>
      </div>

      <div v-else-if="atividade" class="detalhes-card">
        <div class="header-section">
          <p class="ong">{{ atividade.ong_nome }}</p>
          <h1>{{ atividade.titulo }}</h1>
        </div>

        <div class="informacoes">
          <div>
            <strong>Dias</strong>
            <span>{{ atividade.dias }}</span>
          </div>

          <div>
            <strong>Horário</strong>
            <span>{{ atividade.horario }}</span>
          </div>

          <div>
            <strong>Vagas</strong>
            <span>{{ atividade.vagas }}</span>
          </div>
        </div>

        <section class="secao">
          <h2>Sobre a atividade</h2>
          <p>{{ atividade.descricao }}</p>
        </section>

        <section v-if="atividade.detalhes" class="secao">
          <h2>Detalhes da atividade</h2>
          <p class="detalhes-texto">{{ atividade.detalhes }}</p>
        </section>

        <section class="ong-info">
          <h2>Informações da ONG</h2>
          <p><strong>ONG:</strong> {{ atividade.ong_nome }}</p>
          <p><strong>Localização:</strong> {{ atividade.ong_endereco || 'Não informado' }}</p>
          <p><strong>Contato:</strong> {{ atividade.ong_contato || 'Não informado' }}</p>
        </section>

        <div class="botoes">
          <button type="button" class="btn-back" @click="router.push('/atividades')">
            Voltar
          </button>

          <button type="button" class="btn-participar" @click="participar">
            Quero ser voluntário
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import http from '../api/http'

const route = useRoute()
const router = useRouter()

const atividade = ref(null)
const carregando = ref(true)
const erro = ref('')


async function carregar() {
  try {
    const { data: usuario } = await http.get('/api/auth/me')

    if (
      !usuario.autenticado ||
      usuario.tipo_sessao !== 'usuario' ||
      usuario.tipo_usuario !== 'voluntario'
    ) {
      router.push('/login')
      return
    }

    const { data } = await http.get(`/api/atividades/${route.params.atividadeId}`)
    atividade.value = data
  } catch (err) {
    console.error('Erro ao carregar atividade:', err)
    erro.value = err.response?.data?.detail || 'Erro ao carregar atividade.'
  } finally {
    carregando.value = false
  }
}

function participar() {
  router.push({
    name: 'formulario_voluntario',
    params: {
      atividadeId: atividade.value.id
    }
  })
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

<style scoped src="../styles/atividade_detalhe.css"></style>