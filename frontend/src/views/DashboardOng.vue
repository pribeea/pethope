<template>
  <div class="page-dashboard-ong">
    <header>
      <h1>PetHope 🐾</h1>
      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <main>
      <section>
        <p>Bem-vinda, {{ nome }}</p>
        <h2>Gerenciamento</h2>

        <div class="cards">
          <router-link to="/cadastro_animal" class="card">Cadastrar Animal</router-link>
          <router-link to="/animais" class="card">Meus Animais</router-link>
          <router-link to="/solicitacoes" class="card">Solicitações de Adoção</router-link>
          <a href="#" class="card">Voluntários</a>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()
const nome = ref('')

async function carregar() {
  const { data } = await http.get('/api/auth/me')
  if (!data.autenticado || data.tipo_sessao !== 'ong') {
    router.push('/login_ong')
    return
  }
  nome.value = data.nome
}

async function sair() {
  await http.post('/api/auth/logout')
  router.push('/')
}

onMounted(carregar)
</script>

<style scoped src="../styles/dashboard_ong.css"></style>
