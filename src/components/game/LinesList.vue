<template>
  <div
    v-if="lines.length > 0"
    v-show="show"
    class="w-full max-w-md flex-none mb-2 max-h-[108px] overflow-y-auto"
  >
    <div
      v-for="(line, index) in lines"
      :key="index"
      class="flex items-center justify-between px-3 py-1 mb-1 rounded-md cursor-pointer active:scale-95 transition-all duration-150"
      :class="
        editingIndex === index
          ? 'bg-[var(--tg-theme-button-color)]'
          : 'bg-[var(--tg-theme-secondary-bg-color)]'
      "
      @click="onEditLine(index)"
    >
      <span
        class="text-sm"
        :class="
          editingIndex === index
            ? 'text-[var(--tg-theme-button-text-color)]'
            : 'text-[var(--tg-theme-hint-color)]'
        "
      >
        Line {{ index + 1 }}
      </span>

      <div class="flex items-center gap-2">
        <span
          class="text-sm font-bold"
          :class="
            editingIndex === index
              ? 'text-[var(--tg-theme-button-text-color)]'
              : 'text-[var(--tg-theme-text-color)]'
          "
        >
          <template v-if="editingIndex === index">
            {{ selectedNumbers[0] !== '?' ? selectedNumbers[0] : '...' }} ,
            {{ selectedNumbers[1] !== '?' ? selectedNumbers[1] : '...' }}
          </template>
          <template v-else> {{ line[0] }} , {{ line[1] }} </template>
        </span>

        <button
          class="text-sm cursor-pointer hover:scale-110 transition-transform"
          :class="
            editingIndex === index
              ? 'text-[var(--tg-theme-button-text-color)]'
              : 'text-red-400'
          "
          @click.stop="onDeleteLine(index)"
        >
          ❌
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  lines: Array,
  show: Boolean,
  editingIndex: Number,
  selectedNumbers: Array,
});

const emit = defineEmits(['editLine', 'deleteLine']);

const onEditLine = (index) => {
  emit('editLine', index);
};

const onDeleteLine = (index) => {
  emit('deleteLine', index);
};
</script>
