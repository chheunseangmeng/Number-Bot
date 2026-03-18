import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGridStore = defineStore('grid', () => {
  const games = ref([])
  const selectedNumbers = ref([])
  const startParam = ref('')
  const editingIndex = ref(null)
  const _pendingSelection = ref([])
  const userData = ref(null)
  const MAX_SELECTION = 2
  const MAX_GAMES = 5  // ✅ Correct limit

  const selectedCount = computed(() => selectedNumbers.value.length)
  const gamesCount = computed(() => games.value.length)
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

  function saveGame() {
    if (selectedNumbers.value.length !== MAX_SELECTION) return
    
    if (editingIndex.value !== null) {
      // Update existing game
      games.value[editingIndex.value] = [...selectedNumbers.value]
      editingIndex.value = null
      
      if (_pendingSelection.value.length === MAX_SELECTION) {
        selectedNumbers.value = [..._pendingSelection.value]
        _pendingSelection.value = []
      } else {
        selectedNumbers.value = []
      }
    } else if (games.value.length < MAX_GAMES) {
      // Add new game
      games.value.push([...selectedNumbers.value])
      selectedNumbers.value = []
    }
    
    saveToSession()
  }

  function editGame(index) {
    if (editingIndex.value !== null) {
      if (selectedNumbers.value.length === MAX_SELECTION) {
        games.value[editingIndex.value] = [...selectedNumbers.value]
      }
    } else {
      if (games.value.length < MAX_GAMES) {
        if (selectedNumbers.value.length === MAX_SELECTION) {
          games.value.push([...selectedNumbers.value])
        }
      } else {
        _pendingSelection.value = [...selectedNumbers.value]
      }
    }

    editingIndex.value = index
    selectedNumbers.value = [...games.value[index]]
    saveToSession()
  }

  function clearAll() {
    games.value = []
    selectedNumbers.value = []
    editingIndex.value = null
    _pendingSelection.value = []
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
    sessionStorage.setItem('games', JSON.stringify(games.value))
    sessionStorage.setItem('editingIndex', JSON.stringify(editingIndex.value))
    sessionStorage.setItem('userData', JSON.stringify(userData.value))
    sessionStorage.setItem('startParam', JSON.stringify(startParam.value))
  }

  function loadFromSession() {
    const savedNumbers = sessionStorage.getItem('selectedNumbers')
    if (savedNumbers) selectedNumbers.value = JSON.parse(savedNumbers)
    
    const savedGames = sessionStorage.getItem('games')
    if (savedGames) games.value = JSON.parse(savedGames)
    
    const savedEditingIndex = sessionStorage.getItem('editingIndex')
    if (savedEditingIndex) editingIndex.value = JSON.parse(savedEditingIndex)
    
    const savedUserData = sessionStorage.getItem('userData')
    if (savedUserData) userData.value = JSON.parse(savedUserData)
    
    const savedStartParam = sessionStorage.getItem('startParam')
    if (savedStartParam) startParam.value = JSON.parse(savedStartParam)
  }

  return {
    games,
    selectedNumbers,
    startParam,
    editingIndex,
    userData,
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
    setUserData,
    saveToSession,
    loadFromSession,
  }
})