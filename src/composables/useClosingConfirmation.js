import { onMounted } from "vue";

export function useClosingConfirmation() {
  onMounted(() => {
    const tg = window.Telegram?.WebApp;
    if (tg) {
      tg.enableClosingConfirmation();
    }
  });
}