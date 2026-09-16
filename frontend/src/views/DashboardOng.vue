<template>
  <div class="pagina-ong">

    <!-- NAVBAR -->
    <nav class="navbar">

      <router-link to="/dashboard_ong" class="logo">
        <span class="logo-pata">🐾</span>
        <span>PetHope</span>
      </router-link>

      <div class="menu">
        <router-link to="/dashboard_ong">Início</router-link>
        <router-link to="/animais">Meus animais</router-link>
        <router-link to="/solicitacoes">Adoções</router-link>
        <router-link to="/atividades-ong">Voluntários</router-link>
        <router-link to="/perfil">Perfil</router-link>

        <a href="#" @click.prevent="sair">
          Sair
        </a>
      </div>

    </nav>


    <!-- CONTEÚDO -->
    <main class="conteudo">

      <p class="boas-vindas">
        Bem-vinda, {{ nome }}!
      </p>

      <h1>Gerenciamento</h1>


      <!-- CADASTRAR ANIMAL -->
      <router-link
        to="/cadastro_animal"
        class="card-opcao"
      >

        <div class="icone icone-rosa">

          <svg viewBox="0 0 24 24">
            <path
              d="M20.8 8.6c0-2.5-2-4.4-4.4-4.4-1.6 0-3 .8-3.9 2.1a4.7 4.7 0 0 0-3.9-2.1c-2.4 0-4.4 2-4.4 4.4 0 5 8.3 10.4 8.3 10.4s8.3-5.3 8.3-10.4Z"
            />

            <path
              d="M6 12.5h2.3l1.3-2.3 1.6 4 1.2-1.7h2.3"
            />
          </svg>

        </div>

        <div class="texto-opcao">

          <h2>Cadastrar Animal</h2>

          <p>
            Cadastre um novo animal no sistema com informações e fotos.
          </p>

        </div>

        <span class="seta">›</span>

      </router-link>


      <!-- SOLICITAÇÕES -->
      <router-link
        to="/solicitacoes"
        class="card-opcao"
      >

        <div class="icone icone-amarelo">

          <svg viewBox="0 0 24 24">

            <path
              d="M3 14.5h4l2.6 1.5H15c1 0 1-1.3 0-1.3h-2.8"
            />

            <path
              d="M3 14.2v-4.4h2.4c.8 0 1.5.3 2.1.9l1.4 1.3h3.6c1.3 0 1.3 2 0 2"
            />

            <path
              d="M15.5 6.7c0-1.2-1-2.1-2.1-2.1-.8 0-1.4.4-1.9 1a2.6 2.6 0 0 0-1.9-1c-1.2 0-2.1 1-2.1 2.1 0 2.4 4 5 4 5s4-2.5 4-5Z"
            />

          </svg>

        </div>

        <div class="texto-opcao">

          <h2>Solicitações de Adoção</h2>

          <p>
            Acompanhe e gerencie todas as solicitações de adoção recebidas.
          </p>

        </div>

        <span class="seta">›</span>

      </router-link>


      <!-- VOLUNTARIADO -->
      <router-link
        to="/cadastrar-atividade"
        class="card-opcao"
      >

        <div class="icone icone-verde">

          <svg viewBox="0 0 24 24">

            <rect
              x="6"
              y="4.5"
              width="12"
              height="16"
              rx="1.6"
            />

            <path
              d="M9.5 4.5V3.8c0-.7.6-1.3 1.3-1.3h2.4c.7 0 1.3.6 1.3 1.3v.7"
            />

            <path
              d="M9 10.5h6M9 14h6M9 17.5h3.5"
            />

          </svg>

        </div>

        <div class="texto-opcao">

          <h2>Cadastrar Voluntariado</h2>

          <p>
            Cadastre novas atividades e oportunidades para voluntários.
          </p>

        </div>

        <span class="seta">›</span>

      </router-link>

    </main>


    <!-- PATINHAS DECORATIVAS -->
    <div class="patinhas">
      <span class="pata-grande">🐾</span>
      <span class="pata-pequena">🐾</span>
    </div>


    <!-- RODAPÉ -->
    <footer>

      <span class="footer-pata">🐾</span>

      <strong>PetHope</strong>

      <span>·</span>

      <span>
        Fazendo a diferença na vida dos animais.
      </span>

    </footer>

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

    console.log('DADOS DA SESSÃO:', data)

    if (!data.autenticado || data.tipo_sessao !== 'ong') {
      router.push('/login_ong')
      return
    }

    nome.value = data.nome

  } catch (erro) {
    console.error('Erro ao carregar sessão:', erro)
    router.push('/login_ong')
  }
}

async function sair() {

  try {

    await http.post('/api/auth/logout')

  } catch (erro) {

    console.error('Erro ao sair:', erro)

  }

  router.push('/')
}
onMounted(carregar)

</script>


<style scoped src="../styles/dashboard_ong.css"></style>
