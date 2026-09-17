<template>
  <div class="page-lista-animais">
<div class="main-wrapper">
      <div class="header-section">
        <div class="header-section-texto">
          <h2>Meus animais</h2>
          <p class="subtitle">Gerencie os animais cadastrados pela sua ONG.</p>
        </div>

        <svg class="header-section-arte" viewBox="0 0 200 140" aria-hidden="true">
          <ellipse cx="100" cy="72" rx="88" ry="56" fill="#f3e5fb" />
          <g fill="#a86fd1">
            <circle cx="70" cy="60" r="7" />
            <circle cx="86" cy="50" r="7" />
            <circle cx="104" cy="50" r="7" />
            <circle cx="120" cy="60" r="7" />
            <ellipse cx="95" cy="78" rx="26" ry="19" />
          </g>
          <g fill="#e0a8e8">
            <path d="M148 34c-6 0-10 5-10 10 0 7 10 14 10 14s10-7 10-14c0-5-4-10-10-10Z" />
            <path d="M164 52c-4 0-7 3.5-7 7 0 5 7 10 7 10s7-5 7-10c0-3.5-3-7-7-7Z" />
          </g>
        </svg>
      </div>

      <h2 class="titulo-secao">🐾 Pets disponíveis</h2>

      <div v-if="carregando" class="loading">
        <p>🔄 Carregando seus pets...</p>
      </div>

      <div v-else class="cards-container">

        <div
          v-if="animais.length"
          v-for="animal in animais"
          :key="animal.id"
          class="animal-card"
        >

          <div v-if="animal.foto" class="animal-foto">
            <img
              :src="urlFoto(animal.foto)"
              :alt="`Foto de ${animal.nome}`"
            />
            <span class="animal-favorito">♡</span>
          </div>

          <div v-else class="animal-foto sem-foto">
            <span>🐾</span>
            <span class="animal-favorito">♡</span>
          </div>

          <div class="animal-info">

            <div class="titulo-animal">
              <p class="animal-ong">{{ animal.ong_nome || 'ONG não informada' }}</p>
              <h3>{{ animal.nome }}</h3>

              <router-link
                :to="`/animal/${animal.id}`"
                class="btn-detalhes"
              >
                Ver detalhes
              </router-link>
            </div>

            <p>
              <strong>Status:</strong>

              <span v-if="animal.status === 'Disponível'">
                🟢 Disponível
              </span>

              <span
                v-else-if="
                  animal.status === 'Em processo de adoção'
                "
              >
                🟡 Processo de adoção
              </span>

              <span
                v-else-if="animal.status === 'Adotado'"
              >
                🔴 Adotado
              </span>

              <span v-else>
                ⚪ {{ animal.status }}
              </span>
            </p>

          </div>
        </div>

        <div v-else-if="erro" class="erro">
          <p>❌ {{ erro }}</p>
        </div>

        <div v-else class="empty-state">
          <p>Nenhum pet cadastrado no momento.</p>
        </div>

      </div>

      <div class="footer-actions">
        <router-link
          to="/dashboard_ong"
          class="btn-back"
        >
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

const animais = ref([])
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
    const { data } = await http.get('/api/animals', {
      params: {
        minha_ong: true
      }
    })

    animais.value = data
  } catch (err) {
    console.error(
      'Erro ao carregar animais:',
      err
    )

    if (err.response?.status === 401) {
      router.push('/login_ong')
      return
    }

    erro.value =
      err.response?.data?.detail ||
      'Erro ao carregar animais'
  } finally {
    carregando.value = false
  }
}

async function sair() {
  try {
    await http.post('/api/auth/logout')
    router.push('/')
  } catch (err) {
    console.error(
      'Erro ao fazer logout:',
      err
    )
  }
}

onMounted(carregar)
</script>

<style scoped src="../styles/lista_animais.css"></style>
