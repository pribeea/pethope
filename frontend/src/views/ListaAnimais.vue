<template>
  <div class="page-lista-animais">
    <header>
      <h2>
        <img src="/pata-branca.png" class="logo-pata" alt="" />
        PetHope
      </h2>

      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <div class="main-wrapper">
      <div class="header-section">
        <h2>Escolha o seu pet</h2>
        <p class="subtitle">Encontre o companheiro ideal.</p>
      </div>

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
          </div>

          <div v-else class="animal-foto sem-foto">
            <span>🐾</span>
          </div>

          <div class="animal-info">

            <div class="titulo-animal">
              <h3>{{ animal.nome }}</h3>

              <router-link
                :to="`/animal/${animal.id}`"
                class="btn-detalhes"
              >
                Ver detalhes
              </router-link>
            </div>

            <p>
              <strong>Espécie:</strong>
              {{ animal.especie }}
            </p>

            <p>
              <strong>Idade:</strong>
              {{ animal.idade ?? 'Não informada' }}

              <span
                v-if="
                  animal.idade !== null &&
                  animal.idade !== undefined
                "
              >
                anos
              </span>
            </p>

            <p>
              <strong>Sexo:</strong>
              {{ animal.sexo || 'Não informado' }}
            </p>

            <p>
              <strong>Descrição:</strong>
              {{ animal.descricao || 'Sem descrição cadastrada.' }}
            </p>

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
