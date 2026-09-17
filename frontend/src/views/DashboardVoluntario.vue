<template>
  <div class="page-dashboard">

    <!-- NAVBAR -->
    <header class="navbar">

      <h2 class="logo">
        <img
          src="/pata-branca.png"
          class="logo-pata"
          alt=""
        />
        PetHope
      </h2>

      <nav class="menu">

        <router-link to="/dashboard_voluntario">
          Início
        </router-link>

        <router-link :to="{ name: 'ongs' }">
          Ongs disponíveis
        </router-link>

        <router-link to="/minhas_adocoes">
          Minhas adoções
        </router-link>

        <router-link to="/atividades">
          Voluntários
        </router-link>

        <router-link to="/doacoes">
          Doações
        </router-link>

        <router-link to="/perfil">
          Perfil
        </router-link>

        <a href="#" @click.prevent="sair">
          Sair
        </a>

      </nav>

    </header>


    <!-- CONTEÚDO -->
    <main class="dashboard-container">

      <!-- BOAS-VINDAS -->
      <section class="welcome-section">

        <div class="welcome-text">

          <p class="welcome-small">
            Seja bem-vindo ao PetHope! 🐾
          </p>

          <h1>
            Olá, {{ nome }}!
          </h1>

          <p class="welcome-description">
            Faça parte da nossa rede de voluntários e ajude
            a transformar a vida dos animais.
          </p>

          <router-link
            to="/atividades"
            class="btn-primary"
          >
            Encontrar atividades
          </router-link>

        </div>


        <!-- ARTE -->
        <div class="welcome-art">

          <div class="art-circle"></div>

          <span class="paw paw-1">🐾</span>
          <span class="paw paw-2">🐾</span>
          <span class="paw paw-3">🐾</span>

          <div class="art-heart">
            ♡
          </div>

        </div>

      </section>


      <!-- AÇÕES -->
      <section class="actions-section">

        <div class="section-title">

          <h2>
            O que você quer fazer?
          </h2>

          <p>
            Acesse rapidamente as principais opções.
          </p>

        </div>


        <div class="cards-grid">


          <!-- ADOTAR -->
          <div class="action-card destaque">

            <div class="card-icon">
              🐶
            </div>

            <div class="card-content">

              <h3>
                Encontrar um pet
              </h3>

              <p>
                Conheça nossas ONGs parceiras e encontre
                um animal esperando por um lar.
              </p>

              <router-link
                :to="{ name: 'ongs' }"
                class="card-link"
              >
                Ver ONGs →
              </router-link>

            </div>

          </div>


          <!-- ADOÇÕES -->
          <div class="action-card">

            <div class="card-icon">
              ❤️
            </div>

            <div class="card-content">

              <h3>
                Minhas adoções
              </h3>

              <p>
                Acompanhe os animais que você solicitou
                para adoção e veja o andamento das solicitações.
              </p>

              <router-link
                to="/minhas_adocoes"
                class="card-link"
              >
                Ver minhas adoções →
              </router-link>

            </div>

          </div>


          <!-- ATIVIDADES -->
          <div class="action-card">

            <div class="card-icon">
              🐾
            </div>

            <div class="card-content">

              <h3>
                Ser voluntário
              </h3>

              <p>
                Encontre atividades de ONGs parceiras
                e participe das ações.
              </p>

              <router-link
                to="/atividades"
                class="card-link"
              >
                Ver atividades →
              </router-link>

            </div>

          </div>


          <!-- MINHAS ATIVIDADES -->
          <div class="action-card">

            <div class="card-icon">
              📋
            </div>

            <div class="card-content">

              <h3>
                Minhas atividades
              </h3>

              <p>
                Acompanhe suas inscrições e veja
                as atividades de voluntariado das quais participa.
              </p>

              <router-link
                to="/minhas-atividades-voluntario"
                class="card-link"
              >
                Minhas atividades →
              </router-link>

            </div>

          </div>


          <!-- DOAÇÃO -->
          <div class="action-card">

            <div class="card-icon">
              💜
            </div>

            <div class="card-content">

              <h3>
                Fazer uma doação
              </h3>

              <p>
                Ajude uma ONG parceira a continuar
                cuidando dos animais.
              </p>

              <router-link
                to="/doacoes"
                class="card-link"
              >
                Doar agora →
              </router-link>

            </div>

          </div>


          <!-- HISTÓRICO DE DOAÇÕES -->
          <div class="action-card">

            <div class="card-icon">
              💰
            </div>

            <div class="card-content">

              <h3>
                Minhas doações
              </h3>

              <p>
                Consulte o histórico das doações
                que você já realizou.
              </p>

              <router-link
                to="/minhas-doacoes"
                class="card-link"
              >
                Ver histórico →
              </router-link>

            </div>

          </div>


        </div>

      </section>


      <!-- FRASE FINAL -->
      <section class="bottom-message">

        <div class="bottom-paw">
          🐾
        </div>

        <div>

          <h3>
            Pequenos gestos fazem grandes diferenças.
          </h3>

          <p>
            Cada adoção, doação e ação voluntária ajudam
            a transformar a vida de um animal.
          </p>

        </div>

      </section>

    </main>

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

    if (data.tipo_usuario !== 'voluntario') {

      if (data.tipo_usuario === 'adotante') {
        router.push('/dashboard_adotante')
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
