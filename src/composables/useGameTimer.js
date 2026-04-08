import { computed, ref, onUnmounted } from 'vue';

export function useGameTimer() {
  const timeToExpiry = ref(null);
  let expiryCountdownInterval = null;

  const getExpiryTimeUTC = (expiryHourUTC, expiryMinuteUTC = 0) => {
    const now = new Date();
    const expiryTime = new Date(
      Date.UTC(
        now.getUTCFullYear(),
        now.getUTCMonth(),
        now.getUTCDate(),
        expiryHourUTC,
        expiryMinuteUTC,
        0,
      ),
    );

    if (now.getTime() >= expiryTime.getTime()) {
      expiryTime.setUTCDate(expiryTime.getUTCDate() + 1);
    }

    return expiryTime;
  };

  const getCambodiaTime = (expiryHourUTC, expiryMinuteUTC = 0) => {
    const expiryUTC = getExpiryTimeUTC(expiryHourUTC, expiryMinuteUTC);
    const expiryCambodia = new Date(expiryUTC.getTime() + 7 * 60 * 60 * 1000);

    const year = expiryCambodia.getUTCFullYear();
    const month = String(expiryCambodia.getUTCMonth() + 1).padStart(2, '0');
    const day = String(expiryCambodia.getUTCDate()).padStart(2, '0');
    const hours = String(expiryCambodia.getUTCHours()).padStart(2, '0');
    const minutes = String(expiryCambodia.getUTCMinutes()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}`;
  };

  const updateTimeToExpiry = (expiryHourUTC, expiryMinuteUTC = 0) => {
    const now = new Date();
    const expiryTime = getExpiryTimeUTC(expiryHourUTC, expiryMinuteUTC);
    const diffMs = expiryTime.getTime() - now.getTime();

    if (diffMs <= 0) {
      timeToExpiry.value = null;
      if (expiryCountdownInterval) {
        clearInterval(expiryCountdownInterval);
        expiryCountdownInterval = null;
      }
      return;
    }

    const totalSeconds = Math.floor(diffMs / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    timeToExpiry.value = { hours, minutes, seconds };
  };

  const startExpiryCountdown = (expiryHourUTC, expiryMinuteUTC = 0) => {
    if (expiryCountdownInterval) {
      clearInterval(expiryCountdownInterval);
    }

    updateTimeToExpiry(expiryHourUTC, expiryMinuteUTC);

    expiryCountdownInterval = setInterval(() => {
      updateTimeToExpiry(expiryHourUTC, expiryMinuteUTC);
    }, 1000);
  };

  const stopExpiryCountdown = () => {
    if (expiryCountdownInterval) {
      clearInterval(expiryCountdownInterval);
      expiryCountdownInterval = null;
    }
  };

  const formattedTimeToExpiry = computed(() => {
    if (!timeToExpiry.value) return '';
    const { hours, minutes, seconds } = timeToExpiry.value;
    return `${hours}h ${minutes}m ${seconds}s`;
  });

  return {
    timeToExpiry,
    formattedTimeToExpiry,
    getExpiryTimeUTC,
    getCambodiaTime,
    startExpiryCountdown,
    stopExpiryCountdown,
    updateTimeToExpiry,
  };
}
