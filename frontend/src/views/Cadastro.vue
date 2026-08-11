<template>
<div class="page-cadastro">
    <div class="main-wrapper">
      <div class="sidebar">
        <div class="logo-container">🐾 PETHOPE</div>
        <div class="dog-image-container">
          <img src="/imagens/img_cadastro.jpg" alt="Pets" class="pet-img" />
        </div>
      </div>

      <div class="container">
        <h1>Criar Conta</h1>
        <p class="subtitle">Bem-vindo ao PetHope! Garanta o melhor para os pets. 🐾</p>

        <form @submit.prevent="cadastrar">
          <div class="form-group">
            <label for="nome">Nome Completo:</label>
            <input id="nome" v-model="form.nome" type="text" required placeholder="Digite seu nome" />
          </div>

          <div class="form-group">
            <label for="email">E-mail:</label>
            <input id="email" v-model="form.email" type="email" required placeholder="exemplo@email.com" />
          </div>

          <div class="form-group">
            <label for="senha">Senha:</label>
            <input id="senha" v-model="form.senha" type="password" required minlength="6" placeholder="Mínimo 6 caracteres" />
          </div>

          <div class="form-group">
            <label for="tipo">Tipo de Usuário:</label>
            <select id="tipo" v-model="form.tipo" required>
              <option value="" disabled selected>Selecione uma opção...</option>
              <option value="voluntario">Voluntário</option>
              <option value="adotante">Adotante</option>
            </select>
          </div>

          <div class="button-group">
            <button type="button" class="btn-back" @click="$router.back()">Voltar</button>
            <button type="submit" class="btn-next">Cadastrar</button>
          </div>

          <div id="mensagem" :style="{ color: cor, display: mensagem ? 'block' : 'none' }">
            {{ mensagem }}
          </div>
        </form>
      </div>
    </div>
</div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()

const form = reactive({
  nome: '',
  email: '',
  senha: '',
  tipo: '',
})

const mensagem = ref('')
const cor = ref('#27ae60')

async function cadastrar() {
  try {
    await http.post('/api/users', form)
    mensagem.value = 'Cadastro realizado! Redirecionando...'
    cor.value = '#27ae60'
    setTimeout(() => router.push('/login'), 1000)
  } catch (err) {
    cor.value = '#d9534f'
    mensagem.value = err.response?.data?.detail || 'Erro ao cadastrar'
  }
}
</script>

<style scoped src="../styles/cadastro.css"></style>
