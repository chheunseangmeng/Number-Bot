<template>
  <div class="min-h-screen flex flex-col bg-[var(--tg-theme-bg-color)]">
    <!-- Header -->
    <header class="text-center">
      <h1 class="text-md font-bold text-gray-600 italic">
        Select number below
      </h1>
      <!-- <p class="text-sm text-[var(--tg-theme-hint-color)]">
        Select 2 numbers (1-40)
      </p> -->

   
      <div
        v-if="store.startParam"
        class="mt-2 text-xs text-[var(--tg-theme-hint-color)]"
      >
        Referral: {{ store.startParam }}
      </div>
    </header>

    <main class="flex-1 p-3">
      <!-- Grid at TOP -->
      <NumberGrid />

      <hr class="mt-2 mb-2">

      <!-- 2 Boxes in MIDDLE -->
      <div class="grid grid-cols-4 gap-2 max-w-md mx-auto">
        <!-- Box 1-->
        <div
          class="col-span-2 h-12 rounded-md flex items-center justify-center text-3xl font-bold transition-all duration-200"
          :class="[
            selectedNumbers[0]
              ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]'
              : 'bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-hint-color)] border-dashed border-[var(--tg-theme-hint-color)]',
          ]"
        >
          {{ selectedNumbers[0] || "?" }}
        </div>

        <!-- Box 2 -->
        <div
          class="col-span-2 h-12 rounded-md flex items-center justify-center text-3xl font-bold transition-all duration-200"
          :class="[
            selectedNumbers[1]
              ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]'
              : 'bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-hint-color)] border-dashed border-[var(--tg-theme-hint-color)]',
          ]"
        >
          {{ selectedNumbers[1] || "?" }}
        </div>
      </div>

      <!-- Selection counter under boxes -->
      <p
        class="text-center text-sm mt-1 mb-1 text-[var(--tg-theme-hint-color)]"
      >
        {{ store.selectedCount }}/2 numbers selected
      </p>

      <!-- Submit Button at BOTTOM -->
      <div class="max-w-md mx-auto">
        <SubmitButton
          :disabled="!canSubmit"
          :text="submitButtonText"
          @click="handleSubmit"
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from "vue";
import NumberGrid from "../components/grid/NumberGrid.vue";
import SubmitButton from "../components/ui/SubmitButton.vue";
import { useGridStore } from "../stores/gridStore";
import { useTelegram } from "../composables/useTelegram";

const store = useGridStore();
const { hapticFeedback, showPopup, sendData } = useTelegram();

// Simple array for 2 boxes
const selectedNumbers = computed(() => {
  const boxes = ["?", "?"];
  store.selectedNumbers.forEach((num, index) => {
    if (index < 2) {
      boxes[index] = num;
    }
  });
  return boxes;
});

// Submit button enabled only when exactly 2 numbers selected
const canSubmit = computed(() => {
  return store.selectedCount === 2;
});

const submitButtonText = computed(() => {
  if (store.selectedCount === 0) return "Select 2 numbers";
  if (store.selectedCount === 1) return "Select 1 more";
  return "Submit";
});

const handleSubmit = async () => {
  if (!canSubmit.value) return;

  hapticFeedback("medium");
  const numbers = [...store.selectedNumbers];
  
  // REMOVED: All user-related data (fullName, username, userId)
  
  // SIMPLIFIED payload - only send what's needed
  const payload = {
    selectedNumbers: numbers,
    startParam: store.startParam || null,
    submittedAt: new Date().toISOString(),
  };

  const sentToBot = sendData(payload);
  if (sentToBot) {
    await showPopup(
      "Submitted successfully!",
      "Success"
    );
    return;
  }

  await showPopup(
    "Could not send data to Telegram bot. Please try again.",
    "Send Failed"
  );
};
</script>