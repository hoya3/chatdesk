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
    <RouterLink to="/" class="brand">
      <span class="brand-mark">C</span>
      상담 채팅
    </RouterLink>
    <nav>
      <template v-if="auth.isLoggedIn">
        <span class="user">{{ auth.user?.name }}님</span>
        <button class="btn-ghost" @click="auth.logout()">로그아웃</button>
      </template>
      <template v-else>
        <RouterLink to="/login" class="link">로그인</RouterLink>
        <RouterLink to="/signup" class="btn-primary btn-sm">회원가입</RouterLink>
      </template>
    </nav>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<style>
:root {
  --color-bg: #f6f7fb;
  --color-surface: #ffffff;
  --color-border: #e6e8f0;
  --color-text: #14161f;
  --color-text-muted: #6b7080;
  --color-primary: #4f46e5;
  --color-primary-hover: #4338ca;
  --color-primary-soft: #eef1ff;
  --color-danger: #dc2626;
  --radius-md: 10px;
  --radius-lg: 16px;
  --shadow-card: 0 1px 2px rgba(20, 22, 31, 0.04), 0 8px 24px rgba(20, 22, 31, 0.06);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: "Pretendard", -apple-system, "Malgun Gothic", "Segoe UI", sans-serif;
  background: var(--color-bg);
  color: var(--color-text);
  -webkit-font-smoothing: antialiased;
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 32px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 10;
}
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 15px;
  text-decoration: none;
  color: var(--color-text);
}
.brand-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 8px;
  background: var(--color-primary);
  color: #fff;
  font-size: 13px;
  font-weight: 700;
}
.nav nav {
  display: flex;
  gap: 16px;
  align-items: center;
}
.nav .link {
  color: var(--color-text-muted);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}
.nav .link:hover {
  color: var(--color-text);
}
.user {
  font-size: 14px;
  color: var(--color-text-muted);
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  border: none;
  border-radius: var(--radius-md);
  background: var(--color-primary);
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.15s ease;
}
.btn-primary:hover {
  background: var(--color-primary-hover);
}
.btn-primary:disabled {
  opacity: 0.6;
  cursor: default;
}
.btn-sm {
  padding: 7px 14px;
  font-size: 13px;
}
.btn-ghost {
  padding: 7px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-ghost:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

main {
  max-width: 480px;
  margin: 72px auto;
  padding: 0 20px;
}
</style>
