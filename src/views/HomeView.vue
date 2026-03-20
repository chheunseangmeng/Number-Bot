<template>
  <div class="h-screen flex flex-col bg-[var(--tg-theme-bg-color)]">
    <!-- HEADER -->
    <header class="text-center flex-none pt-2">
      <h1 class="text-md font-bold text-gray-600 italic">
        Select your numbers
      </h1>
      <div
        v-if="store.startParam"
        class="mt-1 text-xs text-[var(--tg-theme-hint-color)]"
      >
        Referral: {{ store.startParam }}
      </div>
    </header>

    <!-- MAIN -->
    <div class="flex-1 flex flex-col items-center p-2 min-h-0 w-full">
      <!-- Grid -->
      <NumberGrid />

      <hr class="w-full max-w-md my-2" />

      <!-- GAMES LIST -->
      <div
        v-if="store.games.length > 0 || store.selectedCount > 0"
        v-show="isShowGames"
        class="w-full max-w-md flex-none mb-2"
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
            <template v-else>
              {{ game[0] }} , {{ game[1] }}
            </template>
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

      <!-- SELECTION BOXES -->
      <div class="flex gap-2 w-full max-w-md flex-none">
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

      <!-- TOGGLE -->
      <p
        @click="isShowGames = !isShowGames"
        class="text-center text-sm text-[var(--tg-theme-hint-color)] mt-1 underline cursor-pointer"
      >
        {{ isShowGames ? "Hide" : "Show" }} game list (
        {{
          store.gamesCount +
          (store.editingIndex === null && store.gamesCount < store.MAX_GAMES ? 1 : 0)
        }}/{{ store.MAX_GAMES }})
      </p>

      <!-- ACTION BUTTONS -->
      <div class="w-full max-w-md flex-none mt-1 mb-1">
        <!-- Not ready -->
        <NextButton
          v-if="!canSubmit"
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
            text="Add Game"
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
import { computed, ref } from "vue"
import { useRouter } from "vue-router"
import NumberGrid from "@/components/grid/NumberGrid.vue"
import NextButton from "@/components/ui/NextButton.vue"
import { useGridStore } from "../stores/gridStore"
import { useTelegram } from "../composables/useTelegram"

const store = useGridStore()
const router = useRouter()
const { hapticFeedback } = useTelegram()

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

const handleSubmit = () => {
  if (!canSubmit.value) return
  hapticFeedback("medium")

   if (store.selectedCount === 2 && store.editingIndex === null && store.gamesCount < store.MAX_GAMES) {
    store.saveGame()
  }


  router.push("/payment")
}
</script>