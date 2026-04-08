<template>
  <div class="h-screen flex flex-col bg-[var(--tg-theme-bg-color)]">
    <!-- HEADER -->
    <header class="flex items-center justify-between px-2 py-2 flex-none">
      <!-- Left: Profile -->
      <div class="flex items-center gap-2">
        <img
          v-if="store.userData?.photo_url"
          :src="store.userData.photo_url"
          class="w-10 h-10 rounded-full object-cover"
        />
        <div class="flex flex-col">
          <span class="text-sm font-semibold text-[var(--tg-theme-text-color)]">
            {{ store.userData?.full_name }}
          </span>
          <span
            class="text-[10px] text-[var(--tg-theme-hint-color)] cursor-pointer select-none"
            @click="handleGameIdTap"
          >
            {{ formattedGameId }} | {{ gameExpiryDateTimeCambodia }}
          </span>
        </div>
      </div>

      <!-- Right: Reset All Button + Countdown -->
      <div class="text-right">
        <div class="text-right">
          <div v-if="timeToExpiry !== null" class="text-xs text-[var(--tg-theme-hint-color)] mb-1">
            <span class="font-mono">{{ formattedTimeToExpiryCambodia }}</span>
          </div>
          <div v-else class="text-xs text-red-400 mb-1">⏰ Game Expired</div>
        </div>
        <button
          v-if="store.lines.length > 0 || store.selectedCount > 0"
          class="text-xs text-red-400 px-3 py-1 rounded-md hover:bg-red-500 hover:text-white border cursor-pointer active:scale-95 transition-all duration-300 ease-in-out"
          @click="handleResetAll"
        >
          Reset all lines
        </button>
      </div>
    </header>

    <!-- ADMIN PANEL -->
    <div
      v-if="showAdminPanel"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-6"
      @click.self="showAdminPanel = false"
    >
      <div class="bg-white rounded-2xl p-6 w-full max-w-xs text-center shadow-xl">
        <div class="text-3xl mb-2">⚙️</div>
        <h2 class="text-sm font-bold text-gray-800 mb-1">Admin Config</h2>
        <p class="text-xs text-gray-400 mb-5">Game settings</p>

        <!-- One game per day toggle -->
        <div class="flex items-center justify-between px-2 py-3 bg-gray-50 rounded-xl mb-4">
          <span class="text-sm font-semibold text-gray-700">One game per day</span>
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
            Current: {{ expiryHourUTC }}:00 UTC ({{ expiryHourUTC + 7 }}:00 Cambodia)
          </p>
        </div>

        <button
          class="w-full py-2 rounded-lg text-sm font-semibold bg-gray-100 text-gray-600 active:scale-95 transition-all"
          @click="showAdminPanel = false"
        >
          Close
        </button>
      </div>
    </div>

    <!-- ALREADY PLAYED TODAY -->
    <div
      v-if="alreadyPlayedToday"
      class="flex-1 flex flex-col items-center justify-center px-6 text-center"
    >
      <div class="text-5xl mb-4">🚫</div>
      <h2 class="text-lg font-bold text-[var(--tg-theme-text-color)] mb-2">
        Come back tomorrow!
      </h2>
      <p class="text-sm text-[var(--tg-theme-hint-color)]">
        You have already played today ({{ formattedGameId }}). A new game will
        be available tomorrow.
      </p>
    </div>

    <!-- MAIN -->
    <div v-else class="flex-1 flex flex-col items-center p-2 min-h-0 w-full">
      <NumberGrid />

      <hr class="w-full max-w-md my-2" />

      <!-- LINES LIST - default visible -->
      <div
        v-if="store.lines.length > 0"
        v-show="isShowLines"
        class="w-full max-w-md flex-none mb-2 max-h-[108px] overflow-y-auto"
      >
        <div
          v-for="(line, index) in store.lines"
          :key="index"
          class="flex items-center justify-between px-3 py-1 mb-1 rounded-md cursor-pointer active:scale-95 transition-all duration-150"
          :class="
            store.editingIndex === index
              ? 'bg-[var(--tg-theme-button-color)]'
              : 'bg-[var(--tg-theme-secondary-bg-color)]'
          "
          @click="handleEditLine(index)"
        >
          <span
            class="text-sm"
            :class="
              store.editingIndex === index
                ? 'text-[var(--tg-theme-button-text-color)]'
                : 'text-[var(--tg-theme-hint-color)]'
            "
          >
            Line {{ index + 1 }}
          </span>

          <div class="flex items-center gap-2">
            <span
              class="text-sm font-bold"
              :class="
                store.editingIndex === index
                  ? 'text-[var(--tg-theme-button-text-color)]'
                  : 'text-[var(--tg-theme-text-color)]'
              "
            >
              <template v-if="store.editingIndex === index">
                {{ selectedNumbers[0] !== "?" ? selectedNumbers[0] : "..." }} ,
                {{ selectedNumbers[1] !== "?" ? selectedNumbers[1] : "..." }}
              </template>
              <template v-else> {{ line[0] }} , {{ line[1] }} </template>
            </span>

            <button
              class="text-sm cursor-pointer hover:scale-110 transition-transform"
              :class="
                store.editingIndex === index
                  ? 'text-[var(--tg-theme-button-text-color)]'
                  : 'text-red-400'
              "
              @click.stop="handleDeleteLine(index)"
            >
              ❌
            </button>
          </div>
        </div>
      </div>

      <!-- SELECTION BOXES -->
      <div
        v-if="store.linesCount < store.MAX_LINES || store.editingIndex !== null"
        class="flex gap-2 w-full max-w-md flex-none"
      >
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
            @click="store.deselectNumber(store.selectedNumbers[0])"
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
            @click="store.deselectNumber(store.selectedNumbers[1])"
          >
            ❌
          </span>
        </div>
      </div>

      <!-- Toggle show lines -->
      <div
        v-if="store.lines.length > 0"
        class="flex items-center justify-center w-full max-w-md mt-1"
      >
        <p
          @click="isShowLines = !isShowLines"
          class="text-sm text-[var(--tg-theme-hint-color)] underline cursor-pointer"
        >
          {{ isShowLines ? "Hide" : "Show" }} line list (
          {{ store.linesCount }}/{{ store.MAX_LINES }})
        </p>
      </div>

      <!-- ACTION BUTTONS -->
      <div class="w-full max-w-md flex-none mt-1 mb-1">
        <!-- MAX reached → Pay Now -->
        <NextButton
          v-if="store.linesCount === store.MAX_LINES && store.editingIndex === null"
          text="Pay Now"
          variant="primary"
          class="w-full"
          @click="handleSubmit"
        />

        <!-- Normal -->
        <div v-else class="flex gap-2">
          <NextButton
            v-if="canSave"
            text="Save Line"
            variant="secondary"
            class="flex-1"
            :disabled="!canSubmit"
            @click="handleSaveLine"
          />

          <NextButton
            v-if="canAddLine"
            text="Add Line"
            variant="secondary"
            class="flex-1"
            :disabled="!canSubmit"
            @click="handleSaveLine"
          />

          <NextButton
            text="Pay Now"
            variant="primary"
            class="flex-1"
            :disabled="!canNext"
            @click="handleSubmit"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from "vue"
