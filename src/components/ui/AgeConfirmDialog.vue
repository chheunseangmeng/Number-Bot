<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-6">
    <div class="bg-white rounded-2xl p-6 w-full max-w-xs text-center shadow-xl">
      <div class="text-5xl mb-3">🔞</div>
      <h2 class="text-base font-bold text-gray-800 mb-1">Age Verification</h2>
      <p class="text-sm text-gray-500 mb-5">
        You must be 18 years or older to use this app. Are you 18+?
      </p>
      <div class="flex gap-3">
        <button
          class="flex-1 py-2 rounded-lg text-sm font-semibold
                 bg-gray-100 text-gray-600
                 active:scale-95 transition-all"
          @click="$emit('no')"
        >
          No
        </button>
        <button
          class="flex-1 py-2 rounded-lg text-sm font-semibold
                 bg-[#1e88e5] text-white
                 active:scale-95 transition-all"
          @click="$emit('yes')"
        >
          Yes, I'm 18+
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(['yes', 'no'])
</script>