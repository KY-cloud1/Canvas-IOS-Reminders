import { useState } from "react";
import { useServerSettings } from "../../hooks/useServerSettings";
import type { ServerSettings, ServerSettingsUpdate } from "../../types/server";
import styles from "./ServerSettingsPanel.module.css";

/**
 * Displays and manages the server's current settings.
 *
 * Retrieves the current settings from the backend and renders a form
 * that allows the user to update them.
 */
export function ServerSettingsPanel() {
    const {
        serverSettings,
        isLoading,
        isSaving,
        error,
        saveSettings,
    } = useServerSettings();

    if (isLoading) {
        return <div>Loading settings...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (!serverSettings) {
        return <div>No server settings available.</div>;
    }

    return (
        <div className={styles.settingsCard}>
            <h2 className={styles.centeredLine}>Server Settings</h2>

            <SettingsForm
                settings={serverSettings}
                onSubmit={saveSettings}
                isSaving={isSaving}
            />
        </div>
    );
}

interface SettingsFormProps {
    settings: ServerSettings;
    onSubmit: (settings: ServerSettingsUpdate) => Promise<void>;
    isSaving: boolean;
}

function SettingsForm({ settings, onSubmit, isSaving }: SettingsFormProps) {
    const [refreshInterval, setRefreshInterval] = useState(settings.refresh_interval);
    const [weeksDelta, setWeeksDelta] = useState(settings.weeks_delta);

    const [canvasEnabled, setCanvasEnabled] = useState(settings.canvas.enabled);
    const [canvasGraphqlUrl, setCanvasGraphqlUrl] = useState(settings.canvas.graphql_url);

    const [gradescopeEnabled, setGradescopeEnabled] = useState(settings.gradescope.enabled);
    const [gradescopeEmail, setGradescopeEmail] = useState(settings.gradescope.email);

    const [ngrokEnabled, setNgrokEnabled] = useState(settings.ngrok.enabled);
    const [ngrokDomain, setNgrokDomain] = useState(settings.ngrok.domain);

    return (
        <form>
            <h3>General:</h3>
            <label>
                Refresh Interval:{" "}
                <input
                    type="number"
                    value={refreshInterval}
                    onChange={(e) => setRefreshInterval(Number(e.target.value))}
                />
            </label>
            <br />
            <label>
                Weeks Delta:{" "}
                <input
                    type="number"
                    value={weeksDelta}
                    onChange={(e) => setWeeksDelta(Number(e.target.value))}
                />
            </label>

            <h3>Canvas:</h3>
            <label>
                Enabled:{" "}
                <input
                    type="checkbox"
                    checked={canvasEnabled}
                    onChange={(e) => setCanvasEnabled(e.target.checked)}
                />
            </label>
            <br />
            <label>
                GraphQL URL:{" "}
                <input
                    type="text"
                    value={canvasGraphqlUrl || ""}
                    onChange={(e) => setCanvasGraphqlUrl(e.target.value)}
                />
            </label>
            <br />
            <label>
                Authtoken Configured:{" "}
                {settings.canvas.token_configured ? "Yes" : "No"}
            </label>

            <h3>Gradescope:</h3>
            <label>
                Enabled:{" "}
                <input
                    type="checkbox"
                    checked={gradescopeEnabled}
                    onChange={(e) => setGradescopeEnabled(e.target.checked)}
                />
            </label>
            <br />
            <label>
                Email:{" "}
                <input
                    type="text"
                    value={gradescopeEmail || ""}
                    onChange={(e) => setGradescopeEmail(e.target.value)}
                />
            </label>
            <br />
            <label>
                Password Configured:{" "}
                {settings.gradescope.password_configured ? "Yes" : "No"}
            </label>

            <h3>ngrok:</h3>
            <label>
                Enabled:{" "}
                <input
                    type="checkbox"
                    checked={ngrokEnabled}
                    onChange={(e) => setNgrokEnabled(e.target.checked)}
                />
            </label>
            <br />
            <label>
                Domain:{" "}
                <input
                    type="text"
                    value={ngrokDomain || ""}
                    onChange={(e) => setNgrokDomain(e.target.value)}
                />
            </label>
            <br />
            <label>
                Authtoken Configured:{" "}
                {settings.ngrok.authtoken_configured ? "Yes" : "No"}
            </label>
        </form>
    );
}