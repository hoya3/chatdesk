const BASE_URL = import.meta.env.VITE_CHATWOOT_BASE_URL || "http://localhost:3000";
const WEBSITE_TOKEN = import.meta.env.VITE_CHATWOOT_WEBSITE_TOKEN || "";

let readyPromise = null;

/**
 * Chatwoot SDK 스크립트를 앱 전체에서 한 번만 로드한다.
 * (App.vue의 onMounted에서 1회 호출)
 */
export function loadChatwoot() {
  if (readyPromise) return readyPromise;

  readyPromise = new Promise((resolve) => {
    window.chatwootSettings = {
      position: "right",
      type: "standard",
      launcherTitle: "채팅하기",
    };

    const script = document.createElement("script");
    script.src = `${BASE_URL}/packs/js/sdk.js`;
    script.async = true;
    document.body.appendChild(script);

    script.onload = () => {
      window.chatwootSDK.run({ websiteToken: WEBSITE_TOKEN, baseUrl: BASE_URL });
    };

    window.addEventListener("chatwoot:ready", () => resolve(), { once: true });
  });

  return readyPromise;
}

/**
 * 로그인 성공 직후 호출한다.
 * @param {{identifier: string, identifier_hash: string, email: string, name: string}} chatwootIdentity
 *        백엔드 /login 응답의 chatwoot 필드를 그대로 넘기면 된다.
 */
export async function identify(chatwootIdentity) {
  await loadChatwoot(); // 위젯이 아직 로드 안 됐으면 기다린다.
  window.$chatwoot?.setUser(chatwootIdentity.identifier, {
    identifier_hash: chatwootIdentity.identifier_hash,
    email: chatwootIdentity.email,
    name: chatwootIdentity.name,
  });
}

/**
 * 로그아웃 시 반드시 호출한다.
 * 호출하지 않으면 같은 브라우저를 쓰는 다음 방문자가 이전 사용자의
 * 대화 이력을 이어받는 사고가 될 수 있다.
 */
export function resetChatwoot() {
  window.$chatwoot?.reset();
}
