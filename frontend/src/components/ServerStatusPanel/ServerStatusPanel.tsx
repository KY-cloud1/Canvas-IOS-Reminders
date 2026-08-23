import { useServerStatus } from "../../hooks/useServerStatus";
import styles from "./ServerStatusPanel.module.css";

/**
 * Renders the current backend server status.
 *
 * Displays loading and error states while the server status is being
 * retrieved and renders the current status information when available.
 */
export function ServerStatusPanel() {
    const {
        serverStatus,
        isLoading,
        error,
    } = useServerStatus();

    return (
        <div className={styles.statusCard}>
            <h2 className={styles.centeredLine}>Server Status</h2>

            {isLoading && (
                <div>Loading server status...</div>
            )}

            {error && (
                <div>{error}</div>
            )}

            {!error && !serverStatus && (
                <div>No server status available.</div>
            )}

            {!isLoading && !error && serverStatus && (
                <>
                    <p><span className={styles.label}>Status:</span> {serverStatus.status}</p>
                    <p><span className={styles.label}>Number of Cached Assignments:</span> {serverStatus.cached_assignments}</p>
                    <p>
                        <span className={styles.label}>Last Refresh:</span>{" "}
                        {serverStatus.last_refresh
                            ? new Date(serverStatus.last_refresh).toLocaleString(undefined, {
                                dateStyle: "short",
                                timeStyle: "short",
                            })
                            : "Never"}
                    </p>
                    <p><span className={styles.label}>Last Refresh Error:</span> {serverStatus.last_refresh_error ?? "None"}</p>

                </>
            )}

        </div>
    );
}
