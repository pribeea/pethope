<template>
  <div class="page-lista-atividades">
    <header>
      <h2>
        <img src="/pata-branca.png" class="logo-pata" alt="" />
        PetHope
      </h2>

      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <div class="main-wrapper">

      <div class="header-section">
        <h2>Minhas atividades</h2>

        <p class="subtitle">
          Acompanhe as atividades de voluntariado nas quais você se inscreveu.
        </p>
      </div>

      <div v-if="carregando" class="loading">
        <p>🔄 Carregando atividades...</p>
      </div>

      <div v-else-if="erro" class="erro">
        <p>❌ {{ erro }}</p>
      </div>

      <div v-else class="cards-container">

        <article
          v-if="atividades.length"
          v-for="atividade in atividades"
          :key="atividade.id"
          class="atividade-card"
        >

          <div class="atividade-info">
            <div class="atividade-topo">
              <div>
                <h3>{{ atividade.titulo }}</h3>

                <span
                  class="status"
                  :class="classeStatus(atividade.status)"
                >
                  {{ atividade.status }}
                </span>
              </div>

              <span class="ong">
                {{ atividade.ong_nome }}
              </span>
            </div>

            <p>
              <strong>Descrição:</strong>
              {{ atividade.descricao }}
            </p>

            <p>
              <strong>Dias:</strong>
              {{ atividade.dias }}
            </p>

            <p>
              <strong>Horário:</strong>
              {{ atividade.horario }}
            </p>

            <router-link
              :to="{ name: 'detalhes_atividade', params: { atividadeId: atividade.atividade_id } }"
              class="btn-detalhes"
            >
              Ver detalhes
            </router-link>

          </div>
        </article>

        <div v-else class="empty-state">
          <p>Você ainda não se inscreveu em nenhuma atividade.</p>
        </div>

      </div>
      <div class="footer-actions">

        <router-link to="/dashboard_voluntario" class="btn-back">
          Voltar
        </router-link>

      </div>
    </div>
  </div>
</template>

<script setup>

import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()

const atividades = ref([])
const carregando = ref(true)
const erro = ref('')

async function carregarAtividades() {

  carregando.value = true
  erro.value = ''

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

    const { data } = await http.get('/api/atividades/minhas')
    atividades.value = data

  } catch (err) {

    console.error('Erro ao carregar atividades:', err)

    if (err.response?.status === 401) {
      router.push('/login')
      return
    }

    erro.value = err.response?.data?.detail || 'Não foi possível carregar suas atividades.'

  } finally {

    carregando.value = false

  }
}

function classeStatus(status) {

  if (status === 'Aprovada') {
    return 'aprovada'
  }

  if (status === 'Recusada') {
    return 'recusada'
  }

  return 'pendente'

}

async function sair() {

  try {
    await http.post('/api/auth/logout')
    router.push('/')

  } catch (err) {

    console.error('Erro ao fazer logout:', err)
  }
}

onMounted(carregarAtividades)

</script>

<style scoped>

.loading {
  width: 100%;
  padding: 40px 0;
  color: #3C0D3C;
  font-weight: bold;
  font-size: 16px;
  text-align: left;
}

.erro {
  width: 100%;
  padding: 20px 0;
  color: #d9534f;
  font-weight: bold;
  font-size: 16px;
  text-align: left;
}

</style>

<style scoped src="../styles/minhas_atividades_voluntario.css"></style>