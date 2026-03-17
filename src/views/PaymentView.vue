<template>
  <div class="h-screen flex flex-col bg-[var(--tg-theme-bg-color)]">
    <!-- Header -->
    <header class="text-center px-4 pt-4 flex-none">
      <h1 class="text-md font-bold text-gray-600 italic">Payment</h1>
      <p class="text-xs text-[var(--tg-theme-hint-color)] mt-1">
        Select your bank and complete payment
      </p>
    </header>

    <div class="flex-1 flex flex-col items-center p-4 min-h-0 w-full overflow-y-auto">

      <!-- Order Summary -->
      <div class="w-full max-w-md bg-[var(--tg-theme-secondary-bg-color)] rounded-xl p-4 mb-4 flex-none">
        <h2 class="text-sm font-semibold text-[var(--tg-theme-hint-color)] mb-2">
          Order Summary
        </h2>
        <div
          v-for="(game, index) in allGames"
          :key="index"
          class="flex justify-between items-center py-1"
        >
          <span class="text-sm text-[var(--tg-theme-hint-color)]">Game {{ index + 1 }}</span>
          <span class="text-sm font-bold text-[var(--tg-theme-text-color)]">
            {{ game[0] }} , {{ game[1] }}
          </span>
        </div>
        <hr class="my-2 border-[var(--tg-theme-hint-color)] opacity-20" />
        <div class="flex justify-between items-center">
          <span class="text-sm font-semibold text-[var(--tg-theme-hint-color)]">Total</span>
          <span class="text-lg font-bold text-[var(--tg-theme-text-color)]">
            ${{ totalAmount.toFixed(2) }}
          </span>
        </div>
      </div>

      <!-- Bank Selection -->
      <div class="w-full max-w-md flex-none">
        <h2 class="text-sm font-semibold text-[var(--tg-theme-hint-color)] mb-2">
          Select Bank
        </h2>
        <div class="grid grid-cols-2 gap-3">
          <button
            v-for="bank in banks"
            :key="bank.name"
            class="flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-all duration-150 active:scale-95 focus:outline-none"
            :class="
              selectedBank === bank.name
                ? 'border-[var(--tg-theme-button-color)]'
                : 'border-[var(--tg-theme-secondary-bg-color)] bg-[var(--tg-theme-secondary-bg-color)]'
            "
            @click="selectedBank = bank.name"
          >
            <!-- Bank Logo -->
            <img
              :src="bank.logo"
              :alt="bank.name"
              class="w-9 h-9 rounded-lg object-contain flex-shrink-0"
            />

            <span
              class="text-sm font-semibold"
              :class="
                selectedBank === bank.name
                  ? 'text-[var(--tg-theme-button-color)]'
                  : 'text-[var(--tg-theme-text-color)]'
              "
            >
              {{ bank.name }}
            </span>

            <!-- Checkmark -->
            <span
              v-if="selectedBank === bank.name"
              class="ml-auto text-[var(--tg-theme-button-color)] text-lg"
            >✓</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Pay Now Button -->
    <div class="w-full max-w-md mx-auto px-4 pb-4 flex-none">
      <button
        class="w-full py-3 px-6 rounded-xl text-lg font-semibold transition-all active:scale-95 focus:outline-none disabled:opacity-30 disabled:cursor-not-allowed"
        :class="
          selectedBank
            ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]'
            : 'bg-gray-300 text-gray-500'
        "
        :disabled="!selectedBank"
        @click="handlePayNow"
      >
        Pay Now
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { useGridStore } from "../stores/gridStore"
import { useTelegram } from "../composables/useTelegram"

const router = useRouter()
const store = useGridStore()
const { hapticFeedback, sendData, showPopup } = useTelegram()

const selectedBank = ref("")
const PRICE_PER_GAME = 1.0

const banks = [
  { name: "ABA",      logo: "/banks/aba.png" },
  { name: "ACLEDA",   logo: "/banks/acleda.png" },
  { name: "JTrust",   logo: "/banks/jtrust.png" },
  { name: "Wingbank", logo: "/banks/wing.png" },
]

const allGames = computed(() => {
  if (store.editingIndex !== null) {
    return store.games.map((g, i) =>
      i === store.editingIndex ? [...store.selectedNumbers] : g
    )
  }
  return [...store.games, [...store.selectedNumbers]]
})

const totalAmount = computed(() => allGames.value.length * PRICE_PER_GAME)

const handlePayNow = async () => {
  if (!selectedBank.value) return
  hapticFeedback("medium")

  const payload = {
    // ─── User data from Telegram ───
    telegram_id: store.userData?.telegram_id || null,
    full_name: store.userData?.full_name || null,
    username: store.userData?.username || null,
    phone_number: store.userData?.phone_number || null,
    // ─── Game data ────────────────
    games: allGames.value,
    bank_name: selectedBank.value,
    amount: totalAmount.value,
    start_param: store.startParam || null,
    submitted_at: new Date().toISOString(),
  }

  const sent = sendData(payload)
  if (sent) {
    await showPopup("Payment submitted successfully!", "Success")
    store.clearAll()
    router.push("/")
  } else {
    await showPopup("Could not send payment. Please try again.", "Error")
  }
}
</script>