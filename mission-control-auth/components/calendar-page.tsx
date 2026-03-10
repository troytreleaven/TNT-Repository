"use client";

// app/calendar/page.tsx
// Replace the entire contents of app/calendar/page.tsx with this file

import { useEffect, useState } from "react";
import { useSession, signIn, signOut } from "next-auth/react";
import { format, isToday, isTomorrow } from "date-fns";
import { Calendar, Clock, RefreshCw, LogIn, LogOut, MapPin, Plus } from "lucide-react";

// ─── Types ───────────────────────────────────────────────────────────────────

interface CalendarEvent {
  id: string;
  title: string;
  description: string;
  startTime: string;
  endTime: string;
  location: string | null;
  type: "meeting" | "call" | "class" | "block";
  htmlLink: string;
}

// ─── Hardcoded Jarvis scheduled tasks (unchanged from original) ───────────────

const SCHEDULED_TASKS = [
  {
    id: "1",
    name: "Daily Health Check",
    description: "System health monitoring every 30 minutes",
    schedule: "*/30 * * * *",
    status: "active",
    assignee: "Jarvis",
    category: "alert",
  },
  {
    id: "2",
    name: "Daily Dad Joke",
    description: "Send daily dad joke via Telegram",
    schedule: "0 9 * * *",
    status: "active",
    assignee: "Jarvis",
    category: "reminder",
  },
  {
    id: "3",
    name: "Daily Spend Report",
    description: "Monitor OpenClaw API usage and costs",
    schedule: "0 8 * * *",
    status: "active",
    assignee: "Jarvis",
    category: "report",
  },
  {
    id: "4",
    name: "Calendar Sync",
    description: "Daily sync of calendar events and tasks",
    schedule: "0 7 * * *",
    status: "active",
    assignee: "Jarvis",
    category: "sync",
  },
  {
    id: "5",
    name: "Prospecting Block Reminder",
    description: "Reminder for morning prospecting block 10 AM - 12 PM",
    schedule: "0 10 * * 1-5",
    status: "active",
    assignee: "Troy",
    category: "reminder",
  },
  {
    id: "6",
    name: "Weekly Revenue Report",
    description: "Generate weekly revenue and pipeline report",
    schedule: "0 18 * * 5",
    status: "paused",
    assignee: "Jarvis",
    category: "report",
  },
];

// ─── Style maps ──────────────────────────────────────────────────────────────

const EVENT_STYLES: Record<string, string> = {
  meeting: "bg-blue-50 border-blue-200",
  class: "bg-purple-50 border-purple-200",
  call: "bg-green-50 border-green-200",
  block: "bg-slate-50 border-slate-200",
};

const TASK_STATUS_STYLES: Record<string, string> = {
  active: "bg-green-100 text-green-800 border-green-200",
  paused: "bg-yellow-100 text-yellow-800 border-yellow-200",
};

const CATEGORY_ICONS: Record<string, string> = {
  automation: "⚙️",
  reminder: "🔔",
  report: "📊",
  sync: "🔄",
  alert: "🚨",
};

// ─── Helpers ─────────────────────────────────────────────────────────────────

function formatEventTime(start: string, end: string): string {
  const s = new Date(start);
  const e = new Date(end);
  const timeRange = `${format(s, "h:mm a")} - ${format(e, "h:mm a")}`;
  if (isToday(s)) return `Today, ${timeRange}`;
  if (isTomorrow(s)) return `Tomorrow, ${timeRange}`;
  return format(s, "EEE, MMM d 'at' h:mm a");
}

function humanSchedule(cron: string): string {
  const parts = cron.split(" ");
  if (parts[0] === "*/30") return "Every 30 minutes";
  if (parts[0] === "0" && parts[1] === "*/6") return "Every 6 hours";
  if (parts[0] === "0" && parts[1] === "9") return "Daily at 9 AM";
  if (parts[0] === "0" && parts[1] === "7") return "Daily at 7 AM";
  if (parts[0] === "0" && parts[1] === "8") return "Daily at 8 AM";
  if (parts[0] === "0" && parts[1] === "10" && parts[4] === "1-5") return "Weekdays at 10 AM";
  if (parts[0] === "0" && parts[1] === "18" && parts[4] === "5") return "Fridays at 6 PM";
  return cron;
}

