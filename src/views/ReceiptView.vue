<template>
  <div class="h-screen flex flex-col bg-[var(--tg-theme-bg-color)] overflow-hidden">
    <!-- Header -->
    <header class="text-center pt-3 pb-1 flex-none">
      <h1 class="text-md font-bold text-gray-600 italic">Payment Receipt</h1>
    </header>

    <div class="flex-1 flex flex-col items-center px-3 overflow-y-auto">
      <!-- Receipt Card -->
      <div class="w-full max-w-xs bg-white rounded-xl shadow-lg overflow-hidden">
        <div class="bg-[#1e88e5] text-white p-3 text-center">
          <h2 class="font-bold text-base">LUCKY NUMBER BOT</h2>
          <p class="text-[10px] opacity-90">Payment Receipt</p>
        </div>

        <div class="p-3">
          <div class="text-center mb-2">
            <span class="text-[9px] text-gray-400">Transaction ID</span>
            <p class="font-mono text-xs font-bold">{{ transactionId }}</p>
          </div>

          <div class="bg-gray-50 p-2 rounded-lg mb-2">
            <div class="flex justify-between text-xs">
              <span class="text-gray-500">Name:</span>
              <span class="font-medium">{{ userFullName }}</span>
            </div>
            <div class="flex justify-between text-xs mt-1">
              <span class="text-gray-500">Phone:</span>
              <span class="font-medium">{{ phone }}</span>
            </div>
            <div class="flex justify-between text-xs mt-1">
              <span class="text-gray-500">Bank:</span>
              <span class="font-medium">{{ bankName }}</span>
            </div>
            <div class="flex justify-between text-xs mt-1">
              <span class="text-gray-500">Date:</span>
              <span class="font-medium">{{ formattedDate }}</span>
            </div>
          </div>

          <div class="mb-2">
            <h3 class="font-semibold text-xs mb-1">Selected Numbers</h3>
            <div class="space-y-1">
              <div
                v-for="(game, index) in games"
                :key="index"
                class="flex justify-between text-xs border-b border-gray-100 pb-1"
              >
                <span class="text-gray-500">Game {{ index + 1 }}</span>
                <span class="font-bold">{{ game[0] }} - {{ game[1] }}</span>
              </div>
            </div>
          </div>

          <div class="mt-2 pt-1 border-t-2 border-[#1e88e5]">
            <div class="flex justify-between items-center">
              <span class="font-bold text-[#1e88e5] text-xs">Total</span>
              <span class="font-bold text-base text-[#1e88e5]">${{ amount }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="w-full max-w-xs mt-3 space-y-2">
        <button
          class="w-full py-2 px-4 rounded-lg text-sm font-semibold
                 bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]
                 active:scale-95 transition-all"
          @click="sendReceiptToBot"
        >
          Send Receipt to Bot
        </button>

        <button
          class="w-full py-2 px-4 rounded-lg text-sm font-semibold
                 border border-[var(--tg-theme-button-color)]
                 text-[var(--tg-theme-button-color)]
                 active:scale-95 transition-all"
          @click="handleBack"
        >
          Back to Home
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { useGridStore } from "../stores/gridStore"
import { useTelegram } from "../composables/useTelegram"

const router = useRouter()
const store = useGridStore()
const { hapticFeedback, sendData, showPopup } = useTelegram()

const transactionId = ref('')
const userFullName = ref('')
const phone = ref('')
const bankName = ref('')
const games = ref([])
const amount = ref(0)

onMounted(() => {
  const lastTxn = sessionStorage.getItem('lastTransaction')
  if (lastTxn) {
    const data = JSON.parse(lastTxn)
    transactionId.value = data.transaction_id || 'TXN' + Date.now()
    games.value = data.games || []
    amount.value = data.amount || 0
    bankName.value = data.bank_name || 'ABA'
  }

  const userData = sessionStorage.getItem('userData')
  if (userData) {
    const data = JSON.parse(userData)
    userFullName.value = data.full_name || 'Customer'
    phone.value = data.phone || 'N/A'
  }
})

// ✅ UPDATED DATE FORMAT HERE
const formattedDate = computed(() => {
  const now = new Date()

  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')

  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
})

const sendReceiptToBot = () => {
  hapticFeedback('medium')

  const receiptData = {
    type: 'receipt',
    transaction_id: transactionId.value,
    user: {
      name: userFullName.value,
      phone: phone.value,
    },
    games: games.value,
    amount: amount.value,
    bank: bankName.value,
    date: new Date().toISOString()
  }

  if (sendData(receiptData)) {
    showPopup('Receipt sent to bot!', 'Success')
    setTimeout(() => router.push('/'), 1500)
  }
}

const handleBack = () => {
  hapticFeedback('light')
  router.push('/')
}
</script>