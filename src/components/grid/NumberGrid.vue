<template>
  <div class="grid grid-cols-4 gap-2 w-full max-w-md flex-1 min-h-0"
       style="grid-auto-flow: column; grid-template-rows: repeat(10, 1fr)">
    <button
      v-for="n in 40"
      :key="n"
      class="w-full rounded-md text-xl font-semibold transition-all duration-200
             flex items-center justify-center shadow-sm active:scale-95
             focus:outline-none focus:ring-2 focus:ring-[var(--tg-theme-button-color)]"
      :class="[
        store.isSelected(n)
          ? 'bg-[var(--tg-theme-accent-text-color,#6ab2f2)] text-white border-2 border-white shadow-md'
          : store.canSelectMore
            ? 'bg-[var(--tg-theme-button-color,#40a7e3)] text-[var(--tg-theme-button-text-color,white)] hover:opacity-90'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed opacity-50'
      ]"
      :disabled="!store.isSelected(n) && !store.canSelectMore"
      @click="handleClick(n)"
    >
      {{ n }}
    </button>
  </div>
</template>

<script setup>
import { useGridStore } from '../../stores/gridStore'

const store = useGridStore()

const handleClick = (number) => {
  if (store.canSelectMore) {
    store.selectNumber(number)
  }
}
</script>