<template>
  <div v-if="animal" class="page-editar-animal">
    <h1>Editar Animal</h1>

    <form @submit.prevent="salvar">
      <label>Nome:</label><br />
      <input type="text" v-model="animal.nome" required /><br /><br />

      <label>Espécie:</label><br />
      <input type="text" v-model="animal.especie" required /><br /><br />

      <label>Raça:</label><br />
      <input type="text" v-model="animal.raca" /><br /><br />

      <label>Idade:</label><br />
      <input type="number" v-model.number="animal.idade" /><br /><br />

      <label>Sexo:</label><br />
      <select v-model="animal.sexo">
        <option value="Macho">Macho</option>
        <option value="Fêmea">Fêmea</option>
        <option value="Outro">Outro</option>
      </select><br /><br />

      <label>Descrição:</label><br />
      <textarea
        v-model="animal.descricao"
        rows="5"
        cols="40"
      ></textarea><br /><br />

      <div class="foto-section">
        <label>Foto do animal:</label>

        <div v-if="animal.foto && !fotoPreview" class="foto-atual">
          <p>Foto atual:</p>
          <img
            :src="urlFoto(animal.foto)"
            :alt="`Foto de ${animal.nome}`"
            class="foto-animal"
          />
        </div>

        <div v-if="fotoPreview" class="foto-preview">
          <p>Nova foto:</p>
          <img
            :src="fotoPreview"
            :alt="`Prévia da nova foto de ${animal.nome}`"
            class="foto-animal"
          />
        </div>
        
        <div v-if="!animal.foto && !fotoPreview" class="sem-foto">
          <p>Este animal ainda não possui foto.</p>
        </div>

        <label class="upload-foto">
          <span class="upload-texto">
            <strong>Selecionar uma foto</strong>
            <small>JPG, JPEG, PNG ou WEBP</small>
          </span>

          <input
            type="file"
            accept="image/jpeg,image/png,image/webp"
            @change="selecionarFoto"
          />
        </label>
      </div>

      <br />

      <button type="submit" :disabled="salvando">
        {{ salvando ? 'Salvando...' : 'Salvar alterações' }}
      </button>
    </form>

    <br />

    <router-link to="/animais">Cancelar</router-link>
  </div>

  <div v-else-if="erro" class="erro">
    <p>{{ erro }}</p>
  </div>

  <div v-else class="carregando">
    <p>Carregando animal...</p>
  </div>
</template>

<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  }
})

const router = useRouter()

const animal = ref(null)
const erro = ref('')
const fotoSelecionada = ref(null)
const fotoPreview = ref('')
const salvando = ref(false)

function urlFoto(caminho) {
  if (!caminho) return ''

  if (caminho.startsWith('http')) {
    return caminho
  }

  const baseURL = http.defaults.baseURL || 'http://localhost:8000'

  return `${baseURL}${caminho}`
}

function selecionarFoto(event) {
  const arquivo = event.target.files?.[0]

  if (!arquivo) {
    return
  }

  if (!arquivo.type.startsWith('image/')) {
    alert('Selecione um arquivo de imagem.')
    event.target.value = ''
    return
  }

  const formatosPermitidos = [
    'image/jpeg',
    'image/png',
  ]

  if (!formatosPermitidos.includes(arquivo.type)) {
    alert('Formato não permitido. Use JPG, JPEG ou PNG.')
    event.target.value = ''
    return
  }

  if (fotoPreview.value) {
    URL.revokeObjectURL(fotoPreview.value)
  }
  fotoSelecionada.value = arquivo
  fotoPreview.value = URL.createObjectURL(arquivo)
}

async function carregar() {
  try {
    erro.value = ''

    const { data } = await http.get(`/api/animals/${props.id}`)

    animal.value = data
  } catch (err) {
    console.error('Erro ao carregar animal:', err)

    erro.value =
      err.response?.data?.detail ||
      'Não foi possível carregar o animal.'
  }
}

async function salvar() {
  if (!animal.value) {
    return
  }

  salvando.value = true
  erro.value = ''

  try {
    await http.put(`/api/animals/${props.id}`, {
      nome: animal.value.nome,
      especie: animal.value.especie,
      raca: animal.value.raca,
      idade: animal.value.idade,
      sexo: animal.value.sexo,
      descricao: animal.value.descricao
    })

    if (fotoSelecionada.value) {
      const formData = new FormData()

      formData.append('foto', fotoSelecionada.value)

      await http.post(
        `/api/animals/${props.id}/foto`,
        formData
      )
    }
    
    router.push('/animais')
  } catch (err) {
    console.error('Erro ao salvar alterações:', err)

    erro.value =
      err.response?.data?.detail ||
      'Erro ao salvar as alterações.'

    salvando.value = false
  }
}

onMounted(carregar)

onBeforeUnmount(() => {
  if (fotoPreview.value) {
    URL.revokeObjectURL(fotoPreview.value)
  }
})
</script>

<style scoped src="../styles/editar_animal.css"></style>
