import { onMounted } from "vue";

export function useClosingConfirmation() {
  onMounted(() => {
    const tg = window.Telegram?.WebApp;

    if (tg) {
      tg.enableClosingConfirmation();
      tg.BackButton.show();
      tg.BackButton.onClick(() => {
        tg.showConfirm("Are you sure you want to leave this page?", (confirmed) => {
          if (confirmed) {
            tg.close();
          }
        });
      });
    }
  });
}