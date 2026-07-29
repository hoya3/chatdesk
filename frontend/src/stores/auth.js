import { defineStore } from "pinia";
import api from "../services/api";
import { identify, resetChatwoot } from "../services/chatwoot";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: JSON.parse(localStorage.getItem("user") || "null"),
    token: localStorage.getItem("access_token") || null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async signup({ email, password, name }) {
      await api.post("/signup", { email, password, name });
    },

    async login({ email, password }) {
      const { data } = await api.post("/login", { email, password });

      this.token = data.access_token;
      this.user = { email: data.chatwoot.email, name: data.chatwoot.name };

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("user", JSON.stringify(this.user));

      // Chatwoot 위젯을 로그인 사용자로 식별시킨다.
      await identify(data.chatwoot);
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      resetChatwoot();
    },

    /** 새로고침 이후도 로그인 상태였다면 /me로 재확인하고 위젯을 다시 식별한다. */
    async restoreSession() {
      if (!this.token) return;
      try {
        const { data } = await api.get("/me");
        this.user = { email: data.user.email, name: data.user.name };
        localStorage.setItem("user", JSON.stringify(this.user));
        await identify(data.chatwoot);
      } catch {
        // 토큰 만료 등 - 로그아웃 처리
        this.logout();
      }
    },
  },
});
