<template>
  <div class="w-full max-w-md flex-none mt-1 mb-1">
    <!-- MAX reached → Pay Now -->
    <NextButton
      v-if="isMaxReached"
      text="Pay Now"
      variant="primary"
      class="w-full"
      @click="onSubmit"
    />

    <!-- Normal -->
    <div v-else class="flex gap-2">
      <NextButton
        v-if="canSave"
        text="Save Line"
        variant="secondary"
        class="flex-1"
        :disabled="!canSubmit"
        @click="onSaveLine"
      />

      <NextButton
        v-if="canAddLine"
        text="Add Line"
        variant="secondary"
        class="flex-1"
        :disabled="!canSubmit"
        @click="onSaveLine"
      />

      <NextButton
        text="Pay Now"
        variant="primary"
        class="flex-1"
        :disabled="!canNext"
        @click="onSubmit"
      />
    </div>
  </div>
</template>

<script setup>
import NextButton from '../ui/NextButton.vue';

const props = defineProps({
  isMaxReached: Boolean,
  canSave: Boolean,
  canAddLine: Boolean,
  canSubmit: Boolean,
  canNext: Boolean,
});

const emit = defineEmits(['saveLine', 'submit']);

const onSaveLine = () => {
  emit('saveLine');
};

const onSubmit = () => {
  emit('submit');
};
</script>
