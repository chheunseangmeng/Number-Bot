import { onMounted } from 'vue'
import { useGridStore } from '../stores/gridStore'

export function useTelegram() {
  const store = useGridStore()
  const getTelegramWebApp = () => window.Telegram?.WebApp || null
  const isTelegramContext = () => {
    const tg = getTelegramWebApp()
    return Boolean(tg && typeof tg.initData === 'string' && tg.initData.length > 0)
  }

  onMounted(() => {
    // Get ALL data from URL parameters (provided by team's bot)
    const urlParams = new URLSearchParams(window.location.search)
    
    // Parse user data from URL
    const userData = {
      bot_id: urlParams.get('tg_bot_id'),
      chat_id: urlParams.get('tg_chat_id'),
      user_id: urlParams.get('tg_user_id'),
      is_bot: urlParams.get('tg_user_is_bot') === 'true',
      first_name: urlParams.get('tg_user_first_name'),
      last_name: urlParams.get('tg_user_last_name'),
      username: urlParams.get('tg_user_username'),
      language_code: urlParams.get('tg_user_language_code'),
      full_name: urlParams.get('tg_user_full_name'),
      phone: urlParams.get('tg_phone'),
      // Parse the JSON string
      raw_user: JSON.parse(urlParams.get('tg_user') || '{}')
    }
    
    // Store in Pinia AND sessionStorage
    store.setUserData(userData)
    sessionStorage.setItem('userData', JSON.stringify(userData))
    
    // Load saved game data from sessionStorage
    store.loadFromSession()
    
    // Apply Telegram theme if available
    const tg = getTelegramWebApp()
    if (tg) {
      tg.ready()
      tg.expand()
      
      const theme = tg.themeParams
      if (theme) {
        Object.keys(theme).forEach(key => {
          document.documentElement.style.setProperty(`--tg-theme-${key}`, theme[key])
        })
      }
      
      console.log('Telegram Mini App initialized with user data:', userData)
    } else {
      console.log('Running outside Telegram - using fallback mode')
    }
  })

  const hapticFeedback = (style = 'light') => {
    try {
      if (isTelegramContext() && window.Telegram?.WebApp?.HapticFeedback) {
        window.Telegram.WebApp.HapticFeedback.impactOccurred(style)
      } else {
        console.log('Haptic feedback (fallback):', style)
      }
    } catch (error) {
      console.warn('Haptic feedback failed:', error)
    }
  }

  const showPopup = (message, title = 'Message') =>
    new Promise((resolve) => {
      try {
        if (isTelegramContext() && window.Telegram?.WebApp?.showPopup) {
          window.Telegram.WebApp.showPopup(
            {
              title,
              message,
              buttons: [{ type: 'ok', id: 'ok' }]
            },
            (buttonId) => {
              resolve(buttonId || 'ok')
            }
          )
        } else {
          window.alert(`${title}\n\n${message}`)
          resolve('ok')
        }
      } catch (error) {
        console.warn('Telegram popup failed, using alert fallback:', error)
        window.alert(`${title}\n\n${message}`)
        resolve('ok')
      }
    })

  const sendData = (payload) => {
    try {
      const tg = getTelegramWebApp()
      if (!tg?.sendData) {
        return false
      }
      const serializedPayload =
        typeof payload === 'string' ? payload : JSON.stringify(payload)
      tg.sendData(serializedPayload)
      return true
    } catch (error) {
      console.warn('Failed to send data to Telegram bot:', error)
      return false
    }
  }

  const closeMiniApp = () => {
    try {
      const tg = getTelegramWebApp()
      if (isTelegramContext() && tg?.close) {
        tg.close()
      }
    } catch (error) {
      console.warn('Failed to close Telegram Mini App:', error)
    }
  }

  return {
    hapticFeedback,
    showPopup,
    sendData,
    closeMiniApp,
  }
}