// ─── Main Component ───────────────────────────────────────────────────────────

export default function CalendarPage() {
  const { data: session, status } = useSession();
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastRefreshed, setLastRefreshed] = useState<Date | null>(null);

  const fetchEvents = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/calendar");
      if (res.status === 401) {
        setError("Please connect your Google Calendar to see events.");
        setEvents([]);
        return;
      }
      if (!res.ok) throw new Error("Failed to fetch events");
      const data = await res.json();
      setEvents(data.events || []);
      setLastRefreshed(new Date());
    } catch (err) {
      setError("Could not load calendar events. Try refreshing.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (session) {
      fetchEvents();
    }
  }, [session]);

  const isAuthenticated = status === "authenticated";

  return (
    <div className="h-full flex flex-col bg-slate-50">
      {/* ── Header ── */}
      <div className="flex items-center justify-between p-4 border-b bg-white">
        <div>
          <h1 className="text-2xl font-bold text-[#1a1a2e]">Calendar & Schedule</h1>
          <p className="text-sm text-muted-foreground">
            {isAuthenticated
              ? lastRefreshed
                ? `Last updated ${format(lastRefreshed, "h:mm a")}`
                : "Connected to Google Calendar"
              : "Connect Google Calendar to see live events"}
          </p>
        </div>
        <div className="flex items-center gap-3">
          {isAuthenticated ? (
            <>
              <button
                onClick={fetchEvents}
                disabled={loading}
                className="flex items-center gap-2 px-3 py-2 text-sm border rounded-md hover:bg-slate-50 disabled:opacity-50"
              >
                <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
                Refresh
              </button>
              <button
                onClick={() => signOut()}
                className="flex items-center gap-2 px-3 py-2 text-sm border rounded-md hover:bg-slate-50 text-muted-foreground"
              >
                <LogOut className="h-4 w-4" />
                Disconnect
              </button>
            </>
          ) : (
            <button
              onClick={() => signIn("google")}
              className="flex items-center gap-2 px-4 py-2 text-sm bg-[#d4af37] text-[#1a1a2e] font-medium rounded-md hover:bg-[#d4af37]/90"
            >
              <LogIn className="h-4 w-4" />
              Connect Google Calendar
            </button>
          )}
          <button className="flex items-center gap-2 px-4 py-2 text-sm bg-[#d4af37] text-[#1a1a2e] font-medium rounded-md hover:bg-[#d4af37]/90">
            <Plus className="h-4 w-4" />
            Add Schedule
          </button>
        </div>
      </div>

      {/* ── Body ── */}
      <div className="flex-1 overflow-auto p-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {/* ── Today's Schedule (live from Google) ── */}
          <div className="lg:col-span-2 rounded-lg border bg-white shadow-sm">
            <div className="flex items-center gap-2 p-6 pb-3">
              <Calendar className="h-5 w-5" />
              <h3 className="text-xl font-semibold text-[#1a1a2e]">Today's Schedule</h3>
              {isAuthenticated && (
                <span className="ml-auto text-xs text-green-600 bg-green-50 border border-green-200 rounded-full px-2 py-0.5">
                  Live
                </span>
              )}
            </div>
            <div className="p-6 pt-0">
              {!isAuthenticated ? (
                <div className="text-center py-10">
                  <Calendar className="h-12 w-12 mx-auto text-muted-foreground mb-3 opacity-30" />
                  <p className="text-muted-foreground mb-4">
                    Connect your Google Calendar to see today's events here
                  </p>
                  <button
                    onClick={() => signIn("google")}
                    className="flex items-center gap-2 px-4 py-2 text-sm bg-[#d4af37] text-[#1a1a2e] font-medium rounded-md hover:bg-[#d4af37]/90 mx-auto"
                  >
                    <LogIn className="h-4 w-4" />
                    Connect Google Calendar
                  </button>
                </div>
              ) : loading ? (
                <div className="flex items-center justify-center py-10">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#1a1a2e]" />
                </div>
              ) : error ? (
                <div className="text-center py-8 text-muted-foreground">
                  <p>{error}</p>
                </div>
              ) : events.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <p>No events scheduled for today 🎉</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {events.map((event) => (
                    <div
                      key={event.id}
                      className={`p-4 rounded-lg border ${EVENT_STYLES[event.type] || EVENT_STYLES.meeting} flex items-start justify-between`}
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs border rounded-full px-2 py-0.5 capitalize">
                            {event.type}
                          </span>
                          <span className="text-sm text-muted-foreground">
                            {formatEventTime(event.startTime, event.endTime)}
                          </span>
                        </div>
                        <h3 className="font-semibold text-[#1a1a2e]">{event.title}</h3>
                        {event.description && (
                          <p className="text-sm text-muted-foreground line-clamp-1">
                            {event.description}
                          </p>
                        )}
                        {event.location && (
                          <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
                            <MapPin className="h-3 w-3" />
                            {event.location}
                          </p>
                        )}
                      </div>
                      {event.htmlLink && (
                        <a
                          href={event.htmlLink}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-blue-500 hover:underline ml-4 shrink-0"
                        >
                          Open ↗
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* ── Scheduled Tasks (Jarvis cron jobs) ── */}
          <div className="rounded-lg border bg-white shadow-sm">
            <div className="flex items-center gap-2 p-6 pb-3">
              <Clock className="h-5 w-5" />
              <h3 className="text-xl font-semibold text-[#1a1a2e]">Scheduled Tasks</h3>
            </div>
            <div className="p-6 pt-0">
              <div className="space-y-3 max-h-[400px] overflow-y-auto">
                {SCHEDULED_TASKS.map((task) => (
                  <div
                    key={task.id}
                    className="p-4 rounded-lg border bg-white hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-lg">{CATEGORY_ICONS[task.category]}</span>
                        <h4 className="font-medium text-[#1a1a2e]">{task.name}</h4>
                      </div>
                      <span
                        className={`text-xs border rounded-full px-2 py-0.5 ${TASK_STATUS_STYLES[task.status]}`}
                      >
                        {task.status}
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground mb-2">{task.description}</p>
                    <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {humanSchedule(task.schedule)}
                      </span>
                      <span>{task.assignee}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* ── Schedule Overview ── */}
          <div className="rounded-lg border bg-white shadow-sm">
            <div className="flex items-center gap-2 p-6 pb-3">
              <RefreshCw className="h-5 w-5" />
              <h3 className="text-xl font-semibold text-[#1a1a2e]">Schedule Overview</h3>
            </div>
            <div className="p-6 pt-0 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded-lg bg-green-50 border border-green-200">
                  <div className="text-2xl font-bold text-green-800">
                    {SCHEDULED_TASKS.filter((t) => t.status === "active").length}
                  </div>
                  <div className="text-sm text-green-600">Active Tasks</div>
                </div>
                <div className="p-4 rounded-lg bg-yellow-50 border border-yellow-200">
                  <div className="text-2xl font-bold text-yellow-800">
                    {SCHEDULED_TASKS.filter((t) => t.status === "paused").length}
                  </div>
                  <div className="text-sm text-yellow-600">Paused</div>
                </div>
              </div>
              <div className="p-4 rounded-lg bg-blue-50 border border-blue-200">
                <div className="text-2xl font-bold text-blue-800">{events.length}</div>
                <div className="text-sm text-blue-600">
                  {isAuthenticated ? "Live Events Today" : "Events Today (connect to see)"}
                </div>
              </div>
              <div className="p-4 rounded-lg bg-slate-50 border border-slate-200">
                <h4 className="font-medium mb-2 text-sm">Connection Status</h4>
                <div className="flex items-center gap-2">
                  <div
                    className={`h-2 w-2 rounded-full ${isAuthenticated ? "bg-green-500" : "bg-slate-300"}`}
                  />
                  <span className="text-sm text-muted-foreground">
                    {isAuthenticated
                      ? `Connected as ${session?.user?.email}`
                      : "Google Calendar not connected"}
                  </span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
