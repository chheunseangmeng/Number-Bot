<template>
  <div class="h-screen flex flex-col bg-[var(--tg-theme-bg-color)]">
    <!-- Header -->
    <header class="text-center flex-none">
      <h1 class="text-md font-bold text-gray-600 italic">
        Select number below
      </h1>
      <div
        v-if="store.startParam"
        class="mt-1 text-xs text-[var(--tg-theme-hint-color)]"
      >
        Referral: {{ store.startParam }}
      </div>
    </header>

    <!-- Shared container for grid + boxes + counter + submit -->
    <div class="flex-1 flex flex-col items-center p-2 min-h-0 w-full">
      <!-- Number Grid Cell-->
      <div class="grid grid-cols-4 gap-2 w-full max-w-md flex-1 min-h-0"
           style="grid-auto-flow: column; grid-template-rows: repeat(10, 1fr)">
        <GridCell v-for="n in 40" :key="n" :number="n" />
      </div>

      <hr class="w-full max-w-md my-2" />

      <!-- Contain 2 Boxes -->
      <div class="flex gap-2 w-full max-w-md flex-none">
        <!-- Box 1 -->
        <div
          class="flex-1 h-12 rounded-md flex items-center justify-center text-3xl font-bold transition-all duration-200"
          :class="
            selectedNumbers[0]
              ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]'
              : 'bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-hint-color)] border border-dashed border-[var(--tg-theme-hint-color)]'
          "
        >
          {{ selectedNumbers[0] || "?" }}
        </div>

        <!-- Box 2 -->
        <div
          class="flex-1 h-12 rounded-md flex items-center justify-center text-3xl font-bold transition-all duration-200"
          :class="
            selectedNumbers[1]
              ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]'
              : 'bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-hint-color)] border border-dashed border-[var(--tg-theme-hint-color)]'
          "
        >
          {{ selectedNumbers[1] || "?" }}
        </div>
      </div>

      <!-- Counter -->
      <p
        class="text-center text-sm text-[var(--tg-theme-hint-color)] flex-none mt-1"
      >
        {{ store.selectedCount }}/2 numbers selected
      </p>

      <!-- Submit Button -->
      <div class="w-full max-w-md flex-none mt-1 mb-1">
        <SubmitButton
          :disabled="!canSubmit"
          :text="submitButtonText"
          @click="handleSubmit"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import GridCell from "../components/grid/GridCell.vue";
import SubmitButton from "../components/ui/SubmitButton.vue";
import { useGridStore } from "../stores/gridStore";
import { useTelegram } from "../composables/useTelegram";

const store = useGridStore();
const { hapticFeedback, showPopup, sendData } = useTelegram();

// Selected numbers for boxes
const selectedNumbers = computed(() => {
  const boxes = ["?", "?"];
  store.selectedNumbers.forEach((num, i) => {
    if (i < 2) boxes[i] = num;
  });
  return boxes;
});

// Submit button
const canSubmit = computed(() => store.selectedCount === 2);
const submitButtonText = computed(() => {
  if (store.selectedCount === 0) return "Select 2 numbers";
  if (store.selectedCount === 1) return "Select 1 more";
  return "Submit";
});

// Handle submit
const handleSubmit = async () => {
  if (!canSubmit.value) return;
  hapticFeedback("medium");

  const payload = {
    selectedNumbers: [...store.selectedNumbers],
    startParam: store.startParam || null,
    submittedAt: new Date().toISOString(),
  };

  const sentToBot = sendData(payload);
  if (sentToBot) {
    await showPopup("Submitted successfully!", "Success");
  } else {
    await showPopup(
      "Could not send data to Telegram bot. Please try again.",
      "Send Failed",
    );
  }
};
</script>
