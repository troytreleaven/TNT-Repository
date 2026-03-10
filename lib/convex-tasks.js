// Convex client for Mission Control Task Board
// Connection: https://vibrant-crocodile-289.convex.cloud

import { ConvexHttpClient } from "convex/browser";

const CONVEX_URL = "https://vibrant-crocodile-289.convex.cloud";

// Create client
const convex = new ConvexHttpClient(CONVEX_URL);

// Task types
interface Task {
  _id: string;
  _creationTime: number;
  title: string;
  description: string;
  assignee: "Troy" | "Jarvis";
  status: "backlog" | "in-progress" | "review" | "done";
  priority: "low" | "medium" | "high";
  dueDate?: string;
  createdAt: number;
  updatedAt: number;
}

// Query functions
export async function getAllTasks(): Promise<Task[]> {
  return await convex.query("tasks:getAll");
}

export async function getTasksByStatus(status: string): Promise<Task[]> {
  return await convex.query("tasks:getByStatus", { status });
}

export async function getTasksByAssignee(assignee: "Troy" | "Jarvis"): Promise<Task[]> {
  return await convex.query("tasks:getByAssignee", { assignee });
}

// Mutation functions
export async function createTask(task: {
  title: string;
  description: string;
  assignee: "Troy" | "Jarvis";
  status: "backlog" | "in-progress" | "review" | "done";
  priority: "low" | "medium" | "high";
  dueDate?: string;
}): Promise<string> {
  const result = await convex.mutation("tasks:create", {
    ...task,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  });
  return result;
}

export async function updateTask(id: string, updates: Partial<Task>): Promise<void> {
  await convex.mutation("tasks:update", {
    id,
    ...updates,
    updatedAt: Date.now(),
  });
}

export async function deleteTask(id: string): Promise<void> {
  await convex.mutation("tasks:remove", { id });
}

// Export client for advanced use
export { convex };
