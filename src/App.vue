<template>
  <div>
    <AgeConfirmDialog
      v-if="showAgeConfirm"
      @yes="handleYes"
      @no="handleNo"
    />
    <router-view v-if="!showAgeConfirm" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTelegram } from './composables/useTelegram'
import { useGridStore } from './stores/gridStore'
import AgeConfirmDialog from './components/ui/AgeConfirmDialog.vue'

const { closeMiniApp, hapticFeedback } = useTelegram()
const store = useGridStore()
const showAgeConfirm = ref(false)

onMounted(() => {
  store.loadFromSession()
  if (!sessionStorage.getItem('age_confirmed')) {
    showAgeConfirm.value = true
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