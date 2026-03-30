<template>
  <div>
    <!-- Age Confirm -->
    <ConfirmDialog
      v-if="showAgeConfirm"
      title="Age Verification"
      message="You must be 18 years or older to use this app. Are you 18+?"
      yesText="Yes, I'm 18+"
      noText="No"
      icon="🔞"
      @yes="handleYes"
      @no="handleNo"
    />

    <!-- Exit Confirm -->
    <ConfirmDialog
      v-if="showExitConfirm"
      title="Leave Page"
      message="Are you sure you want to leave this page?"
      yesText="Yes"
      noText="Stay"
      icon="⚠️"
      @yes="confirmExit"
      @no="showExitConfirm = false"
    />

    <!-- Main App -->
    <router-view v-if="!showAgeConfirm" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ConfirmDialog from './components/ui/ConfirmDialog.vue'
import { useTelegram } from './composables/useTelegram'
import { useGridStore } from './stores/gridStore'

const { closeMiniApp, hapticFeedback } = useTelegram()
const store = useGridStore()

const showAgeConfirm = ref(false)
const showExitConfirm = ref(false)

onMounted(() => {
  const tg = window.Telegram?.WebApp

  store.loadFromSession()

  // Age check
  if (!sessionStorage.getItem('age_confirmed')) {
    showAgeConfirm.value = true
  }

  if (tg) {
    tg.enableClosingConfirmation()
    tg.BackButton.show()

    tg.BackButton.onClick(() => {
      showExitConfirm.value = true
    })
  }
})

const handleYes = () => {
  hapticFeedback('light')
  sessionStorage.setItem('age_confirmed', 'true')
  showAgeConfirm.value = false
}

const handleNo = () => {
  hapticFeedback('light')
  closeMiniApp()
}

const confirmExit = () => {
  closeMiniApp()
}
</script>