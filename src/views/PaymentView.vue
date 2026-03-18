<template>
  <div class="h-screen flex flex-col bg-[var(--tg-theme-bg-color)] overflow-hidden">
    <!-- Header -->
    <header class="text-center pt-3 pb-1 flex-none">
      <h1 class="text-md font-bold text-gray-600 italic">Payment</h1>
      <p class="text-xs text-[var(--tg-theme-hint-color)]">
        Select your bank
      </p>
    </header>

    <div class="flex-1 flex flex-col items-center px-3 overflow-y-auto">
      <!-- Order Summary -->
      <div class="w-full max-w-xs bg-[var(--tg-theme-secondary-bg-color)] rounded-xl p-3 mb-3 flex-none">
        <h2 class="text-xs font-semibold text-[var(--tg-theme-hint-color)] mb-1">
          Order Summary
        </h2>

        <div
          v-for="(game, index) in allGames"
          :key="index"
          class="flex justify-between items-center py-1"
        >
          <span class="text-xs text-[var(--tg-theme-hint-color)]">Game {{ index + 1 }}</span>
          <span class="text-xs font-bold text-[var(--tg-theme-text-color)]">
            {{ game[0] }} , {{ game[1] }}
          </span>
        </div>

        <hr class="my-1 border-[var(--tg-theme-hint-color)] opacity-20" />
        <div class="flex justify-between items-center">
          <span class="text-xs font-semibold text-[var(--tg-theme-hint-color)]">Total</span>
          <span class="text-base font-bold text-[var(--tg-theme-text-color)]">
            ${{ totalAmount.toFixed(2) }}
          </span>
        </div>
      </div>

      <!-- Bank Selection -->
      <div class="w-full max-w-xs flex-none">
        <h2 class="text-xs font-semibold text-[var(--tg-theme-hint-color)] mb-2">
          Select Bank
        </h2>
        <div class="grid grid-cols-2 gap-2">
          <button
            v-for="bank in banks"
            :key="bank.name"
            class="flex items-center gap-2 px-2 py-2 rounded-lg border-2 transition-all duration-150 active:scale-95 focus:outline-none"
            :class="
              selectedBank === bank.name
                ? 'border-[var(--tg-theme-button-color)]'
                : 'border-[var(--tg-theme-secondary-bg-color)] bg-[var(--tg-theme-secondary-bg-color)]'
            "
            @click="selectedBank = bank.name"
          >
            <img
              :src="bank.logo"
              :alt="bank.name"
              class="w-7 h-7 rounded-md object-contain flex-shrink-0"
            />
            <span
              class="text-xs font-semibold"
              :class="
                selectedBank === bank.name
                  ? 'text-[var(--tg-theme-button-color)]'
                  : 'text-[var(--tg-theme-text-color)]'
              "
            >
              {{ bank.name }}
            </span>
            <span
              v-if="selectedBank === bank.name"
              class="ml-auto text-[var(--tg-theme-button-color)] text-sm"
            >✓</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Pay Now Button -->
    <div class="w-full max-w-xs mx-auto px-3 pb-3 pt-3 flex-none mb-10">
      <button
        class="w-full py-4 px-4 rounded-lg text-sm font-semibold transition-all active:scale-95 focus:outline-none disabled:opacity-30 disabled:cursor-not-allowed"
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
  { name: "ABA",    logo: "/banks/aba.png" },
  { name: "ACLEDA", logo: "/banks/acleda.png" },
  { name: "JTrust", logo: "/banks/jtrust.png" },
  { name: "Wing",   logo: "/banks/wing.png" },
]

const allGames = computed(() => {
  if (store.editingIndex !== null) {
    return store.games.map((g, i) =>
      i === store.editingIndex ? [...store.selectedNumbers] : g
    )
  }
  if (store.selectedCount === 2) {
    return [...store.games, [...store.selectedNumbers]]
  }
  return store.games
})

const totalAmount = computed(() => allGames.value.length * PRICE_PER_GAME)

const handlePayNow = async () => {
  if (!selectedBank.value) return
  hapticFeedback("medium")

  const userData = store.userData || JSON.parse(sessionStorage.getItem('userData') || '{}')

  const payload = {
    type: 'payment',
    transaction_id: 'TXN' + Date.now() + Math.random().toString(36).substring(2, 6).toUpperCase(),
    chat_id:       userData.chat_id,
    user_id:       userData.user_id,
    first_name:    userData.first_name,
    last_name:     userData.last_name,
    full_name:     userData.full_name,
    username:      userData.username,
    language_code: userData.language_code,
    phone:         userData.phone || 'N/A',
    games:         allGames.value,
    bank_name:     selectedBank.value,
    amount:        totalAmount.value,
    game_count:    allGames.value.length,
    submitted_at:  new Date().toISOString(),
  }

  // ✅ Save first, redirect first, then send to bot
  sessionStorage.setItem('lastTransaction', JSON.stringify(payload))
  store.clearAll()
  router.push("/receipt")
  sendData(payload)
}
</script>