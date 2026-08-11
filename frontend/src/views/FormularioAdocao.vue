<template>
<div class="page-formulario-adocao">
    <div class="container" v-if="animal">
      <h1>Solicitação de adoção</h1>
      <p>Animal: {{ animal.nome }}</p>

      <form @submit.prevent="enviar">
        <div class="form-group">
          <label for="nome">Nome completo:</label>
          <input id="nome" v-model="form.nome" type="text" required placeholder="Digite seu nome completo" />
        </div>

        <div class="form-group">
          <label for="cpf">CPF:</label>
          <input id="cpf" v-model="form.cpf" type="text" required placeholder="000.000.000-00" />
        </div>

        <div class="form-group">
          <label for="rg">RG:</label>
          <input id="rg" v-model="form.rg" type="text" required placeholder="00.000.000-0" />
        </div>

        <div class="form-group">
          <label for="telefone">Telefone:</label>
          <input id="telefone" v-model="form.telefone" type="text" required placeholder="(00) 00000-0000" />
        </div>

        <div class="form-group">
          <label for="endereco">Endereço:</label>
          <input id="endereco" v-model="form.endereco" type="text" required placeholder="Rua, número, bairro" />
        </div>

        <div class="form-group">
          <label for="motivo">Por que deseja adotar este animal?</label>
          <textarea id="motivo" v-model="form.motivo" rows="5" required placeholder="Conte um pouco sobre sua motivação"></textarea>
        </div>

        <div class="button-group">
          <button type="button" class="btn-back" @click="$router.back()">Voltar</button>
          <button type="submit" class="btn-next">Enviar Solicitação</button>
        </div>

        <p id="msg" :style="{ color: '#28a745' }">{{ msg }}</p>
      </form>
    </div>
</div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const props = defineProps({ id: { type: [String, Number], required: true } })
const router = useRouter()
const animal = ref(null)
const msg = ref('')

const form = reactive({
  nome: '',
  cpf: '',
  rg: '',
  telefone: '',
  endereco: '',
  motivo: '',
})

async function carregar() {
  const { data } = await http.get(`/api/animals/${props.id}`)
  animal.value = data
}

async function enviar() {
  const { data } = await http.post(`/api/animals/${props.id}/adopt`, form)
  msg.value = data.mensagem
  setTimeout(() => router.push('/adocao'), 1500)
}

onMounted(carregar)
</script>

<style scoped src="../styles/formulario_adocao.css"></style>