import { useRouter } from "vue-router"
import NumberGrid from "@/components/grid/NumberGrid.vue"
import NextButton from "@/components/ui/NextButton.vue"
import { useGridStore } from "../stores/gridStore"
import { useTelegram } from "../composables/useTelegram"

const store = useGridStore()
const router = useRouter()
const { hapticFeedback } = useTelegram()

// ADMIN PANEL 
const showAdminPanel = ref(false)
const oneGamePerDay = ref(localStorage.getItem("one_game_per_day") !== "false")

// Expiry hour in UTC (default 19 = 7PM UTC)
const expiryHourUTC = ref(parseInt(localStorage.getItem("expiry_hour_utc") || "19"))

let tapCount = 0
let tapTimer = null

const handleGameIdTap = () => {
  tapCount++
  if (tapTimer) clearTimeout(tapTimer)

  if (tapCount >= 2) {
    tapCount = 0
    hapticFeedback("medium")
    showAdminPanel.value = true
  } else {
    tapTimer = setTimeout(() => {
      tapCount = 0
    }, 600)
  }
}

const toggleOneGamePerDay = () => {
  oneGamePerDay.value = !oneGamePerDay.value
  localStorage.setItem("one_game_per_day", oneGamePerDay.value ? "true" : "false")
  hapticFeedback("light")
  initGameId()
}

