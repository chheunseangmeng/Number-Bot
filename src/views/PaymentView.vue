<template>
  <div class="h-screen flex flex-col bg-[var(--tg-theme-bg-color)] overflow-hidden">
    <!-- Header -->
    <header class="text-center pt-3 pb-1 flex-none relative">
      <button
        class="absolute left-3 border px-2 py-1 rounded-md top-3 text-sm text-[var(--tg-theme-hint-color)] active:scale-95 transition-all"
        @click="handleBack"
      >
        <i class="fa-solid fa-angle-left"></i>Back
      </button>
      <h1 class="text-md font-bold text-gray-600 italic">Payment</h1>
      <p class="text-xs text-[var(--tg-theme-hint-color)]">
        Select your bank
      </p>
    </header>

    <!-- Expired Overlay -->
    <div
      v-if="isExpired"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-6"
    >
      <div class="bg-white rounded-2xl p-6 w-full max-w-xs text-center shadow-xl">
        <div class="text-5xl mb-3">⏰</div>
        <h2 class="text-base font-bold text-gray-800 mb-1">Time Expired!</h2>
        <p class="text-sm text-gray-500 mb-5">
          Please click OK to return and complete your payment.
        </p>
        <button
          class="w-full py-2 rounded-lg text-sm font-semibold bg-[#1e88e5] text-white active:scale-95 transition-all"
          @click="handleExpiredConfirm"
        >
          OK
        </button>
      </div>
    </div>

    <div class="flex-1 flex flex-col items-center px-3 overflow-y-auto">
      <!-- Order Summary -->
      <div class="w-full max-w-xs bg-[var(--tg-theme-secondary-bg-color)] rounded-xl p-3 mb-3 flex-none">
        <h2 class="text-xs font-semibold text-[var(--tg-theme-hint-color)] mb-1">
          Order Summary
        </h2>

        <div
          v-for="(line, index) in allLines"
          :key="index"
          class="flex justify-between items-center py-1"
        >
          <span class="text-xs text-[var(--tg-theme-hint-color)]">Line {{ index + 1 }}</span>
          <span class="text-xs font-bold text-[var(--tg-theme-text-color)]">
            {{ line[0] }} , {{ line[1] }}
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

      <!-- Countdown Timer -->
      <div class="w-full max-w-xs flex-none mt-8 flex flex-col items-center">
        <div class="relative w-28 h-28">
          <svg class="w-28 h-28 -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50" cy="50" r="44"
              fill="none"
              stroke="currentColor"
              stroke-width="5"
              class="text-[var(--tg-theme-hint-color)] opacity-20"
            />
            <circle
              cx="50" cy="50" r="44"
              fill="none"
              stroke-width="5"
              stroke-linecap="round"
              :stroke="timeLeft <= 30 ? '#ef4444' : 'var(--tg-theme-button-color)'"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="dashOffset"
              style="transition: stroke-dashoffset 0.3s linear, stroke 0.3s"
            />
          </svg>

          <div class="absolute inset-0 flex flex-col items-center justify-center">
            <span
              class="text-xl font-bold tabular-nums"
              :class="timeLeft <= 30 ? 'text-red-500' : 'text-[var(--tg-theme-text-color)]'"
            >
              {{ formattedTime }}
            </span>
            <span class="text-[9px] font-medium mt-0.5 text-[var(--tg-theme-hint-color)]">
              remaining
            </span>
          </div>
        </div>

        <div v-if="timeLeft <= 30 && timeLeft > 0" class="mt-3">
          <p class="text-xs font-semibold text-red-500 flex items-center gap-1">
            Hurry up! <span>⚠️</span>
          </p>
        </div>
        <p v-else class="text-[10px] mt-2 text-[var(--tg-theme-hint-color)]">
          Time remaining to pay
        </p>
      </div>
    </div>

    <!-- Pay Now Button -->
    <div class="w-full max-w-xs mx-auto mt-4 mb-8 flex-none">
      <button
        class="w-full py-3 px-4 rounded-lg text-sm font-semibold transition-all active:scale-95 focus:outline-none disabled:opacity-30 disabled:cursor-not-allowed"
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
import { ref, computed, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"
import { useGridStore } from "../stores/gridStore"
import { useTelegram } from "../composables/useTelegram"

const router = useRouter()
const store = useGridStore()
const { hapticFeedback } = useTelegram()

const selectedBank = ref("")
const PRICE_PER_LINE = 1.0
const TOTAL_TIME = 180
const isExpired = ref(false)
const timeLeft = ref(TOTAL_TIME)
let countdownInterval = null

// Countdown
const circumference = 2 * Math.PI * 44

const dashOffset = computed(() => {
  const progress = timeLeft.value / TOTAL_TIME
  return circumference * (1 - progress)
})

const formattedTime = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60)
  const seconds = String(timeLeft.value % 60).padStart(2, "0")
  return `${minutes}:${seconds}`
})

