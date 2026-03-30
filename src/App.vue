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

onMounted(() => {
  const tg = window.Telegram?.WebApp
  store.loadFromSession()

  if (!sessionStorage.getItem('age_confirmed')) {
    showAgeConfirm.value = true
  }

  if (tg) {
    tg.enableClosingConfirmation()
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
</script>