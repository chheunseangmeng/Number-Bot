<template>
  <div class="h-screen flex flex-col bg-[var(--tg-theme-bg-color)]">
    <!-- Header Component -->
    <GameHeader
      :userData="store.userData"
      :formattedGameId="formattedGameId"
      :gameExpiryTime="gameExpiryDateTimeCambodia"
      :timeToExpiry="timeToExpiry"
      :formattedCountdown="formattedTimeToExpiry"
      :hasLines="store.lines.length > 0 || store.selectedCount > 0"
      @gameIdTap="handleGameIdTap"
      @resetAll="handleResetAll"
    />

    <!-- Admin Panel Component -->
    <AdminPanel
      :show="showAdminPanel"
      v-model:hour="expiryHourUTC"
      v-model:minute="expiryMinuteUTC"
      @close="showAdminPanel = false"
      @toggleGamePerDay="handleToggleGamePerDay"
    />

    <!-- Already Played or Expired -->
    <div
      v-if="alreadyPlayedToday || isGameExpired"
      class="flex-1 flex flex-col items-center justify-center px-6 text-center"
    >
      <div class="text-5xl mb-4">🚫</div>
      <h2 class="text-lg font-bold text-[var(--tg-theme-text-color)] mb-2">
        Come back tomorrow!
      </h2>
      <p v-if="alreadyPlayedToday" class="text-sm text-[var(--tg-theme-hint-color)]">
        You have already played today ({{ formattedGameId }}). A new game will
        be available tomorrow.
      </p>
      <p v-else class="text-sm text-[var(--tg-theme-hint-color)]">
        Today&apos;s game has expired. A new game will be available tomorrow.
      </p>
    </div>

    <!-- MAIN -->
    <div v-else class="flex-1 flex flex-col items-center p-2 min-h-0 w-full">
      <NumberGrid />

      <hr class="w-full max-w-md my-2" />

      <!-- Lines List Component -->
      <LinesList
        :lines="store.lines"
        :show="isShowLines"
        :editingIndex="store.editingIndex"
        :selectedNumbers="selectedNumbers"
        @editLine="handleEditLine"
        @deleteLine="handleDeleteLine"
      />

      <!-- Selection Boxes Component -->
      <SelectionBoxes
        :show="
          store.linesCount < store.MAX_LINES || store.editingIndex !== null
        "
        :selectedNumbers="selectedNumbers"
        @deselect="store.deselectNumber"
      />

      <!-- Toggle show lines -->
      <div
        v-if="store.lines.length > 0"
        class="flex items-center justify-center w-full max-w-md mt-1"
      >
        <p
          @click="isShowLines = !isShowLines"
          class="text-sm text-[var(--tg-theme-hint-color)] underline cursor-pointer"
        >
          {{ isShowLines ? 'Hide' : 'Show' }} line list (
          {{ store.linesCount }}/{{ store.MAX_LINES }})
        </p>
      </div>

      <!-- Game Actions Component -->
      <GameActions
        :isMaxReached="
          store.linesCount === store.MAX_LINES && store.editingIndex === null
        "
        :canSave="canSave"
        :canAddLine="canAddLine"
        :canSubmit="canSubmit"
        :canNext="canNext"
        @saveLine="handleSaveLine"
        @submit="handleSubmit"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import NumberGrid from '@/components/grid/NumberGrid.vue';
import GameHeader from '@/components/game/GameHeader.vue';
import LinesList from '@/components/game/LinesList.vue';
import SelectionBoxes from '@/components/game/SelectionBoxes.vue';
import GameActions from '@/components/game/GameActions.vue';
import AdminPanel from '@/components/admin/AdminPanel.vue';
import { useGridStore } from '../stores/gridStore';
import { useTelegram } from '../composables/useTelegram';
import { useGameTimer } from '../composables/useGameTimer';

const store = useGridStore();
const router = useRouter();
const { hapticFeedback } = useTelegram();

// ADMIN SETTINGS
const showAdminPanel = ref(false);
const oneGamePerDay = ref(localStorage.getItem('one_game_per_day') !== 'false');
const expiryHourUTC = ref(
  parseInt(localStorage.getItem('expiry_hour_utc') || '19'),
);
const expiryMinuteUTC = ref(
  parseInt(localStorage.getItem('expiry_minute_utc') || '0'),
);

// TIMER
const {
  timeToExpiry,
  formattedTimeToExpiry,
  getCambodiaTime,
  startExpiryCountdown,
  stopExpiryCountdown,
} = useGameTimer();

const gameExpiryDateTimeCambodia = computed(() =>
  getCambodiaTime(expiryHourUTC.value, expiryMinuteUTC.value),
);

const isGameExpired = computed(() => {
  const now = new Date();
  const expiryTodayUTC = new Date(
    Date.UTC(
      now.getUTCFullYear(),
      now.getUTCMonth(),
      now.getUTCDate(),
      expiryHourUTC.value,
      expiryMinuteUTC.value,
      0,
    ),
  );
  return now.getTime() >= expiryTodayUTC.getTime();
});

// GAME ID
const gameId = ref(1);
const alreadyPlayedToday = ref(false);

