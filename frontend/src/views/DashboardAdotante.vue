<template>
  <div class="page-dashboard">
    <header>
      <h2><img src="/pata-branca.png" class="logo-pata" alt="" />PetHope</h2>
      <a href="#" style="color: white" @click.prevent="sair">Sair</a>
    </header>

    <div class="container">
      <h2>Bem-vindo, {{ nome }}</h2>

      <div class="card">
        <h3>ONGs parceiras</h3>
        <p>Conheça as ONGs cadastradas e veja os animais de cada uma.</p>
        <router-link class="btn" :to="{ name: 'ongs' }">Ver ONGs</router-link>
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
  try {
    const { data } = await http.get('/api/auth/me')

    if (!data.autenticado || data.tipo_sessao !== 'usuario') {
      router.push('/login')
      return
    }

    if (data.tipo_usuario !== 'adotante') {
      if (data.tipo_usuario === 'voluntario') {
        router.push('/dashboard_voluntario')
      } else {
        router.push('/login')
      }
      return
    }

    nome.value = data.nome
  } catch (err) {
    console.error('Erro ao carregar dashboard:', err)
    router.push('/login')
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

<style scoped src="../styles/dashboard.css"></style>
