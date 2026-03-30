<template>
  <button
    class="w-full h-10 px-6 rounded-md text-sm font-semibold transition-all
           active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed
           focus:outline-none focus:ring-2 focus:ring-[var(--tg-theme-button-color)]
           flex items-center justify-center"
    :class="[
      variant === 'primary'
        ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)] hover:opacity-90'
        : 'bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-hint-color)] hover:opacity-90'
    ]"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot>{{ text }}</slot>
  </button>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: 'Next'
  },
  variant: {
    type: String,
    default: 'primary'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])
</script>