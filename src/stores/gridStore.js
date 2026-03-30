import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGridStore = defineStore('grid', () => {
  const lines = ref([])
  const selectedNumbers = ref([])
  const startParam = ref('')
  const editingIndex = ref(null)
  const _pendingSelection = ref([])
  const userData = ref(null)
  const MAX_SELECTION = 2
  const MAX_LINES = 5

  const selectedCount = computed(() => selectedNumbers.value.length)
  const linesCount = computed(() => lines.value.length)
  const canSelectMore = computed(() => selectedNumbers.value.length < MAX_SELECTION)

  const isSelected = (number) => selectedNumbers.value.includes(number)

  function selectNumber(number) {
    if (selectedNumbers.value.length < MAX_SELECTION) {
      selectedNumbers.value.push(number)
      saveToSession()
    }
  }

  function deselectNumber(number) {
    const index = selectedNumbers.value.indexOf(number)
    if (index > -1) {
      selectedNumbers.value.splice(index, 1)
      saveToSession()
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
    saveToSession()
  }

  function saveLine() {
    if (selectedNumbers.value.length !== MAX_SELECTION) return

    if (editingIndex.value !== null) {
      // Update existing line
      lines.value[editingIndex.value] = [...selectedNumbers.value]
      editingIndex.value = null

      if (_pendingSelection.value.length === MAX_SELECTION) {
        selectedNumbers.value = [..._pendingSelection.value]
        _pendingSelection.value = []
      } else {
        selectedNumbers.value = []
      }
    } else if (lines.value.length < MAX_LINES) {
      // Add new line
      lines.value.push([...selectedNumbers.value])
      selectedNumbers.value = []
    }

    saveToSession()
  }

  function editLine(index) {
    if (editingIndex.value !== null) {
      if (selectedNumbers.value.length === MAX_SELECTION) {
        lines.value[editingIndex.value] = [...selectedNumbers.value]
      }
    } else {
      if (lines.value.length < MAX_LINES) {
        if (selectedNumbers.value.length === MAX_SELECTION) {
          lines.value.push([...selectedNumbers.value])
        }
      } else {
        _pendingSelection.value = [...selectedNumbers.value]
      }
    }

    editingIndex.value = index
    selectedNumbers.value = [...lines.value[index]]
    saveToSession()
  }

  function clearAll() {
    lines.value = []
    selectedNumbers.value = []
    editingIndex.value = null
    _pendingSelection.value = []
    saveToSession()
  }

  function deleteLine(index) {
    lines.value.splice(index, 1)
    editingIndex.value = null
    selectedNumbers.value = []
    saveToSession()
  }

  function setStartParam(param) {
    startParam.value = param
    saveToSession()
  }

  function setUserData(data) {
    userData.value = data
    saveToSession()
  }

  // Session Storage functions
  function saveToSession() {
    sessionStorage.setItem('selectedNumbers', JSON.stringify(selectedNumbers.value))
    sessionStorage.setItem('lines', JSON.stringify(lines.value))
    sessionStorage.setItem('editingIndex', JSON.stringify(editingIndex.value))
    sessionStorage.setItem('userData', JSON.stringify(userData.value))
    sessionStorage.setItem('startParam', JSON.stringify(startParam.value))
  }

  function loadFromSession() {
    const savedNumbers = sessionStorage.getItem('selectedNumbers')
    if (savedNumbers) selectedNumbers.value = JSON.parse(savedNumbers)

    const savedLines = sessionStorage.getItem('lines')
    if (savedLines) lines.value = JSON.parse(savedLines)

    const savedEditingIndex = sessionStorage.getItem('editingIndex')
    if (savedEditingIndex) editingIndex.value = JSON.parse(savedEditingIndex)

    const savedUserData = sessionStorage.getItem('userData')
    if (savedUserData) userData.value = JSON.parse(savedUserData)

    const savedStartParam = sessionStorage.getItem('startParam')
    if (savedStartParam) startParam.value = JSON.parse(savedStartParam)
  }

  return {
    lines,
    selectedNumbers,
    startParam,
    editingIndex,
    userData,
    MAX_SELECTION,
    MAX_LINES,
    selectedCount,
    linesCount,
    canSelectMore,
    isSelected,
    selectNumber,
    deselectNumber,
    toggleNumber,
    clearSelection,
    saveLine,
    editLine,
    clearAll,
    deleteLine,
    setStartParam,
    setUserData,
    saveToSession,
    loadFromSession,
  }
})