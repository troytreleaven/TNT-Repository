// app/providers.tsx
// Create this NEW file at: app/providers.tsx
// Then wrap your app layout with it (see instructions below)

"use client";

import { SessionProvider } from "next-auth/react";

export function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}

// ─────────────────────────────────────────────────────────────────────────────
// INSTRUCTIONS FOR JARVIS:
//
// After creating this file, update app/layout.tsx to wrap the app with Providers.
// Find the section that looks like:
//
//   <body>
//     <ConvexClientProvider>
//       ...
//     </ConvexClientProvider>
//   </body>
//
// And change it to:
//
//   import { Providers } from "./providers";
//
//   <body>
//     <Providers>
//       <ConvexClientProvider>
//         ...
//       </ConvexClientProvider>
//     </Providers>
//   </body>
//
// This makes useSession() work throughout the app.
// ─────────────────────────────────────────────────────────────────────────────
