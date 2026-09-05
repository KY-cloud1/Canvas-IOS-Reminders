import { useEffect, useState } from "react";
import { getStatus } from "../api/server";
import type { ServerStatus } from "../types/server";

/**
  * Retrieves and manages the backend server status.
  *
  * Fetches the initial server status from the backend and then listens
  * for live server status updates through an SSE connection. The SSE
  * connection is automatically closed when the hook is unmounted.
  *
  * @returns An object containing the current server status, loading state,
  * and error state.
  */
export function useServerStatus() {
    const [serverStatus, setServerStatus] = useState<ServerStatus | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let isMounted = true;

        async function loadInitialStatus() {
            try {
                const status = await getStatus();

                if (isMounted) {
                    setServerStatus(status);
                    setError(null);
                }
            } catch {
                if (isMounted) {
                    setError("Failed to fetch server status.")
                }
            } finally {
                if (isMounted) {
                    setIsLoading(false);
                }
            }
        }

        void loadInitialStatus();

        const events = new EventSource("/api/events");

        events.addEventListener("server_status", (event) => {
            try {
                const status = JSON.parse(event.data) as ServerStatus;

                if (isMounted) {
                    setServerStatus(status);
                    setError(null);
                }
            } catch {
                if (isMounted) {
                    setError("Failed to parse server status update.")
                }
            }
        });

        return () => {
            isMounted = false;
            events.close();
        }
    }, []);

    return {
        serverStatus,
        isLoading,
        error,
    };
}
