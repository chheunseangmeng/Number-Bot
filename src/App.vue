<template>
  <div>
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

    <ConfirmDialog
      v-if="showExitConfirm"
      title="Leave App"
      message="Are you sure you want to leave this Mini App"
      yesText="Yes, Leave"
      noText="No"
      icon="⚠️"
      @yes="handleLeave"
      @no="showExitConfirm = false"
    />

    <router-view v-if="!showAgeConfirm" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ConfirmDialog from './components/ui/ConfirmDialog.vue'
import { useTelegram } from './composables/useTelegram'
import { useGridStore } from './stores/gridStore'
import { useBackButton } from './composables/useBackButton'

const { closeMiniApp, hapticFeedback } = useTelegram()
const store = useGridStore()
const { showExitConfirm, init, handleLeave } = useBackButton(closeMiniApp)

const showAgeConfirm = ref(false)

onMounted(() => {
  store.loadFromSession()
  if (!sessionStorage.getItem('age_confirmed')) {
    showAgeConfirm.value = true
  }
  init()
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