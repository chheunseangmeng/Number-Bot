<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-6">
    <div class="bg-white rounded-2xl p-6 w-full max-w-xs text-center shadow-xl animate-scaleIn">

      <!-- Icon -->
      <div v-if="icon" class="text-5xl mb-3">{{ icon }}</div>

      <!-- Title -->
      <h2 class="text-base font-bold text-gray-800 mb-1">
        {{ title }}
      </h2>

      <!-- Message -->
      <p class="text-sm text-gray-500 mb-5">
        {{ message }}
      </p>

      <!-- Buttons -->
      <div class="flex gap-3">
        <button
          class="flex-1 py-2 rounded-lg text-sm font-semibold
                 bg-gray-100 text-gray-600
                 active:scale-95 transition-all"
          @click="$emit('no')"
        >
          {{ noText }}
        </button>

        <button
          class="flex-1 py-2 rounded-lg text-sm font-semibold
                 bg-[#1e88e5] text-white
                 active:scale-95 transition-all"
          @click="$emit('yes')"
        >
          {{ yesText }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: "Confirmation"
  },
  message: {
    type: String,
    default: "Are you sure?"
  },
  yesText: {
    type: String,
    default: "Yes"
  },
  noText: {
    type: String,
    default: "No"
  },
  icon: {
    type: String,
    default: ""
  }
})

defineEmits(['yes', 'no'])
</script>

<style>
@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.animate-scaleIn {
  animation: scaleIn 0.2s ease;
}
</style>