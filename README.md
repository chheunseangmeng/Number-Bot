# LuckyNumber Mini App

A Telegram Mini App for selecting lucky numbers and processing payments.

---

## 📱 What is the process of this app?

This Mini App is built with **Vue 3** and is opened by the LuckyNumber Bot after the user completes onboarding. It communicates with the bot in two ways:
- **Bot → Mini App**: User data is passed via URL parameters when the Mini App opens
- **Mini App → Bot**: Payment data is sent back when the user closes the receipt

---

## 🔄 User Flow

```
Bot Onboarding → Mini App Opens → Select Numbers → Payment → Receipt → Close
```

1. **Onboarding** — Bot handles welcome, contact sharing, age confirmation
2. **Home** — User selects 2 numbers per game (max 5 games)
3. **Payment** — User selects bank and confirms
4. **Receipt** — Displays summary, sends data to bot on Close

---

## 🎮 Game Rules

- Select **2 numbers** per game (1–40)
- Max **5 games** per session

---

## 🏦 Supported Banks

- ABA

---

## 📡 Communication

```
Bot ──── URL Params ────→ Mini App
Mini App ── sendData() ──→ Bot
```

- **Bot → Mini App**: Only via URL params when opening the Mini App
- **Mini App → Bot**: Only via `sendData()` — sends once then Mini App closes

---

## 🚀 Deployment

Deployed on **Vercel** — requires `vercel.json` for routing:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

---

## 🛠️ Tech Stack

- **Vue 3** + **Pinia** + **Vue Router**
- **Tailwind CSS**
- **Telegram Mini App SDK**
- **Vercel**

## Project Setup

```sh
npm install
```
```sh
npm run dev
```
### Compile and Minify for Production
```sh
npm run build
```