const saveExpiryTime = () => {
  let hour = expiryHourUTC.value
  if (isNaN(hour)) hour = 19
  if (hour < 0) hour = 0
  if (hour > 23) hour = 23
  
  expiryHourUTC.value = hour
  localStorage.setItem("expiry_hour_utc", hour.toString())
  hapticFeedback("light")
  
  // Restart countdown with new expiry time
  startExpiryCountdown()
}

// GAME ID 
const gameId = ref(1)
const alreadyPlayedToday = ref(false)

const formattedGameId = computed(
  () => "Game #" + String(gameId.value).padStart(3, "0")
)

const getTodayDate = () => {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`
}

const initGameId = () => {
  const today = getTodayDate()
  const lastDate = localStorage.getItem("last_played_date")
  const storedGameId = parseInt(localStorage.getItem("game_id") || "0")
  const lastTxn = localStorage.getItem("lastTransaction")
  const sessionStarted = sessionStorage.getItem("session_started")

  if (lastDate === today) {
    gameId.value = storedGameId || 1

    if (oneGamePerDay.value && lastTxn && !sessionStarted) {
      alreadyPlayedToday.value = true
    } else {
      alreadyPlayedToday.value = false
    }
  } else {
    const newId = storedGameId + 1
    gameId.value = newId
    localStorage.setItem("game_id", newId)
    localStorage.setItem("last_played_date", today)
    localStorage.removeItem("lastTransaction")
    alreadyPlayedToday.value = false
  }

  sessionStorage.setItem("session_started", "true")
}

// COUNTDOWN TO CUSTOM EXPIRY TIME UTC 
const timeToExpiry = ref(null)
let expiryCountdownInterval = null

// Get today's expiry time based on admin configured hour (UTC)
const getExpiryTimeUTC = () => {
  const now = new Date()
  const expiryTime = new Date(
    Date.UTC(
      now.getUTCFullYear(),
      now.getUTCMonth(),
      now.getUTCDate(),
      expiryHourUTC.value,  // Admin configurable hour
      0,
      0
    )
  )

  if (now.getTime() >= expiryTime.getTime()) {
    expiryTime.setUTCDate(expiryTime.getUTCDate() + 1)
  }

  return expiryTime
}

// Convert UTC to Cambodia time (UTC+7) for display
const gameExpiryDateTimeCambodia = computed(() => {
  const expiryUTC = getExpiryTimeUTC()
  const expiryCambodia = new Date(expiryUTC.getTime() + 7 * 60 * 60 * 1000)
  
  const year = expiryCambodia.getUTCFullYear()
  const month = String(expiryCambodia.getUTCMonth() + 1).padStart(2, '0')
  const day = String(expiryCambodia.getUTCDate()).padStart(2, '0')
  const hours = String(expiryCambodia.getUTCHours()).padStart(2, '0')
  const minutes = String(expiryCambodia.getUTCMinutes()).padStart(2, '0')
  
  return `${year}-${month}-${day} ${hours}:${minutes}`
})

const updateTimeToExpiry = () => {
  const now = new Date()
  const expiryTime = getExpiryTimeUTC()
  const diffMs = expiryTime.getTime() - now.getTime()

  if (diffMs <= 0) {
    timeToExpiry.value = null

    if (expiryCountdownInterval) {
      clearInterval(expiryCountdownInterval)
      expiryCountdownInterval = null
    }

    return
  }

  const totalSeconds = Math.floor(diffMs / 1000)
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const seconds = totalSeconds % 60

  timeToExpiry.value = { hours, minutes, seconds }
}

const formattedTimeToExpiryCambodia = computed(() => {
  if (!timeToExpiry.value) return ""
  const { hours, minutes, seconds } = timeToExpiry.value
  return `${hours}h ${minutes}m ${seconds}s`
})

const startExpiryCountdown = () => {
  if (expiryCountdownInterval) {
    clearInterval(expiryCountdownInterval)
  }

  updateTimeToExpiry()

  expiryCountdownInterval = setInterval(() => {
    updateTimeToExpiry()
  }, 1000)
}

// Watch for expiry hour changes
watch(expiryHourUTC, () => {
  startExpiryCountdown()
})
// END COUNTDOWN 

// GAME LOGIC 
const selectedNumbers = computed(() => {
  const boxes = ["?", "?"]
  store.selectedNumbers.forEach((num, i) => {
    if (i < 2) boxes[i] = num
  })
  return boxes
})

const isShowLines = ref(true)

const canSubmit = computed(() => store.selectedCount === 2)

const canAddLine = computed(
  () =>
    store.selectedCount === 2 &&
    store.editingIndex === null &&
    store.linesCount < store.MAX_LINES - 1
)

const canSave = computed(
  () => store.selectedCount === 2 && store.editingIndex !== null
)

const canNext = computed(() => store.selectedCount !== 1)

const handleSaveLine = () => {
  if (!canSubmit.value) return
  store.saveLine()
  hapticFeedback("light")
}

const handleEditLine = (index) => {
  store.editLine(index)
  hapticFeedback("light")
}

const handleDeleteLine = async (index) => {
  hapticFeedback("light")

  const confirmed = await new Promise((resolve) => {
    try {
      if (window.Telegram?.WebApp?.showPopup) {
        window.Telegram.WebApp.showPopup(
          {
            title: `Delete Line ${index + 1}`,
            message: `Are you sure you want to delete Line ${index + 1}?`,
            buttons: [
              { id: "no", type: "cancel" },
              { id: "yes", type: "destructive", text: "Delete" },
            ],
          },
          (buttonId) => resolve(buttonId === "yes")
        )
      } else {
        resolve(window.confirm(`Are you sure you want to delete Line ${index + 1}?`))
      }
    } catch (error) {
      resolve(window.confirm(`Are you sure you want to delete Line ${index + 1}?`))
    }
  })

  if (confirmed) {
    store.deleteLine(index)
    hapticFeedback("medium")
  }
}

const handleResetAll = async () => {
  hapticFeedback("light")

  const confirmed = await new Promise((resolve) => {
    try {
      if (window.Telegram?.WebApp?.showPopup) {
        window.Telegram.WebApp.showPopup(
          {
            title: "Reset All Lines",
            message: "Are you sure you want to reset all lines?",
            buttons: [
              { id: "no", type: "cancel" },
              { id: "yes", type: "destructive", text: "Yes" },
            ],
          },
          (buttonId) => resolve(buttonId === "yes")
        )
      } else {
        resolve(window.confirm("Are you sure you want to reset all lines?"))
      }
    } catch (error) {
      resolve(window.confirm("Are you sure you want to reset all lines?"))
    }
  })

  if (confirmed) {
    store.clearAll()
    hapticFeedback("medium")
  }
}

const handleSubmit = () => {
  if (!canNext.value) return
  hapticFeedback("medium")

  if (
    store.selectedCount === 2 &&
    store.editingIndex === null &&
    store.linesCount < store.MAX_LINES
  ) {
    store.saveLine()
  }

  router.push("/payment")
}

// LIFECYCLE 
onMounted(() => {
  sessionStorage.removeItem("session_started")
  initGameId()
  startExpiryCountdown()
})

onUnmounted(() => {
  if (expiryCountdownInterval) {
    clearInterval(expiryCountdownInterval)
    expiryCountdownInterval = null
  }
})
</script>