const startCountdown = () => {
  countdownInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
      if (timeLeft.value <= 0) {
        clearInterval(countdownInterval)
        isExpired.value = true
        hapticFeedback("medium")
      }
    }
  }, 1000)
}

onMounted(() => {
  const savedStartTime = sessionStorage.getItem("payment_start_time")

  if (savedStartTime) {
    const elapsed = Math.floor((Date.now() - parseInt(savedStartTime)) / 1000)
    const remaining = TOTAL_TIME - elapsed
    if (remaining <= 0) {
      isExpired.value = true
      return
    }
    timeLeft.value = remaining
  } else {
    sessionStorage.setItem("payment_start_time", Date.now().toString())
    timeLeft.value = TOTAL_TIME
  }

  startCountdown()
})

onUnmounted(() => {
  clearInterval(countdownInterval)
})

// Expired
const handleExpiredConfirm = () => {
  sessionStorage.removeItem("payment_start_time")
  router.push("/")
}

// Banks
const banks = [
  { name: "ABA",    logo: "/banks/aba.png" },
  { name: "ACLEDA", logo: "/banks/acleda.png" },
  { name: "JTrust", logo: "/banks/jtrust.png" },
  { name: "Wing",   logo: "/banks/wing.png" },
]

// All Lines
const allLines = computed(() => {
  if (store.editingIndex !== null) {
    return store.lines.map((l, i) =>
      i === store.editingIndex ? [...store.selectedNumbers] : l
    )
  }
  if (store.selectedCount === 2) {
    return [...store.lines, [...store.selectedNumbers]]
  }
  return store.lines
})

const totalAmount = computed(() => allLines.value.length * PRICE_PER_LINE)

// Generate Transaction ID
const generateTransactionId = () => {
  const timestamp = Date.now().toString().slice(-8)
  const randomPart = Math.random().toString(36).substring(2, 4).toUpperCase()
  return `TXN${timestamp}${randomPart}`
}

// Generate Reference
const generateReference = () => {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, "0")
  const day = String(now.getDate()).padStart(2, "0")
  const seq = String(Math.floor(Math.random() * 999) + 1).padStart(3, "0")
  return `REF-${year}${month}${day}${seq}`
}

// Back - keep timer running
const handleBack = () => {
  hapticFeedback("light")
  clearInterval(countdownInterval)
  router.push("/")
}

// Pay Now - reset timer
const handlePayNow = () => {
  if (!selectedBank.value) return
  hapticFeedback("medium")
  clearInterval(countdownInterval)
  sessionStorage.removeItem("payment_start_time")

  const userData = store.userData || JSON.parse(sessionStorage.getItem("userData") || "{}")

  const payload = {
    type:           "payment",
    transaction_id: generateTransactionId(),
    reference:      generateReference(),
    chat_id:        userData.chat_id,
    user_id:        userData.user_id,
    first_name:     userData.first_name,
    last_name:      userData.last_name,
    full_name:      userData.full_name,
    username:       userData.username,
    language_code:  userData.language_code,
    phone:          userData.phone || "N/A",
    lines:          allLines.value,
    bank_name:      selectedBank.value,
    amount:         totalAmount.value,
    line_count:     allLines.value.length,
    submitted_at:   new Date().toISOString(),
  }

  sessionStorage.setItem("lastTransaction", JSON.stringify(payload))
  store.clearAll()
  router.push("/receipt")
}
</script>

<style scoped>
.tabular-nums {
  font-variant-numeric: tabular-nums;
}
</style>