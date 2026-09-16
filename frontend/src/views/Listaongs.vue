<template>
  <div class="page-ongs">

    <!-- HEADER -->
    <header>
      <h2>
        <img src="/pata-branca.png" class="logo-pata" alt="" />
        PetHope
      </h2>

      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <!-- CONTEÚDO -->
    <div class="container">

      <h1>ONGs parceiras</h1>

      <p class="subtitle">
        Conheça as ONGs cadastradas e veja os animais disponíveis em cada uma.
      </p>

      <!-- CARREGANDO -->
      <div v-if="carregando" class="loading">
        <p>🔄 Carregando ONGs...</p>
      </div>

      <!-- ERRO -->
      <div v-else-if="erro" class="erro">
        <p>❌ {{ erro }}</p>
      </div>

      <!-- NENHUMA ONG -->
      <p
        v-else-if="ongs.length === 0"
        class="mensagem"
      >
        Nenhuma ONG cadastrada no momento.
      </p>

      <!-- LISTA DE ONGS -->
      <div v-else class="ongs-container">

        <div
          v-for="ong in ongs"
          :key="ong.id"
          class="card"
        >

          <h3>{{ ong.nome }}</h3>

          <p>
            <strong>Endereço:</strong>
            {{ ong.endereco || 'Não informado' }}
          </p>

          <p>
            <strong>Contato:</strong>
            {{ ong.contato || 'Não informado' }}
          </p>

          <div class="card-actions">

            <router-link
              class="btn"
              :to="{
                name: 'animais_por_ong',
                params: { ongId: ong.id }
              }"
            >
              Ver animais disponíveis
            </router-link>

            <router-link
              class="btn btn-doar"
              :to="{
                name: 'formulario_doacao',
                params: { ongId: ong.id }
              }"
            >
              💜 Fazer doação
            </router-link>

          </div>

        </div>

      </div>

      <!-- VOLTAR -->
      <div class="footer-actions">
        <router-link
          to="/dashboard_adotante"
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

const ongs = ref([])
const carregando = ref(true)
const erro = ref('')


async function carregar() {
  carregando.value = true
  erro.value = ''

  try {

    // Verifica se existe usuário logado
    const { data: me } = await http.get('/api/auth/me')

    if (!me.autenticado || me.tipo_sessao !== 'usuario') {
      router.push('/login')
      return
    }

    // Busca as ONGs
    const { data } = await http.get('/api/ongs')

    ongs.value = data

  } catch (err) {

    console.error('Erro ao carregar ONGs:', err)

    erro.value =
      err.response?.data?.detail ||
      'Erro ao carregar ONGs. Tente novamente.'

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


<style scoped src="../styles/ongs.css"></style>
