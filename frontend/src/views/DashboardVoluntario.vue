<template>
  <div class="page-dashboard">
    <header>
      <h2>PetHope 🐾</h2>
      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <div class="container">
      <h2>Olá, {{ nome }}</h2>

      <div class="card">
        <h3>Animais disponíveis</h3>
        <p>Veja animais para adoção.</p>
        <router-link class="btn" to="/adocao">Ver animais</router-link>
      </div>

      <div class="card">
        <h3>Ser voluntário</h3>
        <p>Ajude ONGs e participe de eventos.</p>
        <a class="btn" href="#">Quero ajudar</a>
      </div>
    </div>
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
  if (!data.autenticado || data.tipo_sessao !== 'usuario') {
    router.push('/login')
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

<style scoped src="../styles/dashboard.css"></style>
