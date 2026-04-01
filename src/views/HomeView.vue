<template>
  <div class="h-screen flex flex-col bg-[var(--tg-theme-bg-color)]">

    <!-- Exit Confirm -->
    <div
      v-if="showExitConfirm"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-6"
    >
      <div class="bg-white rounded-2xl p-6 w-full max-w-xs text-center shadow-xl">
        <div class="text-5xl mb-3">⚠️</div>
        <h2 class="text-base font-bold text-gray-800 mb-1">Leave App</h2>
        <p class="text-sm text-gray-500 mb-5">Are you sure you want to leave this Mini App?</p>
        <div class="flex gap-3">
          <button
            class="flex-1 py-2 rounded-lg text-sm font-semibold bg-gray-100 text-gray-600 active:scale-95 transition-all"
            @click="showExitConfirm = false"
          >
            No
          </button>
          <button
            class="flex-1 py-2 rounded-lg text-sm font-semibold bg-red-500 text-white active:scale-95 transition-all"
            @click="handleLeave"
          >
            Yes, Leave
          </button>
        </div>
      </div>
    </div>

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

      <!-- Right: Reset + Close Buttons -->
      <div class="flex items-center gap-2">
        <button
          v-if="store.lines.length > 0 || store.selectedCount > 0"
          class="text-xs text-red-400 px-3 py-1 rounded-md hover:bg-red-500 hover:text-white border cursor-pointer active:scale-95 transition-all duration-300 ease-in-out"
          @click="handleReset"
        >
          {{
            store.editingIndex !== null
              ? `Reset Line ${store.editingIndex + 1}`
              : "Reset all lines"
          }}
        </button>

        <!-- Close Button -->
        <button
          class="text-xs text-gray-400 px-3 py-1 rounded-md border cursor-pointer active:scale-95 hover:bg-gray-200 transition-all duration-300 ease-in-out"
          @click="showExitConfirm = true"
        >
          Close
        </button>
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

      <!-- LINES LIST - only show saved lines -->
      <div
        v-if="store.lines.length > 0"
        v-show="isShowLines"
        class="w-full max-w-md flex-none mb-2 max-h-[108px] overflow-y-auto"
      >
        <!-- Saved Lines -->
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
        </div>
      </div>

      <!-- SELECTION BOXES -->
      <div
        v-if="store.linesCount < store.MAX_LINES || store.editingIndex !== null"
        class="flex gap-2 w-full max-w-md flex-none"
      >
        <!-- Box 1 -->
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

        <!-- Box 2 -->
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
        <!-- MAX reached → FULL NEXT -->
        <NextButton
          v-if="store.linesCount === store.MAX_LINES && store.editingIndex === null"
          text="Next"
          variant="primary"
          class="w-full"
          @click="handleSubmit"
        />

        <!-- Normal -->
        <div v-else class="flex gap-2">
          <NextButton
            v-if="canSave"
            text="Add Line"
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
            text="Next"
            variant="primary"
            class="flex-1"
            :disabled="!canSubmit && store.linesCount === 0"
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
const { hapticFeedback, closeMiniApp } = useTelegram()

// Exit Confirm
const showExitConfirm = ref(false)

const handleLeave = () => {
  hapticFeedback('light')
  closeMiniApp()
}

// Game ID & 1-per-day logic
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

const isShowLines = ref(false)
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

const handleSaveLine = () => {
  if (!canSubmit.value) return
  store.saveLine()
  hapticFeedback("light")
}

const handleEditLine = (index) => {
  store.editLine(index)
  hapticFeedback("light")
}

const handleReset = async () => {
  hapticFeedback("light")

  const isEditingLine = store.editingIndex !== null
  const lineNumber = store.editingIndex + 1
  const title = isEditingLine ? `Reset Line ${lineNumber}` : "Reset Lines"
  const message = isEditingLine
    ? `Are you sure you want to reset Line ${lineNumber}?`
    : "Are you sure you want to reset all lines?"

  const confirmed = await new Promise((resolve) => {
    try {
      if (window.Telegram?.WebApp?.showPopup) {
        window.Telegram.WebApp.showPopup(
          {
            title,
            message,
            buttons: [
              { id: "no", type: "cancel" },
              { id: "yes", type: "destructive", text: "Yes" },
            ],
          },
          (buttonId) => resolve(buttonId === "yes")
        )
      } else {
        resolve(window.confirm(message))
      }
    } catch (error) {
      console.warn("showPopup failed:", error)
      resolve(window.confirm(message))
    }
  })

  if (confirmed) {
    if (isEditingLine) {
      store.deleteLine(store.editingIndex)
    } else {
      store.clearAll()
    }
    hapticFeedback("medium")
  }
}

const handleSubmit = () => {
  if (!canSubmit.value && store.linesCount === 0) return
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
</script>