<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-6"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl p-6 w-full max-w-xs text-center shadow-xl">
      <div class="text-3xl mb-2">⚙️</div>
      <h2 class="text-sm font-bold text-gray-800 mb-1">Admin Config</h2>
      <p class="text-xs text-gray-400 mb-5">Game settings</p>

      <!-- One game per day toggle -->
      <div
        class="flex items-center justify-between px-2 py-3 bg-gray-50 rounded-xl mb-4"
      >
        <span class="text-sm font-semibold text-gray-700"
          >One game per day</span
        >
        <button
          class="relative w-12 h-6 rounded-full transition-colors duration-300 focus:outline-none"
          :class="oneGamePerDay ? 'bg-blue-500' : 'bg-gray-300'"
          @click="toggleOneGamePerDay"
        >
          <span
            class="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform duration-300"
            :class="oneGamePerDay ? 'translate-x-6' : 'translate-x-0'"
          />
        </button>
      </div>

      <!-- Expiry Time Setting (UTC) -->
      <div class="px-2 py-3 bg-gray-50 rounded-xl mb-4">
        <label class="text-sm font-semibold text-gray-700 block mb-2">
          Game Expiry Time (UTC)
        </label>
        <input
          type="number"
          v-model.number="expiryHourUTC"
          min="0"
          max="23"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg text-center text-lg font-bold"
          @change="saveExpiryTime"
        />
        <p class="text-[10px] text-gray-400 mt-1">
          Current: {{ expiryHourUTC }}:00 UTC ({{ expiryHourUTC + 7 }}:00
          Cambodia)
        </p>
      </div>

      <button
        class="w-full py-2 rounded-lg text-sm font-semibold bg-gray-100 text-gray-600 active:scale-95 transition-all"
        @click="close"
      >
        Close
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  modelValue: {
    type: Number,
    default: 19,
  },
});

const emit = defineEmits(['update:modelValue', 'close', 'toggleGamePerDay']);

const oneGamePerDay = ref(localStorage.getItem('one_game_per_day') !== 'false');
const expiryHourUTC = ref(props.modelValue);

const toggleOneGamePerDay = () => {
  oneGamePerDay.value = !oneGamePerDay.value;
  localStorage.setItem(
    'one_game_per_day',
    oneGamePerDay.value ? 'true' : 'false',
  );
  emit('toggleGamePerDay', oneGamePerDay.value);
};

const saveExpiryTime = () => {
  let hour = expiryHourUTC.value;
  if (isNaN(hour)) hour = 19;
  if (hour < 0) hour = 0;
  if (hour > 23) hour = 23;

  expiryHourUTC.value = hour;
  localStorage.setItem('expiry_hour_utc', hour.toString());
  emit('update:modelValue', hour);
};

const close = () => {
  emit('close');
};

watch(
  () => props.modelValue,
  (newVal) => {
    expiryHourUTC.value = newVal;
  },
);
</script>
