<script setup>
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
</script>

<template>
  <div class="hero">
    <span class="badge">Live Chat</span>
    <h1>실시간 상담, 바로 시작하세요</h1>
    <p v-if="auth.isLoggedIn" class="lead">
      <strong>{{ auth.user?.name }}</strong>님, 환영합니다. 우측 하단 채팅 버블을 눌러 상담을 시작해보세요.
    </p>
    <p v-else class="lead">
      게스트로도 바로 상담을 시작할 수 있어요. 로그인하면 이전 상담 이력이 이어집니다.
    </p>

    <div class="hint">
      <span class="dot" />
      우측 하단 버블을 확인해 주세요
    </div>
  </div>
</template>

<style scoped>
.hero {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: 40px 32px;
  text-align: center;
}
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.02em;
  margin-bottom: 16px;
}
h1 {
  font-size: 24px;
  margin: 0 0 12px;
  letter-spacing: -0.01em;
}
.lead {
  color: var(--color-text-muted);
  font-size: 15px;
  line-height: 1.6;
  margin: 0;
}
.hint {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 28px;
  padding: 8px 14px;
  border-radius: 999px;
  background: var(--color-bg);
  color: var(--color-text-muted);
  font-size: 13px;
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22c55e;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15);
}
</style>
