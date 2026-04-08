<template>
  <header class="flex items-center justify-between px-2 py-2 flex-none">
    <!-- Left: Profile -->
    <div class="flex items-center gap-2">
      <img
        v-if="userData?.photo_url"
        :src="userData.photo_url"
        class="w-10 h-10 rounded-full object-cover"
      />
      <div class="flex flex-col">
        <span class="text-sm font-semibold text-[var(--tg-theme-text-color)]">
          {{ userData?.full_name }}
        </span>
        <span
          class="text-[10px] text-[var(--tg-theme-hint-color)] cursor-pointer select-none"
          @click="onGameIdTap"
        >
          {{ formattedGameId }} | {{ gameExpiryTime }}
        </span>
      </div>
    </div>

    <!-- Right: Reset All Button + Countdown -->
    <div class="text-right">
      <div class="text-right">
        <div
          v-if="timeToExpiry !== null"
          class="text-xs text-[var(--tg-theme-hint-color)] mb-1"
        >
        <span class="font-mono">{{ formattedCountdown }}</span>
        </div>
        <div v-else class="text-xs text-red-400 mb-1">⏰ Game Expired</div>
      </div>
      <button
        v-if="hasLines"
        class="text-xs text-red-400 px-3 py-1 rounded-md hover:bg-red-500 hover:text-white border cursor-pointer active:scale-95 transition-all duration-300 ease-in-out"
        @click="onResetAll"
      >
        Reset all lines
      </button>
    </div>
  </header>
</template>

<script setup>
const props = defineProps({
  userData: Object,
  formattedGameId: String,
  gameExpiryTime: String,
  timeToExpiry: Object,
  formattedCountdown: String,
  hasLines: Boolean,
});

const emit = defineEmits(['gameIdTap', 'resetAll']);

const onGameIdTap = () => {
  emit('gameIdTap');
};

const onResetAll = () => {
  emit('resetAll');
};
</script>
