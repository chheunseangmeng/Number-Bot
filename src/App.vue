<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useTelegram } from './composables/useTelegram'

onMounted(() => {
  const { } = useTelegram()
})
</script>