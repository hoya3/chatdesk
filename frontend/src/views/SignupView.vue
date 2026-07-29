<script setup>
import { ref } from "vue";
import { useRouter, RouterLink } from "vue-router";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const router = useRouter();

const name = ref("");
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const isSubmitting = ref(false);

async function handleSubmit() {
  errorMessage.value = "";
  isSubmitting.value = true;
  try {
    await auth.signup({ name: name.value, email: email.value, password: password.value });
    await auth.login({ email: email.value, password: password.value });
    router.push("/");
  } catch (err) {
    errorMessage.value = err.response?.data?.detail || "회원가입에 실패했습니다.";
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <form class="card" @submit.prevent="handleSubmit">
    <div class="card-head">
      <h1>계정 만들기</h1>
      <p class="sub">몇 초면 가입 끝, 바로 상담을 시작할 수 있어요.</p>
    </div>

    <label>
      이름
      <input v-model="name" type="text" required placeholder="홍길동" />
    </label>

    <label>
      이메일
      <input v-model="email" type="email" required autocomplete="email" placeholder="you@example.com" />
    </label>

    <label>
      비밀번호
      <input v-model="password" type="password" required autocomplete="new-password" placeholder="••••••••" />
    </label>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <button class="btn-primary" type="submit" :disabled="isSubmitting">
      {{ isSubmitting ? "가입 중..." : "회원가입" }}
    </button>

    <p class="switch">
      이미 계정이 있으신가요? <RouterLink to="/login">로그인</RouterLink>
    </p>
  </form>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: 32px;
}
.card-head h1 {
  font-size: 20px;
  margin: 0 0 4px;
  letter-spacing: -0.01em;
}
.sub {
  margin: 0;
  font-size: 14px;
  color: var(--color-text-muted);
}
label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
}
input {
  padding: 11px 13px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 15px;
  font-weight: 400;
  color: var(--color-text);
  background: var(--color-bg);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
input:focus {
  outline: none;
  border-color: var(--color-primary);
  background: #fff;
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}
.error {
  color: var(--color-danger);
  font-size: 13px;
  margin: 0;
}
.switch {
  text-align: center;
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
}
.switch a {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
}
</style>
