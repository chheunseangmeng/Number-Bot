<template>
  <div class="h-screen flex flex-col bg-[var(--tg-theme-bg-color)] overflow-hidden">
    <div class="flex-1 flex flex-col items-center px-3 mt-4 overflow-y-auto">
      
      <!-- Receipt Card -->
      <div 
        ref="receiptRef"
        class="w-full max-w-full bg-white rounded-lg shadow-sm overflow-hidden"
      >
        <!-- Header -->
        <div class="bg-[#1e88e5] text-white p-4 text-center">
          <h2 class="font-bold text-base">LUCKY NUMBER BOT</h2>
          <p class="text-[10px] opacity-90">Payment Receipt</p>
        </div>

        <!-- Body -->
        <div class="p-4">
          <!-- Transaction ID -->
          <div class="text-center mb-3">
            <span class="text-[9px] text-gray-400">Transaction ID</span>
            <p class="font-mono text-xs font-bold">{{ transactionId }}</p>
          </div>

          <!-- Reference Number -->
          <div class="text-center mb-3">
            <span class="text-[9px] text-gray-400">Reference Number</span>
            <p class="font-mono text-xs font-bold">{{ referenceNumber }}</p>
          </div>

          <!-- User Info -->
          <div class="bg-gray-50 p-3 rounded-lg mb-3 space-y-1">
            <div class="flex justify-between text-xs">
              <span class="text-gray-500">Name:</span>
              <span class="font-medium">{{ userFullName }}</span>
            </div>
            <div class="flex justify-between text-xs">
              <span class="text-gray-500">Phone:</span>
              <span class="font-medium">{{ phone }}</span>
            </div>
            <div class="flex justify-between text-xs">
              <span class="text-gray-500">Bank:</span>
              <span class="font-medium">{{ bankName }}</span>
            </div>
            <div class="flex justify-between text-xs">
              <span class="text-gray-500">Date:</span>
              <span class="font-medium">{{ formattedDate }}</span>
            </div>
          </div>

          <!-- Games -->
          <div class="mb-3">
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

          <!-- Total -->
          <div class="mt-3 pt-2 border-t-2 border-[#1e88e5]">
            <div class="flex justify-between items-center mb-2">
              <span class="font-bold text-[#1e88e5] text-xs">Total</span>
              <span class="font-bold text-base text-[#1e88e5]">${{ amount }}</span>
            </div>
            <p class="text-center text-[10px] text-gray-500 mt-1 italic">Thank you for your purchase!</p>
          </div>
        </div>
      </div>

      <!-- Save to Photos Button -->
      <div class="w-full max-w-xs mt-4">
        <button
          class="w-full py-3 px-4 rounded-lg text-sm font-semibold
                 bg-blue-500 text-white
                 active:scale-95 transition-all"
          @click="saveImage"
        >
          Save to Photos
        </button>
      </div>

      <!-- Close Button -->
      <div class="w-full max-w-xs mt-2 mb-6">
        <button
          class="w-full py-3 px-4 rounded-lg text-sm font-semibold
                 bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]
                 active:scale-95 transition-all"
          @click="handleClose"
        >
          Close
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useTelegram } from "../composables/useTelegram"
import html2canvas from "html2canvas"

const { hapticFeedback, sendData, closeMiniApp } = useTelegram()

const receiptRef = ref(null)

const transactionId = ref('')
const referenceNumber = ref('')
const userFullName = ref('')
const phone = ref('')
const bankName = ref('')
const games = ref([])
const amount = ref(0)
const submittedAt = ref('')

// Detect iOS only
const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream

onMounted(() => {
  const lastTxn = sessionStorage.getItem('lastTransaction')
  if (lastTxn) {
    const data = JSON.parse(lastTxn)
    transactionId.value = data.transaction_id || 'N/A'
    referenceNumber.value = 'REF' + Date.now().toString().slice(-8)
    games.value = data.games || []
    amount.value = data.amount || 0
    bankName.value = data.bank_name || 'N/A'
    userFullName.value = data.full_name || 'Customer'
    phone.value = data.phone || 'N/A'
    submittedAt.value = data.submitted_at || new Date().toISOString()
  }
})

const formattedDate = computed(() => {
  const date = new Date(submittedAt.value || new Date())
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
})

const saveImage = async () => {
  if (!receiptRef.value) return
  hapticFeedback('medium')

  try {
    const canvas = await html2canvas(receiptRef.value, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#ffffff',
    })

    canvas.toBlob(async (blob) => {
      const file = new File([blob], `receipt_${transactionId.value}.png`, { type: 'image/png' })

      if (isIOS && navigator.share && navigator.canShare({ files: [file] })) {
        // iOS only → native share
        await navigator.share({
          files: [file],
          title: 'Payment Receipt',
        })
      } else {
        // Android + Desktop → direct download
        const link = document.createElement("a")
        link.href = URL.createObjectURL(blob)
        link.download = `receipt_${transactionId.value}.png`
        link.click()
      }
    }, 'image/png')

  } catch (error) {
    console.error('Failed to save receipt:', error)
    alert('Could not save image. Please take a screenshot instead.')
  }
}

const handleClose = () => {
  hapticFeedback('light')
  const lastTxn = JSON.parse(sessionStorage.getItem('lastTransaction') || '{}')
  sendData(lastTxn)
  closeMiniApp()
}
</script>