const formattedGameId = computed(
  () => 'Game #' + String(gameId.value).padStart(3, '0'),
);

const getTodayDate = () => {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
};

const initGameId = () => {
  const today = getTodayDate();
  const lastDate = localStorage.getItem('last_played_date');
  const storedGameId = parseInt(localStorage.getItem('game_id') || '0');
  const lastTxn = localStorage.getItem('lastTransaction');
  const sessionStarted = sessionStorage.getItem('session_started');

  if (lastDate === today) {
    gameId.value = storedGameId || 1;

    if (oneGamePerDay.value && lastTxn && !sessionStarted) {
      alreadyPlayedToday.value = true;
    } else {
      alreadyPlayedToday.value = false;
    }
  } else {
    const newId = storedGameId + 1;
    gameId.value = newId;
    localStorage.setItem('game_id', newId);
    localStorage.setItem('last_played_date', today);
    localStorage.removeItem('lastTransaction');
    alreadyPlayedToday.value = false;
  }

  sessionStorage.setItem('session_started', 'true');
};

// GAME LOGIC
let tapCount = 0;
let tapTimer = null;

const handleGameIdTap = () => {
  tapCount++;
  if (tapTimer) clearTimeout(tapTimer);

  if (tapCount >= 2) {
    tapCount = 0;
    hapticFeedback('medium');
    showAdminPanel.value = true;
  } else {
    tapTimer = setTimeout(() => {
      tapCount = 0;
    }, 600);
  }
};

const handleToggleGamePerDay = (value) => {
  oneGamePerDay.value = value;
  hapticFeedback('light');
  initGameId();
};

const selectedNumbers = computed(() => {
  const boxes = ['?', '?'];
  store.selectedNumbers.forEach((num, i) => {
    if (i < 2) boxes[i] = num;
  });
  return boxes;
});

const isShowLines = ref(true);

const canSubmit = computed(() => store.selectedCount === 2);

const canAddLine = computed(
  () =>
    store.selectedCount === 2 &&
    store.editingIndex === null &&
    store.linesCount < store.MAX_LINES - 1,
);

const canSave = computed(
  () => store.selectedCount === 2 && store.editingIndex !== null,
);

const canNext = computed(() => store.selectedCount !== 1);

const handleSaveLine = () => {
  if (!canSubmit.value) return;
  store.saveLine();
  hapticFeedback('light');
};

const handleEditLine = (index) => {
  store.editLine(index);
  hapticFeedback('light');
};

const handleDeleteLine = async (index) => {
  hapticFeedback('light');

  const confirmed = await new Promise((resolve) => {
    try {
      if (window.Telegram?.WebApp?.showPopup) {
        window.Telegram.WebApp.showPopup(
          {
            title: `Delete Line ${index + 1}`,
            message: `Are you sure you want to delete Line ${index + 1}?`,
            buttons: [
              { id: 'no', type: 'cancel' },
              { id: 'yes', type: 'destructive', text: 'Delete' },
            ],
          },
          (buttonId) => resolve(buttonId === 'yes'),
        );
      } else {
        resolve(
          window.confirm(`Are you sure you want to delete Line ${index + 1}?`),
        );
      }
    } catch (error) {
      resolve(
        window.confirm(`Are you sure you want to delete Line ${index + 1}?`),
      );
    }
  });

  if (confirmed) {
    store.deleteLine(index);
    hapticFeedback('medium');
  }
};

const handleResetAll = async () => {
  hapticFeedback('light');

  const confirmed = await new Promise((resolve) => {
    try {
      if (window.Telegram?.WebApp?.showPopup) {
        window.Telegram.WebApp.showPopup(
          {
            title: 'Reset All Lines',
            message: 'Are you sure you want to reset all lines?',
            buttons: [
              { id: 'no', type: 'cancel' },
              { id: 'yes', type: 'destructive', text: 'Yes' },
            ],
          },
          (buttonId) => resolve(buttonId === 'yes'),
        );
      } else {
        resolve(window.confirm('Are you sure you want to reset all lines?'));
      }
    } catch (error) {
      resolve(window.confirm('Are you sure you want to reset all lines?'));
    }
  });

  if (confirmed) {
    store.clearAll();
    hapticFeedback('medium');
  }
};

const handleSubmit = () => {
  if (!canNext.value) return;
  hapticFeedback('medium');

  if (
    store.selectedCount === 2 &&
    store.editingIndex === null &&
    store.linesCount < store.MAX_LINES
  ) {
    store.saveLine();
  }

  router.push('/payment');
};

// Watch expiry time changes
watch([expiryHourUTC, expiryMinuteUTC], () => {
  startExpiryCountdown(expiryHourUTC.value, expiryMinuteUTC.value);
  localStorage.setItem('expiry_hour_utc', expiryHourUTC.value.toString());
  localStorage.setItem('expiry_minute_utc', expiryMinuteUTC.value.toString());
});

// LIFECYCLE
onMounted(() => {
  sessionStorage.removeItem('session_started');
  initGameId();
  startExpiryCountdown(expiryHourUTC.value, expiryMinuteUTC.value);
});

onUnmounted(() => {
  stopExpiryCountdown();
});
</script>



