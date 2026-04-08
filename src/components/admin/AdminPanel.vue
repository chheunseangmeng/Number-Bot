<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm px-5"
    @click.self="close"
  >
    <div
      class="bg-white rounded-2xl p-5 w-full max-w-sm text-left shadow-2xl border border-gray-100"
    >
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-base font-bold text-gray-900">Admin Settings</h2>
          <p class="text-xs text-gray-500">Adjust game rules and timing</p>
        </div>
        <button
          class="text-xs font-semibold text-gray-500 hover:text-gray-800"
          @click="close"
        >
          Close
        </button>
      </div>

      <!-- One game per day toggle -->
      <div class="px-3 py-3 bg-gray-50 rounded-xl mb-4 border border-gray-100">
        <div class="flex items-center justify-between">
          <div>
            <span class="text-sm font-semibold text-gray-800">One game per day</span>
            <p class="text-[11px] text-gray-500 mt-0.5">
              Prevent multiple plays within the same day
            </p>
          </div>
          <button
            class="relative w-12 h-6 rounded-full transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
            :class="oneGamePerDay ? 'bg-blue-500' : 'bg-gray-300'"
            @click="toggleOneGamePerDay"
          >
            <span
              class="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform duration-300"
              :class="oneGamePerDay ? 'translate-x-6' : 'translate-x-0'"
            />
          </button>
        </div>
        <div class="mt-2">
          <span
            class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold"
            :class="
              oneGamePerDay ? 'bg-blue-50 text-blue-700' : 'bg-gray-100 text-gray-600'
            "
          >
            {{ oneGamePerDay ? 'Enabled' : 'Disabled' }}
          </span>
        </div>
      </div>

      <!-- Expiry Time Setting (UTC) -->
      <div class="px-3 py-3 bg-gray-50 rounded-xl mb-4 border border-gray-100">
        <label class="text-sm font-semibold text-gray-800 block mb-1">
          Game expiry time (UTC)
        </label>
        <p class="text-[11px] text-gray-500 mb-2">
          Use 0-23 for hours and 0-59 for minutes. Cambodia time is UTC+7.
        </p>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="text-[11px] text-gray-500 block mb-1">Hour</label>
            <input
              type="number"
              v-model.number="expiryHourUTC"
              min="0"
              max="23"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg text-center text-lg font-bold focus:outline-none focus:ring-2 focus:ring-blue-400"
              @change="saveExpiryTime"
            />
          </div>
          <div>
            <label class="text-[11px] text-gray-500 block mb-1">Minute</label>
            <input
              type="number"
              v-model.number="expiryMinuteUTC"
              min="0"
              max="59"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg text-center text-lg font-bold focus:outline-none focus:ring-2 focus:ring-blue-400"
              @change="saveExpiryTime"
            />
          </div>
        </div>
        <p class="text-[10px] text-gray-400 mt-2">
          Current: {{ paddedHour }}:{{ paddedMinute }} UTC ({{ cambodiaTime }})
        </p>
      </div>

      <div class="flex gap-2">
        <button
          class="flex-1 py-2 rounded-lg text-sm font-semibold bg-gray-100 text-gray-700 active:scale-95 transition-all"
          @click="close"
        >
          Cancel
        </button>
        <button
          class="flex-1 py-2 rounded-lg text-sm font-semibold bg-blue-600 text-white hover:bg-blue-700 active:scale-95 transition-all"
          @click="close"
        >
          Done
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  hour: {
    type: Number,
    default: 19,
  },
  minute: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(['update:hour', 'update:minute', 'close', 'toggleGamePerDay']);

const oneGamePerDay = ref(localStorage.getItem('one_game_per_day') !== 'false');
const expiryHourUTC = ref(props.hour);
const expiryMinuteUTC = ref(props.minute);

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
  let minute = expiryMinuteUTC.value;
  if (isNaN(hour)) hour = 19;
  if (isNaN(minute)) minute = 0;
  if (hour < 0) hour = 0;
  if (hour > 23) hour = 23;
  if (minute < 0) minute = 0;
  if (minute > 59) minute = 59;

  expiryHourUTC.value = hour;
  expiryMinuteUTC.value = minute;
  localStorage.setItem('expiry_hour_utc', hour.toString());
  localStorage.setItem('expiry_minute_utc', minute.toString());
  emit('update:hour', hour);
  emit('update:minute', minute);
};

const close = () => {
  emit('close');
};

const paddedHour = computed(() =>
  String(expiryHourUTC.value).padStart(2, '0'),
);
const paddedMinute = computed(() =>
  String(expiryMinuteUTC.value).padStart(2, '0'),
);
const cambodiaTime = computed(() => {
  const hour = (expiryHourUTC.value + 7) % 24;
  return `${String(hour).padStart(2, '0')}:${paddedMinute.value} Cambodia`;
});

watch(
  () => props.hour,
  (newVal) => {
    expiryHourUTC.value = newVal;
  },
);
watch(
  () => props.minute,
  (newVal) => {
    expiryMinuteUTC.value = newVal;
  },
);
</script>
