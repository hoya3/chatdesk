<script setup>
import { onMounted } from "vue";
import { RouterLink, RouterView } from "vue-router";
import { useAuthStore } from "./stores/auth";
import { loadChatwoot } from "./services/chatwoot";

const auth = useAuthStore();

onMounted(() => {
  // 위젯은 앱 전체에서 한 번만 로드한다.
  loadChatwoot();
  // 새로고침 이후도 로그인 상태가 남아있으면 즉시 재식별한다.
  auth.restoreSession();
});
</script>

<template>
  <header class="nav">
    <RouterLink to="/" class="brand">상담 채팅 데모</RouterLink>
    <nav>
      <template v-if="auth.isLoggedIn">
        <span class="user">{{ auth.user?.name }} 님</span>
        <button @click="auth.logout()">로그아웃</button>
      </template>
      <template v-else>
        <RouterLink to="/login">로그인</RouterLink>
        <RouterLink to="/signup">회원가입</RouterLink>
      </template>
    </nav>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<style>
body {
  margin: 0;
  font-family: -apple-system, "Malgun Gothic", sans-serif;
  background: #f7f7f8;
}
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 24px;
  background: #fff;
  border-bottom: 1px solid #e5e5e5;
}
.brand {
  font-weight: 700;
  text-decoration: none;
  color: #222;
}
.nav nav {
  display: flex;
  gap: 12px;
  align-items: center;
}
main {
  max-width: 480px;
  margin: 60px auto;
  padding: 0 20px;
}
</style>
