<template>
<div class="page-formulario-doacao">
    <div class="container" v-if="doacao">
      <h1>💜 Pagamento da doação</h1>
      <p class="aviso-simulacao">
        ⚠️ Ambiente de simulação (protótipo acadêmico). Nenhum valor real será cobrado.
      </p>

      <p class="resumo">
        Doação de <strong>R$ {{ doacao.valor.toFixed(2) }}</strong> para
        <strong>{{ doacao.ong_nome }}</strong>
      </p>

      <div class="qr-wrapper">
        <img :src="doacao.qr_code_base64" alt="QR Code de pagamento (Pix simulado)" />
      </div>

      <div class="form-group">
        <label>Código de pagamento (Pix Copia e Cola simulado):</label>
        <div class="copia-cola">
          <input type="text" :value="doacao.codigo_pagamento" readonly />
          <button type="button" @click="copiar(doacao.codigo_pagamento)">Copiar</button>
        </div>
      </div>

      <div class="form-group">
        <label>Link de pagamento (simulado):</label>
        <div class="copia-cola">
          <input type="text" :value="doacao.link_pagamento" readonly />
          <button type="button" @click="copiar(doacao.link_pagamento)">Copiar</button>
        </div>
      </div>

      <p v-if="copiado" class="msg-copiado">Copiado para a área de transferência!</p>

      <div v-if="doacao.status === 'Pendente'" class="button-group">
        <button type="button" class="btn-back" @click="$router.push('/dashboard_adotante')">
          Fazer isso depois
        </button>

        <button type="button" class="btn-next" :disabled="confirmando" @click="confirmarPagamento">
          {{ confirmando ? 'Confirmando...' : 'Já paguei / Confirmar doação' }}
        </button>
      </div>

      <div v-else class="sucesso">
        <p>✅ Doação confirmada! Muito obrigado por apoiar a {{ doacao.ong_nome }}.</p>
        <router-link class="btn-next" to="/dashboard_adotante">
          Voltar ao dashboard
        </router-link>
      </div>
    </div>

    <div class="container" v-else-if="erro">
      <p class="erro-form">❌ {{ erro }}</p>
    </div>
</div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import http from '../api/http'

const props = defineProps({ id: { type: [String, Number], required: true } })

const doacao = ref(null)
const erro = ref('')
const confirmando = ref(false)
const copiado = ref(false)

async function carregar() {
  try {
    const { data } = await http.get(`/api/doacoes/${props.id}`)
    doacao.value = data
  } catch (err) {
    console.error('Erro ao carregar doação:', err)
    erro.value = err.response?.data?.detail || 'Doação não encontrada.'
  }
}

async function confirmarPagamento() {
  confirmando.value = true
  try {
    const { data } = await http.post(`/api/doacoes/${props.id}/confirmar`)
    doacao.value.status = data.status
  } catch (err) {
    console.error('Erro ao confirmar doação:', err)
  } finally {
    confirmando.value = false
  }
}

async function copiar(texto) {
  try {
    await navigator.clipboard.writeText(texto)
    copiado.value = true
    setTimeout(() => (copiado.value = false), 2000)
  } catch (err) {
    console.error('Erro ao copiar:', err)
  }
}

onMounted(carregar)
</script>

<style scoped src="../styles/formulario_doacao.css"></style>