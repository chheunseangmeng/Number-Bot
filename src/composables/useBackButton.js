import { ref } from 'vue'

export function useBackButton(onConfirm) {
  const showExitConfirm = ref(false)

  const init = () => {
    const tg = window.Telegram?.WebApp
    if (tg) {
      tg.enableClosingConfirmation()
      tg.BackButton.show()
      tg.BackButton.onClick(() => {
        showExitConfirm.value = true
      })
    }
  }

  const handleLeave = () => {
    onConfirm()
  }

  return {
    showExitConfirm,
    init,
    handleLeave,
  }
}