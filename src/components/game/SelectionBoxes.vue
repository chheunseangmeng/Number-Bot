<template>
  <div v-if="show" class="flex gap-2 w-full max-w-md flex-none">
    <div
      class="flex-1 h-10 rounded-md flex items-center justify-center text-2xl font-bold relative"
      :class="
        selectedNumbers[0] !== '?'
          ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]'
          : 'bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-hint-color)] border border-dashed border-[var(--tg-theme-hint-color)]'
      "
    >
      {{ selectedNumbers[0] }}
      <span
        v-if="selectedNumbers[0] !== '?'"
        class="absolute top-0 right-1 text-sm cursor-pointer"
        @click="onDeselect(selectedNumbers[0])"
      >
        ❌
      </span>
    </div>

    <div
      class="flex-1 h-10 rounded-md flex items-center justify-center text-2xl font-bold relative"
      :class="
        selectedNumbers[1] !== '?'
          ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]'
          : 'bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-hint-color)] border border-dashed border-[var(--tg-theme-hint-color)]'
      "
    >
      {{ selectedNumbers[1] }}
      <span
        v-if="selectedNumbers[1] !== '?'"
        class="absolute top-0 right-1 text-sm cursor-pointer"
        @click="onDeselect(selectedNumbers[1])"
      >
        ❌
      </span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: Boolean,
  selectedNumbers: Array,
});

const emit = defineEmits(['deselect']);

const onDeselect = (number) => {
  emit('deselect', number);
};
</script>
