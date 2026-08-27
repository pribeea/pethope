<template>
<div class="page-cadastro-atividade">
    <header>
      <h2>
        <img src="/pata-branca.png" class="logo-pata" alt="" />PetHope</h2>
      <a href="#" @click.prevent="sair">Sair</a>
    </header>

    <main class="container">
      <h1>Cadastro de atividade</h1>
      <p>Cadastre uma nova oportunidade de voluntariado.</p>

      <form @submit.prevent="cadastrar">
        <div class="form-group">
          <label for="titulo">Título:</label>
          <input id="titulo" v-model="form.titulo" type="text" equired maxlength="150" placeholder="Ex.: Feira de adoção"/>
        </div>

        <div class="form-group">
          <label for="descricao">Descrição:</label>
          <textarea id="descricao" v-model="form.descricao" rows="5" required maxlength="1000" placeholder="Descreva resumidamente a atividade."></textarea>
        </div>

        <div class="form-group">
          <label for="detalhes">Detalhes da atividade:</label>
          <textarea id="detalhes" v-model="form.detalhes" rows="6" maxlength="3000" placeholder="Informe detalhes, orientações, materiais necessários, responsabilidades dos voluntários etc."></textarea>
        </div>

        <div class="linha">
          <div class="form-group">
            <label for="dias">Dias:</label>
            <input id="dias" v-model="form.dias" type="text" required maxlength="100" placeholder="Ex.: Segunda e quarta"/>
          </div>

          <div class="form-group">
            <label for="horario">Horário:</label>
            <input id="horario" v-model="form.horario" type="text" required maxlength="100" placeholder="Ex.: 08:00 às 12:00" />
          </div>

          <div class="form-group campo-vagas">
            <label for="vagas">Vagas:</label>
            <input id="vagas" v-model.number="form.vagas" type="number" min="1" max="1000" required/>
          </div>
        </div>

        <p v-if="msg" id="msg" :class="{ erro: erro }">
          {{ msg }}
        </p>

        <div class="button-group">
          <button
            type="button"
            class="btn-back"
            @click="router.push('/dashboard_ong')"
          >
            Voltar
          </button>

          <button
            type="submit"
            class="btn-next"
            :disabled="enviando"
          >
            {{ enviando ? 'Cadastrando...' : 'Cadastrar atividade' }}
          </button>
        </div>
      </form>
    </main>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()

const enviando = ref(false)
const msg = ref('')
const erro = ref(false)

const form = reactive({
  titulo: '',
  descricao: '',
  dias: '',
  horario: '',
  detalhes: '',
  vagas: 1,
})

async function cadastrar() {
  msg.value = ''
  erro.value = false

  try {
    enviando.value = true

    await http.post('/api/atividades', {
      titulo: form.titulo,
      descricao: form.descricao,
      dias: form.dias,
      horario: form.horario,
      detalhes: form.detalhes || null,
      vagas: form.vagas,
    })

    msg.value = 'Atividade cadastrada com sucesso!'

    setTimeout(() => {
      router.push('/atividades-ong')
    }, 1000)
  } catch (err) {
    erro.value = true
    msg.value = err.response?.data?.detail || 'Não foi possível cadastrar a atividade.'
  } finally {
    enviando.value = false
  }
}

async function sair() {
  try {
    await http.post('/api/auth/logout')
    router.push('/')
  } catch (err) {
    console.error(err)
  }
}
</script>

<style scoped src="../styles/cadastro_atividade.css"></style>