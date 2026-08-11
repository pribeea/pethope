<template>
  <div class="page-dashboard">
    <header>
      <h2>PetHope 🐾</h2>
      <a href="#" style="color: white" @click.prevent="sair">Sair</a>
    </header>

    <div class="container">
      <h2>Bem-vindo, {{ nome }}</h2>

      <div class="card">
        <h3>Adotar um pet</h3>
        <p>Veja os animais disponíveis para adoção.</p>
        <router-link class="btn" to="/adocao">Ver pets</router-link>
      </div>

      <div class="card">
        <h3>Minhas adoções</h3>
        <p>Veja os animais que você adotou.</p>
        <router-link class="btn" to="/minhas_adocoes">Minhas solicitações de adoção</router-link>
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
