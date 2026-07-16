<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
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
    <h1>회원가입</h1>

    <label>
      이름
      <input v-model="name" type="text" required />
    </label>

    <label>
      이메일
      <input v-model="email" type="email" required autocomplete="email" />
    </label>

    <label>
      비밀번호
      <input v-model="password" type="password" required autocomplete="new-password" />
    </label>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <button type="submit" :disabled="isSubmitting">
      {{ isSubmitting ? "가입 중..." : "회원가입" }}
    </button>
  </form>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  gap: 14px;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  padding: 28px;
}
label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
  color: #444;
}
input {
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 15px;
}
button {
  padding: 10px 12px;
  border: none;
  border-radius: 6px;
  background: #2f5496;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
}
button:disabled {
  opacity: 0.6;
  cursor: default;
}
.error {
  color: #c0392b;
  font-size: 14px;
  margin: 0;
}
</style>
