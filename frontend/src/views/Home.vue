<template>
<div class="page-home">
    <div class="main-container">
      <div class="left-section">
        <div class="logo">🐾 PetHope</div>

        <div class="hero-content">
          <h1>Bem vindo ao PetHope!</h1>
          <p>
            Uma plataforma que ajuda ONGs de proteção animal a organizar
            adoções, doações, animais e voluntários de forma simples, rápida e
            prática.
          </p>
        </div>

        <div class="selection-area">
          <h2>COMO DESEJA SE CADASTRAR?</h2>

          <div class="options-container">
            <router-link to="/cadastro" class="card-option">
              <span>Pessoa Física</span>
            </router-link>

            <router-link to="/cadastro_ong" class="card-option">
              <span>Sou uma ONG</span>
            </router-link>
          </div>
        </div>

        <div class="login-footer">
          Já tem uma conta?
          <router-link to="/opcoes_login">Faça login aqui</router-link>
        </div>
      </div>

      <div class="right-section">
        <img src="/imagens/img_index.jpg" alt="PetHope" />
      </div>
    </div>
</div>
</template>

<script setup>
</script>

<style scoped src="../styles/index.css"></style>
