<template>
  <div class="login-page">
    <div class="login-box">
      <LogoIxc></LogoIxc>
      <h1><p>SSL Manager</p></h1>
      <button class="login-button" @click="loginWithOIDC">Login with SSO</button>
    </div>
  </div>
</template>

<script>
definePageMeta({
  layout: 'layout-login'
})

export default {
  methods: {
    async loginWithOIDC() {
      try {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', 'https://papaya.ixcsoft.com.br:8000/auth_user/login/', true);
        xhr.onreadystatechange = function () {
          if (xhr.readyState == 4 && xhr.status == 200) {
            const hashResponse = JSON.parse(xhr.responseText);
            const { redirectURL } = hashResponse;

            // Redireciona para a nova rota no backend, que lida com o redirecionamento correto
            window.location.href = redirectURL;

            // Limpe a URL após o redirecionamento
            window.history.replaceState({}, document.title, window.location.pathname);
          }
        };
        xhr.send();
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
/* Seu estilo aqui */
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.login-box {
  text-align: center;
  padding: 100px;
  border: 1px solid #525151;
  border-radius: 8px;
  background-color: #00AEEF;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #636466;
  padding: 5px;
}

.login-button {
  background-color: #033a5f;
  color: #fff;
  padding: 10px 50px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #0a80cf;
}
</style>
