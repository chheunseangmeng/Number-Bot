import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGridStore = defineStore('grid', () => {
  const games = ref([])
  const selectedNumbers = ref([])
  const startParam = ref('')
  const editingIndex = ref(null)
  const _pendingSelection = ref([])
  const MAX_SELECTION = 2
  const MAX_GAMES = 5

  const selectedCount = computed(() => selectedNumbers.value.length)
  const gamesCount = computed(() => games.value.length)
  const canSelectMore = computed(() => selectedNumbers.value.length < MAX_SELECTION)

  const isSelected = (number) => selectedNumbers.value.includes(number)

  function selectNumber(number) {
    if (selectedNumbers.value.length < MAX_SELECTION) {
      selectedNumbers.value.push(number)
    }
  }

  function deselectNumber(number) {
    const index = selectedNumbers.value.indexOf(number)
    if (index > -1) {
      selectedNumbers.value.splice(index, 1)
    }
  }

  function toggleNumber(number) {
    if (selectedNumbers.value.includes(number)) {
      deselectNumber(number)
    } else if (selectedNumbers.value.length < MAX_SELECTION) {
      selectNumber(number)
    }
  }

  function clearSelection() {
    selectedNumbers.value = []
  }

  function saveGame() {
    if (selectedNumbers.value.length !== MAX_SELECTION) return
    if (editingIndex.value !== null) {
      games.value[editingIndex.value] = [...selectedNumbers.value]
      editingIndex.value = null
      if (_pendingSelection.value.length === MAX_SELECTION) {
        selectedNumbers.value = [..._pendingSelection.value]
        _pendingSelection.value = []
      } else {
        selectedNumbers.value = []
      }
    } else if (games.value.length < MAX_GAMES - 1) {
      games.value.push([...selectedNumbers.value])
      selectedNumbers.value = []
    }
  }

  function editGame(index) {
    if (editingIndex.value !== null) {
      if (selectedNumbers.value.length === MAX_SELECTION) {
        games.value[editingIndex.value] = [...selectedNumbers.value]
      }
    } else {
      if (games.value.length < MAX_GAMES - 1) {
        if (selectedNumbers.value.length === MAX_SELECTION) {
          games.value.push([...selectedNumbers.value])
        }
      } else {
        _pendingSelection.value = [...selectedNumbers.value]
      }
    }

    editingIndex.value = index
    selectedNumbers.value = [...games.value[index]]
  }

  function clearAll() {
    games.value = []
    selectedNumbers.value = []
    editingIndex.value = null
    _pendingSelection.value = []
  }

  function setStartParam(param) {
    startParam.value = param
  }

  return {
    games,
    selectedNumbers,
    startParam,
    editingIndex,
    MAX_SELECTION,
    MAX_GAMES,
    selectedCount,
    gamesCount,
    canSelectMore,
    isSelected,
    selectNumber,
    deselectNumber,
    toggleNumber,
    clearSelection,
    saveGame,
    editGame,
    clearAll,
    setStartParam,
  }
})