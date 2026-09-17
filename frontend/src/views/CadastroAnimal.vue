<template>
  <div class="page-cadastro-animal">
    <div class="main-wrapper">
      <div class="sidebar">
        <div class="logo-container">
          <img src="/pata-branca.png" class="logo-pata" alt="" />
          PETHOPE
        </div>

        <div class="dog-image-container">
          <img
            src="/imagens/img_cadastro.jpg"
            alt="Pets"
            class="pet-img"
          />
        </div>
      </div>

      <div class="container">
        <h1>Cadastrar Animal</h1>

        <p class="subtitle">
          Registre um novo amigo para encontrar um lar. 🐾
        </p>

        <form @submit.prevent="cadastrar">

          <div class="form-group">
            <label for="nome">Nome:</label>

            <input
              id="nome"
              v-model="form.nome"
              type="text"
              required
              placeholder="Nome do animal"
            />
          </div>

          <div class="form-row">

            <div class="form-group half">
              <label for="especie">Espécie:</label>

              <input
                id="especie"
                v-model="form.especie"
                type="text"
                required
                placeholder="Ex: Cachorro"
              />
            </div>

            <div class="form-group half">
              <label for="raca">Raça:</label>

              <input
                id="raca"
                v-model="form.raca"
                type="text"
                placeholder="Ex: Poodle"
              />
            </div>

          </div>

          <div class="form-row">

            <div class="form-group half">
              <label for="idade">Idade:</label>

              <div class="idade-container">
                <input
                  id="idade"
                  v-model.number="form.idade"
                  type="number"
                  min="0"
                  placeholder="Idade"
                />

                <select v-model="form.unidade_idade">
                  <option value="anos">Anos</option>
                  <option value="meses">Meses</option>
                </select>
              </div>
            </div>

            <div class="form-group half">
              <label for="sexo">Sexo:</label>

              <input
                id="sexo"
                v-model="form.sexo"
                type="text"
                placeholder="Macho/Fêmea"
              />
            </div>

          </div>

          <div class="form-group">
            <label for="descricao">Descrição:</label>

            <textarea
              id="descricao"
              v-model="form.descricao"
              placeholder="Conte um pouco sobre o pet..."
            ></textarea>
          </div>

          <div class="form-group foto-group">

            <label for="foto">
              Foto do animal
              <span>(opcional)</span>:
            </label>

            <label class="upload-foto" for="foto">

              <span class="upload-texto">
                <strong>Escolher uma foto</strong>
                <small>JPG, JPEG, PNG ou WEBP</small>
              </span>

              <input
                id="foto"
                type="file"
                accept="image/jpeg,image/png,image/webp"
                @change="selecionarFoto"
              />

            </label>

            <div
              v-if="fotoPreview"
              class="foto-preview"
            >

              <img
                :src="fotoPreview"
                alt="Prévia da foto do animal"
              />

              <button
                type="button"
                class="remover-foto"
                @click="removerFoto"
              >
                Remover foto
              </button>

            </div>

          </div>

          <div class="button-group">

            <button
              type="button"
              class="btn-back"
              @click="$router.back()"
            >
              Voltar
            </button>

            <button
              type="submit"
              class="btn-next"
            >
              Cadastrar
            </button>

          </div>

          <p
            id="msg"
            :style="{ color: '#d9534f' }"
          >
            {{ msg }}
          </p>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import http from '../api/http'

const router = useRouter()

const form = reactive({
  nome: '',
  especie: '',
  raca: '',
  idade: null,
  unidade_idade: 'anos',
  sexo: '',
  descricao: '',
})

const msg = ref('')
const fotoSelecionada = ref(null)
const fotoPreview = ref('')

function selecionarFoto(event) {
  const arquivo = event.target.files?.[0]

  if (!arquivo) {
    return
  }

  const formatosPermitidos = [
    'image/jpeg',
    'image/png',
    'image/webp',
  ]

  if (!formatosPermitidos.includes(arquivo.type)) {
    msg.value =
      'Formato de imagem não permitido. Use JPG, JPEG, PNG ou WEBP.'

    event.target.value = ''
    return
  }

  if (fotoPreview.value) {
    URL.revokeObjectURL(fotoPreview.value)
  }

  fotoSelecionada.value = arquivo
  fotoPreview.value = URL.createObjectURL(arquivo)

  msg.value = ''
}

function removerFoto() {
  fotoSelecionada.value = null

  if (fotoPreview.value) {
    URL.revokeObjectURL(fotoPreview.value)
    fotoPreview.value = ''
  }

  const input = document.getElementById('foto')

  if (input) {
    input.value = ''
  }
}

async function cadastrar() {
  try {
    const { data } = await http.post(
      '/api/animals',
      form
    )

    if (fotoSelecionada.value) {
      const formData = new FormData()

      formData.append(
        'foto',
        fotoSelecionada.value
      )

      await http.post(
        `/api/animals/${data.id}/foto`,
        formData
      )
    }

    router.push('/animais')

  } catch (err) {
    msg.value =
      err.response?.data?.detail ||
      'Erro ao cadastrar'
  }
}

onBeforeUnmount(() => {
  if (fotoPreview.value) {
    URL.revokeObjectURL(fotoPreview.value)
  }
})
</script>

<style scoped src="../styles/cadastro_animal.css"></style>
