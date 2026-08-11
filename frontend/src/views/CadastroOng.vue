<template>
<div class="page-cadastro-ong">
    <div class="main-wrapper">
      <div class="container">
        <h1>Cadastro de ONG</h1>
        <p class="subtitle">Cadastre sua instituição e ajude a transformar vidas. 🐾</p>

        <form @submit.prevent="cadastrar">
          <div class="form-group">
            <label for="nome">Nome da ONG:</label>
            <input id="nome" v-model="form.nome" type="text" required placeholder="Nome da instituição" />
          </div>

          <div class="form-group">
            <label for="cnpj">CNPJ:</label>
            <input id="cnpj" v-model="form.cnpj" type="text" required placeholder="00.000.000/0000-00" />
          </div>

          <div class="form-group">
            <label for="endereco">Endereço:</label>
            <input id="endereco" v-model="form.endereco" type="text" required placeholder="Rua, número, bairro" />
          </div>

          <div class="form-group">
            <label for="contato">Contato:</label>
            <input id="contato" v-model="form.contato" type="text" required placeholder="(00) 00000-0000" />
          </div>

          <div class="form-group">
            <label for="senha">Senha:</label>
            <input id="senha" v-model="form.senha" type="password" required placeholder="Crie uma senha segura" />
          </div>

          <div class="button-group">
            <button type="button" class="btn-back" @click="$router.back()">Voltar</button>
            <button type="submit" class="btn-next">Cadastrar ONG</button>
          </div>

          <div id="mensagem" :style="{ color: cor, display: mensagem ? 'block' : 'none' }">
            {{ mensagem }}
          </div>
        </form>
      </div>

      <div class="sidebar">
        <div class="logo-container">🐾 PETHOPE</div>
        <div class="dog-image-container">
          <img src="/imagens/img_cadastro.jpg" alt="Pets" class="pet-img" />
        </div>
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
  cnpj: '',
  endereco: '',
  contato: '',
  senha: '',
})

const mensagem = ref('')
const cor = ref('#27ae60')

async function cadastrar() {
  try {
    await http.post('/api/ongs', form)
    mensagem.value = 'ONG cadastrada com sucesso!'
    cor.value = '#27ae60'
    setTimeout(() => router.push('/login_ong'), 1000)
  } catch (err) {
    cor.value = '#d9534f'
    mensagem.value = err.response?.data?.detail || 'Erro ao cadastrar ONG'
  }
}
</script>

<style scoped src="../styles/cadastro_ong.css"></style>
