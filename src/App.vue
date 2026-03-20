<template>
  <router-view />
</template>

<script setup>
import { useTelegram } from './composables/useTelegram'
import { useGridStore } from './stores/gridStore'

useTelegram()

const store = useGridStore()
store.loadFromSession()
</script>