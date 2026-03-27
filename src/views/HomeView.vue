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
          <span class="text-[10px] text-[var(--tg-theme-hint-color)]">
            {{ formattedGameId }} | 4:00 PM
          </span>
        </div>
      </div>

      <!-- Right: Title -->
      <div class="text-right">
        <h1 class="text-sm font-bold text-gray-600 italic">
          Select your numbers
        </h1>
      </div>
    </header>

    <!-- ALREADY PLAYED TODAY -->
    <div
      v-if="alreadyPlayedToday"
      class="flex-1 flex flex-col items-center justify-center px-6 text-center"
    >
      <div class="text-5xl mb-4">🎮</div>
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
      <!-- Grid -->
      <NumberGrid />

      <hr class="w-full max-w-md my-2" />

      <!-- GAMES LIST -->
      <div
        v-if="store.games.length > 0 || store.selectedCount > 0"
        v-show="isShowGames"
        class="w-full max-w-md flex-none mb-2 max-h-[108px] overflow-y-auto"
      >
        <!-- Saved -->
        <div
          v-for="(game, index) in store.games"
          :key="index"
          class="flex items-center justify-between px-3 py-1 mb-1 rounded-md cursor-pointer active:scale-95 transition-all duration-150"
          :class="
            store.editingIndex === index
              ? 'bg-[var(--tg-theme-button-color)]'
              : 'bg-[var(--tg-theme-secondary-bg-color)]'
          "
          @click="handleEditGame(index)"
        >
          <span
            class="text-sm"
            :class="
              store.editingIndex === index
                ? 'text-[var(--tg-theme-button-text-color)]'
                : 'text-[var(--tg-theme-hint-color)]'
            "
          >
            Game {{ index + 1 }}
          </span>

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
            <template v-else> {{ game[0] }} , {{ game[1] }} </template>
          </span>
        </div>

        <!-- Current row -->
        <div
          v-if="store.editingIndex === null && store.gamesCount < store.MAX_GAMES"
          class="flex items-center justify-between px-3 py-1 mb-1 rounded-md bg-[var(--tg-theme-secondary-bg-color)]"
        >
          <span class="text-sm text-[var(--tg-theme-hint-color)]">
            Game {{ store.gamesCount + 1 }}
          </span>
          <span class="text-sm font-bold text-[var(--tg-theme-text-color)]">
            {{ selectedNumbers[0] !== "?" ? selectedNumbers[0] : "..." }} ,
            {{ selectedNumbers[1] !== "?" ? selectedNumbers[1] : "..." }}
          </span>
        </div>
      </div>

      <!-- SELECTION BOXES - hide when max games reached -->
      <div
        v-if="store.gamesCount < store.MAX_GAMES"
        class="flex gap-2 w-full max-w-md flex-none"
      >
        <!-- Box 1 -->
        <div
          class="flex-1 h-12 rounded-md flex items-center justify-center text-3xl font-bold relative"
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

        <!-- Box 2 -->
        <div
          class="flex-1 h-12 rounded-md flex items-center justify-center text-3xl font-bold relative"
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

      <!-- TOGGLE + RESET -->
      <div class="flex items-center justify-between w-full max-w-md mt-1">
        <p
          @click="isShowGames = !isShowGames"
          class="text-sm text-[var(--tg-theme-hint-color)] underline cursor-pointer"
        >
          {{ isShowGames ? "Hide" : "Show" }} game list (
          {{
            store.gamesCount +
            (store.editingIndex === null && store.gamesCount < store.MAX_GAMES
              ? 1
              : 0)
          }}/{{ store.MAX_GAMES }})
        </p>

        <!-- RESET BUTTON -->
        <button
          v-if="store.games.length > 0 || store.selectedCount > 0"
          class="text-xs text-red-400 underline cursor-pointer active:scale-95 transition-all"
          @click="handleReset"
        >
          Reset all lines
        </button>
      </div>

      <!-- ACTION BUTTONS -->
      <div class="w-full max-w-md flex-none mt-1 mb-1">
        <!-- Not ready -->
        <NextButton
          v-if="!canSubmit && store.gamesCount < store.MAX_GAMES"
          :disabled="true"
          text="Select 2 numbers"
        />

        <!-- MAX reached → FULL NEXT -->
        <NextButton
          v-else-if="store.gamesCount === store.MAX_GAMES && store.editingIndex === null"
          text="Next"
          variant="primary"
          class="w-full"
          @click="handleSubmit"
        />

        <!-- Normal -->
        <div v-else class="flex gap-2">
          <NextButton
            v-if="canSave"
            text="Save"
            variant="secondary"
            class="flex-1"
            @click="handleSaveGame"
          />

          <NextButton
            v-if="canAddGame"
            text="Add Line"
            variant="secondary"
            class="flex-1"
            @click="handleSaveGame"
          />

          <NextButton
            text="Next"
            variant="primary"
            class="flex-1"
            @click="handleSubmit"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import NumberGrid from "@/components/grid/NumberGrid.vue"
import NextButton from "@/components/ui/NextButton.vue"
import { useGridStore } from "../stores/gridStore"
import { useTelegram } from "../composables/useTelegram"

const store = useGridStore()
const router = useRouter()
const { hapticFeedback } = useTelegram()

// ── Game ID & 1-per-day logic ──────────────────────────────
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

  if (lastDate === today) {
    gameId.value = storedGameId || 1
    const lastTxn = sessionStorage.getItem("lastTransaction")
    if (lastTxn) {
      alreadyPlayedToday.value = true
    }
  } else {
    const newId = storedGameId + 1
    gameId.value = newId
    localStorage.setItem("game_id", newId)
    localStorage.setItem("last_played_date", today)
    alreadyPlayedToday.value = false
  }
}

onMounted(() => {
  initGameId()
})

// Selected Numbers
const selectedNumbers = computed(() => {
  const boxes = ["?", "?"]
  store.selectedNumbers.forEach((num, i) => {
    if (i < 2) boxes[i] = num
  })
  return boxes
})

const isShowGames = ref(false)
const canSubmit = computed(() => store.selectedCount === 2)

const canAddGame = computed(
  () =>
    store.selectedCount === 2 &&
    store.editingIndex === null &&
    store.gamesCount < store.MAX_GAMES - 1
)

const canSave = computed(
  () => store.selectedCount === 2 && store.editingIndex !== null
)

const handleSaveGame = () => {
  store.saveGame()
  hapticFeedback("light")
}

const handleEditGame = (index) => {
  store.editGame(index)
  hapticFeedback("light")
}

const handleReset = async () => {
  hapticFeedback("light")

  const confirmed = await new Promise((resolve) => {
    try {
      if (window.Telegram?.WebApp?.showPopup) {
        window.Telegram.WebApp.showPopup(
          {
            title: "Reset Lines",
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
      console.warn("showPopup failed:", error)
      resolve(window.confirm("Are you sure you want to reset all lines?"))
    }
  })

  if (confirmed) {
    store.clearAll()
    hapticFeedback("medium")
  }
}

const handleSubmit = () => {
  if (!canSubmit.value && store.gamesCount < store.MAX_GAMES) return
  hapticFeedback("medium")

  if (
    store.selectedCount === 2 &&
    store.editingIndex === null &&
    store.gamesCount < store.MAX_GAMES
  ) {
    store.saveGame()
  }

  router.push("/payment")
}
</script>