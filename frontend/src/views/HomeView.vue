<script setup>
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
</script>

<template>
  <div class="card">
    <h1>웹 실시간 상담 채팅 데모</h1>
    <p v-if="auth.isLoggedIn">
      {{ auth.user?.name }}님, 환영합니다. 우측 하단 채팅 버블로 상담을 시작해보세요.
    </p>
    <p v-else>
      게스트로도 바로 상담을 시작할 수 있습니다. 로그인하면 이전 상담 이력이 이어집니다.
    </p>
  </div>
</template>

<style scoped>
.card {
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  padding: 28px;
}
</style>
