// app/api/calendar/route.ts
// Create this file at: app/api/calendar/route.ts

import { getServerSession } from "next-auth";
import { NextResponse } from "next/server";
import GoogleProvider from "next-auth/providers/google";
import NextAuth from "next-auth";

// Reuse the same auth config
const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      authorization: {
        params: {
          scope:
            "openid email profile https://www.googleapis.com/auth/calendar.readonly",
          access_type: "offline",
          prompt: "consent",
        },
      },
    }),
  ],
  callbacks: {
    async jwt({ token, account }: any) {
      if (account) {
        token.accessToken = account.access_token;
      }
      return token;
    },
    async session({ session, token }: any) {
      session.accessToken = token.accessToken;
      return session;
    },
  },
  secret: process.env.NEXTAUTH_SECRET,
};

export async function GET() {
  const session = await getServerSession(authOptions);

  if (!session || !(session as any).accessToken) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  const accessToken = (session as any).accessToken;

  // Build time range: start of today to end of today (Toronto timezone)
  const now = new Date();
  const startOfDay = new Date(now);
  startOfDay.setHours(0, 0, 0, 0);
  const endOfDay = new Date(now);
  endOfDay.setHours(23, 59, 59, 999);

  const params = new URLSearchParams({
    timeMin: startOfDay.toISOString(),
    timeMax: endOfDay.toISOString(),
    singleEvents: "true",
    orderBy: "startTime",
    maxResults: "50",
  });

  try {
    const response = await fetch(
      `https://www.googleapis.com/calendar/v3/calendars/primary/events?${params}`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (!response.ok) {
      const error = await response.json();
      console.error("Google Calendar API error:", error);
      return NextResponse.json(
        { error: "Failed to fetch calendar events" },
        { status: response.status }
      );
    }

    const data = await response.json();

    // Transform Google Calendar events into the shape Mission Control expects
    const events = (data.items || []).map((item: any) => ({
      id: item.id,
      title: item.summary || "Untitled Event",
      description: item.description || "",
      startTime: item.start?.dateTime || item.start?.date,
      endTime: item.end?.dateTime || item.end?.date,
      location: item.location || null,
      type: inferEventType(item.summary || ""),
      htmlLink: item.htmlLink,
    }));

    return NextResponse.json({ events });
  } catch (err) {
    console.error("Calendar fetch error:", err);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}

// Infer event type from title for color-coding (matches existing Mission Control logic)
function inferEventType(title: string): string {
  const t = title.toLowerCase();
  if (t.includes("call") || t.includes("phone")) return "call";
  if (
    t.includes("class") ||
    t.includes("course") ||
    t.includes("training") ||
    t.includes("carnegie")
  )
    return "class";
  if (t.includes("block") || t.includes("prospecting") || t.includes("focus"))
    return "block";
  return "meeting";
}
