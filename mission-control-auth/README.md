# Google Calendar Integration for Mission Control
## Instructions for Jarvis

This package wires up live Google Calendar data to replace the hardcoded events
on the Calendar page. Follow the steps below in order.

---

## Overview of Changes

1. Add 3 environment variables to `.env.local`
2. Install 1 new package (`next-auth`)
3. Add 2 new API route files
4. Replace the calendar page component

---

## Step 1: Environment Variables

Add these to your `.env.local` file (create it in the project root if it doesn't exist):

```
GOOGLE_CLIENT_ID=794402546207-4t8268cm4nifv1i4308sem1hbp843u8e.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
NEXTAUTH_SECRET=mission-control-secret-change-this-in-production
NEXTAUTH_URL=http://localhost:3000
```

---

## Step 2: Install Dependencies

```bash
npm install next-auth
```

---

## Step 3: Add API Routes

### File 1: `app/api/auth/[...nextauth]/route.ts`
*(Create this file — new file, doesn't exist yet)*
See: `api-routes/auth-route.ts`

### File 2: `app/api/calendar/route.ts`
*(Create this file — new file, doesn't exist yet)*
See: `api-routes/calendar-route.ts`

---

## Step 4: Replace the Calendar Page

Replace the contents of `app/calendar/page.tsx` with the file in:
`components/calendar-page.tsx`

---

## Step 5: Update Google Cloud Console

In Google Cloud Console, add the production URL to the OAuth client's
Authorized Redirect URIs once deployed:
`https://YOUR-PRODUCTION-URL/api/auth/callback/google`

---

## How It Works

- User visits the Calendar page and clicks "Connect Google Calendar"
- They're redirected to Google's OAuth screen and grant access
- Google returns an access token stored in the session
- The calendar page fetches today's events from the Google Calendar API
- Events display live, refreshed on each page load
