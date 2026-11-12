export const apiBase =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ?? "http://localhost:8000";

export type ApiErrorDetail = string | { msg: string }[] | Record<string, unknown>;

export class ApiError extends Error {
  readonly status: number;
  readonly detail: ApiErrorDetail;

  constructor(status: number, detail: ApiErrorDetail) {
    super(formatApiErrorDetail(detail));
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

export function formatApiErrorDetail(detail: ApiErrorDetail): string {
  if (typeof detail === "string") {
    return detail;
  }
  if (Array.isArray(detail)) {
    const first = detail[0];
    return first?.msg ?? "Request failed";
  }
  if (detail && typeof detail === "object" && "detail" in detail) {
    return formatApiErrorDetail(detail.detail as ApiErrorDetail);
  }
  return "Request failed";
}

export async function fetchJson<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers);
  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  const response = await fetch(`${apiBase}${path}`, { ...options, headers });
  if (response.status === 204) {
    return undefined as T;
  }
  const text = await response.text();
  const data = text ? (JSON.parse(text) as unknown) : null;
  if (!response.ok) {
    const detail =
      data && typeof data === "object" && "detail" in data
        ? (data as { detail: ApiErrorDetail }).detail
        : text || response.statusText;
    throw new ApiError(response.status, detail);
  }
  return data as T;
}
